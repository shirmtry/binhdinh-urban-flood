/* Ngập úng đô thị Quy Nhơn 2026 – HTK · Hotline/Zalo: 0396241674
 * Dữ liệu mô phỏng – cập nhật 09/11/2026
 * Dự báo ngập qua API Flask + form báo ngập cộng đồng lưu localStorage.
 */
(function () {
  'use strict';

  /* ---------- Dự báo ngập theo lượng mưa ---------- */
  var predictForm = document.getElementById('predict-form');
  var predictStatus = document.getElementById('predict-status');
  var predictBody = document.getElementById('predict-body');

  function setStatus(el, msg, ok) {
    el.textContent = msg;
    el.className = 'status ' + (ok ? 'ok' : 'err');
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function renderPrediction(data) {
    var rows = data.results.map(function (r, i) {
      // Cập nhật màu + số trên bản đồ SVG
      var dot = document.getElementById('dot-' + r.id);
      var depth = document.getElementById('depth-' + r.id);
      if (dot) {
        dot.setAttribute('fill', r.color);
        var title = dot.querySelector('title');
        if (title) title.textContent = r.name + ' – ' + r.levelLabel + ' (' + r.depthCm + 'cm, mưa ' + data.rainMm + 'mm)';
      }
      if (depth) depth.textContent = Math.round(r.depthCm);
      return '<tr><td>' + (i + 1) + '</td><td>' + escapeHtml(r.name) + '</td><td>' +
        escapeHtml(r.ward) + '</td><td><strong>' + r.depthCm + '</strong></td><td>' +
        '<span class="badge" style="background:' + r.color + '">' + escapeHtml(r.levelLabel) + '</span></td></tr>';
    });
    predictBody.innerHTML = rows.join('');
    setStatus(predictStatus, '✔ Dự báo với mưa ' + data.rainMm + 'mm/2h – bản đồ đã cập nhật màu theo mức ngập.', true);
  }

  if (predictForm) {
    predictForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var rain = parseFloat(document.getElementById('rain-mm').value);
      if (isNaN(rain) || rain < 0 || rain > 1000) {
        setStatus(predictStatus, 'Lượng mưa phải từ 0 đến 1000 mm.', false);
        return;
      }
      setStatus(predictStatus, 'Đang tính toán dự báo…', true);
      fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rain_mm: rain })
      })
        .then(function (res) { return res.json().then(function (j) { return { ok: res.ok, data: j }; }); })
        .then(function (r) {
          if (!r.ok || !r.data.ok) throw new Error(r.data.error || 'Lỗi API dự báo.');
          renderPrediction(r.data);
        })
        .catch(function (err) { setStatus(predictStatus, '✖ ' + err.message, false); });
    });
  }

  /* ---------- Form báo ngập cộng đồng (localStorage) ---------- */
  var STORAGE_KEY = 'htk-urban-flood-reports-2026';
  var reportForm = document.getElementById('report-form');
  var reportList = document.getElementById('report-list');
  var reportCount = document.getElementById('report-count');
  var reportStatus = document.getElementById('report-status');
  var reportClear = document.getElementById('report-clear');

  function loadReports() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch (e) { return []; }
  }

  function saveReports(items) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); } catch (e) { /* full/blocked */ }
  }

  function renderReports() {
    var items = loadReports();
    reportCount.textContent = items.length;
    if (!items.length) {
      reportList.innerHTML = '<li>Chưa có báo cáo nào. Hãy là người đầu tiên báo điểm ngập!</li>';
      return;
    }
    reportList.innerHTML = items.map(function (r) {
      return '<li><strong>' + escapeHtml(r.name) + '</strong> báo <strong>' + escapeHtml(r.point) +
        '</strong> – <span class="rp-depth">ngập ~' + escapeHtml(r.depth) + 'cm</span>' +
        (r.desc ? '<br>' + escapeHtml(r.desc) : '') +
        '<div class="rp-meta">⏱ ' + escapeHtml(r.time) + ' · Dữ liệu mô phỏng – cập nhật 09/11/2026</div></li>';
    }).join('');
  }

  if (reportForm) {
    reportForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = document.getElementById('rp-name').value.trim();
      var point = document.getElementById('rp-point').value;
      var depth = document.getElementById('rp-depth').value;
      var desc = document.getElementById('rp-desc').value.trim();
      if (!name) { setStatus(reportStatus, 'Vui lòng nhập họ tên.', false); return; }
      var now = new Date();
      var time = ('0' + now.getDate()).slice(-2) + '/' + ('0' + (now.getMonth() + 1)).slice(-2) +
        '/2026 ' + ('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2);
      var items = loadReports();
      items.unshift({ name: name, point: point, depth: depth, desc: desc, time: time });
      if (items.length > 50) items = items.slice(0, 50);
      saveReports(items);
      renderReports();
      reportForm.reset();
      setStatus(reportStatus, '✔ Đã lưu báo cáo vào trình duyệt. Cảm ơn bạn đã chia sẻ!', true);
    });
    renderReports();
  }

  if (reportClear) {
    reportClear.addEventListener('click', function () {
      saveReports([]);
      renderReports();
      setStatus(reportStatus, 'Đã xoá toàn bộ báo cáo trên trình duyệt này.', true);
    });
  }
})();