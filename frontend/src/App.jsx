import { Navigate, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Advanced from "./pages/Advanced";
import Attendance from "./pages/Attendance";
import CostAnalysis from "./pages/CostAnalysis";
import Dashboard from "./pages/Dashboard";
import Departments from "./pages/Departments";
import Factories from "./pages/Factories";
import Inventory from "./pages/Inventory";
import Login from "./pages/Login";
import Machinery from "./pages/Machinery";
import Maintenance from "./pages/Maintenance";
import Payroll from "./pages/Payroll";
import Profile from "./pages/Profile";
import Production from "./pages/Production";
import Reports from "./pages/Reports";
import Safety from "./pages/Safety";
import Workers from "./pages/Workers";

function ProtectedLayout() {
  const token = localStorage.getItem("afms_token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/departments" element={<Departments />} />
          <Route path="/factories" element={<Factories />} />
          <Route path="/workers" element={<Workers />} />
          <Route path="/attendance" element={<Attendance />} />
          <Route path="/production" element={<Production />} />
          <Route path="/machinery" element={<Machinery />} />
          <Route path="/maintenance" element={<Maintenance />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/payroll" element={<Payroll />} />
          <Route path="/costs" element={<CostAnalysis />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/safety" element={<Safety />} />
          <Route path="/advanced" element={<Advanced />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={<ProtectedLayout />} />
    </Routes>
  );
}

export default App;
