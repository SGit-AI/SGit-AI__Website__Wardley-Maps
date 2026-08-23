/* wardley-maps.sgit.ai — renders /data/link-check.json into /resources/verification.html.

   Everything here is a function of that file. If the file is missing or has never been
   written, the page says so plainly rather than showing an empty table that reads like a
   clean bill of health — which, on a page whose entire subject is that unverified links
   look fine right up until they don't, would be the worst available failure mode. */
(function () {
  'use strict';
  var el = document.getElementById('lc');
  if (!el) return;
  var esc = function (s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;');
  };
  var ORDER = ['error', 'blocked', 'skipped', 'invalid', 'self', 'ok'];
  var LABEL = { ok: 'Responded', error: 'Failed', blocked: 'Refused a robot',
                skipped: 'Not checkable', invalid: 'Malformed', self: 'Ours' };

  function fail(msg) {
    el.innerHTML = '<div class="warnbox"><b>No verification report is published yet.</b> ' +
      esc(msg) + ' The job that writes it is <code>.github/workflows/verify-links.yml</code>; ' +
      'it runs every Monday and on demand, and commits ' +
      '<code>data/link-check.json</code> back to <code>dev</code>. Until it has run, treat ' +
      'every external link on this site as unverified — which is precisely the state this ' +
      'page exists to stop being invisible.</div>';
  }

  fetch('../data/link-check.json').then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function (d) {
    var when = (d.run_at || '').replace('T', ' ').replace('Z', ' UTC');
    var t = d.tally || {};
    var html = '<div class="hgrid">' + ORDER.filter(function (s) { return t[s]; }).map(function (s) {
      var cls = s === 'ok' ? 'strong' : s === 'error' ? 'weak'
              : s === 'blocked' ? 'partial' : 'na';
      return '<button class="hstat s-' + cls + '" data-state="' + s + '">' +
             '<span class="n">' + t[s] + '</span><span class="l">' + LABEL[s] + '</span></button>';
    }).join('') + '</div>' +
    '<p class="hsent">Last run <b>' + esc(when) + '</b> over <b>' + d.count +
    '</b> distinct URLs. Click a count to filter.</p>';

    var rows = (d.results || []).slice().sort(function (a, b) {
      return ORDER.indexOf(a.state) - ORDER.indexOf(b.state) || a.url.localeCompare(b.url);
    });
    html += '<div class="tablewrap"><table id="lctab"><thead><tr><th>State</th><th>Detail</th>' +
            '<th>URL</th><th>Linked from</th></tr></thead><tbody>' +
      rows.map(function (x) {
        var cls = x.state === 'ok' ? 'active'
                : x.state === 'error' ? 'dead'
                : x.state === 'blocked' ? 'dormant' : 'unverified';
        var detail = x.status ? 'HTTP ' + x.status : (x.error || x.reason || '');
        if (x.final_url) detail += ' → redirected';
        var from = (x.linked_from || []).slice(0, 2).join(', ') +
                   ((x.linked_from || []).length > 2 ? ' +' + (x.linked_from.length - 2) : '');
        return '<tr data-state="' + x.state + '"><td><span class="badge s-' + cls + '">' +
          esc(LABEL[x.state] || x.state) + '</span></td><td class="small">' + esc(detail) +
          '</td><td class="small"><a href="' + esc(x.url) + '">' + esc(x.url) +
          '</a>' + (x.final_url ? '<br><span class="dim">now: ' + esc(x.final_url) + '</span>' : '') +
          '</td><td class="small dim">' + esc(from) + '</td></tr>';
      }).join('') + '</tbody></table></div>';
    el.innerHTML = html;

    var active = null;
    el.querySelectorAll('[data-state]').forEach(function (b) {
      if (b.tagName !== 'BUTTON') return;
      b.addEventListener('click', function () {
        active = active === b.dataset.state ? null : b.dataset.state;
        el.querySelectorAll('#lctab tbody tr').forEach(function (tr) {
          tr.style.display = (!active || tr.dataset.state === active) ? '' : 'none';
        });
      });
    });
  }).catch(function (e) { fail('(' + e.message + ').'); });
}());
