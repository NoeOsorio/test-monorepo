import { useMemo, useState } from "react";

function App() {
  const [baseUrl, setBaseUrl] = useState(
    (import.meta.env.VITE_API_URL || "").trim() || "http://localhost:5051",
  );
  const [snapshotText, setSnapshotText] = useState(
    '{\n  "source": "frontend",\n  "note": "test call"\n}',
  );

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const resolvedBaseUrl = useMemo(() => baseUrl.trim(), [baseUrl]);

  function buildUrl(path) {
    const base = resolvedBaseUrl.trim();
    if (!base) return path;
    if (base.endsWith("/"))
      return new URL(path.replace(/^\//, ""), base).toString();
    return new URL(path, base).toString();
  }

  async function runRequest({ label, path, method = "GET", body }) {
    setLoading(true);
    setError("");
    setResult(null);

    const startedAt = performance.now();
    try {
      const res = await fetch(buildUrl(path), {
        method,
        headers: body ? { "Content-Type": "application/json" } : undefined,
        body: body ? JSON.stringify(body) : undefined,
      });

      const contentType = res.headers.get("content-type") || "";
      const data = contentType.includes("application/json")
        ? await res.json()
        : await res.text();

      setResult({
        label,
        url: buildUrl(path),
        method,
        ok: res.ok,
        status: res.status,
        elapsedMs: Math.round(performance.now() - startedAt),
        data,
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  function parseSnapshot() {
    const text = snapshotText.trim();
    if (!text) return null;
    return JSON.parse(text);
  }

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1>Monorepo API Tester</h1>
          <p className="muted">
            Use this to hit the Flask test endpoints and inspect responses.
          </p>
        </div>
      </div>

      <div className="card">
        <label className="label" htmlFor="baseUrl">
          Backend base URL
        </label>
        <div className="row">
          <input
            id="baseUrl"
            className="input"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            placeholder="http://localhost:5051"
            spellCheck={false}
          />
          <button
            className="button"
            onClick={() =>
              runRequest({ label: "Home", path: "/", method: "GET" })
            }
            disabled={loading}
            type="button"
          >
            GET /
          </button>
        </div>
        <div className="hint">
          Resolved: <span className="mono">{resolvedBaseUrl || "(empty)"}</span>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <div className="sectionTitle">Quick tests</div>
          <div className="buttonGrid">
            <button
              className="button"
              onClick={() =>
                runRequest({ label: "Health", path: "/api/health" })
              }
              disabled={loading}
              type="button"
            >
              GET /api/health
            </button>
            <button
              className="button"
              onClick={() => runRequest({ label: "Data", path: "/api/data" })}
              disabled={loading}
              type="button"
            >
              GET /api/data
            </button>
            <button
              className="button"
              onClick={() =>
                runRequest({ label: "DB Test", path: "/api/db/test" })
              }
              disabled={loading}
              type="button"
            >
              GET /api/db/test
            </button>
            <button
              className="button"
              onClick={() =>
                runRequest({
                  label: "Env Vars",
                  path: "/api/test/environment-variables",
                })
              }
              disabled={loading}
              type="button"
            >
              GET /api/test/environment-variables
            </button>
            <button
              className="button"
              onClick={() =>
                runRequest({ label: "Calls List", path: "/api/calls" })
              }
              disabled={loading}
              type="button"
            >
              GET /api/calls
            </button>
          </div>
        </div>

        <div className="card">
          <div className="sectionTitle">Create call</div>
          <label className="label" htmlFor="snapshot">
            Snapshot (JSON)
          </label>
          <textarea
            id="snapshot"
            className="textarea mono"
            value={snapshotText}
            onChange={(e) => setSnapshotText(e.target.value)}
            rows={8}
            spellCheck={false}
          />
          <div className="row">
            <button
              className="button primary"
              onClick={() =>
                runRequest({
                  label: "Create Call",
                  path: "/api/calls",
                  method: "POST",
                  body: parseSnapshot(),
                })
              }
              disabled={loading}
              type="button"
            >
              POST /api/calls
            </button>
            <button
              className="button"
              onClick={() => setSnapshotText("")}
              disabled={loading}
              type="button"
            >
              Clear
            </button>
          </div>
          <div className="hint">
            Leave empty to POST without a snapshot body.
          </div>
        </div>
      </div>

      <div className="card">
        <div className="sectionTitle">Response</div>
        {loading && <div className="muted">Loading…</div>}
        {!loading && error && <div className="error">{error}</div>}
        {!loading && !error && !result && (
          <div className="muted">Run a request to see output.</div>
        )}
        {!loading && !error && result && (
          <div>
            <div className="meta">
              <span className="badge">{result.method}</span>
              <span className={`badge ${result.ok ? "ok" : "bad"}`}>
                {result.status}
              </span>
              <span className="badge">{result.elapsedMs}ms</span>
              <span className="mono">{result.url}</span>
            </div>
            <pre className="pre mono">
              {typeof result.data === "string"
                ? result.data
                : JSON.stringify(result.data, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
