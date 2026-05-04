import { useEffect, useState } from "react";

import {
  createNotification,
  fetchNotifications,
  fetchUsers,
  signin,
  signup,
  markNotificationAsRead,
} from "./api";

const categories = [
  { value: "rent", label: "Rent" },
  { value: "current_bill", label: "Current Bill" },
  { value: "water_bill", label: "Water Bill" },
  { value: "maintenance", label: "Maintenance" },
  { value: "general", label: "General" },
];

const initialAuthForm = {
  username: "",
  password: "",
  role: "user",
};

const initialNotificationForm = {
  title: "",
  message: "",
  category: "rent",
  amount: "",
  due_date: "",
  recipient_ids: [],
};

function App() {
  const [mode, setMode] = useState("signin");
  const [authForm, setAuthForm] = useState(initialAuthForm);
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [notificationForm, setNotificationForm] = useState(initialNotificationForm);
  const [statusMessage, setStatusMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isBusy, setIsBusy] = useState(false);

  useEffect(() => {
    if (!currentUser) {
      return;
    }

    loadUsers();
    loadNotifications(currentUser.id);
  }, [currentUser]);

  async function loadUsers() {
    try {
      const data = await fetchUsers();
      setUsers(data);
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  async function loadNotifications(userId) {
    try {
      const data = await fetchNotifications(userId);
      setNotifications(data);
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  async function handleAuthSubmit(event) {
    event.preventDefault();
    setIsBusy(true);
    setErrorMessage("");
    setStatusMessage("");

    try {
      const action = mode === "signup" ? signup : signin;
      const payload =
        mode === "signup"
          ? authForm
          : { username: authForm.username, password: authForm.password };
      const result = await action(payload);
      setCurrentUser(result.user);
      setStatusMessage(result.message);
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsBusy(false);
    }
  }

  async function handleSendNotification(event) {
    event.preventDefault();
    setIsBusy(true);
    setErrorMessage("");
    setStatusMessage("");

    try {
      await createNotification({
        ...notificationForm,
        amount: notificationForm.amount ? Number(notificationForm.amount) : null,
        due_date: notificationForm.due_date || null,
        sent_by: currentUser.id,
      });
      setNotificationForm(initialNotificationForm);
      setStatusMessage("Notification sent successfully");
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsBusy(false);
    }
  }

  async function handleMarkAsRead(notificationId) {
    setErrorMessage("");
    setStatusMessage("");

    try {
      await markNotificationAsRead(notificationId, currentUser.id);
      setStatusMessage("Notification marked as read");
      await loadNotifications(currentUser.id);
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  function toggleRecipient(userId) {
    setNotificationForm((current) => {
      const exists = current.recipient_ids.includes(userId);
      return {
        ...current,
        recipient_ids: exists
          ? current.recipient_ids.filter((id) => id !== userId)
          : [...current.recipient_ids, userId],
      };
    });
  }

  function logout() {
    setCurrentUser(null);
    setUsers([]);
    setNotifications([]);
    setAuthForm(initialAuthForm);
    setNotificationForm(initialNotificationForm);
    setStatusMessage("");
    setErrorMessage("");
  }

  const userRecipients = users.filter((user) => user.role === "user");

  return (
    <div className="page-shell">
      <div className="background-grid" />
      <main className="app-card">
        <section className="hero">
          <p className="eyebrow">Room Expenses Tracker</p>
          <h1>Admin notices and bill reminders in one place.</h1>
          <p className="hero-copy">
            Send rent, current bill, water bill, and general room updates to the right users,
            then let them track what they have already seen.
          </p>
        </section>

        {!currentUser ? (
          <section className="panel">
            <div className="panel-header">
              <div>
                <h2>{mode === "signup" ? "Create account" : "Sign in"}</h2>
                <p>{mode === "signup" ? "Register as admin or tenant." : "Open your dashboard."}</p>
              </div>
              <button
                type="button"
                className="ghost-button"
                onClick={() => setMode(mode === "signup" ? "signin" : "signup")}
              >
                {mode === "signup" ? "Already have an account?" : "Need an account?"}
              </button>
            </div>

            <form className="form-grid" onSubmit={handleAuthSubmit}>
              <label>
                Username
                <input
                  value={authForm.username}
                  onChange={(event) =>
                    setAuthForm((current) => ({ ...current, username: event.target.value }))
                  }
                  placeholder="bhargav"
                  required
                />
              </label>

              <label>
                Password
                <input
                  type="password"
                  value={authForm.password}
                  onChange={(event) =>
                    setAuthForm((current) => ({ ...current, password: event.target.value }))
                  }
                  placeholder="Enter password"
                  required
                />
              </label>

              {mode === "signup" ? (
                <label>
                  Role
                  <select
                    value={authForm.role}
                    onChange={(event) =>
                      setAuthForm((current) => ({ ...current, role: event.target.value }))
                    }
                  >
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                  </select>
                </label>
              ) : null}

              <button type="submit" className="primary-button" disabled={isBusy}>
                {isBusy ? "Please wait..." : mode === "signup" ? "Create account" : "Sign in"}
              </button>
            </form>
          </section>
        ) : (
          <section className="dashboard">
            <div className="panel">
              <div className="panel-header">
                <div>
                  <h2>
                    Welcome, {currentUser.username} <span className="pill">{currentUser.role}</span>
                  </h2>
                  <p>
                    {currentUser.role === "admin"
                      ? "Send payment reminders and room updates."
                      : "Check the latest notices from your admin."}
                  </p>
                </div>
                <div className="actions">
                  <button
                    type="button"
                    className="ghost-button"
                    onClick={() => loadNotifications(currentUser.id)}
                  >
                    Refresh
                  </button>
                  <button type="button" className="ghost-button" onClick={logout}>
                    Logout
                  </button>
                </div>
              </div>

              {currentUser.role === "admin" ? (
                <form className="form-grid" onSubmit={handleSendNotification}>
                  <label>
                    Title
                    <input
                      value={notificationForm.title}
                      onChange={(event) =>
                        setNotificationForm((current) => ({
                          ...current,
                          title: event.target.value,
                        }))
                      }
                      placeholder="April rent reminder"
                      required
                    />
                  </label>

                  <label>
                    Category
                    <select
                      value={notificationForm.category}
                      onChange={(event) =>
                        setNotificationForm((current) => ({
                          ...current,
                          category: event.target.value,
                        }))
                      }
                    >
                      {categories.map((category) => (
                        <option key={category.value} value={category.value}>
                          {category.label}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className="full-width">
                    Message
                    <textarea
                      value={notificationForm.message}
                      onChange={(event) =>
                        setNotificationForm((current) => ({
                          ...current,
                          message: event.target.value,
                        }))
                      }
                      placeholder="Please pay your room rent before the due date."
                      rows={4}
                      required
                    />
                  </label>

                  <label>
                    Amount
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={notificationForm.amount}
                      onChange={(event) =>
                        setNotificationForm((current) => ({
                          ...current,
                          amount: event.target.value,
                        }))
                      }
                      placeholder="3500"
                    />
                  </label>

                  <label>
                    Due date
                    <input
                      type="date"
                      value={notificationForm.due_date}
                      onChange={(event) =>
                        setNotificationForm((current) => ({
                          ...current,
                          due_date: event.target.value,
                        }))
                      }
                    />
                  </label>

                  <div className="full-width">
                    <span className="field-label">Recipients</span>
                    <div className="recipient-grid">
                      {userRecipients.map((user) => (
                        <label key={user.id} className="checkbox-card">
                          <input
                            type="checkbox"
                            checked={notificationForm.recipient_ids.includes(user.id)}
                            onChange={() => toggleRecipient(user.id)}
                          />
                          <span>{user.username}</span>
                        </label>
                      ))}
                      {!userRecipients.length ? (
                        <p className="hint-text">Create some user accounts first so the admin can target them.</p>
                      ) : null}
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="primary-button"
                    disabled={isBusy || !notificationForm.recipient_ids.length}
                  >
                    {isBusy ? "Sending..." : "Send notification"}
                  </button>
                </form>
              ) : null}
            </div>

            <section className="panel">
              <div className="panel-header">
                <div>
                  <h2>Your notifications</h2>
                  <p>Read the latest payment reminders and room updates.</p>
                </div>
              </div>

              <div className="notification-list">
                {notifications.map((notification) => (
                  <article
                    key={notification.id}
                    className={`notification-card ${notification.is_read ? "read" : "unread"}`}
                  >
                    <div className="notification-topline">
                      <span className="pill accent">{notification.category.replace("_", " ")}</span>
                      <span>{new Date(notification.created_at).toLocaleString()}</span>
                    </div>
                    <h3>{notification.title}</h3>
                    <p>{notification.message}</p>
                    <div className="meta-row">
                      <span>From: {notification.sender_name}</span>
                      {notification.amount ? <span>Amount: Rs. {notification.amount}</span> : null}
                      {notification.due_date ? <span>Due: {notification.due_date}</span> : null}
                    </div>
                    {!notification.is_read ? (
                      <button
                        type="button"
                        className="primary-button"
                        onClick={() => handleMarkAsRead(notification.id)}
                      >
                        Mark as read
                      </button>
                    ) : (
                      <p className="hint-text">
                        Read on {notification.read_at ? new Date(notification.read_at).toLocaleString() : "-"}
                      </p>
                    )}
                  </article>
                ))}

                {!notifications.length ? (
                  <div className="empty-state">
                    <h3>No notifications yet</h3>
                    <p>Admin notices will appear here when they are sent.</p>
                  </div>
                ) : null}
              </div>
            </section>
          </section>
        )}

        {statusMessage ? <p className="feedback success">{statusMessage}</p> : null}
        {errorMessage ? <p className="feedback error">{errorMessage}</p> : null}
      </main>
    </div>
  );
}

export default App;
