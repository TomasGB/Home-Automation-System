import { API_BASE } from "./config";

export async function getLatestSensorData() {
  const res = await fetch(`${API_BASE}/sensors/latest`);
  return res.json();
}
