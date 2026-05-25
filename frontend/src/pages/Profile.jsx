import { BadgeCheck, Mail, Shield, UserRound } from "lucide-react";
import { useEffect, useState } from "react";
import http from "../services/http";

function Profile() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("afms_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    http
      .get("/auth/me")
      .then(({ data }) => {
        if (isMounted) {
          setUser(data);
          localStorage.setItem("afms_user", JSON.stringify(data));
        }
      })
      .catch((profileError) => {
        if (isMounted) {
          setError(profileError.response?.data?.detail || "Unable to load profile.");
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <span className="eyebrow">Account</span>
          <h1>Profile</h1>
          <p>Manage the active AutoFactory Management session and user identity.</p>
        </div>
      </header>

      {error ? <div className="inline-error">{error}</div> : null}

      <section className="profile-panel">
        <div className="profile-hero">
          <div className="profile-avatar">
            {(user?.full_name || "AF")
              .split(" ")
              .slice(0, 2)
              .map((part) => part[0])
              .join("")
              .toUpperCase()}
          </div>
          <div>
            <h2>{user?.full_name || "AutoFactory User"}</h2>
            <p>{user?.role || "Signed-in team member"}</p>
          </div>
        </div>

        <div className="profile-grid">
          <article className="profile-card">
            <UserRound size={20} />
            <span>User ID</span>
            <strong>{user?.id ?? "-"}</strong>
          </article>
          <article className="profile-card">
            <Mail size={20} />
            <span>Email</span>
            <strong>{user?.email ?? "-"}</strong>
          </article>
          <article className="profile-card">
            <Shield size={20} />
            <span>Role</span>
            <strong>{user?.role ?? "-"}</strong>
          </article>
          <article className="profile-card">
            <BadgeCheck size={20} />
            <span>Status</span>
            <strong>{user?.is_active ? "Active" : "Inactive"}</strong>
          </article>
        </div>
      </section>
    </div>
  );
}

export default Profile;
