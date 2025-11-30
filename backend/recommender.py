import json, numpy as np, scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from .models import Item, Event
from collections import Counter
from joblib import load  # ✅ 新增

class TfidfRecommender:
    def __init__(self, session_factory, artifacts_dir="./artifacts"):
        self.session_factory = session_factory
        self.artifacts_dir = artifacts_dir
        self._load()

    def _load(self):
        # 先加载 TF-IDF 矩阵
        self.item_tfidf = sp.load_npz(f"{self.artifacts_dir}/item_tfidf.npz").tocsr()

        # ✅ 优先加载“已拟合”的向量器
        try:
            self.vectorizer = load(f"{self.artifacts_dir}/tfidf_vectorizer.joblib")
            return
        except Exception:
            pass

        # 兜底：只有 vocab 时，需要在同一语料上 fit 一下以获得 idf_
        with open(f"{self.artifacts_dir}/tfidf_vocab.json","r",encoding="utf-8") as f:
            vocab = json.load(f)
        self.vectorizer = TfidfVectorizer(vocabulary=vocab, ngram_range=(1,2))

        # ✅ 用数据库中的文本语料来 fit，确保与 item_tfidf 一致
        if self.session_factory is not None:
            with self.session_factory() as db:
                N = self.item_tfidf.shape[0]
                items = db.query(Item).order_by(Item.id).limit(N).all()
                corpus = [(it.title or "") + " " + (it.abstract or "") + " " + (it.tags or "") for it in items]
            # 仅需拟合（不必 transform）；有了 idf_ 就能在线 transform 查询
            self.vectorizer.fit(corpus)

    def _user_vec(self, db: Session, uid: str):
        ids = [e.item_id for e in db.query(Event).filter(Event.uid == uid).all()]
        N = self.item_tfidf.shape[0]
        ids = [i for i in ids if 1 <= i <= N]
        if not ids:
            return None
        sub = self.item_tfidf[np.array(ids) - 1]
        return np.asarray(sub.mean(axis=0)).ravel()

    def _score_linear(self, sim, items, pop, fresh, avail):
        return 0.5 * sim + 0.2 * pop + 0.2 * fresh + 0.1 * avail

    def recommend(self, db: Session, uid: str | None, q: str | None, k: int = 10):
        # 统一成一维 ndarray
        if uid:
            u = self._user_vec(db, uid)
            if u is None and q:
                u = self.vectorizer.transform([q]).toarray().ravel()
            elif u is None:
                u = np.asarray(self.item_tfidf.mean(axis=0)).ravel()
        else:
            u = self.vectorizer.transform([q or ""]).toarray().ravel()

        sim = self.item_tfidf.dot(u)  # (N,)
        N = sim.shape[0]

        items = db.query(Item).order_by(Item.id).limit(N).all()
        if len(items) < N:
            sim = sim[:len(items)]

        id2idx = {it.id: i for i, it in enumerate(items)}
        years = np.array([it.year or 0 for it in items], dtype=float)
        avail = np.array([1.0 if (it.availability or "") == "available" else 0.0 for it in items], dtype=float)

        ev = db.query(Event).all()
        pop = np.zeros(len(items), dtype=float)
        for e in ev:
            if e.item_id in id2idx:
                pop[id2idx[e.item_id]] += 1.0

        def norm(x):
            if x.size == 0 or x.max() == x.min():
                return np.zeros_like(x, dtype=float)
            return (x - x.min()) / (x.max() - x.min())

        pop = norm(pop); fresh = norm(years); sim = norm(sim)
        score = self._score_linear(sim, items, pop, fresh, avail)

        order = np.argsort(-score)
        chosen, author_count = [], Counter()
        for idx in order:
            a = (items[idx].author or "").strip()
            if author_count[a] >= 2: 
                continue
            chosen.append(idx)
            author_count[a] += 1
            if len(chosen) >= k: break

        results = []
        for idx in chosen:
            it = items[idx]
            reasons = []
            if sim[idx] > 0.6: reasons.append("与你的主题/关键词高度相似")
            if pop[idx] > 0.6: reasons.append("近期更受欢迎")
            if fresh[idx] > 0.6: reasons.append("较新出版/上架")
            if avail[idx] == 1.0: reasons.append("当前可借阅")
            results.append({
                "item_id": it.id, "title": it.title, "author": it.author,
                "score": float(score[idx]), "reason": reasons[:3]
            })
        return results
