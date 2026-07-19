/* Braluma Apple-Inspired Motion & Dynamic Image Sequence Sticky Scroll */
document.addEventListener('DOMContentLoaded', () => {
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Lenis Smooth Scroll Setup
  let lenis = null;

  if (!isReducedMotion && typeof Lenis !== 'undefined') {
    lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 1.8,
    });

    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);

      lenis.on('scroll', ScrollTrigger.update);

      gsap.ticker.add((time) => {
        lenis.raf(time * 1000);
      });

      gsap.ticker.lagSmoothing(0);
    }
  }

  // 2. Apple-Style Hero Entrance Animation (Subtle Scale 0.96 -> 1.0 & Opacity 0 -> 1)
  if (typeof gsap !== 'undefined' && !isReducedMotion) {
    const heroStack = document.querySelector('.hero-content-stack');
    const heroMirrorStage = document.querySelector('.hero-mirror-stage');

    if (heroStack) {
      gsap.fromTo(
        heroStack,
        { opacity: 0, scale: 0.96, y: 15 },
        { opacity: 1, scale: 1, y: 0, duration: 1.2, ease: 'power3.out', delay: 0.1 }
      );
    }

    if (heroMirrorStage) {
      gsap.fromTo(
        heroMirrorStage,
        { opacity: 0, scale: 0.95 },
        { opacity: 1, scale: 1, duration: 1.4, ease: 'power3.out', delay: 0.3 }
      );
    }
  }

  // 3. Apple-Style Pinned Sticky Product Feature Scroll with Synchronized Image Sequence (#destacado-sticky)
  const stickySection = document.querySelector('#destacado-sticky');
  const stepCards = document.querySelectorAll('.sticky-step-card');
  const dynamicImgs = document.querySelectorAll('.sticky-dynamic-img');

  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined' && stickySection && !isReducedMotion && stepCards.length > 0) {
    
    ScrollTrigger.create({
      trigger: stickySection,
      start: 'top top',
      end: '+=2400',
      pin: true,
      scrub: 0.6,
      onUpdate: (self) => {
        const progress = self.progress; // 0.0 to 1.0
        
        // Calculate current step index (0, 1, 2, 3)
        let activeIdx = Math.min(stepCards.length - 1, Math.floor(progress * stepCards.length));
        
        // 1. Synchronize Active Text Card
        stepCards.forEach((card, idx) => {
          if (idx === activeIdx) {
            card.classList.add('active');
          } else {
            card.classList.remove('active');
          }
        });

        // 2. Synchronize Active Image in Frame with Crossfade Transition
        dynamicImgs.forEach((img, idx) => {
          if (idx === activeIdx) {
            img.classList.add('active');
          } else {
            img.classList.remove('active');
          }
        });
      }
    });
  }

  // 4. Smooth Anchor Link Scrolling
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElem = document.querySelector(targetId);
        if (targetElem) {
          e.preventDefault();
          if (lenis) {
            lenis.scrollTo(targetElem);
          } else {
            targetElem.scrollIntoView({ behavior: 'smooth' });
          }
        }
      }
    });
  });
});
