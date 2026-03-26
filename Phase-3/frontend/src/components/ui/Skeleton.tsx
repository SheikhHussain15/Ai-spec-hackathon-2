'use client'

import React from 'react'
import Container from '../layout/Container'

export interface SkeletonProps {
  // Shape
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded'

  // Sizing
  width?: string | number
  height?: string | number
  lines?: number  // For text variant

  // Styling
  className?: string
  animation?: 'shimmer' | 'pulse' | 'none'
}

export default function Skeleton({
  variant = 'text',
  width,
  height,
  lines = 1,
  className = '',
  animation = 'shimmer',
}: SkeletonProps) {
  // Base styles
  const baseStyles = 'bg-gray-200'

  // Variant styles
  const variantStyles = {
    text: 'rounded',
    circular: 'rounded-full',
    rectangular: 'rounded',
    rounded: 'rounded-lg',
  }

  // Animation styles
  const animationStyles = {
    shimmer: 'animate-shimmer bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 bg-[length:1000px_100%]',
    pulse: 'animate-pulse',
    none: '',
  }

  // Inline styles
  const inlineStyles: React.CSSProperties = {}

  if (width) {
    inlineStyles.width = typeof width === 'string' ? width : `${width}px`
  }

  if (height) {
    inlineStyles.height = typeof height === 'string' ? height : `${height}px`
  }

  // Render multiple lines for text variant
  if (variant === 'text' && lines > 1) {
    return (
      <div className={`space-y-2 ${className}`}>
        {Array.from({ length: lines }).map((_, index) => (
          <div
            key={index}
            className={`${baseStyles} ${variantStyles[variant]} ${animationStyles[animation]}`}
            style={inlineStyles}
          />
        ))}
      </div>
    )
  }

  // Single element
  return (
    <div
      className={`${baseStyles} ${variantStyles[variant]} ${animationStyles[animation]} ${className}`}
      style={inlineStyles}
    />
  )
}

/**
 * TaskCardSkeleton Component
 *
 * Skeleton loader that matches the exact dimensions of TaskCard to prevent
 * Cumulative Layout Shift (CLS) during loading states.
 *
 * Visual structure matches TaskCard:
 * - Status badge placeholder at top
 * - Title line (prominent)
 * - Description lines (secondary)
 * - Metadata line (subtle)
 *
 * @feature 007-advanced-ux
 * @user-story US5: Loading States & Performance Feedback
 */
export function TaskCardSkeleton() {
  return (
    <li className="group relative rounded-xl border bg-white p-4 sm:p-5 shadow-sm">
      <div className="flex items-start gap-3 sm:gap-4">
        {/* Checkbox placeholder - matches 44x44px touch target */}
        <div className="mt-0.5 flex-shrink-0">
          <div className="min-w-[44px] min-h-[44px] flex items-center justify-center -ml-2">
            <Skeleton variant="circular" width="20px" height="20px" animation="pulse" />
          </div>
        </div>

        {/* Content - matches TaskCard visual hierarchy */}
        <div className="flex-1 min-w-0 space-y-2">
          {/* Status Badge placeholder */}
          <div className="flex items-center justify-between gap-2 flex-wrap">
            <Skeleton variant="rounded" width="80px" height="20px" animation="pulse" />
            
            {/* Action buttons placeholder (hidden on mobile, visible on desktop) */}
            <div className="hidden sm:flex items-center gap-1">
              <Skeleton variant="circular" width="36px" height="36px" animation="pulse" />
              <Skeleton variant="circular" width="36px" height="36px" animation="pulse" />
            </div>
          </div>

          {/* Title placeholder - PROMINENT (matches h3, text-base/sm:text-lg) */}
          <Skeleton variant="text" height="24px" animation="pulse" className="w-3/4" />

          {/* Description placeholder - SECONDARY (matches p, text-sm) */}
          <Skeleton variant="text" height="18px" lines={2} animation="pulse" className="w-full" />

          {/* Metadata placeholder - SUBTLE (matches text-xs) */}
          <div className="pt-1">
            <Skeleton variant="text" height="14px" width="120px" animation="pulse" />
          </div>
        </div>
      </div>
    </li>
  )
}

/**
 * DashboardSkeleton Component
 *
 * Full dashboard skeleton loader that matches the complete dashboard layout
 * to prevent Cumulative Layout Shift (CLS) during initial page load.
 *
 * Includes:
 * - Page header with title and logout button
 * - Dashboard controls (task count, action buttons)
 * - Multiple TaskCardSkeleton instances (3 cards by default)
 *
 * @feature 007-advanced-ux
 * @user-story US5: Loading States & Performance Feedback
 *
 * @param numberOfTasks - Number of task skeletons to display (default: 3)
 */
export interface DashboardSkeletonProps {
  numberOfTasks?: number
}

export function DashboardSkeleton({ numberOfTasks = 3 }: DashboardSkeletonProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Container size="xl">
        <div className="py-12">
          {/* Header skeleton - matches dashboard header layout */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <Skeleton variant="text" height="36px" width="200px" animation="pulse" />
                <Skeleton variant="text" height="20px" width="280px" animation="pulse" />
              </div>
              <Skeleton variant="rounded" height="40px" width="100px" animation="pulse" />
            </div>
          </div>

          {/* Dashboard controls skeleton */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
            <div className="space-y-2">
              <Skeleton variant="text" height="28px" width="160px" animation="pulse" />
              <Skeleton variant="text" height="18px" width="120px" animation="pulse" />
            </div>
            <div className="flex items-center gap-3">
              <Skeleton variant="rounded" height="40px" width="140px" animation="pulse" />
              <Skeleton variant="rounded" height="40px" width="120px" animation="pulse" />
            </div>
          </div>

          {/* Task list skeleton - multiple TaskCardSkeleton instances */}
          <div className="space-y-4">
            {Array.from({ length: numberOfTasks }).map((_, index) => (
              <TaskCardSkeleton key={index} />
            ))}
          </div>
        </div>
      </Container>
    </div>
  )
}
