import { Building2, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import http from "../services/http";

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const loadDepartments = useCallback(async () => {
    setError("");
    setIsLoading(true);

    try {
      const { data } = await http.get("/departments");
      setDepartments(data);
    } catch (departmentError) {
      setError(
        departmentError.response?.data?.detail ||
          "Unable to load departments from backend.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function fetchInitialDepartments() {
      try {
        const { data } = await http.get("/departments");

        if (isMounted) {
          setDepartments(data);
        }
      } catch (departmentError) {
        if (isMounted) {
          setError(
            departmentError.response?.data?.detail ||
              "Unable to load departments from backend.",
          );
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchInitialDepartments();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Connected module</span>
          <h1>Departments</h1>
          <p>
            Live data from the FastAPI `/departments` endpoint appears here when
            the backend is running and the signed-in user has access.
          </p>
        </div>
        <button
          className="secondary-button"
          disabled={isLoading}
          onClick={loadDepartments}
          type="button"
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>

      <section className="table-panel">
        <div className="table-panel-header">
          <div>
            <h2>Department directory</h2>
            <p>{departments.length} records loaded</p>
          </div>
          <Building2 size={22} />
        </div>

        {error ? <div className="inline-error">{error}</div> : null}

        {isLoading ? (
          <div className="empty-state">Loading departments...</div>
        ) : departments.length ? (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Department</th>
                  <th>Factory ID</th>
                </tr>
              </thead>
              <tbody>
                {departments.map((department) => (
                  <tr key={department.id}>
                    <td>{department.id}</td>
                    <td>{department.department_name}</td>
                    <td>{department.factory_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No departments found.</div>
        )}
      </section>
    </div>
  );
}

export default Departments;
