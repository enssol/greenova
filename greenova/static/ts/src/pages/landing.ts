/**
 * Landing Page Module
 *
 * Handles animations and interactions for the landing page using GSAP.
 */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ScrollSmoother } from 'gsap/ScrollSmoother';
import { Flip } from 'gsap/Flip';

// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger, ScrollSmoother, Flip);

interface AnimationConfig {
  duration: number;
  ease: string;
  delay?: number;
}

interface NewsletterForm extends HTMLFormElement {
  email: HTMLInputElement;
  querySelector(selectors: string): HTMLElement | null;
}

export function initAnimations(): void {
  // Initialize lazy loading for images
  const lazyImages = document.querySelectorAll<HTMLImageElement>('img[loading="lazy"]');
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('loading');
            imageObserver.unobserve(img);
          }
        }
      });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
  }

  // Initialize fade-in animations
  gsap.utils.toArray<HTMLElement>('.fade-in').forEach((element) => {
    ScrollTrigger.create({
      trigger: element,
      start: 'top 85%',
      once: true,
      onEnter: () => {
        const config: AnimationConfig = {
          duration: 0.6,
          ease: 'power2.out',
          delay: element.classList.contains('stagger-1') ? 0 :
                 element.classList.contains('stagger-2') ? 0.15 :
                 element.classList.contains('stagger-3') ? 0.3 :
                 element.classList.contains('stagger-4') ? 0.45 : 0
        };

        gsap.fromTo(element,
          {
            y: 50,
            opacity: 0
          },
          {
            y: 0,
            opacity: 1,
            ...config
          }
        );
      }
    });
  });

  // Initialize smooth scrolling
  const mainContent = document.querySelector<HTMLElement>('#main-content');
  if (mainContent) {
    ScrollSmoother.create({
      wrapper: mainContent,
      content: 'main',
      smooth: 1,
      effects: true
    });
  }

  // Initialize interactive elements
  setupInteractiveElements();
}

function setupInteractiveElements(): void {
  // Logo hover effect
  const logo = document.querySelector<HTMLElement>('.hero-logo');
  if (logo) {
    const logoTimeline = gsap.timeline({ paused: true });
    logoTimeline.to(logo, {
      scale: 1.1,
      duration: 0.3,
      ease: 'power2.out'
    });

    logo.addEventListener('mouseenter', () => {
      logoTimeline.play();
    });

    logo.addEventListener('mouseleave', () => {
      logoTimeline.reverse();
    });
  }

  // Scroll indicator animation
  const scrollIndicator = document.querySelector<HTMLElement>('.scroll-indicator');
  if (scrollIndicator) {
    gsap.to(scrollIndicator, {
      y: 10,
      duration: 1,
      repeat: -1,
      yoyo: true,
      ease: 'power1.inOut'
    });

    scrollIndicator.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = scrollIndicator.getAttribute('href');
      if (targetId) {
        const target = document.querySelector<HTMLElement>(targetId);
        target?.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  }

  // Feature card hover effects
  gsap.utils.toArray<HTMLElement>('.feature-card').forEach(card => {
    const cardTimeline = gsap.timeline({ paused: true });
    const icon = card.querySelector<HTMLElement>('.feature-icon');

    if (icon) {
      cardTimeline
        .to(card, {
          y: -10,
          duration: 0.3,
          ease: 'power2.out'
        })
        .to(icon, {
          scale: 1.1,
          duration: 0.2,
          ease: 'back.out'
        }, 0);

      card.addEventListener('mouseenter', () => {
        cardTimeline.play();
      });

      card.addEventListener('mouseleave', () => {
        cardTimeline.reverse();
      });
    }
  });

  // Newsletter form interaction
  const newsletterForm = document.querySelector<NewsletterForm>('.newsletter-form form');
  if (newsletterForm) {
    newsletterForm.addEventListener('htmx:beforeRequest', () => {
      const button = newsletterForm.querySelector('.newsletter-submit') as HTMLButtonElement | null;
      if (button) {
        button.disabled = true;
      }
    });

    newsletterForm.addEventListener('htmx:afterRequest', () => {
      const button = newsletterForm.querySelector('.newsletter-submit') as HTMLButtonElement | null;
      if (button) {
        button.disabled = false;
      }
    });
  }
}

// Handle theme changes
document.addEventListener('themeChanged', ((e: CustomEvent<{ theme: string }>) => {
  updateThemeAnimations(e.detail.theme);
}) as EventListener);

function updateThemeAnimations(theme: string): void {
  const isDark = theme === 'dark';
  const shadowColor = isDark ? 'rgba(0, 0, 0, 0.3)' : 'rgba(47, 70, 36, 0.07)';

  gsap.utils.toArray<HTMLElement>('.feature-card, .stat-item').forEach(element => {
    gsap.to(element, {
      boxShadow: `0 2px 16px 0 ${shadowColor}`,
      duration: 0.3,
      ease: 'power2.out'
    });
  });
}

// Initialize animations
function init(): void {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnimations);
  } else {
    initAnimations();
  }
}

// Re-initialize on HTMX content swaps
document.body.addEventListener('htmx:afterSwap', () => {
  initAnimations();
});

// Export initialization function
export default init;
