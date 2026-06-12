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
