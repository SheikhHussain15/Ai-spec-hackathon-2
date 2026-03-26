'use client'

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'

/**
 * Badge component variants using class-variance-authority
 * Supports status-based variants with consistent styling
 */
export const badgeVariants = cva(
  'inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors duration-200',
  {
    variants: {
      variant: {
        pending: 'bg-gray-100 text-gray-700',
        'in-progress': 'bg-primary-100 text-primary-700',
        completed: 'bg-success-100 text-success-700',
        error: 'bg-error-100 text-error-700',
      },
    },
    defaultVariants: {
      variant: 'pending',
    },
  }
)

export interface BadgeProps extends VariantProps<typeof badgeVariants> {
  /** Badge content */
  children: React.ReactNode
  /** Additional CSS classes */
  className?: string
  /** Optional icon to display before the text */
  icon?: React.ReactNode
}

/**
 * Badge Component
 *
 * A status indicator badge with color-coded variants for different states.
 * Commonly used for task status, notifications, and labels.
 *
 * @example
 * ```tsx
 * // Task status badges
 * <Badge variant="pending">Pending</Badge>
 * <Badge variant="in-progress">In Progress</Badge>
 * <Badge variant="completed">Completed</Badge>
 * <Badge variant="error">Error</Badge>
 *
 * // Badge with icon
 * <Badge variant="success" icon={<Check className="w-3 h-3" />}>
 *   Done
 * </Badge>
 * ```
 *
 * @feature 007-advanced-ux
 * @accessibility WCAG 2.1 AA compliant with sufficient color contrast
 */
export function Badge({ variant, children, className, icon: Icon }: BadgeProps) {
  return (
    <span className={badgeVariants({ variant, className })}>
      {Icon && <span className="shrink-0">{Icon}</span>}
      {children}
    </span>
  )
}

export default Badge
