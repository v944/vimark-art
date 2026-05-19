(function() {
  'use strict';

  const lightbox = document.getElementById('lightbox');
  const lbImg = document.querySelector('.lightbox-img');
  const lbCaption = document.querySelector('.lightbox-caption');
  const lbCounter = document.querySelector('.lightbox-counter');
  const lbClose = document.querySelector('.lightbox-close');
  const lbPrev = document.querySelector('.lightbox-prev');
  const lbNext = document.querySelector('.lightbox-next');
  const mobileToggle = document.querySelector('.mobile-toggle');
  const sidebar = document.getElementById('sidebar');
  const main = document.getElementById('main');

  let currentItems = [];
  let currentIndex = 0;

  // Mobile sidebar overlay
  let overlay = document.querySelector('.sidebar-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      if (sidebar) sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active', sidebar.classList.contains('open'));
    });
  }

  // Accessibility labels
  if (lbClose) lbClose.setAttribute('aria-label', 'Close');
  if (lbPrev) lbPrev.setAttribute('aria-label', 'Previous image');
  if (lbNext) lbNext.setAttribute('aria-label', 'Next image');

  // Lightbox loader element
  let lbLoader = document.querySelector('.lightbox-loader');
  if (!lbLoader && lightbox) {
    lbLoader = document.createElement('div');
    lbLoader.className = 'lightbox-loader';
    lightbox.insertBefore(lbLoader, lbImg);
  }

  function getGalleryItems() {
    return Array.from(document.querySelectorAll('.gallery-item'));
  }

  function openLightbox(index) {
    currentItems = getGalleryItems();
    if (!currentItems.length) return;
    currentIndex = index;
    updateLightbox();
    preloadAdjacent();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  function updateLightbox() {
    const item = currentItems[currentIndex];
    if (!item) return;
    const img = item.querySelector('img');
    const newSrc = img.dataset.full || img.src;

    if (lbImg.src !== newSrc) {
      lbImg.classList.remove('loaded');
      if (lbLoader) lbLoader.style.display = 'block';
      lbImg.src = newSrc;
    }

    lbCaption.textContent = img.alt || '';
    lbCounter.textContent = (currentIndex + 1) + ' / ' + currentItems.length;
    preloadAdjacent();
  }

  if (lbImg) {
    lbImg.addEventListener('load', () => {
      lbImg.classList.add('loaded');
      if (lbLoader) lbLoader.style.display = 'none';
    });
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % currentItems.length;
    updateLightbox();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + currentItems.length) % currentItems.length;
    updateLightbox();
  }

  // Preload adjacent images
  function preloadAdjacent() {
    if (!currentItems.length) return;
    const indices = [
      (currentIndex + 1) % currentItems.length,
      (currentIndex - 1 + currentItems.length) % currentItems.length
    ];
    indices.forEach(idx => {
      const item = currentItems[idx];
      if (!item) return;
      const src = item.querySelector('img').dataset.full || item.querySelector('img').src;
      const img = new Image();
      img.src = src;
    });
  }

  // Swipe support for lightbox
  let touchStartX = 0;
  let touchEndX = 0;

  if (lightbox) {
    lightbox.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const delta = touchEndX - touchStartX;
      if (delta < -50) nextSlide();
      if (delta > 50) prevSlide();
    }, { passive: true });
  }

  // Event listeners for gallery items
  document.querySelectorAll('.gallery-item').forEach((item) => {
    item.addEventListener('click', () => {
      const items = getGalleryItems();
      const realIndex = items.indexOf(item);
      openLightbox(realIndex >= 0 ? realIndex : 0);
    });
  });

  if (lbClose) lbClose.addEventListener('click', closeLightbox);
  if (lbNext) lbNext.addEventListener('click', nextSlide);
  if (lbPrev) lbPrev.addEventListener('click', prevSlide);

  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (lightbox && lightbox.classList.contains('active')) {
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
      return;
    }
    if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('active');
    }
  });

  // Show / hide sections
  const heroSection = document.querySelector('.hero');
  const projectSections = document.querySelectorAll('.projects-section');
  const aboutSection = document.getElementById('about');
  const contactSection = document.getElementById('contact');
  const navLinks = document.querySelectorAll('.main-nav a');

  function showProjects() {
    if (heroSection) heroSection.classList.remove('hidden');
    projectSections.forEach(s => s.classList.remove('hidden'));
    if (aboutSection) aboutSection.classList.add('hidden');
    if (contactSection) contactSection.classList.add('hidden');
  }

  function showAbout() {
    if (heroSection) heroSection.classList.add('hidden');
    projectSections.forEach(s => s.classList.add('hidden'));
    if (aboutSection) aboutSection.classList.remove('hidden');
    if (contactSection) contactSection.classList.add('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function showContact() {
    if (heroSection) heroSection.classList.add('hidden');
    projectSections.forEach(s => s.classList.add('hidden'));
    if (aboutSection) aboutSection.classList.add('hidden');
    if (contactSection) contactSection.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Navigation click handling
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (!href || !href.startsWith('#')) return;
      const targetId = href.slice(1);

      if (targetId === 'about') {
        e.preventDefault();
        showAbout();
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
        return;
      }

      if (targetId === 'contact') {
        e.preventDefault();
        showContact();
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
        return;
      }

      // Category anchor — show projects and smooth scroll
      e.preventDefault();
      showProjects();
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      const target = document.getElementById(targetId);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
      if (sidebar) sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('active');
    });
  });

  // Hash-based routing for about/contact on load
  function handleHash() {
    const hash = location.hash.slice(1);
    if (hash === 'about') {
      showAbout();
      navLinks.forEach(l => l.classList.remove('active'));
      const aboutLink = document.querySelector('.main-nav a[href="#about"]');
      if (aboutLink) aboutLink.classList.add('active');
      return;
    }
    if (hash === 'contact') {
      showContact();
      navLinks.forEach(l => l.classList.remove('active'));
      const contactLink = document.querySelector('.main-nav a[href="#contact"]');
      if (contactLink) contactLink.classList.add('active');
      return;
    }
    showProjects();
  }

  window.addEventListener('hashchange', handleHash);
  handleHash();

  // Scroll spy — highlight active nav based on scroll position
  function updateActiveNav() {
    const scrollPos = window.scrollY + 120;

    // Check project sections
    for (const section of projectSections) {
      const rect = section.getBoundingClientRect();
      const top = section.offsetTop;
      const bottom = top + section.offsetHeight;
      if (scrollPos >= top && scrollPos < bottom) {
        const id = section.id;
        navLinks.forEach(l => {
          l.classList.toggle('active', l.getAttribute('href') === '#' + id);
        });
        return;
      }
    }
  }

  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();

  // Hero scroll fade effect
  if (heroSection) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      const vh = window.innerHeight;
      const progress = Math.min(scrollY / vh, 1);
      heroSection.style.opacity = 1 - progress * 0.8;
      heroSection.style.transform = 'scale(' + (1 + progress * 0.05) + ')';
    }, { passive: true });
  }
})();
