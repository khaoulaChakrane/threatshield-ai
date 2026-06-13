import { useState, useEffect } from "react";
import { Line, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  ArcElement,
  Filler,
} from "chart.js";
import Layout from "../components/Layout";
import { getHistory } from "../services/api";

const centerTextPlugin = {
  id: "centerText",
  afterDraw(chart) {
    const { ctx, chartArea } = chart;
    const x = (chartArea.left + chartArea.right) / 2;
    const y = (chartArea.top + chartArea.bottom) / 2;
    ctx.save();
    ctx.font = "700 22px JetBrains Mono";
    ctx.fillStyle = "#1C1B1A";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(chart.data.datasets[0].data.reduce((a, b) => a + b, 0), x, y);
    ctx.restore();
  },
};

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  ArcElement,
  Filler,
  centerTextPlugin
);

export default function Dashboard() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getHistory()
      .then(setScans)
      .catch(() => setError("Impossible de charger les données"))
      .finally(() => setLoading(false));
  }, []);

  const total = scans.length;
  const malicious = scans.filter((s) => s.verdict === "malicious").length;
  const benign = total - malicious;
  const recentScans = scans.slice(0, 5);

  // Activité des 7 derniers jours
  const days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];
  const counts = new Array(7).fill(0);
  scans.forEach((s) => {
    const d = new Date(s.created_at).getDay(); // 0=dim..6=sam
    const idx = d === 0 ? 6 : d - 1;
    counts[idx]++;
  });

  const lineData = {
    labels: days,
    datasets: [
      {
        data: counts,
        borderColor: "#1F4D3D",
        backgroundColor: "rgba(31,77,61,0.08)",
        fill: true,
        tension: 0.35,
        pointRadius: 0,
      },
    ],
  };

  const donutData = {
    labels: ["Bénins", "Menaces"],
    datasets: [
      {
        data: [benign, malicious],
        backgroundColor: ["#1F4D3D", "#D6593C"],
        borderWidth: 0,
      },
    ],
  };

  if (loading) {
    return (
      <Layout>
        <div className="page-title">Dashboard</div>
        <p className="page-subtitle">Chargement...</p>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-title">Dashboard</div>
      <div className="page-subtitle">Vue d'ensemble de vos analyses</div>

      {error && <div className="auth-error">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🔍</div>
          <div className="stat-value">{total}</div>
          <div className="stat-label">Scans totaux</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-value danger">{malicious}</div>
          <div className="stat-label">Menaces détectées</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-value">{benign}</div>
          <div className="stat-label">Bénins</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-value">
            {total > 0 ? Math.round((malicious / total) * 100) : 0}%
          </div>
          <div className="stat-label">Taux de menace</div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <div className="chart-label">Activité des scans (7 jours)</div>
          <div style={{ height: "120px" }}>
            <Line
              data={lineData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                  x: { grid: { display: false } },
                  y: { display: false, beginAtZero: true },
                },
              }}
            />
          </div>
        </div>

        <div className="chart-card donut-card">
          <div style={{ width: "84px", height: "84px" }}>
            <Doughnut
              data={donutData}
              options={{
                plugins: { legend: { display: false } },
                cutout: "70%",
              }}
            />
          </div>
          <div className="donut-legend">
            <div className="donut-legend-item">
              <span className="donut-legend-dot" style={{ background: "#1F4D3D" }}></span>
              Bénins — <strong>{benign}</strong>
            </div>
            <div className="donut-legend-item">
              <span className="donut-legend-dot" style={{ background: "#D6593C" }}></span>
              Menaces — <strong>{malicious}</strong>
            </div>
          </div>
        </div>
      </div>

      <div className="section-title">Scans récents</div>

      {recentScans.length === 0 ? (
        <div className="empty-state">
          Aucun scan pour le moment. Va sur "Scanner" pour commencer !
        </div>
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
            {recentScans.map((scan) => (
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
                  {new Date(scan.created_at).toLocaleDateString("fr-FR")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
}