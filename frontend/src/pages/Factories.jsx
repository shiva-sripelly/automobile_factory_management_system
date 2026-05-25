import { Factory, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import http from "../services/http";

function Factories() {
  const [factories, setFactories] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const loadFactories = useCallback(async () => {
    setError("");
    setIsLoading(true);

    try {
      const { data } = await http.get("/factories");
      setFactories(data);
    } catch (factoryError) {
      setError(
        factoryError.response?.data?.detail ||
          "Unable to load factories from backend.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function fetchInitialFactories() {
      try {
        const { data } = await http.get("/factories");

        if (isMounted) {
          setFactories(data);
        }
      } catch (factoryError) {
        if (isMounted) {
          setError(
            factoryError.response?.data?.detail ||
              "Unable to load factories from backend.",
          );
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchInitialFactories();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Connected module</span>
          <h1>Factories</h1>
          <p>
            Live data from the FastAPI `/factories` endpoint, including factory
            location and department totals.
          </p>
        </div>
        <button
          className="secondary-button"
          disabled={isLoading}
          onClick={loadFactories}
          type="button"
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>

      <section className="table-panel">
        <div className="table-panel-header">
          <div>
            <h2>Factory directory</h2>
            <p>{factories.length} records loaded</p>
          </div>
          <Factory size={22} />
        </div>

        {error ? <div className="inline-error">{error}</div> : null}

        {isLoading ? (
          <div className="empty-state">Loading factories...</div>
        ) : factories.length ? (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Factory</th>
                  <th>Location</th>
                  <th>Departments</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {factories.map((factory) => (
                  <tr key={factory.id}>
                    <td>{factory.id}</td>
                    <td>{factory.factory_name}</td>
                    <td>{factory.location}</td>
                    <td>{factory.total_departments}</td>
                    <td>
                      {factory.created_at
                        ? new Date(factory.created_at).toLocaleDateString()
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No factories found.</div>
        )}
      </section>
    </div>
  );
}

export default Factories;
