import { useState, useEffect } from 'react'

function App() {
  const [message, setMessage] = useState('Loading...')

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL || 'http://localhost:5001/')
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(() => setMessage('Could not connect to backend'))
  }, [])

  return (
    <div className="container">
      <h1>🚀 Monorepo Test</h1>
      <p>Backend says: <strong>{message}</strong></p>
    </div>
  )
}

export default App


