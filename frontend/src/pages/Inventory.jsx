import ResourcePage from "../components/ResourcePage";

function Inventory() {
  return (
    <ResourcePage
      chart={{
        labelKey: "material_name",
        title: "Raw material stock",
        valueKey: "stock_quantity",
      }}
      columns={[
        { key: "material_code", label: "Code" },
        { key: "material_name", label: "Material" },
        { key: "stock_quantity", label: "Stock" },
        { key: "unit_price", label: "Unit price" },
        { key: "supplier_id", label: "Supplier" },
      ]}
      description="Track raw materials, supplier links, stock levels, pricing, and warehouse inputs."
      endpoint="/raw-materials/"
      title="Inventory Management"
    />
  );
}

export default Inventory;
