const apiBaseUrl = window.localStorage.getItem("jobrelicApiBase") || "http://127.0.0.1:8000/api";

const demoJobs = [
  {
    id: 1,
    title: "Backend Django Engineer",
    company: "TalentFlow",
    location: "Remote · UK",
    match_score: 91,
    description: "Build matching services, Celery workers, and resilient API integrations.",
    tags: ["Python", "Django", "Celery", "PostgreSQL"],
  },
  {
    id: 2,
    title: "Automation Platform Developer",
    company: "ApplyPilot",
    location: "London",
    match_score: 87,
    description: "Create job ingestion pipelines and intelligent application workflows.",
    tags: ["Python", "Redis", "APIs", "JavaScript"],
  },
  {
    id: 3,
    title: "Product Engineer",
    company: "SwipeHire",
    location: "Hybrid",
    match_score: 82,
    description: "Own frontend interactions, dashboard analytics, and full-stack delivery.",
    tags: ["HTML", "CSS", "JavaScript", "UX"],
  },
];

const state = {
  jobs: [...demoJobs],
  savedJobs: [],
  manualApplications: [],
  autoApplications: [],
};

const elements = {
  swipeCard: document.querySelector("[data-swipe-card]"),
  swipeTitle: document.querySelector("[data-job-title]"),
  swipeMeta: document.querySelector("[data-job-meta]"),
  swipeMatch: document.querySelector("[data-job-match]"),
  swipeDescription: document.querySelector("[data-job-description]"),
  swipeTags: document.querySelector("[data-job-tags]"),
  statsApplied: document.querySelector("[data-stat-applied]"),
  statsAuto: document.querySelector("[data-stat-auto]"),
  statsSaved: document.querySelector("[data-stat-saved]"),
  activityList: document.querySelector("[data-activity-list]"),
  profileForm: document.querySelector("[data-profile-form]"),
  apiInput: document.querySelector("[data-api-base-input]"),
};

function renderSwipeCard() {
  const currentJob = state.jobs[0];

  if (!currentJob) {
    elements.swipeCard.classList.add("is-empty");
    elements.swipeTitle.textContent = "You’re all caught up";
    elements.swipeMeta.textContent = "Fetch more jobs from Adzuna to keep swiping.";
    elements.swipeMatch.textContent = "—";
    elements.swipeDescription.textContent = "No additional opportunities are queued right now.";
    elements.swipeTags.innerHTML = "";
    return;
  }

  elements.swipeCard.classList.remove("is-empty");
  elements.swipeTitle.textContent = currentJob.title;
  elements.swipeMeta.textContent = `${currentJob.company} · ${currentJob.location}`;
  elements.swipeMatch.textContent = `${currentJob.match_score}% match`;
  elements.swipeDescription.textContent = currentJob.description;
  elements.swipeTags.innerHTML = currentJob.tags
    .map((tag) => `<span class="tag">${tag}</span>`)
    .join("");
}

function renderDashboard() {
  elements.statsApplied.textContent = state.manualApplications.length;
  elements.statsAuto.textContent = state.autoApplications.length;
  elements.statsSaved.textContent = state.savedJobs.length;

  const items = [
    ...state.manualApplications.map((job) => `${job.title} · applied manually`),
    ...state.autoApplications.map((job) => `${job.title} · auto-applied`),
    ...state.savedJobs.map((job) => `${job.title} · saved for later`),
  ];

  elements.activityList.innerHTML = items.length
    ? items.map((item) => `<li>${item}</li>`).join("")
    : "<li>No activity yet. Use the swipe controls to start building momentum.</li>";
}

async function postSwipe(action) {
  const currentJob = state.jobs.shift();
  if (!currentJob) {
    return;
  }

  if (action === "apply") {
    state.manualApplications.unshift(currentJob);
  }
  if (action === "save") {
    state.savedJobs.unshift(currentJob);
  }

  renderSwipeCard();
  renderDashboard();

  try {
    await fetch(`${apiBaseUrl}/jobs/${currentJob.id}/swipe/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action }),
    });
  } catch (_error) {
    console.info("Backend not reachable yet; kept the action locally.");
  }
}

async function fetchDashboard() {
  try {
    const response = await fetch(`${apiBaseUrl}/dashboard/`);
    if (!response.ok) {
      throw new Error("Dashboard request failed");
    }
    const payload = await response.json();
    elements.statsApplied.textContent = payload.stats.jobs_applied_for;
    elements.statsAuto.textContent = payload.stats.auto_applied_jobs;
    elements.statsSaved.textContent = payload.stats.saved_jobs;
  } catch (_error) {
    renderDashboard();
  }
}

function handleProfileSave(event) {
  event.preventDefault();
  const formData = new FormData(elements.profileForm);
  const skills = formData.get("skills").split(",").map((value) => value.trim()).filter(Boolean);

  const payload = {
    headline: formData.get("headline"),
    location: formData.get("location"),
    experience_years: Number(formData.get("experience_years") || 0),
    skills,
    auto_apply_threshold: Number(formData.get("auto_apply_threshold") || 85),
    auto_apply_enabled: formData.get("auto_apply_enabled") === "on",
    job_preferences: {
      target_roles: formData.get("target_roles"),
      work_mode: formData.get("work_mode"),
    },
  };

  fetch(`${apiBaseUrl}/profile/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).catch(() => {
    console.info("Profile saved locally only; backend is not running yet.");
  });

  const banner = document.querySelector("[data-profile-banner]");
  banner.textContent = "Profile settings captured. You’re ready to fetch and match jobs.";
}

function init() {
  document.querySelectorAll("[data-swipe-action]").forEach((button) => {
    button.addEventListener("click", () => postSwipe(button.dataset.swipeAction));
  });

  elements.profileForm.addEventListener("submit", handleProfileSave);
  elements.apiInput.value = apiBaseUrl;
  elements.apiInput.addEventListener("change", (event) => {
    window.localStorage.setItem("jobrelicApiBase", event.target.value.trim());
  });

  renderSwipeCard();
  renderDashboard();
  fetchDashboard();
}

init();
