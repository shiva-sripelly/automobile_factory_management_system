import ResourcePage from "../components/ResourcePage";

function Safety() {
  return (
    <ResourcePage
      columns={[
        { key: "id", label: "ID" },
        { key: "worker_id", label: "Worker" },
        { key: "incident_type", label: "Incident" },
        { key: "incident_date", label: "Date" },
        { key: "severity", label: "Severity" },
        { key: "remarks", label: "Remarks" },
      ]}
      description="Monitor safety incidents, severity, worker involvement, incident cost tracking inputs, and alerts."
      endpoint="/safety-incidents/"
      title="Safety Monitoring"
    />
  );
}

export default Safety;
