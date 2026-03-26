/**
 * Checkbox Component
 *
 * Animated checkbox with Framer Motion for smooth toggle interactions.
 * Features scale pulse animation on check/uncheck (200ms duration).
 *
 * @feature 007-advanced-ux
 * @user-story US2: Smooth Animations & Micro-Interactions
 * @accessibility WCAG 2.1 AA compliant with proper focus indicators
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { checkboxVariants } from '@/lib/animations';

export interface CheckboxProps {
  /** Whether the checkbox is checked */
  checked: boolean;
  /** Callback when checked state changes */
  onCheckedChange: (checked: boolean) => void;
  /** Disabled state */
  disabled?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Aria label for accessibility */
  'aria-label'?: string;
}

/**
 * Checkbox Component with animation
 * 
 * Features:
 * - Scale pulse animation on check (200ms)
 * - Smooth color transitions
 * - Visible focus indicator for accessibility
 * - Respects reduced motion preference
 */
export function Checkbox({
  checked,
  onCheckedChange,
  disabled = false,
  className = '',
  'aria-label': ariaLabel,
}: CheckboxProps) {
  return (
    <motion.button
      type="button"
      role="checkbox"
      aria-checked={checked}
      aria-label={ariaLabel}
      disabled={disabled}
      animate={checked ? 'checked' : 'unchecked'}
      variants={checkboxVariants}
      whileTap={{ scale: 0.95 }}
      onClick={() => !disabled && onCheckedChange(!checked)}
      className={`
        relative flex h-5 w-5 items-center justify-center 
        rounded border transition-colors duration-200
        focus-visible:outline-none focus-visible:ring-2 
        focus-visible:ring-primary-500 focus-visible:ring-offset-2
        disabled:cursor-not-allowed disabled:opacity-50
        ${
          checked
            ? 'border-primary-600 bg-primary-600 hover:border-primary-700 hover:bg-primary-700'
            : 'border-gray-300 bg-white hover:border-primary-500 hover:bg-primary-50'
        }
        ${className}
      `}
    >
      <motion.div
        initial={false}
        animate={{ opacity: checked ? 1 : 0, scale: checked ? 1 : 0.5 }}
        transition={{ duration: 0.15 }}
      >
        <Check className="h-3.5 w-3.5 text-white" strokeWidth={3} />
      </motion.div>
    </motion.button>
  );
}

export default Checkbox;
