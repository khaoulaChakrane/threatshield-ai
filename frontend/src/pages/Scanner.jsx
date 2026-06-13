import { useState } from "react";
import Layout from "../components/Layout";
import { scanUrl, scanIp, scanDomain } from "../services/api";

export default function Scanner() {
  const [scanType, setScanType] = useState("url");
  const [target, setTarget] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handlers = { url: scanUrl, ip: scanIp, domain: scanDomain };

  const labels = {
    url: "URL à analyser",
    ip: "Adresse IP à analyser",
    domain: "Domaine à analyser",
  };

  const placeholders = {
    url: "https://example.com",
    ip: "118.25.6.39",
    domain: "example.com",
  };

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const data = await handlers[scanType](target);
      setResult(data);
    } catch (err) {
      setError("Erreur lors de l'analyse. Vérifie le format et réessaie.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <div className="page-title">Scanner</div>
      <div className="page-subtitle">Analyser une URL, une IP ou un domaine</div>

      <div className="chart-card" style={{ maxWidth: "560px" }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Type de cible</label>
            <div className="scan-type-toggle">
              <button
                type="button"
                className={`toggle-btn ${scanType === "url" ? "active" : ""}`}
                onClick={() => setScanType("url")}
              >
                URL
              </button>
              <button
                type="button"
                className={`toggle-btn ${scanType === "ip" ? "active" : ""}`}
                onClick={() => setScanType("ip")}
              >
                Adresse IP
              </button>
              <button
                type="button"
                className={`toggle-btn ${scanType === "domain" ? "active" : ""}`}
                onClick={() => setScanType("domain")}
              >
                Domaine
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>{labels[scanType]}</label>
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder={placeholders[scanType]}
              required
            />
          </div>

          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Analyse en cours..." : "Lancer l'analyse"}
          </button>
        </form>
      </div>

      {error && (
        <div className="auth-error" style={{ maxWidth: "560px", marginTop: "1rem" }}>
          {error}
        </div>
      )}

      {result && (
        <div className="scan-result" style={{ maxWidth: "560px" }}>
          <div className="scan-result-header">
            <span className={`badge badge-${result.verdict}`}>
              {result.verdict === "malicious" ? "⚠ Malveillant" : "✓ Bénin"}
            </span>
            <span className="scan-result-score">{result.risk_score}%</span>
          </div>
          <div className="scan-result-target">{result.target}</div>
          <div className="risk-bar-track" style={{ width: "100%", height: "8px" }}>
            <div
              className="risk-bar-fill"
              style={{
                width: `${result.risk_score}%`,
                background: result.verdict === "malicious" ? "#D6593C" : "#1F4D3D",
              }}
            ></div>
          </div>
          <div className="scan-result-date">
            Analysé le {new Date(result.created_at).toLocaleString("fr-FR")}
          </div>
        </div>
      )}
    </Layout>
  );
}