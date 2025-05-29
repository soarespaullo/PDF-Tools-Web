document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("darkModeToggle");
  const icon = document.getElementById("darkModeIcon");

  // Aplica modo escuro se estava ativo
  const darkModeAtivo = localStorage.getItem("darkMode") === "true";
  if (darkModeAtivo) {
    document.body.classList.add("dark-mode");
    if (icon) {
      icon.classList.replace("ri-moon-line", "ri-sun-line");
    }
  }

  // Só adiciona o listener se o botão existir na página
  if (toggleBtn && icon) {
    toggleBtn.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
      const modoEscuroAtivo = document.body.classList.contains("dark-mode");
      localStorage.setItem("darkMode", modoEscuroAtivo);

      icon.classList.toggle("ri-moon-line", !modoEscuroAtivo);
      icon.classList.toggle("ri-sun-line", modoEscuroAtivo);
    });
  }
});

