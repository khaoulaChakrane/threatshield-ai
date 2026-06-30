import { useState } from "react";
import Layout from "../components/Layout";
import { scanUrl, scanIp, scanDomain, scanFile, scanEmail, predictML } from "../services/api";

export default function Scanner() {
  const [scanType, setScanType] = useState("url");
  const [target, setTarget] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [mlResult, setMlResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const labels = {
    url: "URL à analyser",
    ip: "Adresse IP à analyser",
    domain: "Domaine à analyser",
    file: "Fichier à analyser",
    email: "Email (.eml) à analyser",
  };

  const placeholders = {
    url: "https://example.com",
    ip: "118.25.6.39",
    domain: "example.com",
  };

  const types = [
    { key: "url", label: "URL" },
    { key: "ip", label: "Adresse IP" },
    { key: "domain", label: "Domaine" },
    { key: "file", label: "Fichier" },
    { key: "email", label: "Email" },
  ];

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setMlResult(null);
    setLoading(true);

    try {
      let data;
      if (scanType === "url") {
        data = await scanUrl(target);
        try {
          const ml = await predictML(target);
          setMlResult(ml);
        } catch (mlErr) {
          console.error("ML Error:", mlErr.response?.status, mlErr.response?.data);
        }
      } else if (scanType === "ip") {
        data = await scanIp(target);
      } else if (scanType === "domain") {
        data = await scanDomain(target);
      } else if (scanType === "file") {
        if (!file) { setError("Sélectionne un fichier d'abord"); setLoading(false); return; }
        data = await scanFile(file);
      } else if (scanType === "email") {
        if (!file) { setError("Sélectionne un fichier .eml d'abord"); setLoading(false); return; }
        data = await scanEmail(file);
      }
      setResult(data);
    } catch (err) {
      setError("Erreur lors de l'analyse. Vérifie le format et réessaie.");
    } finally {
      setLoading(false);
    }
  }

  const isFileInput = scanType === "file" || scanType === "email";

  return (
    <Layout>
      <div className="page-title">Scanner</div>
      <div className="page-subtitle">
        Analyser une URL, une IP, un domaine, un fichier ou un email
      </div>

      <div className="chart-card" style={{ maxWidth: "560px" }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Type de cible</label>
            <div className="scan-type-toggle">
              {types.map((t) => (
                <button
                  key={t.key}
                  type="button"
                  className={`toggle-btn ${scanType === t.key ? "active" : ""}`}
                  onClick={() => {
                    setScanType(t.key);
                    setResult(null);
                    setMlResult(null);
                    setError("");
                  }}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>{labels[scanType]}</label>
            {isFileInput ? (
              <input
                type="file"
                accept={scanType === "email" ? ".eml" : undefined}
                onChange={(e) => setFile(e.target.files[0])}
                required
              />
            ) : (
              <input
                type="text"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                placeholder={placeholders[scanType]}
                required
              />
            )}
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
        <div style={{ maxWidth: "560px", marginTop: "1rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}>

          <div className="scan-result">
            <div className="scan-result-header">
              <div>
                <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)", marginBottom: "4px" }}>
                  VirusTotal / Heuristique
                </div>
                <span className={`badge badge-${result.verdict}`}>
                  {result.verdict === "malicious" ? "⚠ Malveillant" : "✓ Bénin"}
                </span>
              </div>
              <span className="scan-result-score">{result.risk_score}%</span>
            </div>
            <div className="scan-result-target">{result.target}</div>
            <div className="risk-bar-track" style={{ width: "100%", height: "8px" }}>
              <div className="risk-bar-fill" style={{
                width: `${result.risk_score}%`,
                background: result.verdict === "malicious" ? "#D6593C" : "#1F4D3D",
              }}></div>
            </div>
            <div className="scan-result-date">
              Analysé le {new Date(result.created_at).toLocaleString("fr-FR")}
            </div>
          </div>

          {mlResult && (
            <div className="scan-result">
              <div className="scan-result-header">
                <div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)", marginBottom: "4px" }}>
                     Analyse comportementale ML
                  </div>
                  <span className={`badge badge-${mlResult.ml_verdict}`}>
                    {mlResult.ml_verdict === "malicious" ? "⚠ Malveillant" : "✓ Bénin"}
                  </span>
                </div>
                <span className="scan-result-score">{mlResult.ml_score}%</span>
              </div>
              <div className="risk-bar-track" style={{ width: "100%", height: "8px", marginBottom: "0.75rem" }}>
                <div className="risk-bar-fill" style={{
                  width: `${mlResult.ml_score}%`,
                  background: mlResult.ml_verdict === "malicious" ? "#D6593C" : "#1F4D3D",
                }}></div>
              </div>
              {mlResult.top_features && (
                <div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)", marginBottom: "6px", fontWeight: 600 }}>
                    Features décisives :
                  </div>
                  {mlResult.top_features.map((f) => (
                    <div key={f.feature} style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: "0.8rem",
                      padding: "4px 0",
                      borderBottom: "1px solid var(--border)",
                    }}>
                      <span style={{ fontFamily: "var(--font-mono)", color: "var(--text-secondary)" }}>
                        {f.feature}
                      </span>
                      <span style={{ fontWeight: 600 }}>{f.importance}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

        </div>
      )}
    </Layout>
  );
}