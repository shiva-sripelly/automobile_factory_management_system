import {
  Activity,
  BarChart3,
  Building2,
  Calculator,
  Cpu,
  Factory,
  Gauge,
  LogOut,
  Moon,
  Package,
  ReceiptText,
  ShieldCheck,
  Sun,
  Users,
  Wrench,
} from "lucide-react";
import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";

const navItems = [
  { label: "Dashboard", path: "/", icon: Gauge, enabled: true },
  { label: "Factories", path: "/factories", icon: Factory, enabled: true },
  { label: "Departments", path: "/departments", icon: Building2, enabled: true },
  { label: "Workers", path: "/workers", icon: Users, enabled: true },
  { label: "Attendance", path: "/attendance", icon: Activity, enabled: true },
  { label: "Production", path: "/production", icon: BarChart3, enabled: true },
  { label: "Machinery", path: "/machinery", icon: Cpu, enabled: true },
  { label: "Maintenance", path: "/maintenance", icon: Wrench, enabled: true },
  { label: "Inventory", path: "/inventory", icon: Package, enabled: true },
  { label: "Payroll", path: "/payroll", icon: ReceiptText, enabled: true },
  { label: "Costs", path: "/costs", icon: Calculator, enabled: true },
  { label: "Reports", path: "/reports", icon: BarChart3, enabled: true },
  { label: "Safety", path: "/safety", icon: ShieldCheck, enabled: true },
  { label: "AI & IoT", path: "/advanced", icon: Cpu, enabled: true },
];

function Sidebar() {
  const navigate = useNavigate();
  const user = (() => {
    const saved = localStorage.getItem("afms_user");
    return saved ? JSON.parse(saved) : null;
  })();
  const [isDarkMode, setIsDarkMode] = useState(
    () => localStorage.getItem("afms_theme") === "dark",
  );

  useEffect(() => {
    document.documentElement.classList.toggle("dark-mode", isDarkMode);
    localStorage.setItem("afms_theme", isDarkMode ? "dark" : "light");
  }, [isDarkMode]);

  const handleLogout = () => {
    localStorage.removeItem("afms_token");
    localStorage.removeItem("afms_user");
    navigate("/login", { replace: true });
  };

  return (
    <aside className="sidebar">
      <NavLink
        className={({ isActive }) =>
          isActive ? "sidebar-brand profile-link active" : "sidebar-brand profile-link"
        }
        to="/profile"
      >
        <div className="brand-mark">AF</div>
        <div>
          <strong>{user?.full_name || "AutoFactory"}</strong>
          <span>{user?.role ? `${user.role} profile` : "Management profile"}</span>
        </div>
      </NavLink>

      <nav className="sidebar-nav" aria-label="Main navigation">
        {navItems.map((item) => {
          const Icon = item.icon;

          if (!item.enabled) {
            return (
              <button
                className="nav-item disabled"
                disabled
                key={item.label}
                title="Module will be connected next"
                type="button"
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          }

          return (
            <NavLink
              className={({ isActive }) =>
                isActive ? "nav-item active" : "nav-item"
              }
              end={item.path === "/"}
              key={item.label}
              to={item.path}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <button
        className="theme-button"
        onClick={() => setIsDarkMode((current) => !current)}
        type="button"
      >
        {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
        <span>{isDarkMode ? "Light mode" : "Dark mode"}</span>
      </button>

      <button className="logout-button" onClick={handleLogout} type="button">
        <LogOut size={18} />
        <span>Logout</span>
      </button>
    </aside>
  );
}

export default Sidebar;
