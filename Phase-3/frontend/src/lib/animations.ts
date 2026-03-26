/**
 * Animation Variants Library
 *
 * Centralized Framer Motion animation variants for consistent animations
 * across the application.
 *
 * @feature 007-advanced-ux
 */

import { Variants } from 'framer-motion';
import { useReducedMotion } from 'framer-motion';

/**
 * Custom hook for reduced motion preference
 * Returns true if user prefers reduced motion
 * 
 * @example
 * ```tsx
 * const shouldReduceMotion = useReducedMotionPreference();
 * const variants = shouldReduceMotion ? disabledVariants : pageTransition;
 * ```
 */
export function useReducedMotionPreference(): boolean {
  const shouldReduceMotion = useReducedMotion();
  return shouldReduceMotion ?? false;
}

/**
 * Disabled animation variants for reduced motion preference
 * These variants skip all animations for accessibility
 */
export const disabledAnimationVariants: Variants = {
  initial: {
    opacity: 1,
    x: 0,
    y: 0,
    scale: 1,
  },
  animate: {
    opacity: 1,
    x: 0,
    y: 0,
    scale: 1,
    transition: { duration: 0 },
  },
  exit: {
    opacity: 0,
    x: 0,
    y: 0,
    scale: 1,
    transition: { duration: 0 },
  },
};

/**
 * Page transition animation
 * Used for smooth page-to-page transitions
 * 
 * Reduced motion: Instant transition without animation
 */
export const pageTransition: Variants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.25,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.2,
    },
  },
};

/**
 * Fade in animation
 * Simple opacity transition for subtle appearances
 * 
 * Reduced motion: Instant appearance
 */
export const fadeIn: Variants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: { duration: 0.2 },
  },
};

/**
 * Slide up animation
 * Content slides up from below with fade in
 * 
 * Reduced motion: Instant appearance without movement
 */
export const slideUp: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.25, ease: 'easeOut' },
  },
};

/**
 * List item variants for staggered animations
 * Use with AnimatePresence for smooth list transitions
 * 
 * Reduced motion: Instant appearance without stagger delay
 * 
 * @example
 * ```tsx
 * {items.map((item, index) => (
 *   <motion.div
 *     key={item.id}
 *     variants={listItemVariants}
 *     custom={index}
 *   >
 *     <ItemComponent />
 *   </motion.div>
 * ))}
 * ```
 */
export const listItemVariants: Variants = {
  hidden: {
    opacity: 0,
    x: -20,
  },
  visible: (i: number) => ({
    opacity: 1,
    x: 0,
    transition: {
      delay: i * 0.05,
      duration: 0.2,
      ease: 'easeOut',
    },
  }),
  exit: {
    opacity: 0,
    x: 20,
    transition: { duration: 0.2 },
  },
};

/**
 * Scale in animation
 * Content scales from 95% to 100% with fade in
 * 
 * Reduced motion: Instant appearance at full size
 */
export const scaleIn: Variants = {
  initial: {
    opacity: 0,
    scale: 0.95,
  },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.2, ease: 'easeOut' },
  },
};

/**
 * Checkbox animation variants
 * Subtle pulse effect on check/uncheck
 * 
 * Reduced motion: No pulse animation
 */
export const checkboxVariants = {
  checked: {
    scale: [1, 1.2, 1],
    transition: { duration: 0.2 },
  },
  unchecked: {
    scale: 1,
  },
};

/**
 * Button hover animation
 * Subtle lift effect on hover
 * 
 * Reduced motion: No hover animation
 */
export const buttonHover: Variants = {
  hover: {
    y: -2,
    transition: { duration: 0.15 },
  },
  tap: {
    y: 0,
    transition: { duration: 0.1 },
  },
};

/**
 * Reduced motion variants helper
 * Returns appropriate variants based on motion preference
 * 
 * @param shouldReduceMotion - Whether to reduce motion
 * @param normalVariants - Normal animation variants
 * @returns Appropriate variants for motion preference
 */
export function getMotionVariants(
  shouldReduceMotion: boolean,
  normalVariants: Variants
): Variants {
  if (shouldReduceMotion) {
    return disabledAnimationVariants;
  }
  return normalVariants;
}
