import { Download, FileText, RefreshCw, Search } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
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

function formatValue(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  if (typeof value === "number") {
    return value.toLocaleString();
  }

  return String(value);
}

function downloadCsv(filename, rows, columns) {
  const header = columns.map((column) => column.label).join(",");
  const body = rows
    .map((row) =>
      columns
        .map((column) => `"${formatValue(row[column.key]).replaceAll('"', '""')}"`)
        .join(","),
    )
    .join("\n");
  const blob = new Blob([`${header}\n${body}`], {
    type: "text/csv;charset=utf-8;",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function ResourcePage({
  title,
  eyebrow = "ERP module",
  description,
  endpoint,
  columns,
  chart,
}) {
  const [rows, setRows] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [query, setQuery] = useState("");

  const loadRows = useCallback(async () => {
    setError("");
    setIsLoading(true);

    try {
      const { data } = await http.get(endpoint);
      setRows(Array.isArray(data) ? data : []);
    } catch (resourceError) {
      setError(
        resourceError.response?.data?.detail || `Unable to load ${title}.`,
      );
    } finally {
      setIsLoading(false);
    }
  }, [endpoint, title]);

  useEffect(() => {
    let isMounted = true;

    async function fetchInitialRows() {
      try {
        const { data } = await http.get(endpoint);

        if (isMounted) {
          setRows(Array.isArray(data) ? data : []);
        }
      } catch (resourceError) {
        if (isMounted) {
          setError(
            resourceError.response?.data?.detail || `Unable to load ${title}.`,
          );
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchInitialRows();

    return () => {
      isMounted = false;
    };
  }, [endpoint, title]);

  const filteredRows = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    if (!normalizedQuery) {
      return rows;
    }

    return rows.filter((row) =>
      columns.some((column) =>
        formatValue(row[column.key]).toLowerCase().includes(normalizedQuery),
      ),
    );
  }, [columns, query, rows]);

  const chartRows = useMemo(() => {
    if (!chart) {
      return [];
    }

    return filteredRows.slice(0, 8).map((row) => ({
      name: formatValue(row[chart.labelKey]),
      value: Number(row[chart.valueKey]) || 0,
    }));
  }, [chart, filteredRows]);

  const shouldShowChart = chart && !error && (isLoading || chartRows.length > 0);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">{eyebrow}</span>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
        <button
          className="secondary-button"
          disabled={isLoading}
          onClick={loadRows}
          type="button"
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>

      <section className="module-toolbar" aria-label={`${title} tools`}>
        <label className="search-field">
          <Search size={17} />
          <input
            onChange={(event) => setQuery(event.target.value)}
            placeholder={`Search ${title.toLowerCase()}`}
            type="search"
            value={query}
          />
        </label>
        <div className="toolbar-actions">
          <button
            className="secondary-button"
            onClick={() =>
              downloadCsv(
                `${title.toLowerCase().replaceAll(" ", "-")}.csv`,
                filteredRows,
                columns,
              )
            }
            type="button"
          >
            <Download size={16} />
            Excel
          </button>
          <button
            className="secondary-button"
            onClick={() => window.print()}
            type="button"
          >
            <FileText size={16} />
            PDF
          </button>
        </div>
      </section>

      {shouldShowChart ? (
        <section className="chart-panel">
          <div className="table-panel-header">
            <div>
              <h2>{chart.title}</h2>
              <p>Top {chartRows.length} records from the current filter</p>
            </div>
          </div>
          <div className="chart-canvas">
            {isLoading ? (
              <div className="empty-state">Loading chart...</div>
            ) : (
              <ResponsiveContainer height={260} width="100%">
                <BarChart data={chartRows}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#0f766e" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </section>
      ) : null}

      <section className="table-panel">
        <div className="table-panel-header">
          <div>
            <h2>{title} records</h2>
            <p>{filteredRows.length} records shown</p>
          </div>
        </div>

        {error ? <div className="inline-error">{error}</div> : null}

        {isLoading ? (
          <div className="empty-state">Loading {title.toLowerCase()}...</div>
        ) : filteredRows.length ? (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  {columns.map((column) => (
                    <th key={column.key}>{column.label}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredRows.map((row) => (
                  <tr key={row.id ?? JSON.stringify(row)}>
                    {columns.map((column) => (
                      <td key={column.key}>{formatValue(row[column.key])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No records found.</div>
        )}
      </section>
    </div>
  );
}

export default ResourcePage;
