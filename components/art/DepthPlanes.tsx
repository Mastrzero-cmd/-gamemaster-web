'use client';

import { useEffect } from 'react';

/**
 * Differential scroll motion for independent art planes.
 *
 * Every `.depthPlane` declares its own `--gm-depth` (px of travel per viewport)
 * in CSS: positive values lag behind the scroll (rear/blue planes), negative
 * values lead it (front/red planes). The engine only writes `--gm-shift`, so
 * mobile damping and reduced motion stay in the stylesheet.
 *
 * Positions are measured on mount/resize only; the frame loop is arithmetic,
 * which keeps scrolling free of layout thrash.
 */
export function DepthPlanes() {
  useEffect(() => {
    const root = document.documentElement;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
    let planes: HTMLElement[] = [];
    let state: { center: number; depth: number; current: number; target: number }[] = [];
    let frame = 0;

    const measure = () => {
      planes = Array.from(document.querySelectorAll<HTMLElement>('.depthPlane'));
      const scrollY = window.scrollY;
      state = planes.map((plane) => {
        const previous = Number.parseFloat(plane.style.getPropertyValue('--gm-shift')) || 0;
        const bounds = plane.getBoundingClientRect();
        const depth = Number.parseFloat(getComputedStyle(plane).getPropertyValue('--gm-depth')) || 0;
        return { center: bounds.top + scrollY + bounds.height / 2 - previous, depth, current: previous, target: previous };
      });
    };

    const retarget = () => {
      const viewport = window.innerHeight;
      const scrollY = window.scrollY;
      for (const plane of state) {
        const distance = (plane.center - scrollY - viewport / 2) / viewport;
        plane.target = -Math.max(-1.4, Math.min(1.4, distance)) * plane.depth;
      }
    };

    const tick = () => {
      frame = 0;
      retarget();
      let moving = false;
      state.forEach((plane, index) => {
        const delta = plane.target - plane.current;
        if (Math.abs(delta) > 0.05) {
          plane.current += delta * 0.12;
          moving = true;
        } else {
          plane.current = plane.target;
        }
        planes[index].style.setProperty('--gm-shift', `${plane.current.toFixed(2)}px`);
      });
      if (moving) frame = window.requestAnimationFrame(tick);
    };

    const wake = () => {
      if (reduce.matches || frame) return;
      frame = window.requestAnimationFrame(tick);
    };

    const reset = () => {
      if (frame) window.cancelAnimationFrame(frame);
      frame = 0;
      planes.forEach((plane) => plane.style.removeProperty('--gm-shift'));
      root.style.removeProperty('--gm-pointer-x');
      root.style.removeProperty('--gm-pointer-y');
    };

    const remeasure = () => {
      if (reduce.matches) return reset();
      measure();
      wake();
    };

    const handlePointer = (event: PointerEvent) => {
      if (reduce.matches || !finePointer.matches) return;
      root.style.setProperty('--gm-pointer-x', `${((event.clientX / window.innerWidth) - 0.5).toFixed(3)}`);
      root.style.setProperty('--gm-pointer-y', `${((event.clientY / window.innerHeight) - 0.5).toFixed(3)}`);
    };

    let resizeTimer = 0;
    const handleResize = () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(remeasure, 160);
    };

    const observer = new MutationObserver(handleResize);
    observer.observe(document.body, { childList: true, subtree: true });

    remeasure();
    window.addEventListener('scroll', wake, { passive: true });
    window.addEventListener('resize', handleResize);
    window.addEventListener('pointermove', handlePointer, { passive: true });
    window.addEventListener('load', remeasure);
    reduce.addEventListener('change', remeasure);

    return () => {
      reset();
      observer.disconnect();
      window.clearTimeout(resizeTimer);
      window.removeEventListener('scroll', wake);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('pointermove', handlePointer);
      window.removeEventListener('load', remeasure);
      reduce.removeEventListener('change', remeasure);
    };
  }, []);

  return null;
}
