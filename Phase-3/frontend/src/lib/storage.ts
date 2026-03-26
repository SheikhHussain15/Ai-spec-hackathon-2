/**
 * Storage Utilities
 * 
 * localStorage utilities for chat persistence.
 */

const CHAT_CONVERSATION_KEY = 'chat_conversation_id';

/**
 * Save conversation ID to localStorage
 */
export function saveConversationId(conversationId: string): void {
  try {
    localStorage.setItem(CHAT_CONVERSATION_KEY, conversationId);
  } catch (error) {
    console.error('Failed to save conversation ID:', error);
  }
}

/**
 * Get conversation ID from localStorage
 */
export function getConversationId(): string | null {
  try {
    return localStorage.getItem(CHAT_CONVERSATION_KEY);
  } catch (error) {
    console.error('Failed to get conversation ID:', error);
    return null;
  }
}

/**
 * Clear conversation ID from localStorage
 */
export function clearConversationId(): void {
  try {
    localStorage.removeItem(CHAT_CONVERSATION_KEY);
  } catch (error) {
    console.error('Failed to clear conversation ID:', error);
  }
}
