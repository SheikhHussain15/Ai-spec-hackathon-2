'use client'

import React from 'react'

export interface GridProps {
  children: React.ReactNode
  columns?: 1 | 2 | 3 | 4 | 6 | 12
  gap?: 'sm' | 'md' | 'lg' | 'xl'
  responsive?: boolean
  className?: string
}

export default function Grid({
  children,
  columns = 1,
  gap = 'md',
  responsive = true,
  className = '',
}: GridProps) {
  // Base styles
  const baseStyles = 'grid'
  
  // Column styles
  const columnStyles = {
    1: 'grid-cols-1',
    2: 'grid-cols-2',
    3: 'grid-cols-3',
    4: 'grid-cols-4',
    6: 'grid-cols-6',
    12: 'grid-cols-12',
  }
  
  // Gap styles
  const gapStyles = {
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
    xl: 'gap-8',
  }
  
  // Responsive styles (mobile-first: 1 col → 2 cols → 3 cols → 4 cols)
  const responsiveStyles = responsive
    ? 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4'
    : columnStyles[columns]
  
  // Combine classes
  const gridClasses = [
    baseStyles,
    responsiveStyles,
    gapStyles[gap],
    className,
  ].filter(Boolean).join(' ')
  
  return (
    <div className={gridClasses}>
      {children}
    </div>
  )
}
