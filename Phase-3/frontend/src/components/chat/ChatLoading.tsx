/**
 * ChatLoading Component
 * 
 * Displays loading indicator while agent processes request.
 */

'use client';

import React from 'react';

export default function ChatLoading() {
  return (
    <div className="flex justify-start w-full mb-4">
      <div className="bg-gray-100 rounded-2xl px-4 py-3">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}
