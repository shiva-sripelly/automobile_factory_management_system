import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/auth": "http://127.0.0.1:8000",
      "/ai-production-prediction": "http://127.0.0.1:8000",
      "/analytics": "http://127.0.0.1:8000",
      "/attendance": "http://127.0.0.1:8000",
      "/departments": "http://127.0.0.1:8000",
      "/factory-expenses": "http://127.0.0.1:8000",
      "/factories": "http://127.0.0.1:8000",
      "/inventory-transactions": "http://127.0.0.1:8000",
      "/iot-monitoring": "http://127.0.0.1:8000",
      "/machinery": "http://127.0.0.1:8000",
      "/maintenance": "http://127.0.0.1:8000",
      "/payroll": "http://127.0.0.1:8000",
      "/production-lines": "http://127.0.0.1:8000",
      "/raw-materials": "http://127.0.0.1:8000",
      "/reports": "http://127.0.0.1:8000",
      "/safety-incidents": "http://127.0.0.1:8000",
      "/workers": "http://127.0.0.1:8000",
    },
  },
});
