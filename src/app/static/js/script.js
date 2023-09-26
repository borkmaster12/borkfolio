document.addEventListener("DOMContentLoaded", () => {
  currentNavElement = document.querySelector(
    `[href='${window.location.pathname}']`
  );
  if (currentNavElement) {
    currentNavElement.classList.add("active");
  }
});
