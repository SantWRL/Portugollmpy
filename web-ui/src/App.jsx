import React, { useState, useEffect, useRef } from 'react'

function App() {
  const [input, setInput] = useState('')
  const [portugol, setPortugol] = useState('')
  const [logs, setLogs] = useState([])
  const [variables, setVariables] = useState({})
  const [loading, setLoading] = useState(false)
  const terminalEndRef = useRef(null)

  // Auto-scroll terminal
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  // Live translation (debounce)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (input.trim()) {
        translate(input)
      } else {
        setPortugol('')
      }
    }, 400)
    return () => clearTimeout(timer)
  }, [input])

  const [status, setStatus] = useState({ loaded: false, vars: 0 })

  // Check API status on mount
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const res = await fetch('http://localhost:5000/status')
        const data = await res.json()
        setStatus({ loaded: data.modelo_carregado, vars: data.total_variaveis })
      } catch (err) {
        setStatus({ loaded: false, vars: 0 })
      }
    }
    checkStatus()
    const interval = setInterval(checkStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const translate = async (frase) => {
    try {
      const res = await fetch('http://localhost:5000/traduzir', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frase })
      })
      const data = await res.json()
      if (data.portugol) setPortugol(data.portugol)
    } catch (err) {
      console.error("Erro na tradução", err)
    }
  }

  const [lastUpdatedVar, setLastUpdatedVar] = useState(null)
  const [currentThought, setCurrentThought] = useState("")

  const sugestoes = [
    { label: "📦 Variável", cmd: "crie a variavel pontos como 100" },
    { label: "➕ Incrementar", cmd: "aumente pontos em 10" },
    { label: "⚖️ Condicional", cmd: "se pontos for maior que 50 entao mostre nivel_alto senao mostre nivel_baixo" },
    { label: "🔄 Loop", cmd: "repita 5 vezes" },
    { label: "⌨️ Entrada", cmd: "leia o valor de nome" },
    { label: "🧪 Cálculo", cmd: "some x com y" },
  ]

  const gerarPensamento = (cmd) => {
    const c = cmd.toLowerCase()
    const thoughts = [
      "Mapeando tokens de linguagem natural para primitivos lógicos...",
      "Analisando semântica da instrução e resolvendo dependências de contexto...",
      "Alocando registradores virtuais para processamento de fluxo...",
      "Validando sintaxe contra o esquema Tupi-Logic v2.0...",
      "Sincronizando estado do Kernel com a unidade de tradução neural..."
    ]

    if (c.includes("se") || c.includes("for")) return "Identificando estrutura de decisão condicional... Analisando operadores lógicos... " + thoughts[Math.floor(Math.random() * thoughts.length)]
    if (c.includes("repita") || c.includes("vezes") || c.includes("enquanto")) return "Detectando padrão de repetição (loop)... Validando condição de parada... " + thoughts[Math.floor(Math.random() * thoughts.length)]
    if (c.includes("crie") || c.includes("variavel") || c.includes("como")) return "Solicitação de alocação de memória detectada... Validando identificador... " + thoughts[Math.floor(Math.random() * thoughts.length)]

    return thoughts[Math.floor(Math.random() * thoughts.length)]
  }

  const handleRun = async () => {
    if (!portugol || loading) return
    setLoading(true)
    setCurrentThought("")

    // Fase de Pensamento (Chain of Thought)
    const pensamento = gerarPensamento(input)
    let textoPensamento = ""
    for (const char of pensamento) {
      textoPensamento += char
      setCurrentThought(textoPensamento)
      await new Promise(r => setTimeout(r, 10))
    }

    await new Promise(r => setTimeout(r, 500))

    try {
      const res = await fetch('http://localhost:5000/executar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ codigo: portugol })
      })
      const data = await res.json()

      if (data.logs) {
        const finalLogs = data.logs.map(l => ({ type: 'log', content: l }))
        setLogs(prev => [...prev, { type: 'prompt', content: input }, ...finalLogs])
      }
      if (data.variaveis) {
        const changed = Object.keys(data.variaveis).find(k => data.variaveis[k] !== variables[k])
        if (changed) {
          setLastUpdatedVar(changed)
          setTimeout(() => setLastUpdatedVar(null), 1000)
        }
        setVariables(data.variaveis)
        setStatus(prev => ({ ...prev, vars: Object.keys(data.variaveis).length }))
      }
      setInput('')
      setPortugol('')
      setCurrentThought("")
    } catch (err) {
      setLogs(prev => [...prev, { type: 'err', content: "[Erro] Falha catastrófica na comunicação com o Kernel." }])
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    if (!window.confirm("Deseja resetar toda a memória do sistema?")) return
    try {
      await fetch('http://localhost:5000/reset', { method: 'POST' })
      setVariables({})
      setStatus(prev => ({ ...prev, vars: 0 }))
      setLogs(prev => [...prev, { type: 'log', content: '>>> Memória volátil limpa. Registradores zerados.' }])
    } catch (e) {
      alert("Erro ao resetar memória.")
    }
  }

  const formatLog = (log) => {
    const content = log.content
    if (content.includes('[Var]')) return <span className="log-var">{content}</span>
    if (content.includes('[Out]')) return <span className="log-out">{content}</span>
    if (content.includes('[Cond]')) return <span className="log-cond">{content}</span>
    if (content.includes('[Erro]')) return <span className="log-err">{content}</span>
    if (content.includes('[Exec]')) return <span style={{ opacity: 0.4 }}>{content}</span>
    return <span>{content}</span>
  }

  return (
    <div className="app-container">
      <header>
        <div className="logo">
          <h1>TUPI-LOGIC <span className="badge">NEURAL KERNEL</span></h1>
          <div className={`status-dot ${status.loaded ? 'online' : 'offline'}`}>
            {status.loaded ? 'SYSTEM_ONLINE' : 'SYSTEM_OFFLINE'}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '15px' }}>
          <button onClick={handleReset} style={{
            background: 'rgba(255, 68, 68, 0.1)', border: '1px solid rgba(255, 68, 68, 0.2)', color: '#ff4444',
            padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.65rem', fontWeight: 'bold', transition: '0.2s'
          }} onMouseOver={e => e.target.style.background = 'rgba(255, 68, 68, 0.2)'} onMouseOut={e => e.target.style.background = 'rgba(255, 68, 68, 0.1)'}>
            PURGE_MEMORY
          </button>
        </div>
      </header>

      <main className="main-content">
        <section className="suggestions-gallery">
          {sugestoes.map((s, i) => (
            <button key={i} className="suggestion-chip" onClick={() => setInput(s.cmd)}>
              {s.label}
            </button>
          ))}
        </section>

        <section className="glass-card editor-section">
          {currentThought && (
            <div className="thought-block fade-in">
              <div className="thought-header">
                <span>RACIOCÍNIO_VIRTUAL</span>
                <div className="loading-dots"><span></span><span></span><span></span></div>
              </div>
              <p className="thought-text">{currentThought}</p>
            </div>
          )}

          <div className="input-group">
            <textarea
              placeholder="Insira instrução em Linguagem Natural..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleRun())}
              disabled={loading}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', minHeight: '60px' }}>
            <div style={{ flex: 1 }}>
              {portugol && (
                <div className="translation-box fade-in">
                  <p className="portugol-code">{portugol}</p>
                </div>
              )}
            </div>
            <button className="btn-primary" onClick={handleRun} disabled={loading || !portugol}>
              {loading ? 'PROCESSANDO...' : 'EXECUTAR'}
            </button>
          </div>
        </section>

        <section className="terminal">
          <div className="terminal-line" style={{ color: 'var(--text-secondary)', marginBottom: '10px', fontSize: '0.7rem', opacity: 0.6 }}>
            &gt; TUPI_OS [v2.5.0-LTS] | Neural Translator Engine Active
          </div>
          {logs.map((log, i) => (
            <div key={i} className={`terminal-line ${log.type === 'prompt' ? 'fade-in' : ''}`}>
              {log.type === 'prompt' ? (
                <><span className="terminal-prompt">❯</span> <span>{log.content}</span></>
              ) : (
                <>{formatLog(log)}</>
              )}
            </div>
          ))}
          <div ref={terminalEndRef} />
        </section>
      </main>

      <aside className="sidebar">
        <div className="glass-card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ fontSize: '0.7rem', letterSpacing: '2px', color: 'var(--text-secondary)', textTransform: 'uppercase', borderBottom: '1px solid var(--border-color)', paddingBottom: '10px', marginBottom: '15px' }}>
            Memory_Stack
          </h2>
          <div className="var-list">
            {Object.keys(variables).length === 0 ? (
              <p className="empty-state">Pilha de memória vazia.</p>
            ) : (
              Object.entries(variables).map(([name, val]) => (
                <div key={name} className={`var-item fade-in ${lastUpdatedVar === name ? 'var-updated' : ''}`}>
                  <span className="var-name">{name}</span>
                  <span className="var-value">{val}</span>
                </div>
              ))
            )}
          </div>

          <div style={{ marginTop: 'auto', padding: '15px', background: 'rgba(0, 242, 255, 0.03)', borderRadius: '12px', border: '1px dashed rgba(0, 242, 255, 0.2)' }}>
            <h4 style={{ fontSize: '0.6rem', color: 'var(--accent-blue)', marginBottom: '8px', letterSpacing: '1px' }}>PROTOCOLOS_SUGERIDOS</h4>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
              Para operar o Kernel, primeiro crie os dados: <strong>"crie pontos como 0"</strong>. Depois use: <strong>"aumente pontos em 10"</strong> ou <strong>"se pontos &gt; 5 então mostre ok"</strong>.
            </p>
          </div>
        </div>
      </aside>
    </div>
  )
}

export default App
