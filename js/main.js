/* ========================================
   VOYAGE MONDIAL - JavaScript Principal
   ======================================== */

document.addEventListener('DOMContentLoaded', function () {

  // ---- Menu mobile ----
  const menuToggle = document.querySelector('.menu-toggle');
  const mainNav = document.querySelector('.main-nav');

  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function () {
      mainNav.classList.toggle('active');
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !expanded);
    });

    document.addEventListener('click', function (e) {
      if (!menuToggle.contains(e.target) && !mainNav.contains(e.target)) {
        mainNav.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---- FAQ Accordéon ----
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const item = this.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      // Fermer tous les autres
      document.querySelectorAll('.faq-item').forEach(function (el) {
        el.classList.remove('open');
      });

      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  // ---- Calculateur de budget voyage ----
  document.querySelectorAll('.calc-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const calculator = this.closest('.calculator');
      if (!calculator) return;

      const continent = calculator.dataset.continent;
      const nbPersonnes = parseInt(calculator.querySelector('[name="nb-personnes"]').value) || 1;
      const duree = parseInt(calculator.querySelector('[name="duree"]').value) || 7;
      const lifestyle = calculator.querySelector('[name="lifestyle"]').value || 'moyen';

      const budgets = getBudgetData(continent);
      if (!budgets) return;

      const multiplicateur = { economique: 0.6, moyen: 1, confort: 1.6, luxe: 2.8 };
      const mult = multiplicateur[lifestyle] || 1;

      const hebergement = Math.round(budgets.hebergement * mult * nbPersonnes * duree);
      const nourriture = Math.round(budgets.nourriture * mult * nbPersonnes * duree);
      const transport = Math.round(budgets.transport * mult * duree);
      const activites = Math.round(budgets.activites * mult * nbPersonnes * duree);
      const total = hebergement + nourriture + transport + activites;

      const results = calculator.querySelector('.calc-results');
      if (results) {
        results.querySelector('.res-hebergement').textContent = hebergement + ' \u20ac';
        results.querySelector('.res-nourriture').textContent = nourriture + ' \u20ac';
        results.querySelector('.res-transport').textContent = transport + ' \u20ac';
        results.querySelector('.res-activites').textContent = activites + ' \u20ac';
        results.querySelector('.res-total').textContent = total + ' \u20ac';
        results.classList.add('visible');
        results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });

  function getBudgetData(continent) {
    const data = {
      europe: { hebergement: 70, nourriture: 35, transport: 25, activites: 20 },
      asie: { hebergement: 30, nourriture: 15, transport: 12, activites: 10 },
      afrique: { hebergement: 45, nourriture: 20, transport: 18, activites: 25 },
      'amerique-nord': { hebergement: 90, nourriture: 45, transport: 30, activites: 25 },
      'amerique-sud': { hebergement: 35, nourriture: 18, transport: 15, activites: 12 },
      oceanie: { hebergement: 85, nourriture: 40, transport: 35, activites: 30 },
      antarctique: { hebergement: 250, nourriture: 80, transport: 150, activites: 100 }
    };
    return data[continent] || data.europe;
  }

  // ---- Sidebar TOC active state ----
  const tocLinks = document.querySelectorAll('.sidebar-toc a');
  if (tocLinks.length > 0) {
    const headings = [];
    tocLinks.forEach(function (link) {
      const id = link.getAttribute('href');
      if (id && id.startsWith('#')) {
        const el = document.querySelector(id);
        if (el) headings.push({ link: link, el: el });
      }
    });

    window.addEventListener('scroll', function () {
      let current = '';
      headings.forEach(function (h) {
        if (h.el.getBoundingClientRect().top < 150) {
          current = h.link;
        }
      });
      tocLinks.forEach(function (l) { l.classList.remove('active'); });
      if (current) current.classList.add('active');
    });
  }

  // ---- Smooth scroll pour ancres ----
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
