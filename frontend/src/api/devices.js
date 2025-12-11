import { authFetch } from "./authFetch";

export function setLedState(state) {
  return authFetch("/devices/led", {
    method: "POST",
    body: JSON.stringify({ state })
  });
}

export function getLedStatus() {
  return authFetch("/devices/led/state");
}
