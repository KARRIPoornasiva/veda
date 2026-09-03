/**
 * VEDA-2K26: AI AGENT CHALLENGE - CLIENT APPLICATION LOGIC
 * Aditya University • Autonomous AI Agent Hackathon
 */

// ==========================================
// 1. Problem Statements Data (loaded from backend API)
// ==========================================
let problemStatements = [];

async function loadProblemStatements() {
  try {
    const response = await fetch("/api/problems");
    if (!response.ok) throw new Error("Failed to load problem statements");
    const data = await response.json();
    problemStatements = Array.isArray(data) ? data : [];
    renderProblemStatements("all");
  } catch (error) {
    console.error(error);
    problemStatements = [];
    const container = document.getElementById("problemsGridContainer");
    if (container) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted);">
          <p>Unable to load problem statements from the backend API.</p>
        </div>
      `;
    }
  }
}

// ==========================================
// 1.1 Problem Statements Lock State
// ==========================================
let isProblemStatementsLocked = true;

function updateProblemStatementsLockState() {
  const lockedVault = document.getElementById("psLockedVault");
  const unlockedContainer = document.getElementById("psUnlockedContainer");
  const headerBadge = document.getElementById("psHeaderBadge");
  const headerSubtitle = document.getElementById("psHeaderSubtitle");
  const regTrack = document.getElementById("regProblemTrack");

  if (isProblemStatementsLocked) {
    if (lockedVault) lockedVault.style.display = "block";
    if (unlockedContainer) unlockedContainer.style.display = "none";
    if (headerBadge) headerBadge.innerHTML = "🔒 Sealed Confidential";
    if (headerSubtitle) headerSubtitle.innerText = "Official Problem Statements are encrypted and will be revealed simultaneously across all lab workstations at hackathon start time.";
    if (regTrack) {
      regTrack.innerHTML = `
        <option value="GENERAL">General Autonomous AI Agent Track</option>
        <option value="HEALTHCARE">Healthcare & Clinical AI Track (Encrypted)</option>
        <option value="FINTECH">FinTech & Fraud Intelligence Track (Encrypted)</option>
        <option value="DEVTOOLS">DevTools & Code Intelligence Track (Encrypted)</option>
        <option value="EDTECH">Campus & EdTech Assistant Track (Encrypted)</option>
        <option value="RESEARCH">Deep Research & Fact-Checking Track (Encrypted)</option>
      `;
    }
  } else {
    if (lockedVault) lockedVault.style.display = "none";
    if (unlockedContainer) unlockedContainer.style.display = "block";
    if (headerBadge) headerBadge.innerHTML = "⚡ Unlocked & Live";
    if (headerSubtitle) headerSubtitle.innerText = "Official Problem Statements are now live! Teams have 2 hours to build and demonstrate their working AI Agent.";
    if (regTrack) {
      regTrack.innerHTML = `
        <option value="PS-01">PS-01: Healthcare Triaging Agent</option>
        <option value="PS-02">PS-02: FinTech Fraud Forensics Agent</option>
        <option value="PS-03">PS-03: Self-Reflective Code Auditor</option>
        <option value="PS-04">PS-04: Campus Academic Navigator</option>
        <option value="PS-05">PS-05: Fact-Checking Investigative Agent</option>
      `;
    }
  }
}

window.toggleProblemStatementsLock = function() {
  isProblemStatementsLocked = !isProblemStatementsLocked;
  updateProblemStatementsLockState();
  if (isProblemStatementsLocked) {
    showToast("🔒 Problem Statements Locked & Encrypted until Timer Expiry", "warning");
  } else {
    showToast("🔓 Problem Statements Unlocked! Hackathon Sprint is Live!", "success");
  }
};

// ==========================================
// 2. DOM Initialization & Event Listeners
// ==========================================
document.addEventListener("DOMContentLoaded", async () => {
  initNavbarScrollSpy();
  initCountdownTimer();
  updateProblemStatementsLockState();
  await loadProblemStatements();
  initProblemFilters();
  initScoreCalculator();
  initFAQAccordion();
  initModals();
  initParticleCanvas();
  initFormSubmissions();
});

// ==========================================
// 3. Navigation & Scroll Spy
// ==========================================
function initNavbarScrollSpy() {
  const navbar = document.querySelector(".navbar-wrapper");
  const navLinks = document.querySelectorAll(".nav-menu .nav-item a");
  const mobileToggle = document.getElementById("mobileMenuToggle");
  const navMenu = document.getElementById("navMenu");

  // Sticky navbar shadow on scroll
  window.addEventListener("scroll", () => {
    if (window.scrollY > 40) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
    updateActiveNavHighlight();
  });

  // Mobile menu toggle
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener("click", () => {
      navMenu.classList.toggle("mobile-open");
    });
  }

  // Smooth scroll and close mobile menu on click
  navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = link.getAttribute("href");
      const targetSection = document.querySelector(targetId);
      if (targetSection) {
        const navHeight = navbar.offsetHeight;
        const targetPos = targetSection.getBoundingClientRect().top + window.pageYOffset - navHeight + 5;
        window.scrollTo({
          top: targetPos,
          behavior: "smooth"
        });
      }
      if (navMenu.classList.contains("mobile-open")) {
        navMenu.classList.remove("mobile-open");
      }
    });
  });

  function updateActiveNavHighlight() {
    const scrollPos = window.scrollY + 120;
    const sections = document.querySelectorAll("section[id]");

    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      const id = sec.getAttribute("id");

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(link => {
          link.classList.remove("active");
          if (link.getAttribute("href") === `#${id}`) {
            link.classList.add("active");
          }
        });
      }
    });
  }
}

// ==========================================
// 4. Live Hackathon Countdown Timer
// ==========================================
function initCountdownTimer() {
  // Target: September 11, 2026, 09:00:00 IST
  const targetDate = new Date("September 11, 2026 09:00:00").getTime();

  const daysEl = document.getElementById("countdownDays");
  const hoursEl = document.getElementById("countdownHours");
  const minutesEl = document.getElementById("countdownMinutes");
  const secondsEl = document.getElementById("countdownSeconds");

  // Synchronized vault digits
  const vDaysEl = document.getElementById("vaultCountdownDays");
  const vHoursEl = document.getElementById("vaultCountdownHours");
  const vMinutesEl = document.getElementById("vaultCountdownMinutes");
  const vSecondsEl = document.getElementById("vaultCountdownSeconds");

  function updateTimer() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    if (distance < 0) {
      const zeroStr = "00";
      if (daysEl) daysEl.innerText = zeroStr;
      if (hoursEl) hoursEl.innerText = zeroStr;
      if (minutesEl) minutesEl.innerText = zeroStr;
      if (secondsEl) secondsEl.innerText = zeroStr;
      if (vDaysEl) vDaysEl.innerText = zeroStr;
      if (vHoursEl) vHoursEl.innerText = zeroStr;
      if (vMinutesEl) vMinutesEl.innerText = zeroStr;
      if (vSecondsEl) vSecondsEl.innerText = zeroStr;

      if (isProblemStatementsLocked) {
        isProblemStatementsLocked = false;
        updateProblemStatementsLockState();
      }
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    const dStr = days < 10 ? `0${days}` : days;
    const hStr = hours < 10 ? `0${hours}` : hours;
    const mStr = minutes < 10 ? `0${minutes}` : minutes;
    const sStr = seconds < 10 ? `0${seconds}` : seconds;

    if (daysEl) daysEl.innerText = dStr;
    if (hoursEl) hoursEl.innerText = hStr;
    if (minutesEl) minutesEl.innerText = mStr;
    if (secondsEl) secondsEl.innerText = sStr;

    if (vDaysEl) vDaysEl.innerText = dStr;
    if (vHoursEl) vHoursEl.innerText = hStr;
    if (vMinutesEl) vMinutesEl.innerText = mStr;
    if (vSecondsEl) vSecondsEl.innerText = sStr;
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

// ==========================================
// 5. Problem Statements Rendering & Filters
// ==========================================
function renderProblemStatements(filterCategory = "all") {
  const container = document.getElementById("problemsGridContainer");
  if (!container) return;

  const filtered = problemStatements.filter(ps => {
    if (filterCategory === "all") return true;
    if (filterCategory === "round-1") return ps.round === "round-1";
    if (filterCategory === "round-2") return ps.round === "round-2";
    return ps.domain === filterCategory;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted);">
        <p>No problem statements match the selected filter.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(ps => `
    <div class="problem-card ${ps.round === 'round-2' ? 'round-2-card' : ''}" data-ps-id="${ps.id}">
      <div>
        <div class="problem-top-meta">
          <span class="ps-id-badge">${ps.id}</span>
          <span class="ps-round-pill ${ps.round === 'round-1' ? 'round-1-pill' : 'round-2-pill'}">
            ${ps.round === 'round-1' ? 'Round 1 (Core)' : 'Round 2 (Advanced)'}
          </span>
        </div>
        <div class="ps-domain-tag">${ps.domainLabel}</div>
        <h3 class="problem-title">${ps.title}</h3>
        <p class="problem-desc-preview">${ps.summary}</p>
        <div class="problem-tech-tags">
          ${ps.techStack.map(t => `<span class="tech-tag">${t}</span>`).join('')}
        </div>
      </div>
      <div class="problem-card-footer">
        <div class="difficulty-indicator">
          <span class="diff-dot ${ps.diffClass}"></span>
          <span>${ps.difficulty}</span>
        </div>
        <button class="btn-view-ps" onclick="openProblemModal('${ps.id}')">
          <span>View Blueprint</span>
          <span>→</span>
        </button>
      </div>
    </div>
  `).join('');
}

function initProblemFilters() {
  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const category = btn.getAttribute("data-filter");
      renderProblemStatements(category);
    });
  });
}

// Global modal opener for Problem Blueprint
window.openProblemModal = function(psId) {
  if (isProblemStatementsLocked) {
    showToast("🔒 Access Denied: Problem statements are sealed until hackathon start time!", "warning");
    return;
  }

  const ps = problemStatements.find(p => p.id === psId);
  if (!ps) return;

  const modalOverlay = document.getElementById("problemDetailModal");
  const modalContent = document.getElementById("problemModalDynamicContent");

  if (!modalOverlay || !modalContent) return;

  modalContent.innerHTML = `
    <div class="modal-header">
      <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
        <span class="ps-id-badge">${ps.id}</span>
        <span class="ps-round-pill ${ps.round === 'round-1' ? 'round-1-pill' : 'round-2-pill'}">
          ${ps.round === 'round-1' ? 'Round 1 (2-Hour Sprint)' : 'Round 2 (Advanced 2-Hour Sprint)'}
        </span>
      </div>
      <h2 class="modal-title">${ps.title}</h2>
      <p class="modal-subtitle">${ps.domainLabel}</p>
    </div>

    <div class="problem-modal-spec-grid">
      <div class="spec-item">
        <span class="spec-key">Challenge Track</span>
        <span class="spec-val">${ps.round === 'round-1' ? 'AI Agent Development' : 'Advanced Multi-Agent Challenge'}</span>
      </div>
      <div class="spec-item">
        <span class="spec-key">Complexity Level</span>
        <span class="spec-val">${ps.difficulty}</span>
      </div>
      <div class="spec-item">
        <span class="spec-key">Permitted Tools</span>
        <span class="spec-val">${ps.techStack.join(', ')}</span>
      </div>
      <div class="spec-item">
        <span class="spec-key">Sprint Duration</span>
        <span class="spec-val">2 Hours (Strict)</span>
      </div>
    </div>

    <h4 class="problem-modal-section-title">Problem Statement Blueprint</h4>
    <p class="problem-modal-text">${ps.fullDescription}</p>

    <h4 class="problem-modal-section-title">Mandatory Agent Capabilities</h4>
    <ul class="rules-list" style="margin-top: 10px;">
      ${ps.capabilities.map(c => `
        <li>
          <span class="rules-bullet-icon bullet-allowed">✓</span>
          <span>${c}</span>
        </li>
      `).join('')}
    </ul>

    <h4 class="problem-modal-section-title">Sample Execution Trace / Input-Output</h4>
    <div style="background: var(--bg-primary); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px; font-family: var(--font-mono); font-size: 0.84rem; color: #38bdf8; margin-top: 8px; line-height: 1.5;">
      ${ps.sampleFlow}
    </div>

    <h4 class="problem-modal-section-title">Evaluation Focus & Benchmarks</h4>
    <p class="problem-modal-text" style="color: var(--text-muted);">${ps.rubricFocus}</p>

    <div class="modal-form-actions">
      <button class="nav-btn-secondary" onclick="closeAllModals()">Close</button>
      <button class="btn-glow-primary" onclick="selectProblemForRegistration('${ps.id}')">Select this Problem</button>
    </div>
  `;

  modalOverlay.classList.add("active");
  document.body.style.overflow = "hidden";
};

window.selectProblemForRegistration = function(psId) {
  closeAllModals();
  openRegisterModal(psId);
};

// ==========================================
// 6. Interactive Evaluation Score Estimator
// ==========================================
function initScoreCalculator() {
  const sAutonomy = document.getElementById("sliderAutonomy");
  const sInnovation = document.getElementById("sliderInnovation");
  const sRobustness = document.getElementById("sliderRobustness");
  const sDemo = document.getElementById("sliderDemo");
  const sCode = document.getElementById("sliderCode");

  const vAutonomy = document.getElementById("valAutonomy");
  const vInnovation = document.getElementById("valInnovation");
  const vRobustness = document.getElementById("valRobustness");
  const vDemo = document.getElementById("valDemo");
  const vCode = document.getElementById("valCode");

  const totalScoreEl = document.getElementById("calcTotalScore");
  const verdictEl = document.getElementById("calcVerdict");

  function calculateTotal() {
    if (!sAutonomy) return;

    const autonomy = parseFloat(sAutonomy.value);
    const innovation = parseFloat(sInnovation.value);
    const robustness = parseFloat(sRobustness.value);
    const demo = parseFloat(sDemo.value);
    const code = parseFloat(sCode.value);

    if (vAutonomy) vAutonomy.innerText = `${autonomy} / 25`;
    if (vInnovation) vInnovation.innerText = `${innovation} / 25`;
    if (vRobustness) vRobustness.innerText = `${robustness} / 20`;
    if (vDemo) vDemo.innerText = `${demo} / 20`;
    if (vCode) vCode.innerText = `${code} / 10`;

    const total = autonomy + innovation + robustness + demo + code;
    if (totalScoreEl) totalScoreEl.innerText = `${total.toFixed(0)} / 100`;

    if (verdictEl) {
      if (total >= 90) {
        verdictEl.innerText = "🏆 Top Contender for 1st Prize (₹6,000)";
        verdictEl.style.color = "var(--amber-gold)";
      } else if (total >= 75) {
        verdictEl.innerText = "🥈 Strong Finalist Track for 2nd/3rd Prize";
        verdictEl.style.color = "var(--cyan-primary)";
      } else if (total >= 60) {
        verdictEl.innerText = "✅ Qualified for Round 2 Shortlisting";
        verdictEl.style.color = "var(--emerald-primary)";
      } else {
        verdictEl.innerText = "⚠️ Needs stronger tool autonomy & live demo";
        verdictEl.style.color = "#fb7185";
      }
    }
  }

  [sAutonomy, sInnovation, sRobustness, sDemo, sCode].forEach(s => {
    if (s) s.addEventListener("input", calculateTotal);
  });

  calculateTotal();
}

// ==========================================
// 7. FAQ Accordions
// ==========================================
function initFAQAccordion() {
  const faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(item => {
    const btn = item.querySelector(".faq-question-btn");
    if (btn) {
      btn.addEventListener("click", () => {
        const isOpen = item.classList.contains("open");
        faqItems.forEach(i => i.classList.remove("open"));
        if (!isOpen) {
          item.classList.add("open");
        }
      });
    }
  });
}

// ==========================================
// 8. In-Page Modals (Registration & Submit)
// ==========================================
function initModals() {
  const modalOverlays = document.querySelectorAll(".modal-overlay");
  const closeBtns = document.querySelectorAll(".modal-close-btn");

  closeBtns.forEach(btn => {
    btn.addEventListener("click", closeAllModals);
  });

  modalOverlays.forEach(overlay => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        closeAllModals();
      }
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeAllModals();
    }
  });
}

window.closeAllModals = function() {
  const modalOverlays = document.querySelectorAll(".modal-overlay");
  modalOverlays.forEach(m => m.classList.remove("active"));
  document.body.style.overflow = "auto";
};

window.openRegisterModal = function(preselectedPs = "") {
  const modal = document.getElementById("registerModal");
  if (!modal) return;

  const trackSelect = document.getElementById("regProblemTrack");
  if (trackSelect && preselectedPs) {
    trackSelect.value = preselectedPs;
  }

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
};

window.openSubmitModal = function() {
  const modal = document.getElementById("submitModal");
  if (!modal) return;
  modal.classList.add("active");
  document.body.style.overflow = "hidden";
};

// ==========================================
// 9. Forms & Local Persistence
// ==========================================
function initFormSubmissions() {
  const regForm = document.getElementById("teamRegistrationForm");
  const subForm = document.getElementById("projectSubmissionForm");
  const memberCountSelect = document.getElementById("regTeamSize");
  const member2Group = document.getElementById("member2FieldsGroup");

  if (memberCountSelect && member2Group) {
    memberCountSelect.addEventListener("change", () => {
      if (memberCountSelect.value === "2") {
        member2Group.style.display = "block";
      } else {
        member2Group.style.display = "none";
      }
    });
  }

  if (regForm) {
    regForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const teamName = document.getElementById("regTeamName").value.trim();
      const leadName = document.getElementById("regLeadName").value.trim();
      const leadRoll = document.getElementById("regLeadRoll").value.trim();
      const leadEmail = document.getElementById("regLeadEmail").value.trim();
      const track = document.getElementById("regProblemTrack").value;

      if (!teamName || !leadName || !leadRoll || !leadEmail) {
        showToast("Please fill all required fields", "warning");
        return;
      }

      const payload = {
        teamName,
        leadName,
        leadRoll,
        leadEmail,
        track,
      };

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Registration failed");
        }

        const teamId = data.team.teamId;
        localStorage.setItem("veda_registered_team", JSON.stringify(data.team));
        closeAllModals();
        showToast(`🎉 Registration Confirmed! Team ID: ${teamId}`, "success");
        regForm.reset();
      } catch (error) {
        showToast(error.message || "Registration failed", "warning");
      }
    });
  }

  if (subForm) {
    subForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const teamId = document.getElementById("subTeamId").value.trim();
      const repoUrl = document.getElementById("subRepoUrl").value.trim();
      const notes = document.getElementById("subAgentNotes").value.trim();

      if (!teamId || !repoUrl) {
        showToast("Please provide Team ID and Repository URL", "warning");
        return;
      }

      try {
        const response = await fetch("/api/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ teamId, repoUrl, notes }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Submission failed");
        }

        closeAllModals();
        showToast("🚀 Solution Submitted Successfully for Evaluation!", "success");
        subForm.reset();
      } catch (error) {
        showToast(error.message || "Submission failed", "warning");
      }
    });
  }
}

// Toast notification helper
function showToast(message, type = "success") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '⚡' : '⚠️'}</span>
    <span class="toast-msg">${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

// ==========================================
// 10. Neural Particle Canvas Animation
// ==========================================
function initParticleCanvas() {
  const canvas = document.getElementById("particles-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  const particleCount = Math.min(Math.floor(window.innerWidth / 20), 65);

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      radius: Math.random() * 1.8 + 1,
      color: Math.random() > 0.5 ? "rgba(0, 242, 254, " : "rgba(168, 85, 247, "
    });
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color + "0.7)";
      ctx.fill();

      // Connect near particles
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          const alpha = (1 - dist / 130) * 0.22;
          ctx.strokeStyle = `rgba(0, 242, 254, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(animate);
  }

  animate();
}
