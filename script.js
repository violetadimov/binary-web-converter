document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("toggleDarkMode");
  if (toggle) {
    fetch("/get-theme")
      .then(res => res.json())
      .then(data => {
        if (data.theme === "dark") {
          document.body.classList.add("dark-mode");
          toggle.checked = true;
        }
      });

    toggle.addEventListener("change", () => {
      const theme = toggle.checked ? "dark" : "light";
      document.body.classList.toggle("dark-mode", theme === "dark");
      fetch("/set-theme", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ theme })
      });
    });
  }
});