'use client'

import React from 'react'

export interface ContainerProps {
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  centered?: boolean
  className?: string
}

export default function Container({
  children,
  size = 'lg',
  centered = true,
  className = '',
}: ContainerProps) {
  // Base styles
  const baseStyles = 'w-full mx-auto px-4 sm:px-6 lg:px-8'
  
  // Size styles
  const sizeStyles = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full',
  }
  
  // Centered styles
  const centeredStyles = centered ? 'mx-auto' : ''
  
  // Combine classes
  const containerClasses = [
    baseStyles,
    sizeStyles[size],
    centeredStyles,
    className,
  ].filter(Boolean).join(' ')
  
  return (
    <div className={containerClasses}>
      {children}
    </div>
  )
}
