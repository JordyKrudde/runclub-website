// ── Header: vast worden bij scrollen ────────────────────────────────────────
(function () {
  const header = document.getElementById('siteheader');
  if (!header) return;

  const observer = new IntersectionObserver(
    ([entry]) => header.classList.toggle('siteheader--vast', !entry.isIntersecting),
    { threshold: 0, rootMargin: '-80px 0px 0px 0px' }
  );

  // Observeer een onzichtbaar anker direct onder de header
  const anker = document.createElement('div');
  anker.style.cssText = 'position:absolute;top:80px;height:1px;width:1px;pointer-events:none;';
  document.body.prepend(anker);
  observer.observe(anker);
})();

// ── Mobiel menu toggle ───────────────────────────────────────────────────────
(function () {
  const menuKnop = document.querySelector('.siteheader__menu-knop');
  const nav = document.getElementById('mobiel-menu');
  if (!menuKnop || !nav) return;

  menuKnop.addEventListener('click', function () {
    const isOpen = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', String(!isOpen));
    nav.classList.toggle('siteheader__nav--open', !isOpen);
    document.body.style.overflow = isOpen ? '' : 'hidden';
  });

  // Sluit menu bij klik op een link
  nav.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
      menuKnop.setAttribute('aria-expanded', 'false');
      nav.classList.remove('siteheader__nav--open');
      document.body.style.overflow = '';
    });
  });
})();
