import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import { getHistory } from "../services/api";

export default function History() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [typeFilter, setTypeFilter] = useState("all");
  const [verdictFilter, setVerdictFilter] = useState("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    getHistory()
      .then(setScans)
      .catch(() => setError("Impossible de charger l'historique"))
      .finally(() => setLoading(false));
  }, []);

  const filtered = scans.filter((s) => {
    if (typeFilter !== "all" && s.scan_type !== typeFilter) return false;
    if (verdictFilter !== "all" && s.verdict !== verdictFilter) return false;
    if (search && !s.target.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const types = [...new Set(scans.map((s) => s.scan_type))];

  if (loading) {
    return (
      <Layout>
        <div className="page-title">Historique</div>
        <p className="page-subtitle">Chargement...</p>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-title">Historique</div>
      <div className="page-subtitle">
        {filtered.length} résultat{filtered.length !== 1 ? "s" : ""} sur {scans.length} scans
      </div>

      {error && <div className="auth-error">{error}</div>}

      <div className="filters-bar">
        <input
          type="text"
          placeholder="Rechercher une cible..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="filter-search"
        />

        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
          <option value="all">Tous les types</option>
          {types.map((t) => (
            <option key={t} value={t}>
              {t.toUpperCase()}
            </option>
          ))}
        </select>

        <select value={verdictFilter} onChange={(e) => setVerdictFilter(e.target.value)}>
          <option value="all">Tous les verdicts</option>
          <option value="benign">Bénin</option>
          <option value="malicious">Malveillant</option>
        </select>
      </div>

      {filtered.length === 0 ? (
        <div className="empty-state">Aucun résultat ne correspond à ces filtres.</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Cible</th>
              <th>Risque</th>
              <th>Verdict</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((scan) => (
              <tr key={scan.id}>
                <td>{scan.scan_type.toUpperCase()}</td>
                <td className="cell-target">{scan.target}</td>
                <td>
                  <div className="risk-bar-wrap">
                    <div className="risk-bar-track">
                      <div
                        className="risk-bar-fill"
                        style={{
                          width: `${scan.risk_score}%`,
                          background:
                            scan.verdict === "malicious" ? "#D6593C" : "#1F4D3D",
                        }}
                      ></div>
                    </div>
                    <span className="cell-score">{scan.risk_score}%</span>
                  </div>
                </td>
                <td>
                  <span className={`badge badge-${scan.verdict}`}>
                    {scan.verdict === "malicious" ? "● Menace" : "● Sain"}
                  </span>
                </td>
                <td className="cell-score">
                  {new Date(scan.created_at).toLocaleString("fr-FR")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
}