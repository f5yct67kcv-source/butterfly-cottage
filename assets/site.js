/* Butterfly Cottage — theme toggle, mobile nav, reveal, lightbox, video */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ---------- Theme ---------- */
  var stored = null; // no localStorage: sandboxed iframes block it
  function preferred() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }
  function applyTheme(t) {
    root.setAttribute('data-theme', t);
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) {
      btn.setAttribute('aria-pressed', String(t === 'dark'));
    }
  }
  applyTheme(stored || preferred());

  var toggle = document.querySelector('[data-theme-toggle]');
  if (toggle) {
    toggle.addEventListener('click', function () {
      stored = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(stored);
    });
  }

  /* ---------- Sticky header state ---------- */
  var header = document.querySelector('.header');
  var onScroll = function () {
    if (header) header.setAttribute('data-scrolled', String(window.scrollY > 12));
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Mobile nav ---------- */
  var burger = document.querySelector('[data-burger]');
  var nav = document.getElementById('primary-nav');
  function closeNav() {
    if (!nav || !burger) return;
    nav.setAttribute('data-open', 'false');
    burger.setAttribute('aria-expanded', 'false');
  }
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      burger.setAttribute('aria-expanded', String(!open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeNav();
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Lightbox ---------- */
  var shots = Array.prototype.slice.call(document.querySelectorAll('.shot'));
  var box = document.querySelector('[data-lightbox]');
  if (shots.length && box) {
    var boxImg = box.querySelector('img');
    var boxCap = box.querySelector('figcaption');
    var index = 0;
    var lastFocus = null;

    function show(i) {
      index = (i + shots.length) % shots.length;
      var src = shots[index].getAttribute('data-full');
      var alt = shots[index].querySelector('img').getAttribute('alt');
      boxImg.setAttribute('src', src);
      boxImg.setAttribute('alt', alt);
      boxCap.textContent = alt + '  ·  ' + (index + 1) + '/' + shots.length;
    }
    function open(i) {
      lastFocus = document.activeElement;
      show(i);
      box.setAttribute('open', '');
      document.body.style.overflow = 'hidden';
      box.querySelector('.lightbox__close').focus();
    }
    function close() {
      box.removeAttribute('open');
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    }

    shots.forEach(function (shot, i) {
      shot.addEventListener('click', function () { open(i); });
    });
    box.addEventListener('click', function (e) {
      var dir = e.target.closest('[data-dir]');
      if (dir) { show(index + (dir.getAttribute('data-dir') === 'next' ? 1 : -1)); return; }
      if (e.target.closest('.lightbox__close') || e.target === box) close();
    });
    window.addEventListener('keydown', function (e) {
      if (!box.hasAttribute('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(index + 1);
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'Tab') {
        var f = box.querySelectorAll('button');
        var first = f[0];
        var last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        else if (!box.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ---------- Click-to-load video (keeps YouTube off first load) ---------- */
  var video = document.querySelector('[data-video]');
  if (video) {
    video.addEventListener('click', function () {
      var id = video.getAttribute('data-video');
      var frame = document.createElement('iframe');
      frame.setAttribute(
        'src',
        'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0'
      );
      frame.setAttribute('title', video.getAttribute('data-video-title') || 'Video');
      frame.setAttribute('allow', 'accelerometer; autoplay; encrypted-media; picture-in-picture');
      frame.setAttribute('allowfullscreen', '');
      frame.setAttribute('loading', 'lazy');
      video.innerHTML = '';
      video.appendChild(frame);
      video.style.cursor = 'default';
    });
  }

  /* ---------- Year ---------- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
