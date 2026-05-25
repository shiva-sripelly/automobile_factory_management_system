import ResourcePage from "../components/ResourcePage";

function Production() {
  return (
    <ResourcePage
      chart={{
        labelKey: "line_name",
        title: "Live production counters",
        valueKey: "current_output",
      }}
      columns={[
        { key: "id", label: "ID" },
        { key: "line_name", label: "Line" },
        { key: "department_id", label: "Department" },
        { key: "target_per_day", label: "Daily target" },
        { key: "current_output", label: "Current output" },
      ]}
      description="Monitor production lines, targets, current output, and live manufacturing counters."
      endpoint="/production-lines/"
      title="Production Monitoring"
    />
  );
}

export default Production;
