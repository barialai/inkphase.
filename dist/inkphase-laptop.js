(() => {
  const video = document.getElementById('inkphase-hero-video');
  if (!video) return;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduceMotion.matches) {
    video.pause();
    return;
  }

  // The audio in this asset is already mixed to 50% of the supplied clip.
  // Browsers that permit audible autoplay will play it on each page load.
  video.volume = 1;
  video.muted = false;

  let awaitingGesture = false;
  const unlockAudio = async () => {
    if (!awaitingGesture) return;
    video.currentTime = 0;
    video.muted = false;
    try {
      await video.play();
      awaitingGesture = false;
      window.removeEventListener('pointerdown', unlockAudio, true);
      window.removeEventListener('keydown', unlockAudio, true);
    } catch {
      video.muted = true;
      video.play().catch(() => {});
    }
  };

  video.play().catch(() => {
    // A browser may reject sound before a visitor interacts with the page.
    // Keep the visual running and enable sound on the first interaction.
    video.muted = true;
    video.play().catch(() => {});
    awaitingGesture = true;
    window.addEventListener('pointerdown', unlockAudio, true);
    window.addEventListener('keydown', unlockAudio, true);
  });
  reduceMotion.addEventListener('change', event => {
    if (event.matches) video.pause();
  });
})();
