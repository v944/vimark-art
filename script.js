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

  // Accessibility labels
  if (lbClose) lbClose.setAttribute('aria-label', 'Close');
  if (lbPrev) lbPrev.setAttribute('aria-label', 'Previous image');
  if (lbNext) lbNext.setAttribute('aria-label', 'Next image');

  function getGalleryItems() {
    return Array.from(document.querySelectorAll('.gallery-item'));
  }

  function openLightbox(index) {
    currentItems = getGalleryItems();
    if (!currentItems.length) return;
    currentIndex = index;
    updateLightbox();
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
    lbImg.src = img.dataset.full || img.src;
    lbCaption.textContent = img.alt || '';
    lbCounter.textContent = (currentIndex + 1) + ' / ' + currentItems.length;
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % currentItems.length;
    updateLightbox();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + currentItems.length) % currentItems.length;
    updateLightbox();
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
    if (!lightbox || !lightbox.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextSlide();
    if (e.key === 'ArrowLeft') prevSlide();
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
    if (heroSection) heroSection.classList.remove('hidden');
    projectSections.forEach(s => s.classList.add('hidden'));
    if (aboutSection) aboutSection.classList.remove('hidden');
    if (contactSection) contactSection.classList.add('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function showContact() {
    if (heroSection) heroSection.classList.remove('hidden');
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
        sidebar.classList.remove('open');
        return;
      }

      if (targetId === 'contact') {
        e.preventDefault();
        showContact();
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        sidebar.classList.remove('open');
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
      sidebar.classList.remove('open');
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

  // Mobile toggle
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }
})();
