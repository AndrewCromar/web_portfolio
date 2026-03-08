document.addEventListener('DOMContentLoaded', function() {
  var imgs = document.querySelectorAll('.progressive-img img[data-src]');
  var i = 0;
  function loadNext() {
    if (i >= imgs.length) return;
    var img = imgs[i++];
    img.onload = function() {
      img.style.opacity = '1';
      loadNext();
    };
    img.onerror = loadNext;
    img.src = img.getAttribute('data-src');
  }
  loadNext();
});
