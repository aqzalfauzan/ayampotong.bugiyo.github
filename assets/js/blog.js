/* Ayam Potong Bu Giyo — skrip kecil bersama: tema, menu, bagikan, cari & label */
(function () {
  var root = document.documentElement;

  // ---- tema terang/gelap (disimpan per pengunjung) ----
  function store(key, val) {
    try { if (val === undefined) return localStorage.getItem(key); localStorage.setItem(key, val); } catch (e) { return null; }
  }
  var saved = store('apbg-theme');
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);

  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    function label() { btn.setAttribute('aria-label', isDark() ? 'Ganti ke tema terang' : 'Ganti ke tema gelap'); }
    label();
    btn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      store('apbg-theme', next);
      label();
    });
  });

  // ---- menu di layar kecil ----
  var menuBtn = document.querySelector('[data-menu-toggle]');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ---- tombol bagikan ----
  var share = document.querySelector('[data-share]');
  if (share) {
    var url = location.protocol.indexOf('http') === 0 ? location.href.split('#')[0] : share.getAttribute('data-url');
    var title = share.getAttribute('data-title') || document.title;
    var enc = encodeURIComponent;
    var links = {
      wa: 'https://wa.me/?text=' + enc(title + ' ' + url),
      fb: 'https://www.facebook.com/sharer/sharer.php?u=' + enc(url),
      x: 'https://twitter.com/intent/tweet?text=' + enc(title) + '&url=' + enc(url),
      tg: 'https://t.me/share/url?url=' + enc(url) + '&text=' + enc(title)
    };
    share.querySelectorAll('[data-net]').forEach(function (a) { a.href = links[a.getAttribute('data-net')]; });
    var copy = share.querySelector('[data-copy]');
    if (copy) {
      copy.addEventListener('click', function () {
        var done = function () { var t = copy.lastChild.textContent; copy.lastChild.textContent = ' Tersalin!'; setTimeout(function () { copy.lastChild.textContent = t; }, 1800); };
        if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { window.prompt('Salin tautan ini:', url); });
        else window.prompt('Salin tautan ini:', url);
      });
    }
  }

  // ---- beranda: cari & saring label ----
  var list = document.querySelector('[data-post-list]');
  if (!list) return;
  var posts = Array.prototype.slice.call(document.querySelectorAll('[data-post]'));
  var note = document.querySelector('[data-filter-note]');
  var empty = document.querySelector('[data-empty]');
  var input = document.querySelector('[data-search-input]');

  function apply() {
    var params = new URLSearchParams(location.search);
    var q = (params.get('q') || '').trim().toLowerCase();
    var label = (params.get('label') || '').trim();
    if (input) input.value = params.get('q') || '';
    var shown = 0;
    posts.forEach(function (p) {
      var okQ = !q || p.textContent.toLowerCase().indexOf(q) !== -1;
      var okL = !label || (p.getAttribute('data-labels') || '').split(',').indexOf(label) !== -1;
      var ok = okQ && okL;
      p.hidden = !ok;
      if (ok) shown++;
    });
    document.querySelectorAll('[data-label-link]').forEach(function (a) {
      a.classList.toggle('on', a.getAttribute('data-label-link') === label);
    });
    if (note) {
      if (q || label) {
        note.hidden = false;
        note.querySelector('span').textContent = shown + ' artikel ' + (label ? 'berlabel "' + label + '"' : '') + (q && label ? ' dan ' : '') + (q ? 'cocok dengan "' + q + '"' : '') + '. ';
      } else note.hidden = true;
    }
    if (empty) empty.hidden = shown !== 0;
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-label-link]');
    var clear = e.target.closest('[data-clear]');
    if (!a && !clear) return;
    e.preventDefault();
    var url = clear ? location.pathname : a.getAttribute('href');
    history.pushState(null, '', url);
    apply();
    list.scrollIntoView({ block: 'start' });
  });
  var form = document.querySelector('[data-search]');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = input.value.trim();
    history.pushState(null, '', q ? '?q=' + encodeURIComponent(q) : location.pathname);
    apply();
  });
  window.addEventListener('popstate', apply);
  apply();
})();
