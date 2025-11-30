from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Item, Event
from .schemas import ItemOut, RecommendOut, FeedbackIn
from .recommender import TfidfRecommender

app = FastAPI(title="Library Recommender")
Base.metadata.create_all(bind=engine)
recommender = TfidfRecommender(None)

@app.get("/search", response_model=list[ItemOut])
def search(q: str = "", limit: int = 10, db: Session = Depends(get_db)):
    rows = db.query(Item).filter(
        Item.title.ilike(f"%{q}%") | Item.abstract.ilike(f"%{q}%")
    ).limit(limit).all()
    return [ItemOut(**r.__dict__) for r in rows]

@app.get("/recommend", response_model=list[RecommendOut])
def recommend(uid: str | None = None, q: str | None = None, k: int = 10,
              db: Session = Depends(get_db)):
    return [RecommendOut(**r) for r in recommender.recommend(db, uid, q, k)]

# ✅ 新增反馈端点：POST /feedback
@app.post("/feedback")
def feedback(payload: FeedbackIn, db: Session = Depends(get_db)):
    db.add(Event(uid=payload.uid, item_id=payload.item_id, action=payload.action))
    db.commit()
    return {"ok": True}
