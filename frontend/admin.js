const loginPanel = document.getElementById("loginPanel");
const dashboardPanel = document.getElementById("dashboardPanel");
const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");
const submissionSearch = document.getElementById("submissionSearch");
const themeToggle = document.getElementById("themeToggle");
const previousPage = document.getElementById("previousPage");
const nextPage = document.getElementById("nextPage");
const pageNumber = document.getElementById("pageNumber");
const paginationSummary = document.getElementById("paginationSummary");
const deleteSubmissionsButton = document.getElementById("deleteSubmissionsButton");
let submissions = [];
let currentPage = 1;
const pageSize = 10;

const savedTheme = localStorage.getItem("veda_admin_theme") || "dark";
document.documentElement.dataset.theme = savedTheme;

function updateThemeButton() {
  const isLight = document.documentElement.dataset.theme === "light";
  themeToggle.textContent = isLight ? "🌙" : "☀️";
  themeToggle.setAttribute("aria-label", isLight ? "Switch to dark mode" : "Switch to light mode");
  themeToggle.setAttribute("title", isLight ? "Switch to dark mode" : "Switch to light mode");
}

themeToggle.addEventListener("click", () => {
  const nextTheme = document.documentElement.dataset.theme === "light" ? "dark" : "light";
  document.documentElement.dataset.theme = nextTheme;
  localStorage.setItem("veda_admin_theme", nextTheme);
  updateThemeButton();
});
updateThemeButton();

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

function renderEmptyRow(message, columns) {
  return `<tr><td colspan="${columns}" class="empty-state">${message}</td></tr>`;
}

function getFilteredSubmissions(searchTerm = "") {
  const normalizedSearch = searchTerm.trim().toLowerCase();
  return submissions.filter(item => {
    if (!normalizedSearch) return true;
    return [item.team_id, item.round, item.repo_url, item.demo_url, item.notes]
      .some(value => String(value ?? "").toLowerCase().includes(normalizedSearch));
  });
}

function renderSubmissions(searchTerm = "") {
  const normalizedSearch = searchTerm.trim().toLowerCase();
  const filteredSubmissions = getFilteredSubmissions(searchTerm);

  const totalPages = Math.max(1, Math.ceil(filteredSubmissions.length / pageSize));
  currentPage = Math.min(currentPage, totalPages);
  const pageStart = (currentPage - 1) * pageSize;
  const pageItems = filteredSubmissions.slice(pageStart, pageStart + pageSize);
  const submissionsTable = document.getElementById("submissionsTable");
  submissionsTable.innerHTML = pageItems.length
    ? pageItems.map(item => `
      <tr>
        <td>${escapeHtml(item.team_id)}</td>
        <td>${escapeHtml(item.round)}</td>
        <td><a href="${escapeHtml(item.repo_url)}" target="_blank" rel="noreferrer">${escapeHtml(item.repo_url)}</a></td>
        <td>${item.demo_url ? escapeHtml(item.demo_url) : "-"}</td>
        <td class="notes-cell">${escapeHtml(item.notes)}</td>
        <td>${formatDate(item.submitted_at)}</td>
        <td><button class="delete-row-button" type="button" data-delete-submission-id="${item.id}">Delete</button></td>
      </tr>`).join("")
    : renderEmptyRow(normalizedSearch ? "No submissions match your search." : "No project submissions yet.", 7);

  const firstResult = filteredSubmissions.length ? pageStart + 1 : 0;
  const lastResult = Math.min(pageStart + pageSize, filteredSubmissions.length);
  paginationSummary.textContent = filteredSubmissions.length
    ? `Showing ${firstResult}-${lastResult} of ${filteredSubmissions.length} submissions`
    : "Showing 0 submissions";
  pageNumber.textContent = `Page ${currentPage} of ${totalPages}`;
  previousPage.disabled = currentPage === 1;
  nextPage.disabled = currentPage === totalPages;
}

async function deleteSubmission(submissionId = null, deleteAll = false) {
  const endpoint = "/api/admin/submissions";
  const requestBody = deleteAll ? { all: true } : { id: submissionId };

  if (deleteAll && !window.confirm("Delete all submissions? This cannot be undone.")) {
    return;
  }

  const response = await fetch(endpoint, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || "Could not delete the submission(s). ");
  }

  document.getElementById("submissionStatus").textContent = data.message;
  await loadDashboard();
}

async function loadDashboard() {
  const response = await fetch("/api/admin/dashboard");
  if (response.status === 401) {
    showLogin();
    return;
  }
  if (!response.ok) throw new Error("Could not load dashboard data");

  const data = await response.json();
  document.getElementById("submissionCount").textContent = data.stats.submissionCount;
  submissions = Array.isArray(data.submissions) ? data.submissions : [];
  renderSubmissions(submissionSearch.value);

  loginPanel.hidden = true;
  dashboardPanel.hidden = false;
}

function showLogin(message = "") {
  dashboardPanel.hidden = true;
  loginPanel.hidden = false;
  loginMessage.textContent = message;
}

loginForm.addEventListener("submit", async event => {
  event.preventDefault();
  loginMessage.textContent = "Signing in...";
  const formData = new FormData(loginForm);

  try {
    const response = await fetch("/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: formData.get("username"),
        password: formData.get("password"),
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Login failed");
    loginForm.reset();
    await loadDashboard();
  } catch (error) {
    loginMessage.textContent = error.message;
  }
});

submissionSearch.addEventListener("input", event => {
  currentPage = 1;
  renderSubmissions(event.target.value);
});

previousPage.addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage -= 1;
    renderSubmissions(submissionSearch.value);
  }
});

nextPage.addEventListener("click", () => {
  const totalPages = Math.max(1, Math.ceil(getFilteredSubmissions(submissionSearch.value).length / pageSize));
  if (currentPage < totalPages) {
    currentPage += 1;
    renderSubmissions(submissionSearch.value);
  }
});

document.getElementById("refreshButton").addEventListener("click", () => {
  loadDashboard().catch(error => {
    document.getElementById("submissionStatus").textContent = error.message;
  });
});

deleteSubmissionsButton.addEventListener("click", () => {
  deleteSubmission(null, true).catch(error => {
    document.getElementById("submissionStatus").textContent = error.message;
  });
});

submissionsTable.addEventListener("click", event => {
  const deleteButton = event.target.closest("[data-delete-submission-id]");
  if (!deleteButton) return;
  const submissionId = Number(deleteButton.dataset.deleteSubmissionId);
  if (!Number.isInteger(submissionId)) return;

  deleteSubmission(submissionId).catch(error => {
    document.getElementById("submissionStatus").textContent = error.message;
  });
});

document.getElementById("logoutButton").addEventListener("click", async () => {
  await fetch("/api/admin/logout", { method: "POST" });
  showLogin("You have been logged out.");
});

loadDashboard().catch(() => showLogin());
