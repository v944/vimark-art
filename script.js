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

  let currentItems = [];
  let currentIndex = 0;

  // Accessibility labels
  if (lbClose) lbClose.setAttribute('aria-label', 'Close');
  if (lbPrev) lbPrev.setAttribute('aria-label', 'Previous image');
  if (lbNext) lbNext.setAttribute('aria-label', 'Next image');

  function getVisibleItems() {
    return Array.from(document.querySelectorAll('.gallery-item:not(.hidden)'));
  }

  function openLightbox(index) {
    currentItems = getVisibleItems();
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
      const visible = getVisibleItems();
      const realIndex = visible.indexOf(item);
      openLightbox(realIndex >= 0 ? realIndex : 0);
    });
  });

  lbClose.addEventListener('click', closeLightbox);
  lbNext.addEventListener('click', nextSlide);
  lbPrev.addEventListener('click', prevSlide);

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') nextSlide();
    if (e.key === 'ArrowLeft') prevSlide();
  });

  // Filtering
  const navLinks = document.querySelectorAll('.main-nav a[data-category], .main-nav a[data-view]');
  const galleryGrid = document.querySelector('.gallery-grid');
  const aboutSection = document.getElementById('about');
  const contactSection = document.getElementById('contact');

  function showAbout() {
    if (galleryGrid) galleryGrid.classList.add('hidden');
    if (aboutSection) aboutSection.classList.remove('hidden');
    if (contactSection) contactSection.classList.add('hidden');
  }

  function showContact() {
    if (galleryGrid) galleryGrid.classList.add('hidden');
    if (aboutSection) aboutSection.classList.add('hidden');
    if (contactSection) contactSection.classList.remove('hidden');
  }

  function showGallery() {
    if (galleryGrid) galleryGrid.classList.remove('hidden');
    if (aboutSection) aboutSection.classList.add('hidden');
    if (contactSection) contactSection.classList.add('hidden');
  }

  function applyFilter(category, subcategory) {
    showGallery();
    document.querySelectorAll('.gallery-item').forEach(item => {
      let show = false;
      if (!category || category === 'all') {
        show = true;
      } else if (subcategory) {
        show = item.dataset.category === category && item.dataset.subcategory === subcategory;
      } else {
        show = item.dataset.category === category;
      }

      if (show) {
        item.classList.remove('hidden');
      } else {
        item.classList.add('hidden');
      }
    });
  }

  function openFolder(folderLi) {
    // Close other folders (accordion)
    document.querySelectorAll('.main-nav .folder.open').forEach(other => {
      if (other !== folderLi) {
        other.classList.remove('open');
      }
    });
    folderLi.classList.add('open');
  }

  function closeFolder(folderLi) {
    folderLi.classList.remove('open');
  }

  function toggleFolder(folderLi) {
    if (folderLi.classList.contains('open')) {
      closeFolder(folderLi);
    } else {
      openFolder(folderLi);
    }
  }

  function setHash(hash) {
    if (location.hash !== hash) {
      location.hash = hash;
    }
  }

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const view = link.dataset.view;

      if (view === 'about') {
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        showAbout();
        setHash('#about');
        sidebar.classList.remove('open');
        return;
      }

      if (view === 'contact') {
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        showContact();
        setHash('#contact');
        sidebar.classList.remove('open');
        return;
      }

      const category = link.dataset.category;
      const subcategory = link.dataset.subcategory || '';
      const parentFolder = link.closest('.folder');

      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      if (subcategory) {
        const parentLink = document.querySelector(`.main-nav a[data-category="${category}"]:not([data-subcategory])`);
        if (parentLink) parentLink.classList.add('active');
        if (parentFolder) openFolder(parentFolder);
        setHash('#' + category + '/' + subcategory);
      } else if (parentFolder) {
        toggleFolder(parentFolder);
        setHash('#' + category);
      } else {
        setHash('#' + category);
      }

      applyFilter(category, subcategory);
      sidebar.classList.remove('open');
    });
  });

  // Mobile toggle
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // Hash-based routing
  function handleHash() {
    const hash = location.hash.slice(1);

    if (hash === 'about') {
      navLinks.forEach(l => l.classList.remove('active'));
      const aboutLink = document.querySelector('.main-nav a[data-view="about"]');
      if (aboutLink) aboutLink.classList.add('active');
      showAbout();
      return;
    }

    if (hash === 'contact') {
      navLinks.forEach(l => l.classList.remove('active'));
      const contactLink = document.querySelector('.main-nav a[data-view="contact"]');
      if (contactLink) contactLink.classList.add('active');
      showContact();
      return;
    }

    const parts = hash.split('/');
    const category = parts[0] || 'all';
    const subcategory = parts[1] || '';

    navLinks.forEach(l => l.classList.remove('active'));
    let targetLink;
    if (subcategory) {
      targetLink = document.querySelector(`.main-nav a[data-category="${category}"][data-subcategory="${subcategory}"]`);
    } else if (category !== 'all') {
      targetLink = document.querySelector(`.main-nav a[data-category="${category}"]:not([data-subcategory])`);
    }
    if (targetLink) {
      targetLink.classList.add('active');
      const parentFolder = targetLink.closest('.folder');
      if (parentFolder) openFolder(parentFolder);
      if (subcategory) {
        const parentLink = document.querySelector(`.main-nav a[data-category="${category}"]:not([data-subcategory])`);
        if (parentLink) parentLink.classList.add('active');
      }
    }

    applyFilter(category, subcategory);
  }

  window.addEventListener('hashchange', handleHash);
  handleHash();

})();
