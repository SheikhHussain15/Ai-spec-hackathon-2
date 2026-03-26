'use client'

import React from 'react'

export interface HeaderProps {
  title: string
  subtitle?: string
  actions?: React.ReactNode
  onBack?: () => void
  className?: string
}

export default function Header({
  title,
  subtitle,
  actions,
  onBack,
  className = '',
}: HeaderProps) {
  return (
    <header className={`w-full ${className}`}>
      <div className="flex items-center justify-between">
        {/* Title section */}
        <div className="flex items-center space-x-3">
          {/* Back button */}
          {onBack && (
            <button
              onClick={onBack}
              className="p-2 -ml-2 rounded-md text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors duration-normal focus:outline-none focus:ring-2 focus:ring-primary-500"
              aria-label="Go back"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
          )}
          
          {/* Title and subtitle */}
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {title}
            </h1>
            {subtitle && (
              <p className="mt-1 text-sm text-gray-600">
                {subtitle}
              </p>
            )}
          </div>
        </div>
        
        {/* Actions */}
        {actions && (
          <div className="flex items-center space-x-2">
            {actions}
          </div>
        )}
      </div>
    </header>
  )
}
