import { useState } from 'react'
import { endpoints, type ApiResult } from './api'
import './App.css'

function App() {
  const [result, setResult] = useState<ApiResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const [symType, setSymType] = useState<'standard' | 'classical'>('classical')
  const [loadingLevel, setLoadingLevel] = useState('1.0')
  const [randomCasesNum, setRandomCasesNum] = useState('100')
  const [itemsInput, setItemsInput] = useState('')

  const run = async (fn: () => Promise<ApiResult>) => {
    setError(null)
    setLoading(true)
    try {
      const data = await fn()
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  const parseItems = (): string[] | undefined => {
    const s = itemsInput.trim()
    if (!s) return undefined
    return s.split(/[\s,]+/).filter(Boolean)
  }

  return (
    <div className="app">
      <header className="header">
        <h1 className="brand">HYNET</h1>
        <p className="tagline">Powering Europe with seamless AC-DC integration</p>
        <p className="subtitle">PowerFactory API — call backend endpoints and view responses</p>
      </header>

      <main className="main">
        <section className="section">
          <h2>Generator</h2>
          <div className="actions">
            <div className="row">
              <label>Sym type</label>
              <select value={symType} onChange={(e) => setSymType(e.target.value as 'standard' | 'classical')}>
                <option value="standard">standard</option>
                <option value="classical">classical</option>
              </select>
              <button onClick={() => run(() => endpoints.symType(symType))} disabled={loading}>
                Change sym type
              </button>
            </div>
            <div className="row">
              <button onClick={() => run(endpoints.disableAvr)} disabled={loading}>Disable AVR</button>
            </div>
            <div className="row">
              <button onClick={() => run(endpoints.generatorControl)} disabled={loading}>Set up generator control</button>
            </div>
          </div>
        </section>

        <section className="section">
          <h2>Relays</h2>
          <div className="actions">
            <div className="row">
              <input
                type="text"
                placeholder="Items (optional, comma/space separated)"
                value={itemsInput}
                onChange={(e) => setItemsInput(e.target.value)}
              />
            </div>
            <div className="row">
              <button onClick={() => run(() => endpoints.addOvercurrentRelay(parseItems()))} disabled={loading}>Add overcurrent relay</button>
              <button className="btn-outline" onClick={() => run(() => endpoints.removeOvercurrentRelay(parseItems()))} disabled={loading}>Remove overcurrent relay</button>
            </div>
            <div className="row">
              <button onClick={() => run(() => endpoints.addUfls(parseItems()))} disabled={loading}>Add UFLS</button>
              <button className="btn-outline" onClick={() => run(() => endpoints.removeUfls(parseItems()))} disabled={loading}>Remove UFLS</button>
            </div>
            <div className="row">
              <button onClick={() => run(() => endpoints.addOfgt(parseItems()))} disabled={loading}>Add OFGT</button>
              <button className="btn-outline" onClick={() => run(() => endpoints.removeOfgt(parseItems()))} disabled={loading}>Remove OFGT</button>
            </div>
            <div className="row">
              <button onClick={() => run(() => endpoints.addUfgt(parseItems()))} disabled={loading}>Add UFGT</button>
              <button className="btn-outline" onClick={() => run(() => endpoints.removeUfgt(parseItems()))} disabled={loading}>Remove UFGT</button>
            </div>
          </div>
        </section>

        <section className="section">
          <h2>Load &amp; generation</h2>
          <div className="actions">
            <div className="row">
              <button onClick={() => run(endpoints.loadType)} disabled={loading}>Change load type</button>
            </div>
            <div className="row">
              <label>Loading level</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={loadingLevel}
                onChange={(e) => setLoadingLevel(e.target.value)}
              />
              <button onClick={() => run(() => endpoints.loadingLevel(Number(loadingLevel)))} disabled={loading}>Set loading level</button>
            </div>
            <div className="row">
              <button onClick={() => run(() => endpoints.initialGenerationLevel(Number(loadingLevel)))} disabled={loading}>Set initial generation level</button>
            </div>
          </div>
        </section>

        <section className="section">
          <h2>Line &amp; simulation</h2>
          <div className="actions">
            <div className="row">
              <button onClick={() => run(endpoints.lineRating)} disabled={loading}>Change line rating</button>
            </div>
            <div className="row">
              <label>Random cases</label>
              <input
                type="number"
                min="1"
                value={randomCasesNum}
                onChange={(e) => setRandomCasesNum(e.target.value)}
              />
              <button onClick={() => run(() => endpoints.randomCases(Number(randomCasesNum)))} disabled={loading}>Generate random cases</button>
            </div>
            <div className="row">
              <button onClick={() => run(endpoints.runN2Contingencies)} disabled={loading}>Run N-2 contingencies</button>
              <button onClick={() => run(endpoints.matching)} disabled={loading}>Matching</button>
              <button onClick={() => run(endpoints.simulation)} disabled={loading}>Simulation</button>
            </div>
          </div>
        </section>

        <section className="section result-section">
          <h2>Last response</h2>
          {loading && <p className="status loading">Loading…</p>}
          {error && <pre className="result error">{error}</pre>}
          {result && !error && (
            <pre className="result success">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
          {!result && !error && !loading && (
            <p className="status muted">Trigger an action above to see the API response here.</p>
          )}
        </section>
      </main>
      <footer className="footer">
        <a href="https://hynet-project.eu" target="_blank" rel="noopener noreferrer">HYNET project</a>
        <span className="footer-sep">·</span>
        <span>Horizon Europe</span>
      </footer>
    </div>
  )
}

export default App
