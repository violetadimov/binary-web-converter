// =================== DARK MODE TOGGLE ===================
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

document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const body = document.body

  hamburger.addEventListener('click', () => {
    const isMobile = window.innerWidth <= 768;

    if (isMobile) {
      //mobile behavior
      const isOpen = sidebar.classList.toggle('visible')
      body.classList.toggle('sidebar-open', isOpen);
      overlay.classList.toggle('active', isOpen);
      hamburger.style.left = isOpen ? '235px' : '15px';
    }
  });
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('visible');
    body.classList.remove('sidebar-open');
    overlay.classList.remove('active');
    hamburger.style.left = '15px';
  });

  const sidebarLinks = sidebar.querySelectorAll('a');

  sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
      const isMobile = window.innerWidth <= 768;
      if (isMobile) {
        sidebar.classList.remove('visible');
        body.classList.remove('sidebar-open');
        overlay.classList.remove('active');
        hamburger.classList.remove('sidebar-open');
        hamburger.style.left = '15px';
      }
    })
  })

  const userIcon = document.getElementById('userIcon');
  const userDropdown = document.getElementById('userDropdown');

  userIcon.addEventListener('click', (e) => {
    userDropdown.classList.toggle('active');
  });

  document.addEventListener('click', (e) => {
    if (!userDropdown.contains(e.target) && e.target !== userIcon) {
      userDropdown.classList.remove('active');
    }
  });
});


