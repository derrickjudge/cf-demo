"""Static HTML/CSS/SVG branding assets for the Value Corp demo UI.

Decorative marketing/login/dashboard markup only; no security-relevant
logic lives here. Kept separate from entry.py so routing/vulnerability
logic and presentation don't intermix.
"""

from urllib.parse import quote

SVG_LOGO_MARK = """<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Value Corp">
  <rect width="40" height="40" rx="9" fill="url(#vc-grad)"/>
  <path d="M11 11 L20 26 L29 11" fill="none" stroke="#ffffff"
        stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
  <defs>
    <linearGradient id="vc-grad" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2563eb"/>
      <stop offset="1" stop-color="#0891b2"/>
    </linearGradient>
  </defs>
</svg>"""

FAVICON_HREF = "data:image/svg+xml," + quote(SVG_LOGO_MARK)

BASE_CSS = """
:root {
  --vc-primary: #2563eb;
  --vc-primary-dark: #1d4ed8;
  --vc-accent: #0891b2;
  --vc-ink: #0f172a;
  --vc-body: #334155;
  --vc-muted: #64748b;
  --vc-border: #e2e8f0;
  --vc-surface: #ffffff;
  --vc-bg: #f1f5f9;
  --vc-danger: #dc2626;
  --vc-danger-bg: #fef2f2;
  --vc-success: #16a34a;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Helvetica, Arial, sans-serif;
  color: var(--vc-body);
  background: var(--vc-bg);
}

a { color: var(--vc-primary); text-decoration: none; }
a:hover { text-decoration: underline; }

.logo-mark svg { width: 28px; height: 28px; display: block; }
.logo-mark--lg svg { width: 56px; height: 56px; }

.brand { display: inline-flex; align-items: center; }

.wordmark {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--vc-ink);
  margin-left: 0.5rem;
}
.wordmark strong { color: var(--vc-primary); font-weight: 700; }

.topbar {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  background: var(--vc-surface);
  border-bottom: 1px solid var(--vc-border);
}

.topnav {
  margin-left: auto;
  display: flex;
  gap: 1.75rem;
}
.topnav a { color: var(--vc-body); font-weight: 500; font-size: 0.95rem; }
.topnav a:hover { color: var(--vc-primary); text-decoration: none; }

.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.auth-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background:
    radial-gradient(circle at 15% 20%, rgba(37, 99, 235, 0.08), transparent 45%),
    radial-gradient(circle at 85% 80%, rgba(8, 145, 178, 0.08), transparent 45%);
}

.auth-card {
  width: 100%;
  max-width: 380px;
  background: var(--vc-surface);
  border: 1px solid var(--vc-border);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.06);
  padding: 2.25rem 2rem;
  text-align: center;
}

.auth-card h1 {
  font-size: 1.4rem;
  color: var(--vc-ink);
  margin: 1rem 0 0.35rem;
}

.auth-sub {
  color: var(--vc-muted);
  font-size: 0.9rem;
  margin: 0 0 1.5rem;
}

.auth-card form {
  text-align: left;
}

.auth-card label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--vc-ink);
  margin-bottom: 0.3rem;
}

.auth-card input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid var(--vc-border);
  border-radius: 8px;
  font-size: 0.95rem;
  color: var(--vc-ink);
}
.auth-card input:focus {
  outline: none;
  border-color: var(--vc-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.auth-card button {
  width: 100%;
  padding: 0.7rem;
  border: none;
  border-radius: 8px;
  background: var(--vc-primary);
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
}
.auth-card button:hover { background: var(--vc-primary-dark); }
.auth-card button:disabled { opacity: 0.7; cursor: default; }

.alert {
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  text-align: left;
}
.alert-error {
  background: var(--vc-danger-bg);
  color: var(--vc-danger);
  border: 1px solid rgba(220, 38, 38, 0.2);
}
.alert-info {
  background: var(--vc-bg);
  color: var(--vc-muted);
  border: 1px solid var(--vc-border);
}

.page-footer {
  text-align: center;
  font-size: 0.8rem;
  color: var(--vc-muted);
  padding: 1.25rem;
}

.app-page { min-height: 100vh; }

.app-shell {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: var(--vc-surface);
  border-right: 1px solid var(--vc-border);
  padding: 1.25rem 1rem;
  flex-shrink: 0;
}

.sidebar .wordmark { display: block; margin: 0.5rem 0 1.75rem 0.35rem; }

.sidenav { display: flex; flex-direction: column; gap: 0.25rem; }
.sidenav a {
  color: var(--vc-body);
  font-weight: 500;
  font-size: 0.9rem;
  padding: 0.55rem 0.75rem;
  border-radius: 8px;
}
.sidenav a:hover { background: var(--vc-bg); text-decoration: none; }
.sidenav a.active {
  background: rgba(37, 99, 235, 0.1);
  color: var(--vc-primary);
}

.app-main { flex: 1; padding: 2rem; }

.app-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
.app-topbar h1 { font-size: 1.4rem; color: var(--vc-ink); margin: 0; }
.signout { font-size: 0.9rem; font-weight: 500; }

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: var(--vc-surface);
  border: 1px solid var(--vc-border);
  border-radius: 10px;
  padding: 1.1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.stat-label { font-size: 0.8rem; color: var(--vc-muted); }
.stat-value { font-size: 1.5rem; font-weight: 700; color: var(--vc-ink); }
.stat-delta { font-size: 0.8rem; font-weight: 600; }
.stat-delta--up { color: var(--vc-success); }
.stat-delta--down { color: var(--vc-danger); }

.panel {
  background: var(--vc-surface);
  border: 1px solid var(--vc-border);
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
}
.panel h2 { font-size: 1.05rem; color: var(--vc-ink); margin: 0 0 0.75rem; }

.activity-list { list-style: none; margin: 0; padding: 0; }
.activity-list li {
  display: flex;
  justify-content: space-between;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--vc-border);
  font-size: 0.9rem;
}
.activity-list li:last-child { border-bottom: none; }
.activity-list span { font-weight: 600; color: var(--vc-ink); }
.activity-list time { color: var(--vc-muted); }

.search-form { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.search-form input {
  flex: 1;
  padding: 0.55rem 0.75rem;
  border: 1px solid var(--vc-border);
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--vc-ink);
}
.search-form input:focus {
  outline: none;
  border-color: var(--vc-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}
.search-form button {
  padding: 0.55rem 1.25rem;
  border: none;
  border-radius: 8px;
  background: var(--vc-primary);
  color: #ffffff;
  font-weight: 600;
  cursor: pointer;
}
.search-form button:hover { background: var(--vc-primary-dark); }

.results-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.results-table th, .results-table td {
  text-align: left;
  padding: 0.55rem 0.75rem;
  border-bottom: 1px solid var(--vc-border);
}
.results-table th {
  color: var(--vc-muted);
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
"""

LOGIN_SCRIPT = """
const form = document.getElementById("login-form");
const errorBox = document.getElementById("login-error");
const submitBtn = document.getElementById("login-submit");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  submitBtn.disabled = true;
  submitBtn.textContent = "Signing in...";

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      window.location.href = "/dashboard";
      return;
    }

    errorBox.textContent = response.status === 429
      ? "Too many attempts. Please wait and try again."
      : "Invalid username or password. Please try again.";
    errorBox.hidden = false;
  } catch (err) {
    errorBox.textContent = "Something went wrong. Please try again.";
    errorBox.hidden = false;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Sign in";
  }
});
"""


SEARCH_SCRIPT = """
const searchForm = document.getElementById("search-form");
const searchStatus = document.getElementById("search-status");
const resultsTable = document.getElementById("search-results");
const resultsBody = resultsTable.querySelector("tbody");

function showStatus(message, kind) {
  searchStatus.textContent = message;
  searchStatus.className = "alert alert-" + kind;
  searchStatus.hidden = false;
}

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  searchStatus.hidden = true;
  resultsTable.hidden = true;
  resultsBody.innerHTML = "";

  const q = document.getElementById("search-q").value;
  let response;
  try {
    response = await fetch("/search?q=" + encodeURIComponent(q));
  } catch (err) {
    showStatus("Search request failed.", "error");
    return;
  }

  if (response.status === 403) {
    showStatus("Blocked by Cloudflare WAF (403).", "error");
    return;
  }
  if (!response.ok) {
    showStatus("Search failed (HTTP " + response.status + ").", "error");
    return;
  }

  let rows;
  try {
    rows = await response.json();
  } catch (err) {
    showStatus("Search returned an unexpected response.", "error");
    return;
  }

  if (!Array.isArray(rows) || rows.length === 0) {
    showStatus("No results.", "info");
    return;
  }

  for (const row of rows) {
    const tr = document.createElement("tr");
    for (const key of ["id", "username", "email", "password_hash"]) {
      const td = document.createElement("td");
      td.textContent = row[key];
      tr.appendChild(td);
    }
    resultsBody.appendChild(tr);
  }
  resultsTable.hidden = false;
});
"""

NAV_ITEMS = [
    ("Overview", "/dashboard"),
    ("Analytics", "#"),
    ("Customers", "/customers"),
    ("Billing", "#"),
    ("Settings", "#"),
]


def _render_sidenav(active_label: str) -> str:
    """Render the sidebar nav links, marking the active page."""
    links = []
    for label, href in NAV_ITEMS:
        classes = "active" if label == active_label else ""
        class_attr = f' class="{classes}"' if classes else ""
        links.append(f'<a{class_attr} href="{href}">{label}</a>')
    return "\n        ".join(links)


def _render_app_shell(title: str, active_label: str, page_content: str) -> str:
    """Wrap page_content in the shared Value Corp topbar/sidebar app shell."""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Value Corp</title>
<link rel="icon" type="image/svg+xml" href="{FAVICON_HREF}">
<style>{BASE_CSS}</style>
</head>
<body class="app-page">
  <div class="app-shell">
    <aside class="sidebar">
      <span class="brand logo-mark">{SVG_LOGO_MARK}</span>
      <span class="wordmark">Value<strong>Corp</strong></span>
      <nav class="sidenav">
        {_render_sidenav(active_label)}
      </nav>
    </aside>
    <div class="app-main">
      {page_content}
    </div>
  </div>
</body>
</html>"""


def render_login_page() -> str:
    """Render the Value Corp login page as a full HTML document string."""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sign in - Value Corp</title>
<link rel="icon" type="image/svg+xml" href="{FAVICON_HREF}">
<style>{BASE_CSS}</style>
</head>
<body class="auth-page">
  <header class="topbar">
    <span class="brand logo-mark">{SVG_LOGO_MARK}</span>
    <span class="wordmark">Value<strong>Corp</strong></span>
    <nav class="topnav">
      <a href="#">Product</a><a href="#">Solutions</a>
      <a href="#">Pricing</a><a href="#">Contact</a>
    </nav>
  </header>

  <main class="auth-main">
    <section class="auth-card">
      <div class="logo-mark logo-mark--lg">{SVG_LOGO_MARK}</div>
      <h1>Sign in to Value Corp</h1>
      <p class="auth-sub">Welcome back. Enter your credentials to continue.</p>

      <div id="login-error" class="alert alert-error" hidden></div>

      <form id="login-form" novalidate>
        <label for="username">Username</label>
        <input id="username" name="username" type="text" autocomplete="username" required>
        <label for="password">Password</label>
        <input id="password" name="password" type="password" autocomplete="current-password" required>
        <button type="submit" id="login-submit">Sign in</button>
      </form>
    </section>
  </main>

  <footer class="page-footer">&copy; 2026 Value Corp. All rights reserved.</footer>
  <script>{LOGIN_SCRIPT}</script>
</body>
</html>"""


def render_dashboard_page() -> str:
    """Render the Value Corp post-login dashboard as a full HTML document string."""
    content = """
      <header class="app-topbar">
        <h1>Dashboard</h1>
        <a class="signout" href="/login">Sign out</a>
      </header>
      <section class="stat-grid">
        <div class="stat-card"><span class="stat-label">Active Users</span><span class="stat-value">2,481</span><span class="stat-delta stat-delta--up">+4.2%</span></div>
        <div class="stat-card"><span class="stat-label">Monthly Revenue</span><span class="stat-value">$48,203</span><span class="stat-delta stat-delta--up">+2.1%</span></div>
        <div class="stat-card"><span class="stat-label">Uptime</span><span class="stat-value">99.98%</span><span class="stat-delta stat-delta--up">stable</span></div>
        <div class="stat-card"><span class="stat-label">Open Tickets</span><span class="stat-value">12</span><span class="stat-delta stat-delta--down">-3</span></div>
      </section>
      <section class="panel">
        <h2>Recent Activity</h2>
        <ul class="activity-list">
          <li><span>alice</span> updated billing details <time>2h ago</time></li>
          <li><span>bob</span> invited a teammate <time>5h ago</time></li>
          <li><span>admin</span> rotated API key <time>1d ago</time></li>
        </ul>
      </section>
    """
    return _render_app_shell("Dashboard", "Overview", content)


def render_customers_page() -> str:
    """Render the Value Corp customer search page as a full HTML document string.

    The search box calls the existing GET /search endpoint -- the SQLi bait
    -- so the injection demo can be triggered by typing into the page
    instead of only via curl. No new vulnerability is introduced here: this
    is presentation only, /search's behavior is unchanged.
    """
    content = f"""
      <header class="app-topbar">
        <h1>Customers</h1>
        <a class="signout" href="/login">Sign out</a>
      </header>
      <section class="panel">
        <h2>Customer Search</h2>
        <form id="search-form" class="search-form" novalidate>
          <input id="search-q" name="q" type="text" placeholder="Search by username...">
          <button type="submit">Search</button>
        </form>
        <div id="search-status" class="alert" hidden></div>
        <table id="search-results" class="results-table" hidden>
          <thead>
            <tr><th>ID</th><th>Username</th><th>Email</th><th>Password Hash</th></tr>
          </thead>
          <tbody></tbody>
        </table>
      </section>
      <script>{SEARCH_SCRIPT}</script>
    """
    return _render_app_shell("Customers", "Customers", content)
