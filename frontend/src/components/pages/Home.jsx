import React, { useEffect, useRef, useState } from 'react'

function Bubble({ role, time, children }) {
  const isUser = role === 'user'
  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-start',
      gap: 12,
      margin: '12px 0',
      padding: '14px 16px',
      borderRadius: 14,
      border: '1px solid rgba(148,163,184,0.15)',
      background: isUser ? 'linear-gradient(180deg, rgba(14,165,233,0.08), rgba(14,165,233,0.06))' : 'linear-gradient(180deg, rgba(30,41,59,0.55), rgba(15,23,42,0.4))'
    }}>
      <div style={{ fontSize: 12, color: '#8b98a5', marginBottom: 6 }}>{time}</div>
      <div style={{ color: '#e2e8f0' }}>{children}</div>
    </div>
  )
}

export default function Home() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const listRef = useRef(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  async function send() {
    if (!input.trim()) return
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    const me = { role: 'user', time: now, content: input }
    setMessages(prev => [...prev, me])
    setInput('')
    try {
      const res = await fetch('http://localhost:8000/api/chat/ask', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: me.content })
      })
      const data = await res.json()
      if (data?.ok) {
        setMessages(prev => [...prev, { role: 'assistant', time: data.time, content: data.answer }])
      } else {
        setMessages(prev => [...prev, { role: 'assistant', time: now, content: 'Error contacting server.' }])
      }
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', time: now, content: 'Network error.' }])
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ color: '#e2e8f0', marginBottom: 8 }}>Mino</h1>
      <div ref={listRef} style={{
        height: '70vh', overflow: 'auto',
        border: '1px solid rgba(148,163,184,0.15)', borderRadius: 16,
        padding: 16,
        background: 'linear-gradient(180deg, rgba(17,24,39,0.7), rgba(2,6,23,0.5))'
      }}>
        {messages.map((m, i) => (
          <Bubble key={i} role={m.role} time={m.time}>{m.content}</Bubble>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
        <input value={input} onChange={e => setInput(e.target.value)}
               onKeyDown={e => e.key === 'Enter' && send()}
               placeholder="Type your message..."
               style={{ flex: 1, padding: '10px 12px', borderRadius: 12, border: '1px solid rgba(148,163,184,0.15)' }} />
        <button onClick={send} style={{ padding: '10px 14px', borderRadius: 10, border: '1px solid rgba(148,163,184,0.2)' }}>Send</button>
      </div>
    </div>
  )
}