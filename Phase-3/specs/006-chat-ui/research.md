# Research: Chat UI (ChatKit Integration)

**Feature**: 006-chat-ui
**Date**: 2026-02-18
**Status**: Complete

## Next.js App Router Chat Page

### Decision: Protected Client Component with Auth Redirect

Chat page implemented as client component with authentication check on mount. Redirects to login if no JWT token present.

**Pattern**:
```typescript
'use client';

export default function ChatPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      router.push('/login');
      return;
    }
    // Decode JWT to get user ID
    const payload = JSON.parse(atob(token.split('.')[1]));
    setUserId(payload.user_id || payload.sub);
  }, [router]);

  if (!userId) {
    return <LoadingState />;
  }

  return <ChatInterface userId={userId} />;
}
```

**Rationale**: Client-side auth check is sufficient for frontend protection. Backend enforces actual security via JWT validation.

**Alternatives Considered**:
- Server-side auth check: Rejected - adds complexity, backend already validates JWT
- Middleware protection: Rejected - overkill for single protected route

## Conversation State Management

### Decision: Custom React Hook with localStorage Persistence

Chat state managed via `useChat` custom hook. Conversation ID persisted to localStorage only—no messages stored in browser.

**Hook Pattern**:
```typescript
export function useChat(userId: string | null) {
  const [state, setState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    isLoading: false,
    error: null,
  });

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    const savedConversationId = localStorage.getItem(STORAGE_KEY);
    if (savedConversationId) {
      fetchConversationHistory(savedConversationId);
    }
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    // Add user message to state
    // Send to API
    // Add assistant response to state
    // Save conversation ID to localStorage
  }, [userId]);

  return { messages, conversationId, isLoading, error, sendMessage };
}
```

**localStorage Keys**:
- `chat_conversation_id`: Current conversation ID only

**What NOT Stored**:
- Messages (fetched from backend on load)
- User data (from JWT)
- Tokens (use existing auth_token)

**Rationale**: Minimal browser storage reduces security risk. Messages always fetched from authoritative backend source.

## Message Rendering Patterns

### Decision: Component-Based Message Bubbles with Animations

Each message rendered as separate component with role-based styling (user vs assistant).

**Component Structure**:
```typescript
interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  toolCalls?: ToolCall[];
  isLoading?: boolean;
}

export default function ChatMessage({ role, content, toolCalls }) {
  const isUser = role === 'user';
  
  return (
    <div className={isUser ? 'justify-end' : 'justify-start'}>
      <div className={isUser ? 'bg-blue-600' : 'bg-gray-100'}>
        {content}
        {toolCalls && toolCalls.map(renderToolCall)}
      </div>
    </div>
  );
}
```

**Animation Pattern**:
- CSS fade-in animation on mount
- Auto-scroll to bottom when new messages arrive
- Smooth scroll behavior

**Tool Call Display**:
- Expandable/collapsible within assistant messages
- Success/failure color coding (green/red)
- Arguments and results shown in monospace font

## API Integration Strategy

### Decision: Fetch API with JWT from localStorage

All API calls use native fetch with JWT attached from localStorage.

**Pattern**:
```typescript
const token = localStorage.getItem('auth_token');
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
```

**Error Handling**:
- Network errors: Show retry option
- API errors (4xx, 5xx): Show user-friendly message
- Auth errors (401): Redirect to login

**Loading State**:
- Set isLoading=true before API call
- Clear isLoading after response or error
- Show loading indicator in chat

## Summary of Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Check | Client-side on mount | Simple, backend enforces security |
| State Management | Custom React hook | Lightweight, no external dependencies |
| Persistence | localStorage (conversation_id only) | Minimal browser storage |
| Message Storage | Backend only | Authoritative source, security |
| API Client | Native fetch | No extra dependencies |
| Animations | CSS transitions | Performance, simplicity |

## Unresolved Questions

None - all technical decisions resolved with documented rationales.
