import { authFetch } from "./authFetch";

// GET /devices
export function getDevices() {
  return authFetch("/devices");
}

// POST /devices
export function createDevice(device) {
  return authFetch("devices", {
    method: "POST",
    body: JSON.stringify(device)
  });
}

// DELETE /devices/:id
export function deleteDevice(id) {
  return authFetch(`devices/${id}`, {
    method: "DELETE"
  });
}

// PUT /devices/:id
export function updateDevice(id, data) {
  return authFetch(`devices/${id}`, {
    method: "PUT",
    body: JSON.stringify(data)
  });
}

// POST /devices/:id/state
export function setDeviceState(id, state) {
  return authFetch(`devices/${id}/state`, {
    method: "POST",
    body: JSON.stringify({ state })
  });
}

// POST /devices/:id/learn-action
export function learnDeviceAction(id, action) {
  return authFetch(`devices/${id}/learn-action`, {
    method: "POST",
    body: JSON.stringify({ action })
  });
}
