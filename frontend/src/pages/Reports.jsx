import { FileText, RefreshCw } from "lucide-react";
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

function flattenReport(report) {
  return Object.entries(report).flatMap(([group, values]) =>
    Object.entries(values || {}).map(([key, value]) => ({
      metric: `${group} ${key}`.replaceAll("_", " "),
      value: Number(value) || 0,
    })),
  );
}

function Reports() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function loadReport() {
      try {
        const { data } = await http.get("/reports/dashboard");

        if (isMounted) {
          setReport(data);
        }
      } catch (reportError) {
        if (isMounted) {
          setError(
            reportError.response?.data?.detail || "Unable to load reports.",
          );
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadReport();

    return () => {
      isMounted = false;
    };
  }, []);

  const chartRows = useMemo(() => (report ? flattenReport(report) : []), [report]);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Reports center</span>
          <h1>Reports & Analytics</h1>
          <p>
            Monthly cost reports, profit/loss inputs, production efficiency,
            downtime analysis, inventory totals, and safety metrics.
          </p>
        </div>
        <button className="secondary-button" onClick={() => window.print()} type="button">
          <FileText size={16} />
          Export PDF
        </button>
      </header>

      {error ? <div className="inline-error">{error}</div> : null}

      <section className="chart-panel">
        <div className="table-panel-header">
          <div>
            <h2>Analytics overview</h2>
            <p>{isLoading ? "Loading report..." : `${chartRows.length} metrics`}</p>
          </div>
          <RefreshCw size={20} />
        </div>
        <div className="chart-canvas">
          <ResponsiveContainer height={320} width="100%">
            <BarChart data={chartRows.slice(0, 14)}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="metric" hide />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0f766e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="report-grid">
        {report
          ? Object.entries(report).map(([group, values]) => (
              <article className="report-card" key={group}>
                <h2>{group.replaceAll("_", " ")}</h2>
                {Object.entries(values || {}).map(([key, value]) => (
                  <div className="report-row" key={key}>
                    <span>{key.replaceAll("_", " ")}</span>
                    <strong>{Number(value).toLocaleString()}</strong>
                  </div>
                ))}
              </article>
            ))
          : null}
      </section>
    </div>
  );
}

export default Reports;
