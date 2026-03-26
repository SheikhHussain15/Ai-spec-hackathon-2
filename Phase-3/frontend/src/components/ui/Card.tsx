'use client'

import React from 'react'

export interface CardProps {
  // Content
  children: React.ReactNode
  title?: string
  description?: string
  
  // State
  clickable?: boolean
  selected?: boolean
  
  // Behavior
  onClick?: () => void
  
  // Styling
  className?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
}

export default function Card({
  children,
  title,
  description,
  clickable = false,
  selected = false,
  onClick,
  className = '',
  padding = 'md',
  shadow = 'md',
}: CardProps) {
  // Base styles
  const baseStyles = 'bg-white rounded-lg transition-all duration-normal'
  
  // Shadow styles
  const shadowStyles = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
  }
  
  // Clickable/Selected styles
  const interactiveStyles = clickable
    ? 'cursor-pointer hover:shadow-lg'
    : ''
  
  const selectedStyles = selected
    ? 'ring-2 ring-primary-500 border-primary-500'
    : 'border border-gray-200'
  
  // Padding styles
  const paddingStyles = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }
  
  // Combine classes
  const cardClasses = [
    baseStyles,
    shadowStyles[shadow],
    interactiveStyles,
    selectedStyles,
    paddingStyles[padding],
    className,
  ].filter(Boolean).join(' ')
  
  // Handle click
  const handleClick = () => {
    if (clickable && onClick) {
      onClick()
    }
  }
  
  return (
    <div
      className={cardClasses}
      onClick={handleClick}
      role={clickable ? 'button' : undefined}
      tabIndex={clickable ? 0 : undefined}
      onKeyDown={clickable ? (e) => {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
          e.preventDefault()
          onClick?.()
        }
      } : undefined}
    >
      {/* Title and Description */}
      {(title || description) && (
        <div className="mb-4">
          {title && (
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {title}
            </h3>
          )}
          {description && (
            <p className="text-sm text-gray-600">
              {description}
            </p>
          )}
        </div>
      )}
      
      {/* Content */}
      <div>
        {children}
      </div>
    </div>
  )
}
