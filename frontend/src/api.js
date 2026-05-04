const API_BASE_URL = "http://127.0.0.1:8000/api";

async function parseResponse(response) {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Something went wrong");
  }
  return data;
}

export async function signup(payload) {
  const response = await fetch(`${API_BASE_URL}/users/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse(response);
}

export async function signin(payload) {
  const response = await fetch(`${API_BASE_URL}/users/signin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse(response);
}

export async function fetchUsers() {
  const response = await fetch(`${API_BASE_URL}/users/`);
  return parseResponse(response);
}

export async function createNotification(payload) {
  const response = await fetch(`${API_BASE_URL}/notifications/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse(response);
}

export async function fetchNotifications(userId) {
  const response = await fetch(`${API_BASE_URL}/notifications/?user_id=${userId}`);
  return parseResponse(response);
}

export async function markNotificationAsRead(notificationId, userId) {
  const response = await fetch(
    `${API_BASE_URL}/notifications/${notificationId}/read?user_id=${userId}`,
    { method: "PATCH" },
  );
  return parseResponse(response);
}
