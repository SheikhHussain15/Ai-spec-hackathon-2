/**
 * ChatError Component
 *
 * Displays error message with retry option.
 * 
 * Responsive Design:
 * - Mobile (320-639px): Full-width error container, touch-friendly retry button
 * - Tablet+ (768px+): Constrained max-width
 * 
 * Touch Targets: Retry button minimum 44x44px
 *
 * @feature 007-advanced-ux
 * @user-story US3: Responsive Design
 */

'use client';

import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ChatErrorProps {
  message?: string;
  onRetry?: () => void;
}

export default function ChatError({
  message = 'Something went wrong. Please try again.',
  onRetry,
}: ChatErrorProps) {
  return (
    <div className="flex justify-center w-full mb-4">
      <div className="bg-red-50 border border-red-200 rounded-2xl px-4 py-3 max-w-sm sm:max-w-md w-full mx-2 sm:mx-0">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1 min-w-0">
            <p className="text-sm text-red-800 break-words">{message}</p>
            {onRetry && (
              <button
                onClick={onRetry}
                className="mt-2 flex items-center space-x-1 text-sm text-red-600 hover:text-red-800 transition-colors min-h-[44px] min-w-[44px] px-3 -ml-2"
                aria-label="Retry last action"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Retry</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
