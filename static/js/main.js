/* Braluma Main Frontend JavaScript */
document.addEventListener('DOMContentLoaded', () => {
  // Product Detail Gallery Thumbnail Selector
  const mainImage = document.getElementById('main-gallery-image');
  const thumbs = document.querySelectorAll('.thumb-item');

  if (mainImage && thumbs.length > 0) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');

        const newSrc = thumb.getAttribute('data-full');
        const newAlt = thumb.getAttribute('data-alt');

        if (newSrc) {
          mainImage.style.opacity = '0.4';
          setTimeout(() => {
            mainImage.src = newSrc;
            if (newAlt) mainImage.alt = newAlt;
            mainImage.style.opacity = '1';
          }, 150);
        }
      });
    });
  }

  // Kelvin Dial Visual Marker positioning helper
  const kelvinTracks = document.querySelectorAll('.kelvin-track-bar');
  kelvinTracks.forEach(track => {
    const minK = parseInt(track.getAttribute('data-min') || '3000', 10);
    const maxK = parseInt(track.getAttribute('data-max') || '6500', 10);
    
    // Scale domain: 2700K (0%) to 6500K (100%)
    const globalMin = 2700;
    const globalMax = 6500;
    const totalRange = globalMax - globalMin;

    const leftPercent = Math.max(0, Math.min(100, ((minK - globalMin) / totalRange) * 100));
    const rightPercent = Math.max(0, Math.min(100, ((globalMax - maxK) / totalRange) * 100));
    const widthPercent = 100 - leftPercent - rightPercent;

    const highlight = track.querySelector('.kelvin-marker-highlight');
    if (highlight) {
      highlight.style.left = `${leftPercent}%`;
      highlight.style.width = `${Math.max(5, widthPercent)}%`;
    }
  });
});
