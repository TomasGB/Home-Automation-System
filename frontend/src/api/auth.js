import { API_BASE } from "./config";

export async function login(username, password) {
  const res = await fetch(`${API_BASE}auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  return res.json();
}
