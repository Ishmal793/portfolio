/**
 * Ishmal Shahid — Portfolio Interaction Scripts
 * Unified Architecture: Category Filtering, Modals, Theme Sync, Clipboard, Scroll
 */

(function () {
  "use strict";

  /* ----------------------------------------------------
     1. AOS Animations
     ---------------------------------------------------- */
  if (typeof AOS !== "undefined") {
    AOS.init({
      duration: 700,
      easing: "ease-out-cubic",
      once: true,
      offset: 50,
    });
  }

  /* ----------------------------------------------------
     2. Theme Management (Light / Dark)
     ---------------------------------------------------- */
  const html = document.documentElement;
  const themeToggle = document.getElementById("themeToggle");
  const themeToggleMobile = document.getElementById("themeToggleMobile");
  const themeIcons = document.querySelectorAll(".theme-icon");
  const savedTheme = localStorage.getItem("portfolio-theme") || "light";

  function applyTheme(theme) {
    html.setAttribute("data-theme", theme);
    themeIcons.forEach((icon) => {
      icon.className = theme === "dark" ? "fas fa-sun theme-icon" : "fas fa-moon theme-icon";
    });
    localStorage.setItem("portfolio-theme", theme);
  }

  applyTheme(savedTheme);

  function toggleThemeAction() {
    const current = html.getAttribute("data-theme") || "light";
    const next = current === "dark" ? "light" : "dark";
    applyTheme(next);
  }

  if (themeToggle) themeToggle.addEventListener("click", toggleThemeAction);
  if (themeToggleMobile) themeToggleMobile.addEventListener("click", toggleThemeAction);

  /* ----------------------------------------------------
     3. Sticky Navigation & Active Scrollspy
     ---------------------------------------------------- */
  const nav = document.getElementById("mainNav");
  const navLinks = document.querySelectorAll(".navbar-nav .nav-link[href^='#']");
  const sections = document.querySelectorAll("section[id]");
  const scrollTopBtn = document.getElementById("scrollTopBtn");

  function onScroll() {
    const scrollY = window.scrollY;

    if (nav) {
      nav.classList.toggle("scrolled", scrollY > 30);
    }

    if (scrollTopBtn) {
      scrollTopBtn.classList.toggle("visible", scrollY > 350);
    }

    const scrollPos = scrollY + 120;
    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute("id");
      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach((link) => {
          link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
        });
      }
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Close mobile navbar on link click
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      const collapse = document.getElementById("navMenu");
      if (collapse && collapse.classList.contains("show")) {
        const toggler = document.querySelector(".navbar-toggler");
        if (toggler) toggler.click();
      }
    });
  });

  /* ----------------------------------------------------
     4. Project Category Filtering
     ---------------------------------------------------- */
  const filterBtns = document.querySelectorAll(".filter-btn");
  const projectItems = document.querySelectorAll(".project-item");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter");
      projectItems.forEach((item) => {
        const itemCat = item.getAttribute("data-category");
        if (filter === "all" || itemCat === filter) {
          item.style.display = "";
          item.style.opacity = "0";
          setTimeout(() => {
            item.style.transition = "opacity 0.3s ease";
            item.style.opacity = "1";
          }, 20);
        } else {
          item.style.display = "none";
        }
      });
    });
  });

  /* ----------------------------------------------------
     5. Certificate Category Filtering
     ---------------------------------------------------- */
  const certFilterBtns = document.querySelectorAll(".cert-filter-btn");
  const certItems = document.querySelectorAll(".cert-gallery-item");

  certFilterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      certFilterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter");
      certItems.forEach((item) => {
        const itemCat = item.getAttribute("data-category");
        if (filter === "all" || itemCat === filter) {
          item.style.display = "";
          item.style.opacity = "0";
          setTimeout(() => {
            item.style.transition = "opacity 0.3s ease";
            item.style.opacity = "1";
          }, 20);
        } else {
          item.style.display = "none";
        }
      });
    });
  });

  /* ----------------------------------------------------
     6. Project Detail Modal Data Binding
     ---------------------------------------------------- */
  const projectModal = document.getElementById("projectDetailModal");
  if (projectModal) {
    projectModal.addEventListener("show.bs.modal", (event) => {
      const trigger = event.relatedTarget;
      if (!trigger) return;

      const title = trigger.getAttribute("data-proj-title") || "Project Details";
      const desc = trigger.getAttribute("data-proj-desc") || "";
      const img = trigger.getAttribute("data-proj-img") || "";
      const tech = trigger.getAttribute("data-proj-tech") || "";
      const github = trigger.getAttribute("data-proj-github") || "";
      const hf = trigger.getAttribute("data-proj-hf") || "";
      const badge = trigger.getAttribute("data-proj-badge") || "Project";

      document.getElementById("projectDetailModalLabel").textContent = title;
      document.getElementById("modalProjDesc").textContent = desc;
      document.getElementById("modalProjBadge").textContent = badge;

      const imgEl = document.getElementById("modalProjImg");
      imgEl.src = img;
      imgEl.alt = title;

      // Highlights list
      const rawHighlights = trigger.getAttribute("data-proj-highlights") || "";
      const highlightsContainer = document.getElementById("modalProjHighlightsContainer");
      const highlightsList = document.getElementById("modalProjHighlights");
      if (highlightsContainer && highlightsList) {
        highlightsList.innerHTML = "";
        const items = rawHighlights.split("__SEP__").map((h) => h.trim()).filter((h) => h.length > 0);
        if (items.length > 0) {
          highlightsContainer.style.display = "";
          items.forEach((item) => {
            const li = document.createElement("li");
            li.textContent = item;
            highlightsList.appendChild(li);
          });
        } else {
          highlightsContainer.style.display = "none";
        }
      }

      // Tech badges
      const techContainer = document.getElementById("modalProjTech");
      techContainer.innerHTML = "";
      if (tech) {
        tech.split(",").forEach((t) => {
          const item = t.trim();
          if (item) {
            const span = document.createElement("span");
            span.className = "tech-badge font-mono";
            span.textContent = item;
            techContainer.appendChild(span);
          }
        });
      }

      // Action links
      const linksContainer = document.getElementById("modalProjLinks");
      linksContainer.innerHTML = "";
      if (hf) {
        const hfLink = document.createElement("a");
        hfLink.href = hf;
        hfLink.target = "_blank";
        hfLink.rel = "noopener noreferrer";
        hfLink.className = "btn btn-primary btn-sm";
        hfLink.innerHTML = "<span>🤗 Launch Demo</span>";
        linksContainer.appendChild(hfLink);
      }
      if (github) {
        const ghLink = document.createElement("a");
        ghLink.href = github;
        ghLink.target = "_blank";
        ghLink.rel = "noopener noreferrer";
        ghLink.className = "btn btn-secondary btn-sm";
        ghLink.innerHTML = '<i class="fab fa-github me-1"></i> Repository';
        linksContainer.appendChild(ghLink);
      }
    });
  }

  /* ----------------------------------------------------
     7. Certificate Lightbox Modal Data Binding
     ---------------------------------------------------- */
  const certModal = document.getElementById("certModal");
  if (certModal) {
    certModal.addEventListener("show.bs.modal", (event) => {
      const trigger = event.relatedTarget;
      if (!trigger) return;

      const title = trigger.getAttribute("data-cert-title") || "Certificate";
      const img = trigger.getAttribute("data-cert-img") || "";
      const issuer = trigger.getAttribute("data-cert-issuer") || "";
      const date = trigger.getAttribute("data-cert-date") || "";
      const badge = trigger.getAttribute("data-cert-badge") || "Verified";
      const note = trigger.getAttribute("data-cert-note") || "";

      document.getElementById("certModalLabel").textContent = title;
      document.getElementById("certModalBadge").textContent = badge;
      document.getElementById("certModalIssuer").textContent = issuer;
      document.getElementById("certModalDate").textContent = date;
      document.getElementById("certModalNote").textContent = note || "Verified credential issued upon technical assessment.";

      const imgEl = document.getElementById("certModalImg");
      imgEl.src = img;
      imgEl.alt = title;

      const directLink = document.getElementById("certModalDirectLink");
      if (directLink) directLink.href = img;
    });
  }

  /* ----------------------------------------------------
     8. Copy Email to Clipboard
     ---------------------------------------------------- */
  const copyEmailBtn = document.getElementById("copyEmailBtn");
  if (copyEmailBtn) {
    copyEmailBtn.addEventListener("click", () => {
      const email = "ishishahid4@gmail.com";
      navigator.clipboard.writeText(email).then(() => {
        const originalHtml = copyEmailBtn.innerHTML;
        copyEmailBtn.innerHTML = '<i class="fas fa-check text-success"></i>';
        setTimeout(() => {
          copyEmailBtn.innerHTML = originalHtml;
        }, 2000);
      }).catch(() => {
        prompt("Copy email address:", email);
      });
    });
  }

  /* ----------------------------------------------------
     9. Auto-Dismiss Messages
     ---------------------------------------------------- */
  document.querySelectorAll(".toast").forEach((toast) => {
    setTimeout(() => {
      if (typeof bootstrap !== "undefined" && bootstrap.Toast) {
        const bsToast = bootstrap.Toast.getOrCreateInstance(toast);
        bsToast.hide();
      }
    }, 6000);
  });

  /* ----------------------------------------------------
     10. "View All Projects" Toggle Handler
     ---------------------------------------------------- */
  const toggleProjectsBtn = document.getElementById("toggleAllProjectsBtn");
  const extraProjects = document.querySelectorAll(".extra-project-item");

  if (toggleProjectsBtn && extraProjects.length > 0) {
    let isExpanded = false;
    toggleProjectsBtn.addEventListener("click", () => {
      isExpanded = !isExpanded;
      extraProjects.forEach((item) => {
        if (isExpanded) {
          item.classList.remove("d-none");
          item.style.opacity = "0";
          setTimeout(() => {
            item.style.transition = "opacity 0.35s ease";
            item.style.opacity = "1";
          }, 30);
        } else {
          item.classList.add("d-none");
        }
      });

      if (isExpanded) {
        toggleProjectsBtn.innerHTML = '<i class="fas fa-chevron-up me-2"></i> Show Less';
        toggleProjectsBtn.setAttribute("aria-expanded", "true");
      } else {
        toggleProjectsBtn.innerHTML = '<i class="fas fa-layer-group me-2"></i> View All Projects (' + (3 + extraProjects.length) + ')';
        toggleProjectsBtn.setAttribute("aria-expanded", "false");
        const projSection = document.getElementById("projects");
        if (projSection) {
          projSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    });
  }

  /* ----------------------------------------------------
     11. Certificate Lightbox Keyboard Navigation
     ---------------------------------------------------- */
  if (certModal) {
    const certTriggers = Array.from(document.querySelectorAll('[data-bs-target="#certModal"]'));
    let currentCertIndex = -1;

    certModal.addEventListener("show.bs.modal", (event) => {
      const trigger = event.relatedTarget;
      if (trigger) {
        currentCertIndex = certTriggers.indexOf(trigger);
      }
    });

    document.addEventListener("keydown", (e) => {
      if (!certModal.classList.contains("show") || certTriggers.length === 0) return;

      if (e.key === "ArrowRight") {
        if (currentCertIndex >= 0 && currentCertIndex < certTriggers.length - 1) {
          currentCertIndex++;
          certTriggers[currentCertIndex].click();
        }
      } else if (e.key === "ArrowLeft") {
        if (currentCertIndex > 0) {
          currentCertIndex--;
          certTriggers[currentCertIndex].click();
        }
      }
    });
  }

  /* ----------------------------------------------------
     12. Contact Form Loading & Disabled State
     ---------------------------------------------------- */
  const contactForm = document.getElementById("contactForm");
  const contactSubmitBtn = document.getElementById("contactSubmitBtn");
  const submitBtnSpinner = document.getElementById("submitBtnSpinner");
  const submitBtnText = document.getElementById("submitBtnText");

  if (contactForm && contactSubmitBtn) {
    contactForm.addEventListener("submit", function () {
      if (submitBtnSpinner) submitBtnSpinner.classList.remove("d-none");
      if (submitBtnText) submitBtnText.textContent = "Sending Message...";
      contactSubmitBtn.setAttribute("disabled", "disabled");
      contactSubmitBtn.style.opacity = "0.75";
      contactSubmitBtn.style.cursor = "not-allowed";
    });
  }

})();
