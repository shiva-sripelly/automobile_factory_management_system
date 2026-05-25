import { Bell, Cpu, QrCode, ScanFace, Zap } from "lucide-react";
import { useEffect, useState } from "react";
import http from "../services/http";

const featureCards = [
  {
    icon: QrCode,
    title: "QR/Barcode Tracking",
    text: "Ready for material, worker, and vehicle traceability screens.",
  },
  {
    icon: ScanFace,
    title: "Face Recognition Attendance",
    text: "Attendance flow can be extended with camera-based identity checks.",
  },
  {
    icon: Bell,
    title: "Automated Alert System",
    text: "Notification hooks are prepared for machine, safety, and inventory alerts.",
  },
  {
    icon: Zap,
    title: "Predictive Maintenance",
    text: "Maintenance and machine-health endpoints provide the data foundation.",
  },
];

function Advanced() {
  const [iot, setIot] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    async function loadAdvancedData() {
      try {
        const [iotResponse, predictionResponse] = await Promise.all([
          http.get("/iot-monitoring/factory-status"),
          http.get("/ai-production-prediction/next-day"),
        ]);

        if (isMounted) {
          setIot(iotResponse.data);
          setPrediction(predictionResponse.data);
        }
      } catch (advancedError) {
        if (isMounted) {
          setError(
            advancedError.response?.data?.detail ||
              "Unable to load advanced monitoring data.",
          );
        }
      }
    }

    loadAdvancedData();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Advanced features</span>
          <h1>AI & IoT Monitoring</h1>
          <p>
            AI production prediction, IoT machine integration, real-time machine
            monitoring, alerts, multi-factory expansion, and automation-ready
            workflows.
          </p>
        </div>
      </header>

      {error ? <div className="inline-error">{error}</div> : null}

      <section className="stat-grid">
        <article className="stat-card">
          <Cpu size={20} />
          <strong>{iot?.machinery?.active ?? 0}</strong>
          <span>Active machines</span>
        </article>
        <article className="stat-card">
          <Cpu size={20} />
          <strong>{iot?.robotics?.active ?? 0}</strong>
          <span>Active robots</span>
        </article>
        <article className="stat-card">
          <Zap size={20} />
          <strong>{iot?.machinery?.total_running_hours ?? 0}</strong>
          <span>Running hours</span>
        </article>
        <article className="stat-card">
          <Bell size={20} />
          <strong>{prediction?.predictions?.length ?? 0}</strong>
          <span>AI predictions</span>
        </article>
      </section>

      <section className="feature-grid">
        {featureCards.map((feature) => {
          const Icon = feature.icon;
          return (
            <article className="report-card" key={feature.title}>
              <Icon size={22} />
              <h2>{feature.title}</h2>
              <p>{feature.text}</p>
            </article>
          );
        })}
      </section>
    </div>
  );
}

export default Advanced;
