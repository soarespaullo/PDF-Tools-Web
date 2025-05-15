const toggleBtn = document.getElementById('toggleDarkMode');
const donateBtn = document.getElementById('donateBtn');
const body = document.body;

// Aplica preferência salva de modo escuro
if (localStorage.getItem('darkMode') === 'enabled') {
  body.classList.add('dark');
  toggleBtn.innerHTML = '<i class="ri-sun-line"></i>';
}

toggleBtn.addEventListener('click', () => {
  body.classList.toggle('dark');
  if (body.classList.contains('dark')) {
    toggleBtn.innerHTML = '<i class="ri-sun-line"></i>';
    localStorage.setItem('darkMode', 'enabled');
  } else {
    toggleBtn.innerHTML = '<i class="ri-moon-line"></i>';
    localStorage.setItem('darkMode', 'disabled');
  }
});

// Detecta scroll para mostrar/ocultar botões
let lastScrollTop = 0;
window.addEventListener('scroll', () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollTop > lastScrollTop) {
    // Scroll para baixo: esconder botões
    donateBtn.classList.add('hidden');
    toggleBtn.classList.add('hidden');
  } else {
    // Scroll para cima: mostrar botões
    donateBtn.classList.remove('hidden');
    toggleBtn.classList.remove('hidden');
  }
  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // evita negativo
});

