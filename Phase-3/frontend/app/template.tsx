/**
 * Page Transition Template
 *
 * Wraps all pages with Framer Motion for smooth page transitions.
 * Uses the pageTransition variants from the animation library.
 * Respects user's reduced motion preference.
 *
 * @feature 007-advanced-ux
 * @user-story US2: Smooth Animations & Micro-Interactions
 * @accessibility Respects prefers-reduced-motion media query
 */

'use client';

import { motion } from 'framer-motion';
import { pageTransition, getMotionVariants, useReducedMotionPreference } from '@/lib/animations';

export default function Template({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotionPreference();
  const variants = getMotionVariants(shouldReduceMotion, pageTransition);

  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={variants}
    >
      {children}
    </motion.div>
  );
}
