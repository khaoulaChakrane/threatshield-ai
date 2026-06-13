import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8001/api",
});

// Ajoute automatiquement le token JWT à chaque requête
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function getHistory() {
  const res = await api.get("/history/");
  return res.data;
}

export default api;