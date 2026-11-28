// The certificate page (/certificate/?id=<number>): reads one certificate
// of completion from the app's public database and shows it. The number
// starts with the app's letters; each app keeps its records in its own
// Firebase project. Only the record with exactly this number can be read:
// nobody can list certificates (the app's firestore.rules).
(function () {
  'use strict';
  var APPS = {
    pg: { project: 'petrogram-9bc6a', app: 'petrogram', name: 'PetroGram',
          course: 'Oil and Gas Fundamentals', page: '/petrogram/' }
  };
  var main = document.querySelector('main.cert');
  if (!main) return;

  function show(state, why) {
    main.querySelectorAll('.cert-state').forEach(function (el) {
      el.hidden = el.getAttribute('data-state') !== state;
    });
    if (why) main.querySelector('.cert-why').textContent = why;
  }
  function put(cls, text) { main.querySelector('.' + cls).textContent = text; }

  var id = (new URLSearchParams(location.search).get('id') || '').trim().toLowerCase();
  var m = /^([a-z]{2})-[0-9a-f]{20}$/.exec(id);
  if (!id) return show('none', main.dataset.noid);
  var app = m && APPS[m[1]];
  if (!app) return show('none', main.dataset.none);

  fetch('https://firestore.googleapis.com/v1/projects/' + app.project +
        '/databases/(default)/documents/certificates/' + id)
    .then(function (r) {
      if (r.status === 404) return null;
      if (!r.ok) throw new Error('status ' + r.status);
      return r.json();
    })
    .then(function (doc) {
      var f = doc && doc.fields;
      var name = f && f.name && f.name.stringValue;
      var percent = f && f.percent && f.percent.integerValue;
      var issued = f && f.issued && f.issued.timestampValue;
      if (!name || !percent || !issued || (f.app && f.app.stringValue) !== app.app) {
        return show('none', main.dataset.none);
      }
      var lang = document.documentElement.lang || 'en';
      var date = new Date(issued);
      // Always as text, never as HTML: the name was typed by a person.
      put('c-name', name);
      put('c-course', app.name + ': ' + app.course);
      put('c-result', percent + '%');
      put('c-date', date.toLocaleDateString(lang, { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }));
      put('c-id', id);
      var link = main.querySelector('.c-app');
      link.textContent = app.name;
      link.setAttribute('href', link.getAttribute('href').replace(/\/petrogram\/$/, app.page));
      show('ok');
    })
    .catch(function () { show('none', main.dataset.error); });
})();
