/**
 * Chat Page
 * 
 * Protected route for AI chat interface.
 * Integrates with backend chat endpoint.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ChatMessage from '@/components/chat/ChatMessage';
import ChatInput from '@/components/chat/ChatInput';
import { getCurrentUserId, getAuthToken } from '@/lib/auth';
import { MessageSquare } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  toolCalls?: any[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const STORAGE_KEY = 'chat_conversation_id';

export default function ChatPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check authentication on mount
  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.push('/login');
      return;
    }

    const uid = getCurrentUserId();
    if (!uid) {
      router.push('/login');
      return;
    }

    setUserId(uid);

    // Load saved conversation ID
    const savedConversationId = localStorage.getItem(STORAGE_KEY);
    if (savedConversationId) {
      setConversationId(savedConversationId);
      fetchConversationHistory(savedConversationId, uid, token);
    }
  }, [router]);

  const fetchConversationHistory = async (
    convId: string,
    uid: string,
    token: string
  ) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/${uid}/conversations/${convId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.messages) {
          setMessages(
            data.messages.map((msg: any) => ({
              role: msg.role as 'user' | 'assistant',
              content: msg.content,
              timestamp: msg.created_at,
              toolCalls: msg.tool_calls?.calls || [],
            }))
          );
        }
      }
    } catch (error) {
      console.error('Failed to fetch conversation history:', error);
    }
  };

  const sendMessage = async (content: string) => {
    if (!userId || !content.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const token = getAuthToken();
      const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: content,
          conversation_id: conversationId || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      // Save conversation ID for future requests
      if (data.conversation_id) {
        localStorage.setItem(STORAGE_KEY, data.conversation_id);
        setConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        toolCalls: data.tool_calls || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  const retryLastMessage = async () => {
    const lastUserMessage = messages[messages.length - 1];
    if (lastUserMessage && lastUserMessage.role === 'user') {
      // Remove the last user message and retry
      setMessages((prev) => prev.slice(0, -1));
      await sendMessage(lastUserMessage.content);
    }
  };

  if (!userId) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-3 sm:px-4 py-3 flex items-center space-x-3">
        <div className="w-8 h-8 sm:w-10 sm:h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
          <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
        </div>
        <div className="min-w-0 flex-1">
          <h1 className="text-base sm:text-lg font-semibold text-gray-900 truncate">AI Task Assistant</h1>
          {conversationId && (
            <p className="text-xs text-gray-500 hidden sm:block">Conversation active</p>
          )}
        </div>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto px-3 sm:px-4 py-4 sm:py-6">
        <div className="max-w-3xl mx-auto w-full">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              <MessageSquare className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-4 text-gray-300" />
              <p className="text-base sm:text-lg font-medium">Welcome to AI Task Assistant</p>
              <p className="text-sm mt-2 px-4">Start a conversation to manage your tasks</p>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  role={message.role}
                  content={message.content}
                  timestamp={message.timestamp}
                  toolCalls={message.toolCalls}
                />
              ))}

              {isLoading && (
                <ChatMessage role="assistant" content="" isLoading={true} />
              )}

              {error && (
                <div className="flex justify-center w-full mb-4">
                  <div className="bg-red-50 border border-red-200 rounded-2xl px-4 py-3 max-w-sm sm:max-w-md">
                    <p className="text-sm text-red-800">{error}</p>
                    <button
                      onClick={retryLastMessage}
                      className="mt-2 flex items-center space-x-1 text-sm text-red-600 hover:text-red-800 min-h-[44px] min-w-[44px] px-3"
                    >
                      <span>Retry</span>
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </main>

      {/* Input Area */}
      <footer className="bg-white border-t border-gray-200 px-3 sm:px-4 py-3 sm:py-4">
        <div className="max-w-3xl mx-auto w-full">
          <ChatInput
            onSend={sendMessage}
            disabled={isLoading}
            placeholder="Ask me to help with your tasks..."
          />
          <p className="text-xs text-gray-500 text-center mt-2 hidden sm:block">
            AI-powered task management • Powered by OpenAI
          </p>
        </div>
      </footer>
    </div>
  );
}
