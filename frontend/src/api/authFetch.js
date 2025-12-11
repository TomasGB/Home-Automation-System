import { API_BASE } from "./config";

export async function authFetch(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }


  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers
  });

  return res.json();
}
