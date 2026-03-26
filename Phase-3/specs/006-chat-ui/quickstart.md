# Quickstart: Chat UI (ChatKit Integration)

**Feature**: 006-chat-ui
**Version**: 1.0.0
**Last Updated**: 2026-02-18

## Overview

The Chat UI provides a conversational interface for users to interact with the AI agent for task management. Built with Next.js App Router, React hooks, and TypeScript.

## Prerequisites

- Node.js 18+
- Existing Phase-3 frontend with authentication
- Backend chat endpoint running (POST /api/{user_id}/chat)

## Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create or update `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── app/
│   └── chat/
│       └── page.tsx         # Protected chat page
├── src/
│   ├── components/
│   │   └── chat/
│   │       ├── ChatMessage.tsx    # Message bubble
│   │       ├── ChatInput.tsx      # Input field
│   │       ├── ChatLoading.tsx    # Loading indicator
│   │       ├── ChatError.tsx      # Error state
│   │       └── ChatEmptyState.tsx # Empty state
│   ├── hooks/
│   │   └── useChat.ts         # Chat state management
│   └── lib/
│       ├── auth.ts            # JWT utilities
│       └── storage.ts         # localStorage utilities
```

## Running the Chat UI

### Start the Frontend

```bash
cd frontend
npm run dev
```

The chat page will be available at: `http://localhost:3000/chat`

## Usage Examples

### Starting a New Conversation

1. Navigate to `/chat`
2. User is automatically authenticated (redirected if not logged in)
3. Type a message: "Add a task to review the project docs"
4. Agent responds and creates the task
5. Conversation ID is saved to localStorage

### Resuming a Conversation

1. Refresh the page or return to `/chat`
2. Previous conversation history is automatically loaded
3. Continue chatting with full context

### Handling Errors

- **Network Error**: Error message displayed with retry button
- **Auth Error**: Redirected to login page
- **Empty Message**: Send button disabled until valid input

## Component Guide

### ChatMessage

Renders individual messages with role-based styling.

```typescript
<ChatMessage
  role="user"
  content="Add a task"
  timestamp="2026-02-18T12:00:00Z"
  toolCalls={[{ tool_name: 'add_task', success: true }]}
/>
```

### ChatInput

Input field with send button.

```typescript
<ChatInput
  onSend={(message) => sendMessage(message)}
  disabled={isLoading}
  placeholder="Ask me to help with your tasks..."
/>
```

### ChatLoading

Loading indicator while agent processes.

```typescript
{isLoading && <ChatLoading />}
```

### ChatError

Error state with retry option.

```typescript
{error && (
  <ChatError
    message={error}
    onRetry={retryLastMessage}
  />
)}
```

### ChatEmptyState

Welcoming empty state for new users.

```typescript
{messages.length === 0 ? (
  <ChatEmptyState onExampleClick={handleExampleClick} />
) : (
  // Render messages
)}
```

## State Management

### useChat Hook

Manages all chat state:

```typescript
const {
  messages,
  conversationId,
  isLoading,
  error,
  sendMessage,
  clearError,
  retryLastMessage,
  messagesEndRef,
} = useChat(userId);
```

### Conversation Persistence

- Conversation ID stored in localStorage: `chat_conversation_id`
- Messages fetched from backend on page load
- No sensitive data stored in browser

## Authentication

JWT token automatically attached to all API requests:

```typescript
const token = localStorage.getItem('auth_token');
const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

## Testing

### Component Tests

```bash
npm test -- ChatMessage
npm test -- ChatInput
```

### Integration Tests

```bash
npm test -- chat-flow
```

## Troubleshooting

### Chat Page Redirects to Login

**Issue**: User not authenticated

**Solution**: Log in first at `/login`

### Messages Not Loading

**Issue**: Backend API not reachable

**Solution**: 
1. Verify backend is running
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`

### Conversation Not Persisting

**Issue**: localStorage cleared or blocked

**Solution**: 
1. Ensure browser allows localStorage
2. Check browser privacy settings

## API Reference

For detailed API documentation, see backend documentation:
- `POST /api/{user_id}/chat` - Send message to agent
- `GET /api/{user_id}/conversations` - List conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get conversation history

## Next Steps

- Customize chat UI styling
- Add conversation history sidebar
- Implement conversation search
- Add message reactions or feedback
