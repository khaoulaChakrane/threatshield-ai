export default function ScanDetailModal({ scan, onClose }) {
  if (!scan) return null;

  let details = {};
  try {
    details = JSON.parse(scan.details || "{}");
  } catch {
    details = {};
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <span className={`badge badge-${scan.verdict}`}>
            {scan.verdict === "malicious" ? "⚠ Malveillant" : "✓ Bénin"}
          </span>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-target">{scan.target}</div>
        <div className="modal-meta">
          {scan.scan_type.toUpperCase()} · {new Date(scan.created_at).toLocaleString("fr-FR")}
        </div>

        <div className="modal-score-row">
          <div className="risk-bar-track" style={{ width: "100%", height: "8px" }}>
            <div
              className="risk-bar-fill"
              style={{
                width: `${scan.risk_score}%`,
                background: scan.verdict === "malicious" ? "#D6593C" : "#1F4D3D",
              }}
            ></div>
          </div>
          <span className="modal-score">{scan.risk_score}%</span>
        </div>

        <div className="modal-details">
          <div className="modal-details-title">Détails techniques</div>
          <table className="detail-table">
            <tbody>
              {Object.entries(details)
                .filter(([key]) => key !== "stats")
                .map(([key, value]) => (
                  <tr key={key}>
                    <td className="detail-key">{key}</td>
                    <td className="detail-value">
                      {typeof value === "boolean"
                        ? value ? "✓ Oui" : "✕ Non"
                        : String(value)}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>

          {details.stats && (
            <>
              <div className="modal-details-title" style={{ marginTop: "1rem" }}>
                Statistiques moteurs antivirus
              </div>
              <table className="detail-table">
                <tbody>
                  {Object.entries(details.stats).map(([key, value]) => (
                    <tr key={key}>
                      <td className="detail-key">{key}</td>
                      <td className="detail-value">{value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      </div>
    </div>
  );
}