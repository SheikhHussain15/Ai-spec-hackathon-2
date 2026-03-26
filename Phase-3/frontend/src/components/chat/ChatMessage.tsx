/**
 * ChatMessage Component
 *
 * Renders individual chat messages with clear user/assistant distinction.
 * Displays tool call confirmations for assistant messages.
 * Enhanced with Framer Motion for smooth entrance animations.
 * 
 * Responsive Design:
 * - Mobile (320-639px): Full-width message bubbles, optimized padding
 * - Tablet (768px+): Constrained max-width, balanced layout
 * - Desktop (1024px+): Fixed max-width for readability
 * 
 * Touch Targets: All interactive elements minimum 44x44px
 *
 * @feature 007-advanced-ux
 * @user-story US2: Smooth Animations & Micro-Interactions
 * @user-story US3: Responsive Design
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import { fadeIn, slideUp } from '@/lib/animations';

interface ToolCall {
  tool_name: string;
  arguments?: Record<string, any>;
  success?: boolean;
  result?: any;
  error?: string;
}

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  toolCalls?: ToolCall[];
  isLoading?: boolean;
}

export default function ChatMessage({
  role,
  content,
  timestamp,
  toolCalls,
  isLoading = false,
}: ChatMessageProps) {
  const isUser = role === 'user';

  const formatTime = (timestamp?: string) => {
    if (!timestamp) return '';
    return new Date(timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <motion.div
      initial="initial"
      animate="animate"
      variants={slideUp}
      className={clsx(
        'flex w-full mb-4',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={clsx(
          'rounded-2xl px-3 py-2.5 sm:px-4 sm:py-3 shadow-sm max-w-[90%] sm:max-w-[80%] lg:max-w-[70%]',
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-900'
        )}
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        ) : (
          <>
            <div className="text-sm leading-relaxed whitespace-pre-wrap sm:text-base">{content}</div>

            {/* Tool Calls Display */}
            {toolCalls && toolCalls.length > 0 && (
              <div className="mt-3 space-y-2">
                {toolCalls.map((toolCall, index) => (
                  <div
                    key={index}
                    className={clsx(
                      'text-xs rounded-lg p-2 border',
                      toolCall.success
                        ? 'bg-green-50 border-green-200 text-green-800'
                        : 'bg-red-50 border-red-200 text-red-800'
                    )}
                  >
                    <div className="font-medium">
                      {toolCall.tool_name}
                      {toolCall.success ? ' ✓' : ' ✗'}
                    </div>
                    {toolCall.arguments && (
                      <div className="mt-1 text-gray-600 break-all">
                        {JSON.stringify(toolCall.arguments, null, 2)}
                      </div>
                    )}
                    {toolCall.result && (
                      <div className="mt-1 text-gray-600 break-all">
                        Result: {JSON.stringify(toolCall.result, null, 2)}
                      </div>
                    )}
                    {toolCall.error && (
                      <div className="mt-1 text-red-600 break-all">Error: {toolCall.error}</div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Timestamp */}
            {timestamp && (
              <div
                className={clsx(
                  'text-xs mt-2',
                  isUser ? 'text-blue-100' : 'text-gray-500'
                )}
              >
                {formatTime(timestamp)}
              </div>
            )}
          </>
        )}
      </div>
    </motion.div>
  );
}
