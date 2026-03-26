'use client'

import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { type LucideIcon } from 'lucide-react'

/**
 * IconButton component variants using class-variance-authority
 * Supports multiple variants and sizes for icon-only buttons
 */
export const iconButtonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-lg font-medium ' +
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
        sm: 'h-8 w-8',
        md: 'h-10 w-10',
        lg: 'h-12 w-12',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'ghost',
      size: 'md',
    },
  }
)

export interface IconButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof iconButtonVariants> {
  /** Lucide React icon component to render */
  icon: LucideIcon
  /** Tooltip text to display on hover (for accessibility) */
  tooltip?: string
  /** Loading state - shows spinner and disables button */
  loading?: boolean
}

/**
 * IconButton Component
 *
 * A button component designed for icon-only actions.
 * Includes built-in tooltip support for accessibility.
 *
 * @example
 * ```tsx
 * // Basic icon button
 * <IconButton icon={Edit2} aria-label="Edit task" />
 *
 * // With tooltip
 * <IconButton
 *   icon={Trash2}
 *   tooltip="Delete task"
 *   aria-label="Delete task"
 * />
 *
 * // Different variants
 * <IconButton icon={Plus} variant="primary" size="md" />
 * <IconButton icon={Trash2} variant="destructive" size="sm" />
 *
 * // Loading state
 * <IconButton icon={Save} loading aria-label="Saving" />
 * ```
 *
 * @feature 007-advanced-ux
 * @accessibility WCAG 2.1 AA compliant - always provide aria-label
 */
export function IconButton({
  className,
  variant,
  size,
  icon: Icon,
  tooltip,
  loading,
  'aria-label': ariaLabel,
  ...props
}: IconButtonProps) {
  // Create a unique ID for the tooltip
  const tooltipId = `tooltip-${Math.random().toString(36).substr(2, 9)}`

  return (
    <>
      <button
        className={iconButtonVariants({ variant, size, className })}
        aria-label={ariaLabel || tooltip}
        aria-describedby={tooltip ? tooltipId : undefined}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading ? (
          <div className="relative">
            <Icon className="h-5 w-5 opacity-50" />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="h-3 w-3 animate-spin rounded-full border-2 border-current border-t-transparent" />
            </div>
          </div>
        ) : (
          <Icon className="h-5 w-5" />
        )}
      </button>

      {/* Tooltip */}
      {tooltip && (
        <div
          id={tooltipId}
          role="tooltip"
          className="pointer-events-none absolute z-50 px-2 py-1 text-xs font-medium text-white bg-gray-900 rounded-md opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 -translate-y-8 left-1/2 -translate-x-1/2 whitespace-nowrap"
        >
          {tooltip}
          {/* Tooltip arrow */}
          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900" />
        </div>
      )}
    </>
  )
}

export default IconButton
