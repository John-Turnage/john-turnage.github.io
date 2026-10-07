// Theme toggle
(() => {
  const root = document.documentElement;
  const button = document.querySelector(".theme-toggle");
  if (!button) return;
  const label = () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    button.setAttribute("aria-label", `Switch to ${next} theme`);
  };
  label();
  button.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
    label();
  });
})();

// Figure viewer
document.querySelectorAll(".viewer").forEach((viewer) => {
  const slides = [...viewer.querySelectorAll(".viewer__slide")];
  if (slides.length < 2) return;
  const counter = viewer.querySelector(".viewer__count");
  let index = 0;
  const show = (i) => {
    index = (i + slides.length) % slides.length;
    slides.forEach((slide, j) => { slide.hidden = j !== index; });
    counter.textContent = `${index + 1} / ${slides.length}`;
  };
  viewer.querySelector("[data-prev]").addEventListener("click", () => show(index - 1));
  viewer.querySelector("[data-next]").addEventListener("click", () => show(index + 1));
  viewer.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });
  viewer.classList.add("is-ready");
  show(0);
});

// Copy BibTeX
document.querySelectorAll(".copy-button").forEach((button) => {
  button.addEventListener("click", async () => {
    const text = button.parentElement.querySelector("pre").textContent;
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = "Copied";
    } catch (e) {
      button.textContent = "Select and copy manually";
    }
    setTimeout(() => { button.textContent = "Copy BibTeX"; }, 1800);
  });
});

// Abstract/BibTeX toggles
document.querySelectorAll(".pub__toggle").forEach((button) => {
  const panel = document.getElementById(button.getAttribute("aria-controls"));
  button.addEventListener("click", () => {
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    panel.hidden = open;
  });
});

// Remove "Upcoming" tags once the month has passed
document.querySelectorAll(".tag[data-month]").forEach((tag) => {
  const [year, month] = tag.dataset.month.split("-").map(Number);
  if (new Date() >= new Date(year, month, 1)) tag.remove();
});
