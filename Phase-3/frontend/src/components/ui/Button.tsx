'use client'

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { motion, type HTMLMotionProps } from 'framer-motion'
import { Loader2 } from 'lucide-react'
import { buttonHover } from '@/lib/animations'

/**
 * Button component variants using class-variance-authority
 * Supports multiple variants, sizes, and states with consistent styling
 * 
 * Micro-interactions:
 * - Hover: subtle lift effect (150ms duration)
 * - Tap: press down effect (100ms duration)
 * - All transitions: 150-200ms for responsive feedback
 */
export const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center gap-2 rounded-lg font-medium ' +
  'transition-all duration-200 ease-out ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 ' +
  'disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed',
  {
    variants: {
      variant: {
        primary:
          'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800 shadow-sm hover:shadow',
        secondary:
          'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 active:bg-gray-100',
        destructive:
          'bg-error-600 text-white hover:bg-error-700 active:bg-error-800 shadow-sm hover:shadow',
        ghost: 'text-gray-700 hover:bg-gray-100 active:bg-gray-200',
        link: 'text-primary-600 hover:underline active:text-primary-800',
      },
      size: {
        sm: 'h-9 px-3 text-sm min-w-[44px]',
        md: 'h-10 px-4 text-base min-w-[44px]',
        lg: 'h-12 px-6 text-lg min-w-[44px]',
        icon: 'h-10 w-10',
      },
      loading: {
        true: 'pointer-events-none',
      },
      fullWidth: {
        true: 'w-full',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

export interface ButtonProps
  extends Omit<HTMLMotionProps<'button'>, 'ref'>,
    VariantProps<typeof buttonVariants> {
  /** Optional icon to display before children (Lucide icon or any React node) */
  icon?: React.ReactNode
  /** Loading state - shows spinner and disables button */
  loading?: boolean
  /** Button content */
  children?: React.ReactNode
  /** Make button full width */
  fullWidth?: boolean
}

/**
 * Button Component
 *
 * A flexible button component with multiple variants, sizes, and states.
 * Built with class-variance-authority for type-safe variant management.
 * Enhanced with Framer Motion for smooth micro-interactions.
 *
 * @example
 * ```tsx
 * // Primary button
 * <Button variant="primary" size="md">Create Task</Button>
 *
 * // Button with icon
 * <Button variant="destructive" icon={Trash2}>Delete</Button>
 *
 * // Loading button
 * <Button variant="secondary" loading>Saving...</Button>
 *
 * // Icon-only button
 * <Button variant="ghost" size="icon" aria-label="Edit task">
 *   <Edit2 className="w-5 h-5" />
 * </Button>
 * ```
 *
 * @feature 007-advanced-ux
 * @accessibility WCAG 2.1 AA compliant with visible focus indicators
 */
export function Button({
  className,
  variant,
  size,
  icon: Icon,
  loading,
  fullWidth,
  children,
  ...props
}: ButtonProps) {
  return (
    <motion.button
      className={buttonVariants({ variant, size, loading, fullWidth, className })}
      disabled={loading || props.disabled}
      whileHover={!loading && !props.disabled ? 'hover' : undefined}
      whileTap={!loading && !props.disabled ? 'tap' : undefined}
      variants={buttonHover}
      {...props}
    >
      {loading && <Loader2 className="w-4 h-4 animate-spin" />}
      {!loading && Icon}
      {children}
    </motion.button>
  );
}

export default Button;
