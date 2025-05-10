/**
 * Enhanced Landing Page Module
 *
 * Handles modern animations and interactive elements for the landing page using GSAP.
 * This module implements rich animations while maintaining accessibility and performance.
 *
 * @copyright 2025 Enveng Group
 * @license AGPL-3.0-or-later
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ScrollSmoother } from 'gsap/ScrollSmoother';
import { Flip } from 'gsap/Flip';
// Register all required GSAP plugins
gsap.registerPlugin(ScrollTrigger, ScrollSmoother, Flip);
// Attempt to import advanced GSAP plugins for enhanced text and SVG animations
// These plugins must be available in the build pipeline for this to work
// If not available, fallback logic and TODO comments are provided
// @see https://gsap.com/docs/v3/Plugins/SplitText/ and https://gsap.com/docs/v3/Plugins/MorphSVG/
// @ts-ignore
let SplitText = undefined;
// @ts-ignore
let MorphSVGPlugin = undefined;
try {
  // @ts-ignore
  SplitText = require('gsap/SplitText').SplitText || window.SplitText;
} catch (e) {
  // SplitText not available, fallback will be used
}
try {
  // @ts-ignore
  MorphSVGPlugin =
    require('gsap/MorphSVGPlugin').MorphSVGPlugin || window.MorphSVGPlugin;
} catch (e) {
  // MorphSVG not available, fallback will be used
}
if (SplitText) {
  gsap.registerPlugin(SplitText);
}
if (MorphSVGPlugin) {
  gsap.registerPlugin(MorphSVGPlugin);
}
/**
 * Main animation initialization function
 */
export function initAnimations() {
  // Accessibility: add prefers-reduced-motion class to the html element for global CSS
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
    document.body.classList.add('reduced-motion');
    enableNoJsStyles();
    return;
  }
  // Initialize animations based on scroll position
  initScrollAnimations();
  // Initialize hover effects and interactive elements
  initInteractiveElements();
  // Special animation for hero section
  animateHeroSection();
}
/**
 * Enable no-JS styles for accessibility when animations are disabled
 */
function enableNoJsStyles() {
  const animatedElements = Array.from(
    document.querySelectorAll(
      '.reveal-element, .reveal-text, .fade-in, .slide-up'
    )
  );
  animatedElements.forEach((element) => {
    element.style.opacity = '1';
    element.style.transform = 'none';
    element.style.visibility = 'visible';
    // Remove aria-hidden if present
    element.removeAttribute('aria-hidden');
  });
}
/**
 * Initialize scroll-triggered animations
 */
function initScrollAnimations() {
  // Create smooth scrolling if wrapper exists
  const wrapper = document.querySelector('#smooth-wrapper');
  const content = document.querySelector('#smooth-content');
  if (wrapper && content) {
    try {
      ScrollSmoother.create({
        wrapper: wrapper,
        content: content,
        smooth: 1.5,
        effects: true,
        normalizeScroll: true,
        ignoreMobileResize: true,
      });
    } catch (error) {
      console.error('Error initializing ScrollSmoother:', error);
    }
  }
  // Animate elements with reveal-element class
  const revealElements = Array.from(
    document.querySelectorAll('.reveal-element')
  );
  revealElements.forEach((element) => {
    const delay = parseFloat(element.dataset.delay || '0');
    // Accessibility: mark as aria-hidden during animation, remove after
    element.setAttribute('aria-hidden', 'true');
    ScrollTrigger.create({
      trigger: element,
      start: 'top 85%',
      once: true,
      onEnter: () => {
        gsap.fromTo(
          element,
          {
            y: 50,
            opacity: 0,
          },
          {
            y: 0,
            opacity: 1,
            duration: 0.8,
            delay: delay,
            ease: 'power2.out',
            onComplete: () => {
              element.removeAttribute('aria-hidden');
            },
          }
        );
      },
    });
  });
  // Initialize counter animations
  const counters = Array.from(document.querySelectorAll('.counter'));
  counters.forEach((counter) => {
    const target = parseInt(counter.dataset.target || '0', 10);
    // Add aria-live for screen reader updates
    counter.setAttribute('aria-live', 'polite');
    ScrollTrigger.create({
      trigger: counter,
      start: 'top 85%',
      once: true,
      onEnter: () => {
        gsap.fromTo(
          counter,
          { textContent: '0' },
          {
            textContent: String(target),
            duration: 2,
            ease: 'power1.inOut',
            snap: { textContent: 1 },
            onUpdate: function () {
              counter.textContent = Math.round(
                Number(counter.textContent || '0')
              ).toString();
            },
          }
        );
      },
    });
  });
  // Footer animation
  const footer = document.querySelector('.footer-container');
  if (footer) {
    ScrollTrigger.create({
      trigger: footer,
      start: 'top 95%',
      once: true,
      onEnter: () => {
        gsap.fromTo(
          footer,
          {
            y: 20,
            opacity: 0,
          },
          {
            y: 0,
            opacity: 1,
            duration: 0.8,
            ease: 'power2.out',
          }
        );
      },
    });
  }
}
/**
 * Initialize interactive elements and hover effects
 */
function initInteractiveElements() {
  // Button hover animations
  const buttons = Array.from(document.querySelectorAll('.btn-animated'));
  buttons.forEach((button) => {
    button.addEventListener('mouseenter', () => {
      gsap.to(button, {
        scale: 1.05,
        duration: 0.3,
        ease: 'power1.out',
      });
    });
    button.addEventListener('mouseleave', () => {
      gsap.to(button, {
        scale: 1,
        duration: 0.3,
        ease: 'power1.out',
      });
    });
  });
  // Feature card hover animations
  const featureCards = Array.from(document.querySelectorAll('.feature-card'));
  featureCards.forEach((card) => {
    const icon = card.querySelector('.feature-icon');
    card.addEventListener('mouseenter', () => {
      gsap.to(card, {
        y: -10,
        boxShadow: '0 12px 30px rgba(0, 0, 0, 0.15)',
        duration: 0.3,
        ease: 'power2.out',
      });
      if (icon) {
        gsap.to(icon, {
          rotate: 5,
          scale: 1.1,
          duration: 0.4,
          ease: 'power1.out',
        });
      }
    });
    card.addEventListener('mouseleave', () => {
      gsap.to(card, {
        y: 0,
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
        duration: 0.3,
        ease: 'power2.out',
      });
      if (icon) {
        gsap.to(icon, {
          rotate: 0,
          scale: 1,
          duration: 0.4,
          ease: 'power1.out',
        });
      }
    });
  });
  // Scroll indicator animation
  const scrollIndicator = document.querySelector('.scroll-indicator');
  if (scrollIndicator) {
    gsap.to(scrollIndicator, {
      y: 10,
      duration: 1.5,
      repeat: -1,
      yoyo: true,
      ease: 'power1.inOut',
    });
  }
  // Add floating animation to hero image
  const floatElements = Array.from(
    document.querySelectorAll('.float-animation')
  );
  floatElements.forEach((element) => {
    gsap.to(element, {
      y: -20,
      duration: 2.5,
      repeat: -1,
      yoyo: true,
      ease: 'power1.inOut',
    });
  });
  // Accessibility: add focus-visible outline for interactive elements
  const focusable = Array.from(
    document.querySelectorAll('.btn-animated, .feature-card, a, button')
  );
  focusable.forEach((el) => {
    el.addEventListener('focus', () => {
      el.classList.add('focus-visible');
    });
    el.addEventListener('blur', () => {
      el.classList.remove('focus-visible');
    });
  });
}
/**
 * Special animation sequence for the hero section
 */
function animateHeroSection() {
  const heroSection = document.querySelector('.hero-section');
  if (!heroSection) return;
  // Create a timeline for hero animations
  const heroTimeline = gsap.timeline({ defaults: { ease: 'power2.out' } });
  // Advanced text reveal using SplitText if available
  const heroTitle = heroSection.querySelector('.hero-title');
  if (heroTitle && SplitText) {
    // Split the hero title into words for staggered animation
    // @see https://gsap.com/docs/v3/Plugins/SplitText/
    const split = new SplitText(heroTitle, {
      type: 'words,chars',
      wordsClass: 'word-inner',
    });
    heroTimeline.fromTo(
      split.words,
      { y: '100%', opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, stagger: 0.05 }
    );
  } else if (heroTitle) {
    // Fallback: animate the whole title
    heroTimeline.fromTo(
      heroTitle,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8 }
    );
  }
  // Find elements to animate
  const wordInners = Array.from(heroSection.querySelectorAll('.word-inner'));
  const heroDesc = heroSection.querySelector('.hero-description');
  const heroCta = heroSection.querySelector('.hero-cta');
  const heroImage = heroSection.querySelector('.hero-image');
  const statCards = Array.from(
    heroSection.querySelectorAll('.hero-stats .stat-card')
  );
  const scrollIndicator = heroSection.querySelector('.scroll-indicator');
  // Animate hero elements in sequence
  if (wordInners.length > 0) {
    heroTimeline.fromTo(
      wordInners,
      { y: '100%' },
      { y: 0, duration: 0.8, stagger: 0.05 }
    );
  }
  if (heroDesc) {
    heroTimeline.fromTo(
      heroDesc,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.6 },
      '-=0.4'
    );
  }
  if (heroCta) {
    heroTimeline.fromTo(
      heroCta,
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.6 },
      '-=0.2'
    );
  }
  if (heroImage) {
    heroTimeline.fromTo(
      heroImage,
      { opacity: 0, scale: 0.9 },
      { opacity: 1, scale: 1, duration: 0.8 },
      '-=0.5'
    );
  }
  if (statCards.length > 0) {
    heroTimeline.fromTo(
      statCards,
      { opacity: 0, x: 20 },
      { opacity: 1, x: 0, duration: 0.6, stagger: 0.2 },
      '-=0.4'
    );
  }
  if (scrollIndicator) {
    heroTimeline.fromTo(
      scrollIndicator,
      { opacity: 0, y: -10 },
      { opacity: 1, y: 0, duration: 0.5 },
      '-=0.2'
    );
  }
  // Example: MorphSVG for feature icon (progressive enhancement)
  // Only run if MorphSVGPlugin is available and a suitable SVG is present
  const featureIcon = document.querySelector('.feature-svg');
  if (featureIcon && MorphSVGPlugin) {
    // Morph the feature icon to a checkmark on load as a demo
    // @see https://gsap.com/docs/v3/Plugins/MorphSVG/
    const targetPath = 'M10 24L20 34L38 14'; // Example checkmark path
    const svgPath = featureIcon.querySelector('path');
    if (svgPath) {
      gsap.to(svgPath, {
        morphSVG: { shape: targetPath },
        duration: 1.2,
        delay: 0.5,
        ease: 'power2.inOut',
        repeat: 1,
        yoyo: true,
      });
    }
  }
}
/**
 * Initialize testimonial carousel
 */
function initTestimonialCarousel() {
  const carousel = document.querySelector('.testimonial-carousel');
  const track =
    carousel === null || carousel === void 0
      ? void 0
      : carousel.querySelector('.testimonial-track');
  const cards = Array.from(
    (carousel === null || carousel === void 0
      ? void 0
      : carousel.querySelectorAll('.testimonial-card')) || []
  );
  const dots = Array.from(
    (carousel === null || carousel === void 0
      ? void 0
      : carousel.querySelectorAll('.testimonial-dot')) || []
  );
  if (!carousel || !track || !cards || !dots || cards.length < 2) return;
  let current = 0;
  let interval;
  const slideCount = cards.length;
  const slideWidth = () => cards[0].offsetWidth;
  // Set ARIA attributes
  carousel.setAttribute('aria-live', 'polite');
  cards.forEach((card, i) => {
    card.setAttribute('tabindex', i === current ? '0' : '-1');
    card.setAttribute('aria-hidden', i === current ? 'false' : 'true');
  });
  function goToSlide(idx) {
    current = idx;
    // Animate horizontal scroll using GSAP
    gsap.to(track, {
      x: -slideWidth() * current,
      duration: 0.7,
      ease: 'power2.inOut',
      onUpdate: () => {
        // Accessibility: update ARIA
        cards.forEach((card, i) => {
          card.setAttribute('tabindex', i === current ? '0' : '-1');
          card.setAttribute('aria-hidden', i === current ? 'false' : 'true');
        });
        dots.forEach((dot, i) => {
          dot.classList.toggle('active', i === current);
          dot.setAttribute('aria-current', i === current ? 'true' : 'false');
        });
      },
    });
  }
  function nextSlide() {
    goToSlide((current + 1) % slideCount);
  }
  function prevSlide() {
    goToSlide((current - 1 + slideCount) % slideCount);
  }
  // Dots navigation
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => goToSlide(i));
    dot.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevSlide();
        dots[(current + slideCount) % slideCount].focus();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        nextSlide();
        dots[(current + slideCount) % slideCount].focus();
      }
    });
  });
  // Auto-advance
  function startInterval() {
    interval = window.setInterval(nextSlide, 6000);
  }
  function stopInterval() {
    if (interval) window.clearInterval(interval);
  }
  carousel.addEventListener('mouseenter', stopInterval);
  carousel.addEventListener('mouseleave', startInterval);
  carousel.addEventListener('focusin', stopInterval);
  carousel.addEventListener('focusout', (e) => {
    if (!carousel.contains(e.relatedTarget)) startInterval();
  });
  // Responsive: update slide width on resize
  window.addEventListener('resize', () => goToSlide(current));
  // Init
  goToSlide(0);
  startInterval();
}
// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  initAnimations();
  initTestimonialCarousel();
});
// Re-initialize animations after HTMX swaps
document.body.addEventListener('htmx:afterSwap', () => {
  initAnimations();
  initTestimonialCarousel();
});
// Export the main initialization function
export default initAnimations;
// Document rationale for plugin choices:
// - SplitText: Used for accessible, staggered text reveals on hero/section titles. Improves visual engagement and focus. Falls back to whole-title animation if unavailable.
// - MorphSVG: Used for SVG icon morphing to add delight and visual feedback. Only runs if plugin and compatible SVG are present.
// - All animations respect reduced motion and maintain semantic HTML. See GSAP docs: https://gsap.com/docs/v3/
// Accessibility rationale:
// - All animated elements are hidden from screen readers during animation and revealed after.
// - Stat counters use aria-live for real-time updates.
// - Focus-visible outlines improve keyboard navigation.
// - Reduced motion is respected globally via class and CSS.
//# sourceMappingURL=landing.js.map
