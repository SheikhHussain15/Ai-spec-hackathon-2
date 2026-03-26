'use client'

import * as React from 'react'
import { type LucideIcon } from 'lucide-react'
import { AlertCircle, CheckCircle } from 'lucide-react'

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Label text for the input field */
  label: string
  /** Error message to display - shows error state when provided */
  error?: string
  /** Hint text to display below the input (hidden when error is present) */
  hint?: string
  /** Success message to display when field is valid (hidden when error is present) */
  successMessage?: string
  /** Success state - shows green border when field is valid */
  success?: boolean
  /** Icon to display on the left side of the input */
  leftIcon?: LucideIcon
  /** Custom element to display on the right side of the input (e.g., button, toggle) */
  rightElement?: React.ReactNode
}

/**
 * Input Component
 *
 * A flexible input field with label, error/hint/success messages, and icon slots.
 * Supports all standard HTML input attributes via spread props.
 *
 * @example
 * ```tsx
 * // Basic input
 * <Input label="Email" value={email} onChange={setEmail} />
 *
 * // Input with error
 * <Input
 *   label="Email"
 *   value={email}
 *   onChange={setEmail}
 *   error="Please enter a valid email"
 * />
 *
 * // Input with success state
 * <Input
 *   label="Email"
 *   value={email}
 *   onChange={setEmail}
 *   success
 *   successMessage="Email is valid"
 * />
 *
 * // Input with left icon
 * <Input
 *   label="Search"
 *   value={query}
 *   onChange={setQuery}
 *   leftIcon={Search}
 * />
 *
 * // Input with right element
 * <Input
 *   label="Password"
 *   type="password"
 *   value={password}
 *   onChange={setPassword}
 *   rightElement={<Button variant="ghost" size="icon">👁</Button>}
 * />
 * ```
 *
 * @feature 007-advanced-ux
 * @accessibility WCAG 2.1 AA compliant with ARIA labels and visible focus indicators
 */
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      hint,
      successMessage,
      success = false,
      leftIcon: LeftIcon,
      rightElement,
      className,
      id,
      disabled,
      'aria-describedby': ariaDescribedby,
      ...props
    },
    ref
  ) => {
    const inputId = id || label.toLowerCase().replace(/\s+/g, '-')
    const errorId = `${inputId}-error`
    const successId = `${inputId}-success`
    const hintId = `${inputId}-hint`
    
    // Build aria-describedby value based on what messages are shown
    const describedBy = [
      error ? errorId : null,
      success && successMessage ? successId : null,
      hint && !error && !successMessage ? hintId : null,
      ariaDescribedby
    ].filter(Boolean).join(' ') || undefined

    return (
      <div className="space-y-1.5">
        {/* Label */}
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700"
        >
          {label}
        </label>

        {/* Input wrapper */}
        <div className="relative">
          {/* Left Icon */}
          {LeftIcon && (
            <LeftIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          )}

          {/* Input Field */}
          <input
            ref={ref}
            id={inputId}
            aria-describedby={describedBy}
            aria-invalid={!!error}
            className={`
              w-full rounded-lg border bg-white px-3 py-2.5 text-sm
              transition-all duration-200
              placeholder:text-gray-400
              focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-1
              disabled:bg-gray-100 disabled:cursor-not-allowed
              ${LeftIcon ? 'pl-10' : ''}
              ${error
                ? 'border-error-500 focus:border-error-500 focus-visible:ring-error-200'
                : success
                  ? 'border-success-500 focus:border-success-500 focus-visible:ring-success-200'
                  : 'border-gray-300 focus:border-primary-500 focus-visible:ring-primary-200'
              }
              ${className}
            `}
            disabled={disabled}
            {...props}
          />

          {/* Right Element */}
          {rightElement && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2">
              {rightElement}
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <p
            id={errorId}
            role="alert"
            aria-live="assertive"
            className="text-sm text-error-600 flex items-center gap-1.5 font-medium"
          >
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            {error}
          </p>
        )}

        {/* Success Message (only shown when success state and no error) */}
        {success && successMessage && !error && (
          <p
            id={successId}
            role="status"
            aria-live="polite"
            className="text-sm text-success-600 flex items-center gap-1.5"
          >
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
            {successMessage}
          </p>
        )}

        {/* Hint Text (only shown when no error and no success message) */}
        {hint && !error && !successMessage && (
          <p
            id={hintId}
            className="text-sm text-gray-500"
          >
            {hint}
          </p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export default Input
