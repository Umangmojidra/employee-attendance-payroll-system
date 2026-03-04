document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss toasts after 4.5s
  document.querySelectorAll('.toast').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    }, 4500);
  });

  // Animate KPI counters
  document.querySelectorAll('.kpi-val').forEach(function (el) {
    var raw = el.textContent.trim();
    var isP = raw.endsWith('%');
    var num = parseFloat(raw.replace('%','').replace(/[^0-9.]/g,''));
    if (isNaN(num) || num === 0) return;
    var start = Date.now(), dur = 900;
    (function tick() {
      var p = Math.min((Date.now()-start)/dur, 1);
      var e = 1 - Math.pow(1-p, 3);
      el.textContent = (num*e).toFixed(isP ? 1 : 0) + (isP ? '%' : '');
      if (p < 1) requestAnimationFrame(tick);
    })();
  });

  // Animate trend bars
  document.querySelectorAll('.bar-fill').forEach(function (el) {
    var h = el.style.height;
    el.style.height = '0%';
    setTimeout(function () {
      el.style.transition = 'height .6s ease';
      el.style.height = h;
    }, 150);
  });
});
