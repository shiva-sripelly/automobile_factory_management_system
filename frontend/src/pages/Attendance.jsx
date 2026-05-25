import ResourcePage from "../components/ResourcePage";

function Attendance() {
  return (
    <ResourcePage
      chart={{
        labelKey: "attendance_date",
        title: "Overtime trend",
        valueKey: "overtime_hours",
      }}
      columns={[
        { key: "id", label: "ID" },
        { key: "worker_id", label: "Worker" },
        { key: "attendance_date", label: "Date" },
        { key: "check_in", label: "Check in" },
        { key: "check_out", label: "Check out" },
        { key: "overtime_hours", label: "Overtime" },
      ]}
      description="Track attendance, check-in/check-out timings, overtime, and worker presence."
      endpoint="/attendance/"
      title="Attendance Tracking"
    />
  );
}

export default Attendance;
