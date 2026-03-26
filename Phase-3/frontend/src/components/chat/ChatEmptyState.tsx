/**
 * ChatEmptyState Component
 *
 * Displays welcoming empty state for new users with example prompts.
 * 
 * Responsive Design:
 * - Mobile (320-639px): Full-width example buttons, optimized padding
 * - Tablet (768px+): Constrained max-width, balanced layout
 * - Desktop (1024px+): Fixed max-width for readability
 * 
 * Touch Targets: Example buttons minimum 44x44px
 *
 * @feature 007-advanced-ux
 * @user-story US3: Responsive Design
 */

'use client';

import React from 'react';
import { MessageSquare, Lightbulb } from 'lucide-react';

interface ChatEmptyStateProps {
  onExampleClick?: (example: string) => void;
}

const EXAMPLE_PROMPTS = [
  "Add a task to review the project docs tomorrow",
  "What tasks do I have?",
  "Mark my first task as complete",
  "Create a task for the team meeting",
];

export default function ChatEmptyState({ onExampleClick }: ChatEmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4 py-8 sm:py-12">
      <div className="w-14 h-14 sm:w-16 sm:h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
        <MessageSquare className="w-7 h-7 sm:w-8 sm:h-8 text-blue-600" />
      </div>

      <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2 px-2">
        Welcome to AI Task Assistant
      </h2>

      <p className="text-gray-600 mb-6 max-w-md text-sm sm:text-base px-4">
        I can help you manage your tasks through natural conversation.
        Just ask me to create, list, complete, or update your tasks!
      </p>

      <div className="w-full max-w-md px-2">
        <div className="flex items-center space-x-2 mb-3">
          <Lightbulb className="w-4 h-4 text-gray-400" />
          <span className="text-sm font-medium text-gray-500">Try these examples:</span>
        </div>

        <div className="space-y-2">
          {EXAMPLE_PROMPTS.map((example, index) => (
            <button
              key={index}
              onClick={() => onExampleClick?.(example)}
              className="w-full text-left p-3 sm:p-4 bg-gray-50 hover:bg-gray-100 rounded-xl text-sm sm:text-base text-gray-700 transition-colors min-h-[48px] sm:min-h-[52px]"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
