import ResourcePage from "../components/ResourcePage";

function Machinery() {
  return (
    <ResourcePage
      chart={{
        labelKey: "machine_name",
        title: "Machine running hours",
        valueKey: "running_hours",
      }}
      columns={[
        { key: "machine_code", label: "Code" },
        { key: "machine_name", label: "Machine" },
        { key: "machine_type", label: "Type" },
        { key: "department_id", label: "Department" },
        { key: "running_hours", label: "Hours" },
        { key: "machine_status", label: "Status" },
      ]}
      description="Track machinery condition, running hours, department assignment, and status."
      endpoint="/machinery"
      title="Robotics & Machinery"
    />
  );
}

export default Machinery;
