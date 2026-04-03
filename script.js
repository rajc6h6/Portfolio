/* ============================================
   Raj Jaiswal Portfolio — Interactions
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // --- Scroll-based navbar ---
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // --- Mobile nav toggle ---
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      toggle.classList.toggle('active');
    });
    // Close menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        toggle.classList.remove('active');
      });
    });
  }

  // --- Intersection Observer for fade-in ---
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
  });

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const navHeight = nav ? nav.offsetHeight : 0;
        const y = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    });
  });

  // --- Animate KPI sparklines ---
  const sparklines = document.querySelectorAll('.kpi-sparkline');
  sparklines.forEach((sparkline, si) => {
    const bars = sparkline.querySelectorAll('.bar');
    const patterns = [
      [6, 10, 8, 16, 12, 22, 14, 26],
      [10, 18, 14, 8, 20, 12, 24, 16],
      [8, 12, 18, 10, 14, 24, 20, 28],
      [14, 8, 20, 16, 10, 26, 18, 22]
    ];
    const heights = patterns[si % patterns.length];
    bars.forEach((bar, i) => {
      const h = heights[i % heights.length];
      bar.style.height = h + 'px';
      bar.style.transitionDelay = (i * 0.04) + 's';
    });
  });

  // --- Typing / counter animation for KPI values ---
  const kpiValues = document.querySelectorAll('.kpi-value[data-target]');
  const kpiObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateValue(entry.target);
        kpiObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  kpiValues.forEach(el => kpiObserver.observe(el));

  function animateValue(el) {
    const target = el.getAttribute('data-target');
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const isFloat = target.includes('.');
    const endVal = parseFloat(target);
    const duration = 1200;
    const start = performance.now();

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out quad
      const eased = 1 - (1 - progress) * (1 - progress);
      const current = eased * endVal;

      if (isFloat) {
        el.textContent = prefix + current.toFixed(2) + suffix;
      } else {
        el.textContent = prefix + Math.round(current) + suffix;
      }

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = prefix + target + suffix;
      }
    }
    requestAnimationFrame(step);
  }

  // --- Active nav highlight on scroll ---
  const sections = document.querySelectorAll('.section[id]');
  if (sections.length > 0) {
    const navHighlight = () => {
      const scrollPos = window.scrollY + 200;
      sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');
        const link = document.querySelector(`.nav-links a[href="#${id}"]`);
        if (link) {
          if (scrollPos >= top && scrollPos < top + height) {
            link.style.color = 'var(--text-primary)';
          } else {
            link.style.color = '';
          }
        }
      });
    };
    window.addEventListener('scroll', navHighlight, { passive: true });
  }

  // --- Subtle parallax on hero visual ---
  const heroVisual = document.querySelector('.hero-visual');
  if (heroVisual) {
    const hero = document.querySelector('.hero');
    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      heroVisual.style.transform = `translate(${x * 8}px, ${y * 6}px)`;
      heroVisual.style.transition = 'transform 0.3s ease-out';
    });
    hero.addEventListener('mouseleave', () => {
      heroVisual.style.transform = 'translate(0, 0)';
    });
  }

  // --- Mobile Carousel Highlight on Slide ---
  if (window.innerWidth <= 768) {
    const carouselCards = document.querySelectorAll('.exp-card, .project-card, .principle-card, .skill-category, .impact-card');
    
    const observerOptions = {
      root: null,
      rootMargin: '0px -10% 0px -10%', // focus on the center
      threshold: 0.55 // card is mostly in view
    };
    
    const carouselObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('mobile-hover');
        } else {
          entry.target.classList.remove('mobile-hover');
        }
      });
    }, observerOptions);

    carouselCards.forEach(card => {
      carouselObserver.observe(card);
    });
  }
});
