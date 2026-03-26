/**
 * ChatInput Component
 *
 * Input field for sending chat messages.
 * Prevents empty messages and provides send button.
 * 
 * Responsive Design:
 * - Mobile (320-639px): Full-width input, touch-friendly send button
 * - Tablet (768px+): Constrained width, optimized spacing
 * - Desktop (1024px+): Fixed max-width layout
 * 
 * Touch Targets: Send button minimum 44x44px
 *
 * @feature 007-advanced-ux
 * @user-story US3: Responsive Design
 */

'use client';

import React, { useState } from 'react';
import { Send } from 'lucide-react';
import { clsx } from 'clsx';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export default function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Type your message...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSend(trimmedMessage);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex items-end space-x-2 bg-white border border-gray-300 rounded-2xl p-2 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-200 transition-all">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          className={clsx(
            'flex-1 resize-none px-3 py-2 outline-none text-gray-900 placeholder-gray-500 text-sm sm:text-base',
            'max-h-32 min-h-[44px]',
            'disabled:opacity-50 disabled:cursor-not-allowed'
          )}
          style={{ fieldSizing: 'content' } as React.CSSProperties}
        />
        <button
          type="submit"
          disabled={!message.trim() || disabled}
          className={clsx(
            'flex-shrink-0 min-w-[44px] min-h-[44px] p-2.5 sm:p-3 rounded-xl transition-all duration-200 flex items-center justify-center',
            message.trim() && !disabled
              ? 'bg-blue-600 text-white hover:bg-blue-700 active:scale-95'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          )}
          aria-label="Send message"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </form>
  );
}
