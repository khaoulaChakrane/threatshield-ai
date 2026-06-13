import { Link, useNavigate, useLocation } from "react-router-dom";
import { logout } from "../services/auth";

export default function Layout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const links = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/scanner", label: "Scanner" },
    { path: "/history", label: "Historique" },
  ];

  return (
    <div className="layout">
      <header className="topbar">
        <div className="topbar-left">
          <div className="topbar-logo">
            ThreatShield<span className="dot">.</span>
          </div>
          <nav className="topbar-nav">
            {links.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`topbar-link ${
                  location.pathname === link.path ? "active" : ""
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="topbar-right">
          <button className="logout-btn" onClick={handleLogout}>
            Déconnexion
          </button>
          <div className="avatar">K</div>
        </div>
      </header>
      <main className="content">{children}</main>
    </div>
  );
}