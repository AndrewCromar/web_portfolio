document.addEventListener('DOMContentLoaded', function() {
  var divs = document.querySelectorAll('.progressive-img');
  var i = 0;
  function loadNext() {
    if (i >= divs.length) return;
    var div = divs[i++];
    var thumb = div.querySelector('img');
    var fullSrc = thumb.src.replace('/thumbnails', '').replace('.jpg', '.png');
    var img = document.createElement('img');
    img.onload = function() {
      img.style.opacity = '1';
      loadNext();
    };
    img.onerror = loadNext;
    img.src = fullSrc;
    div.appendChild(img);
  }
  loadNext();
});
