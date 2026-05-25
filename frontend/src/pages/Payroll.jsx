import ResourcePage from "../components/ResourcePage";

function Payroll() {
  return (
    <ResourcePage
      chart={{
        labelKey: "worker_id",
        title: "Final salary expenses",
        valueKey: "final_salary",
      }}
      columns={[
        { key: "id", label: "ID" },
        { key: "worker_id", label: "Worker" },
        { key: "basic_salary", label: "Basic" },
        { key: "overtime_amount", label: "Overtime" },
        { key: "deductions", label: "Deductions" },
        { key: "final_salary", label: "Final salary" },
        { key: "payment_status", label: "Status" },
      ]}
      description="Manage worker salary expenses, overtime, deductions, and payment status."
      endpoint="/payroll"
      title="Payroll Management"
    />
  );
}

export default Payroll;
