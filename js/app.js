// Menu burger
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav');

if (burger) {
  burger.addEventListener('click', () => {
    nav.classList.toggle('open');
    const expanded = nav.classList.contains('open');
    burger.setAttribute('aria-expanded', expanded ? 'true' : 'false');
  });

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    });
  });
}

// Before/After Toggle Switch
document.querySelectorAll('.before-after-container').forEach(container => {
  const beforeImg = container.querySelector('.before-img');
  const toggleBtn = container.querySelector('.toggle-btn');
  
  // Initialize: show before image
  beforeImg.style.width = '100%';
  toggleBtn.classList.add('active');
  toggleBtn.setAttribute('aria-pressed', 'true');
  
  toggleBtn.addEventListener('click', () => {
    toggleBtn.classList.toggle('active');
    const isActive = toggleBtn.classList.contains('active');
    toggleBtn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    if (isActive) {
      // Show before
      beforeImg.style.width = '100%';
    } else {
      // Show after
      beforeImg.style.width = '0%';
    }
  });

  // keyboard accessibility: toggle on Enter or Space
  toggleBtn.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleBtn.click();
    }
  });
});

// Contact form removed: site uses phone and email links only.

// Cookie consent: simple implementation
const cookieBanner = document.getElementById('cookie-consent');
const cookieAccept = document.getElementById('cookie-accept');
const cookieDeny = document.getElementById('cookie-deny');
function hasCookieConsent() { return localStorage.getItem('cookie_consent') === 'yes'; }
function setCookieConsent(val) { localStorage.setItem('cookie_consent', val ? 'yes' : 'no'); }

if (cookieBanner) {
  if (!hasCookieConsent()) {
    cookieBanner.style.display = 'block';
  }
  cookieAccept && cookieAccept.addEventListener('click', () => {
    setCookieConsent(true);
    cookieBanner.style.display = 'none';
    // Load GA if configured
    if (window._GA_MEASUREMENT_ID && window._GA_MEASUREMENT_ID !== 'G-XXXXXXX') {
      (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
      new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
      j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
      'https://www.googletagmanager.com/gtag/js?id='+i;f.parentNode.insertBefore(j,f);
      })(window,document,'script','dataLayer',window._GA_MEASUREMENT_ID);
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);} gtag('js', new Date());
      gtag('config', window._GA_MEASUREMENT_ID);
    }
  });
  cookieDeny && cookieDeny.addEventListener('click', () => { setCookieConsent(false); cookieBanner.style.display = 'none'; });
}

// --- Light animations: reveal on scroll (IntersectionObserver) ---
function setupScrollReveal() {
  if (!('IntersectionObserver' in window)) return; // graceful fallback
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        // stagger reveal for children marked .reveal-child
        const children = entry.target.querySelectorAll('.reveal-child');
        if (children && children.length) {
          children.forEach((c, i) => {
            const delay = i * 80;
            c.style.setProperty('--delay', delay + 'ms');
          });
        }
        // one-time reveal: stop observing after adding class
        io.unobserve(entry.target);
      }
    });
  }, { root: null, rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  document.querySelectorAll('.section, .project').forEach(el => io.observe(el));
}

// small hero parallax on pointer devices (only on wide screens)
function setupHeroParallax() {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  if (window.matchMedia('(pointer:fine) and (min-width:721px)').matches) {
    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      const px = (x - 0.5) * 6; // small offset
      const py = (y - 0.5) * 3;
      hero.style.backgroundPosition = `calc(50% + ${px}px) calc(50% + ${py}px)`;
    });
    hero.addEventListener('mouseleave', () => { hero.style.backgroundPosition = 'center'; });
  }
}

// initialize animations on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  try { setupScrollReveal(); } catch (e) { /* noop */ }
  try { setupHeroParallax(); } catch (e) { /* noop */ }
});

// Header shrink behaviour on scroll
function setupHeaderShrink() {
  const header = document.querySelector('.header');
  if (!header) return;
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const y = window.scrollY || window.pageYOffset;
    if (y > 60) header.classList.add('shrink'); else header.classList.remove('shrink');
    lastScroll = y;
  }, { passive: true });
}

// Apply hero and header reveals after DOM ready
document.addEventListener('DOMContentLoaded', () => {
  try { setupHeaderShrink(); } catch (e) {}
  // hero title/lead entrance: mark as reveal-child so it participates in stagger
  const hero = document.querySelector('.hero');
  if (hero) {
    const titles = hero.querySelectorAll('h1, h2, .hero-sub');
    titles.forEach((t, i) => t.classList.add('reveal-child'));
  }
});
