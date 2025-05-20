document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("darkModeToggle");
  const icon = document.getElementById("darkModeIcon");

  // Verifica o localStorage
  const darkModeAtivo = localStorage.getItem("darkMode") === "true";
  if (darkModeAtivo) {
    document.body.classList.add("dark-mode");
    icon.classList.replace("ri-moon-line", "ri-sun-line");
  }

  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const modoEscuroAtivo = document.body.classList.contains("dark-mode");
    localStorage.setItem("darkMode", modoEscuroAtivo);

    // Troca o ícone
    if (modoEscuroAtivo) {
      icon.classList.replace("ri-moon-line", "ri-sun-line");
    } else {
      icon.classList.replace("ri-sun-line", "ri-moon-line");
    }
  });
});

