/**
 * useChat Hook
 * 
 * Manages chat state, conversation persistence, and API communication.
 */

'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { getAuthToken } from '../lib/auth';
import { saveConversationId, getConversationId } from '../lib/storage';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  toolCalls?: any[];
}

interface ChatState {
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
}

export function useChat(userId: string | null) {
  const [state, setState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    isLoading: false,
    error: null,
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    const savedConversationId = getConversationId();
    if (savedConversationId && userId) {
      setState(prev => ({ ...prev, conversationId: savedConversationId }));
      fetchConversationHistory(savedConversationId, userId);
    }
  }, [userId]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [state.messages]);

  const fetchConversationHistory = useCallback(async (conversationId: string, uid: string) => {
    const token = getAuthToken();
    if (!token) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/${uid}/conversations/${conversationId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success && data.messages) {
          setState(prev => ({
            ...prev,
            messages: data.messages.map((msg: any) => ({
              role: msg.role as 'user' | 'assistant',
              content: msg.content,
              timestamp: msg.created_at,
              toolCalls: msg.tool_calls?.calls || [],
            })),
          }));
        }
      }
    } catch (error) {
      console.error('Failed to fetch conversation history:', error);
    }
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!userId || !content.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

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
          conversation_id: state.conversationId || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      
      // Save conversation ID for future requests
      if (data.conversation_id) {
        saveConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        toolCalls: data.tool_calls || [],
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        conversationId: data.conversation_id || prev.conversationId,
        isLoading: false,
      }));
      
      return data;
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to send message',
      }));
      throw error;
    }
  }, [userId, state.conversationId]);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const retryLastMessage = useCallback(async () => {
    const lastUserMessage = state.messages[state.messages.length - 1];
    if (lastUserMessage && lastUserMessage.role === 'user') {
      // Remove the last user message and retry
      setState(prev => ({
        ...prev,
        messages: prev.messages.slice(0, -1),
      }));
      await sendMessage(lastUserMessage.content);
    }
  }, [state.messages, sendMessage]);

  return {
    messages: state.messages,
    conversationId: state.conversationId,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearError,
    retryLastMessage,
    messagesEndRef,
  };
}
