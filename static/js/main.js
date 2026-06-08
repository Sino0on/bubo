// Burger menu
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');

if (burger && nav) {
  burger.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('nav--open');
    burger.setAttribute('aria-expanded', isOpen);
  });

  document.addEventListener('click', (e) => {
    if (!nav.contains(e.target) && !burger.contains(e.target)) {
      nav.classList.remove('nav--open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });
}

// Catalog filters toggle (mobile)
const filtersToggle = document.getElementById('filtersToggle');
const filtersWrap = document.getElementById('filtersWrap');

if (filtersToggle && filtersWrap) {
  filtersToggle.addEventListener('click', () => {
    filtersWrap.classList.toggle('filters-wrap--open');
    filtersToggle.textContent = filtersWrap.classList.contains('filters-wrap--open')
      ? 'Фильтры и поиск ▴'
      : 'Фильтры и поиск ▾';
  });
}

// Auto-dismiss messages
document.querySelectorAll('.message').forEach(msg => {
  setTimeout(() => { msg.style.transition = 'opacity .5s'; msg.style.opacity = '0'; }, 4000);
});
