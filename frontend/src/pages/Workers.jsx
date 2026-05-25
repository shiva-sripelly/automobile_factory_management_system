import ResourcePage from "../components/ResourcePage";

function Workers() {
  return (
    <ResourcePage
      chart={{
        labelKey: "full_name",
        title: "Salary distribution",
        valueKey: "salary",
      }}
      columns={[
        { key: "employee_code", label: "Code" },
        { key: "full_name", label: "Worker" },
        { key: "designation", label: "Designation" },
        { key: "department_id", label: "Department" },
        { key: "shift_type", label: "Shift" },
        { key: "salary", label: "Salary" },
        { key: "status", label: "Status" },
      ]}
      description="Manage workers, salary records, shifts, and active employment status."
      endpoint="/workers"
      title="Worker Management"
    />
  );
}

export default Workers;
