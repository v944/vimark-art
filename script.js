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
    lbCaption.textContent = '';
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
  const navLinks = document.querySelectorAll('.main-nav a[data-category]');

  function applyFilter(category, subcategory) {
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

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const category = link.dataset.category;
      const subcategory = link.dataset.subcategory || '';
      const parentFolder = link.closest('.folder');

      // Update active state
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      if (subcategory) {
        // Subcategory clicked: keep parent open and active too
        const parentLink = document.querySelector(`.main-nav a[data-category="${category}"]:not([data-subcategory])`);
        if (parentLink) parentLink.classList.add('active');
        if (parentFolder) openFolder(parentFolder);
      } else if (parentFolder) {
        // Parent folder link clicked: toggle folder, don't close others unless opening this one
        toggleFolder(parentFolder);
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

  // Default: show all
  applyFilter('all', '');


})();
