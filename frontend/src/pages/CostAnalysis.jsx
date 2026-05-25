import ResourcePage from "../components/ResourcePage";

function CostAnalysis() {
  return (
    <ResourcePage
      chart={{
        labelKey: "expense_type",
        title: "Factory expense breakdown",
        valueKey: "amount",
      }}
      columns={[
        { key: "id", label: "ID" },
        { key: "expense_type", label: "Expense type" },
        { key: "amount", label: "Amount" },
        { key: "expense_date", label: "Date" },
        { key: "remarks", label: "Remarks" },
      ]}
      description="Analyze electricity usage, raw material cost, production line cost, warehouse expenses, and other factory spend."
      endpoint="/factory-expenses/"
      title="Cost Analysis"
    />
  );
}

export default CostAnalysis;
