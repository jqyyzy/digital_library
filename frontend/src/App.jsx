import { useEffect, useState } from 'react'
import axios from 'axios'

export default function App(){
  const [uid, setUid] = useState('u123')
  const [q, setQ] = useState('')
  const [items, setItems] = useState([])
  const [recs, setRecs] = useState([])

  async function doSearch(){
    const {data} = await axios.get(`/api/search`, { params: { q, limit: 10 } })
    setItems(data)
  }
  async function doRecommend(){
    const {data} = await axios.get(`/api/recommend`, { params: { uid, q, k: 10 } })
    setRecs(data)
  }
  useEffect(()=>{ doRecommend() },[])

  return (
    <div style={{maxWidth: 960, margin:'40px auto', fontFamily:'system-ui'}}>
      <h1>图书推荐演示</h1>
      <section style={{marginTop:20, padding:12, border:'1px solid #eee'}}>
        <h3>搜索</h3>
        <input placeholder="输入关键词" value={q} onChange={e=>setQ(e.target.value)} />
        <button onClick={doSearch} style={{marginLeft:8}}>搜索</button>
        <ul>{items.map(it=>(
          <li key={it.id}><b>{it.title}</b> — {it.author}（{it.year||'未知'}）</li>
        ))}</ul>
      </section>

      <section style={{marginTop:20, padding:12, border:'1px solid #eee'}}>
        <h3>为你推荐（uid={uid}）</h3>
        <input value={uid} onChange={e=>setUid(e.target.value)} />
        <button onClick={doRecommend} style={{marginLeft:8}}>刷新推荐</button>
        <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(260px,1fr))', gap:12, marginTop:12}}>
          {recs.map(r=>(
            <div key={r.item_id} style={{border:'1px solid #ddd', borderRadius:8, padding:12}}>
              <div style={{fontWeight:700}}>{r.title}</div>
              <div style={{color:'#666', fontSize:12}}>{r.author}</div>
              <div style={{marginTop:8, fontSize:12}}>
                {r.reason.map((t,i)=>(<span key={i} style={{padding:'2px 6px', border:'1px solid #eee', borderRadius:12, marginRight:6}}>{t}</span>))}
              </div>
              <div style={{marginTop:8, fontSize:12, color:'#999'}}>score: {r.score.toFixed(3)}</div>
              <button onClick={()=>axios.post('/api/feedback', {uid, item_id:r.item_id, action:'click'})} style={{marginTop:8}}>我感兴趣</button>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
