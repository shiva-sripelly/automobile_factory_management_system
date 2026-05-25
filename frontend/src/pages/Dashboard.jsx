import { Activity, Bell, Boxes, Gauge, ShieldCheck, Users } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import http from "../services/http";

function Dashboard() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("afms_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [report, setReport] = useState(null);

  useEffect(() => {
    let isMounted = true;

    Promise.allSettled([http.get("/auth/me"), http.get("/reports/dashboard")]).then(
      ([userResult, reportResult]) => {
        if (!isMounted) {
          return;
        }

        if (userResult.status === "fulfilled") {
          setUser(userResult.value.data);
          localStorage.setItem("afms_user", JSON.stringify(userResult.value.data));
        }

        if (reportResult.status === "fulfilled") {
          setReport(reportResult.value.data);
        }
      },
    );

    return () => {
      isMounted = false;
    };
  }, []);

  const stats = [
    {
      icon: Users,
      label: "Active workers",
      value: report?.workers?.active ?? 0,
    },
    {
      icon: Gauge,
      label: "Production records",
      value: report?.production?.total_records ?? 0,
    },
    {
      icon: Boxes,
      label: "Inventory value",
      value: report?.inventory?.total_inventory_value ?? 0,
    },
    {
      icon: ShieldCheck,
      label: "Safety incidents",
      value: report?.safety?.total_incidents ?? 0,
    },
  ];

  const chartRows = useMemo(
    () => [
      { name: "Payroll", value: Number(report?.finance?.total_payroll) || 0 },
      {
        name: "Factory",
        value: Number(report?.finance?.total_factory_expenses) || 0,
      },
      {
        name: "Maintenance",
        value: Number(report?.finance?.total_maintenance_cost) || 0,
      },
      {
        name: "Production",
        value: Number(report?.production?.total_cost) || 0,
      },
    ],
    [report],
  );

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Factory dashboard</span>
          <h1>Dashboard</h1>
          <p>
            Welcome{user?.full_name ? `, ${user.full_name}` : ""}. Monitor
            production, workers, inventory, cost, reports, and safety from one
            responsive workspace.
          </p>
        </div>
        <div className="status-pill">
          <Activity size={16} />
          Backend ready
        </div>
      </header>

      <section className="notification-strip">
        <Bell size={18} />
        <span>
          Automated alerts are ready for low stock, machine downtime, safety
          incidents, and maintenance follow-ups.
        </span>
      </section>

      <section className="stat-grid" aria-label="Operations summary">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <article className="stat-card" key={stat.label}>
              <Icon size={20} />
              <strong>{Number(stat.value).toLocaleString()}</strong>
              <span>{stat.label}</span>
            </article>
          );
        })}
      </section>

      <section className="chart-panel">
        <div className="table-panel-header">
          <div>
            <h2>Cost overview</h2>
            <p>Payroll, factory, maintenance, and production cost tracking</p>
          </div>
        </div>
        <div className="chart-canvas">
          <ResponsiveContainer height={300} width="100%">
            <BarChart data={chartRows}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0f766e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
