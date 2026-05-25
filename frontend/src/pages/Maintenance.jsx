import ResourcePage from "../components/ResourcePage";

function Maintenance() {
  return (
    <ResourcePage
      chart={{
        labelKey: "maintenance_type",
        title: "Maintenance cost",
        valueKey: "maintenance_cost",
      }}
      columns={[
        { key: "id", label: "ID" },
        { key: "machine_id", label: "Machine" },
        { key: "robot_id", label: "Robot" },
        { key: "maintenance_type", label: "Type" },
        { key: "maintenance_cost", label: "Cost" },
        { key: "maintenance_date", label: "Date" },
        { key: "technician_name", label: "Technician" },
      ]}
      description="Track machine maintenance cost, robot servicing, downtime, and technician work."
      endpoint="/maintenance"
      title="Maintenance Dashboard"
    />
  );
}

export default Maintenance;
