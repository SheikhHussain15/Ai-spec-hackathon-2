/**
 * UI Components Index
 *
 * Central export point for all UI components
 * Import components from here for clean, consistent imports
 *
 * @example
 * ```tsx
 * import { Button, Input, Badge, IconButton } from '@/components/ui'
 * ```
 */

// Core UI Components
export { default as Button } from './Button'
export type { ButtonProps } from './Button'
export { buttonVariants } from './Button'

export { default as Input } from './Input'
export type { InputProps } from './Input'

export { default as Badge } from './Badge'
export type { BadgeProps } from './Badge'
export { badgeVariants } from './Badge'

export { default as Skeleton } from './Skeleton'
export type { SkeletonProps } from './Skeleton'
export { TaskCardSkeleton } from './Skeleton'
export { DashboardSkeleton } from './Skeleton'
export type { DashboardSkeletonProps } from './Skeleton'

export { default as Card } from './Card'
export type { CardProps } from './Card'

export { default as IconButton } from './IconButton'
export type { IconButtonProps } from './IconButton'
export { iconButtonVariants } from './IconButton'

export { default as Checkbox } from './Checkbox'
export type { CheckboxProps } from './Checkbox'

// Layout Components (re-exported from layout folder)
export { default as Container } from '../layout/Container'
export type { ContainerProps } from '../layout/Container'

export { default as Header } from '../layout/Header'
export type { HeaderProps } from '../layout/Header'

export { default as Grid } from '../layout/Grid'
export type { GridProps } from '../layout/Grid'
