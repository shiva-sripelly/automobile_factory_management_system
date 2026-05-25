import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("afms_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("afms_token");
      localStorage.removeItem("afms_user");
    }

    return Promise.reject(error);
  },
);

export default http;
