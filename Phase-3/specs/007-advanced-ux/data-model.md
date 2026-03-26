# Data Model & Component Architecture: Advanced UX & Visual Experience

**Feature**: 007-advanced-ux  
**Date**: 2026-03-06  
**Purpose**: Define UI component architecture, design tokens, and component contracts

---

## 1. Design Tokens

### Color Palette

```typescript
// tailwind.config.js - colors section
colors: {
  // Primary brand color (blue)
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#3b82f6', // Main primary color
    600: '#2563eb', // Hover state
    700: '#1d4ed8', // Active state
    800: '#1e40af',
    900: '#1e3a8a',
  },
  
  // Semantic colors
  success: {
    50: '#ecfdf5',
    500: '#10b981',
    600: '#059669',
    700: '#047857',
  },
  warning: {
    50: '#fffbeb',
    500: '#f59e0b',
    600: '#d97706',
    700: '#b45309',
  },
  error: {
    50: '#fef2f2',
    500: '#ef4444',
    600: '#dc2626',
    700: '#b91c1c',
  },
  
  // Neutral grays
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
}
```

### Spacing Scale

Based on 4px unit (Tailwind default):

```typescript
// spacing: 4px base unit
xs: 0.25rem,  // 4px
sm: 0.5rem,   // 8px
md: 1rem,     // 16px
lg: 1.5rem,   // 24px
xl: 2rem,     // 32px
2xl: 3rem,    // 48px
3xl: 4rem,    // 64px
```

### Typography Scale

```typescript
// tailwind.config.js - fontSize section
fontSize: {
  xs: ['0.75rem', { lineHeight: '1rem', fontWeight: '400' }],    // 12px
  sm: ['0.875rem', { lineHeight: '1.25rem', fontWeight: '400' }], // 14px
  base: ['1rem', { lineHeight: '1.5rem', fontWeight: '400' }],    // 16px
  lg: ['1.125rem', { lineHeight: '1.75rem', fontWeight: '500' }], // 18px
  xl: ['1.25rem', { lineHeight: '1.75rem', fontWeight: '600' }],  // 20px
  '2xl': ['1.5rem', { lineHeight: '2rem', fontWeight: '600' }],   // 24px
  '3xl': ['1.875rem', { lineHeight: '2.25rem', fontWeight: '700' }], // 30px
  '4xl': ['2.25rem', { lineHeight: '2.5rem', fontWeight: '700' }],  // 36px
}
```

### Shadow System (Elevation)

```typescript
// tailwind.config.js - boxShadow section
boxShadow: {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  
  // Interactive states
  focus: '0 0 0 3px rgba(59, 130, 246, 0.3)',
  'focus-error': '0 0 0 3px rgba(239, 68, 68, 0.3)',
}
```

### Border Radius

```typescript
// tailwind.config.js - borderRadius section
borderRadius: {
  none: '0',
  sm: '0.125rem',  // 2px
  DEFAULT: '0.25rem', // 4px
  md: '0.375rem',  // 6px
  lg: '0.5rem',    // 8px
  xl: '0.75rem',   // 12px
  '2xl': '1rem',   // 16px
  full: '9999px',
}
```

### Animation Durations

```typescript
// tailwind.config.js - transitionDuration section
transitionDuration: {
  75: '75ms',
  100: '100ms',
  150: '150ms',  // Micro-interactions
  200: '200ms',  // Standard UI feedback
  250: '250ms',  // Page transitions (lower bound)
  300: '300ms',  // Page transitions (upper bound)
  500: '500ms',
}
```

---

## 2. Component Architecture

### Component Hierarchy

```
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   └── UserMenu
│   └── MainContent
│       ├── PageTransition (Framer Motion)
│       │   └── Page Content
│       └── Footer
│
├── Dashboard
│   ├── DashboardHeader
│   │   ├── PageTitle
│   │   └── ActionButtons
│   ├── TaskList
│   │   ├── TaskCard (animated)
│   │   │   ├── TaskCheckbox
│   │   │   ├── TaskContent
│   │   │   │   ├── TaskTitle
│   │   │   │   ├── TaskDescription
│   │   │   │   └── TaskMetadata
│   │   │   ├── TaskStatus
│   │   │   └── TaskActions
│   │   │       ├── EditButton
│   │   │       └── DeleteButton
│   │   └── EmptyState
│   │       ├── EmptyIllustration
│   │       ├── EmptyMessage
│   │       └── CreateFirstTaskButton
│   └── TaskForm
│       ├── FormField
│       │   ├── Label
│       │   ├── Input/Textarea
│       │   └── ErrorMessage
│       └── SubmitButton
│
└── Chat
    ├── ChatContainer
    │   ├── ChatHeader
    │   ├── MessageList
    │   │   └── MessageBubble (animated)
    │   │       ├── UserMessage
    │   │       ├── AssistantMessage
    │   │       └── ToolExecutionMessage
    │   │           ├── ToolStatus
    │   │           ├── ToolName
    │   │           └── ToolResult
    │   └── ChatInput
    │       ├── InputField
    │       └── SendButton
    └── TypingIndicator
```

---

## 3. Component Contracts

### Button Component

```typescript
// src/components/ui/Button.tsx

import { cva, type VariantProps } from 'class-variance-authority'
import { LucideIcon } from 'lucide-react'

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center gap-2 rounded-lg font-medium ' +
  'transition-all duration-200 ease-out ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 ' +
  'disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed',
  {
    variants: {
      variant: {
        primary: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800 shadow-sm hover:shadow',
        secondary: 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 active:bg-gray-100',
        destructive: 'bg-error-600 text-white hover:bg-error-700 active:bg-error-800 shadow-sm hover:shadow',
        ghost: 'text-gray-700 hover:bg-gray-100 active:bg-gray-200',
        link: 'text-primary-600 hover:underline active:text-primary-800',
      },
      size: {
        sm: 'h-9 px-3 text-sm min-w-[44px]',
        md: 'h-10 px-4 text-base min-w-[44px]',
        lg: 'h-12 px-6 text-lg min-w-[44px]',
        icon: 'h-10 w-10',
      },
      loading: {
        true: 'pointer-events-none',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  icon?: LucideIcon
  loading?: boolean
  children?: React.ReactNode
}

export function Button({
  className,
  variant,
  size,
  icon: Icon,
  loading,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={buttonVariants({ variant, size, loading, className })}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading && <Loader2 className="w-4 h-4 animate-spin" />}
      {!loading && Icon && <Icon className="w-4 h-4" />}
      {children}
    </button>
  )
}
```

**Usage Examples**:
```typescript
<Button variant="primary" size="md">
  Create Task
</Button>

<Button variant="destructive" size="sm" icon={Trash2}>
  Delete
</Button>

<Button variant="secondary" loading>
  Saving...
</Button>

<Button variant="ghost" size="icon" aria-label="Edit task">
  <Edit2 className="w-5 h-5" />
</Button>
```

---

### Input Component

```typescript
// src/components/ui/Input.tsx

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
  hint?: string
  leftIcon?: LucideIcon
  rightElement?: React.ReactNode
}

export function Input({
  label,
  error,
  hint,
  leftIcon: LeftIcon,
  rightElement,
  className,
  id,
  ...props
}: InputProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-')
  
  return (
    <div className="space-y-1.5">
      <label 
        htmlFor={inputId}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
      </label>
      
      <div className="relative">
        {LeftIcon && (
          <LeftIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        )}
        
        <input
          id={inputId}
          className={`
            w-full rounded-lg border bg-white px-3 py-2.5 text-sm
            transition-all duration-200
            placeholder:text-gray-400
            focus:outline-none focus:ring-2 focus:ring-offset-1
            disabled:bg-gray-100 disabled:cursor-not-allowed
            ${LeftIcon ? 'pl-10' : ''}
            ${error
              ? 'border-error-500 focus:border-error-500 focus:ring-error-200'
              : 'border-gray-300 focus:border-primary-500 focus:ring-primary-200'
            }
            ${className}
          `}
          {...props}
        />
        
        {rightElement && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            {rightElement}
          </div>
        )}
      </div>
      
      {error && (
        <p role="alert" className="text-sm text-error-600 flex items-center gap-1.5">
          <AlertCircle className="w-4 h-4" />
          {error}
        </p>
      )}
      
      {hint && !error && (
        <p className="text-sm text-gray-500">{hint}</p>
      )}
    </div>
  )
}
```

---

### Task Card Component

```typescript
// src/components/tasks/TaskCard.tsx

import { motion } from 'framer-motion'
import { Task } from '@/models'
import { Checkbox } from '@/components/ui/Checkbox'
import { Badge } from '@/components/ui/Badge'
import { IconButton } from '@/components/ui/IconButton'

interface TaskCardProps {
  task: Task
  onToggle: (id: string) => void
  onEdit: (task: Task) => void
  onDelete: (id: string) => void
}

export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20, transition: { duration: 0.2 } }}
      whileHover={{ scale: 1.01 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      className={`
        group relative rounded-xl border bg-white p-4 shadow-sm
        transition-shadow duration-200
        hover:shadow-md
        ${task.completed ? 'bg-gray-50' : ''}
      `}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <Checkbox
          checked={task.completed}
          onCheckedChange={() => onToggle(task.id)}
          className="mt-1"
        />
        
        {/* Content */}
        <div className="flex-1 min-w-0 space-y-1">
          {/* Title */}
          <h3 className={`
            font-semibold text-gray-900 truncate
            ${task.completed ? 'line-through text-gray-500' : ''}
          `}>
            {task.title}
          </h3>
          
          {/* Description */}
          {task.description && (
            <p className={`
              text-sm text-gray-600 line-clamp-2
              ${task.completed ? 'line-through text-gray-400' : ''}
            `}>
              {task.description}
            </p>
          )}
          
          {/* Metadata */}
          <div className="flex items-center gap-2">
            <Badge variant={task.status}>
              {task.status}
            </Badge>
            
            {task.dueDate && (
              <span className="text-xs text-gray-500">
                {formatDate(task.dueDate)}
              </span>
            )}
          </div>
        </div>
        
        {/* Actions (visible on hover/focus) */}
        <div className="flex items-center gap-1 opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-within:opacity-100">
          <IconButton
            variant="ghost"
            size="icon"
            onClick={() => onEdit(task)}
            aria-label="Edit task"
          >
            <Edit2 className="w-4 h-4" />
          </IconButton>
          
          <IconButton
            variant="ghost"
            size="icon"
            onClick={() => onDelete(task.id)}
            aria-label="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </IconButton>
        </div>
      </div>
    </motion.div>
  )
}
```

---

### Badge Component

```typescript
// src/components/ui/Badge.tsx

import { cva, type VariantProps } from 'class-variance-authority'

const badgeVariants = cva(
  'inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium',
  {
    variants: {
      variant: {
        pending: 'bg-gray-100 text-gray-700',
        'in-progress': 'bg-primary-100 text-primary-700',
        completed: 'bg-success-100 text-success-700',
        error: 'bg-error-100 text-error-700',
      },
    },
    defaultVariants: {
      variant: 'pending',
    },
  }
)

interface BadgeProps extends VariantProps<typeof badgeVariants> {
  children: React.ReactNode
  className?: string
}

export function Badge({ variant, children, className }: BadgeProps) {
  return (
    <span className={badgeVariants({ variant, className })}>
      {children}
    </span>
  )
}
```

---

### Skeleton Components

```typescript
// src/components/ui/Skeleton.tsx

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={`
        animate-pulse rounded bg-gray-200
        ${className}
      `}
    />
  )
}

// Specialized skeletons
export function TaskCardSkeleton() {
  return (
    <div className="rounded-xl border bg-white p-4 space-y-3">
      <div className="flex items-start gap-3">
        <Skeleton className="h-5 w-5 rounded mt-1" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-5 w-3/4" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-2/3" />
          <div className="flex gap-2 pt-2">
            <Skeleton className="h-5 w-16" />
            <Skeleton className="h-5 w-20" />
          </div>
        </div>
      </div>
    </div>
  )
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />
      <div className="space-y-3">
        {[1, 2, 3].map(i => (
          <TaskCardSkeleton key={i} />
        ))}
      </div>
    </div>
  )
}
```

---

### Message Bubble Component (Chat)

```typescript
// src/components/chat/MessageBubble.tsx

import { motion } from 'framer-motion'
import { Message, ToolExecution } from '@/models'
import { ToolStatus } from './ToolStatus'

interface MessageBubbleProps {
  message: Message
  isLast: boolean
}

export function MessageBubble({ message, isLast }: MessageBubbleProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div className={`
        flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
        ${message.role === 'user' ? 'bg-primary-600' : 'bg-gray-600'}
      `}>
        {message.role === 'user' ? '👤' : '🤖'}
      </div>
      
      {/* Bubble */}
      <div className={`
        max-w-[80%] rounded-2xl px-4 py-3
        ${message.role === 'user' 
          ? 'bg-primary-600 text-white rounded-br-sm' 
          : 'bg-gray-100 text-gray-900 rounded-bl-sm'
        }
      `}>
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        
        {/* Tool executions */}
        {message.tool_executions?.map((tool, index) => (
          <ToolStatus
            key={index}
            tool={tool}
            className="mt-2"
          />
        ))}
        
        {/* Timestamp */}
        <p className={`
          text-xs mt-1
          ${message.role === 'user' ? 'text-primary-200' : 'text-gray-500'}
        `}>
          {formatTime(message.created_at)}
        </p>
      </div>
    </motion.div>
  )
}
```

---

### Tool Status Component (Chat MCP Feedback)

```typescript
// src/components/chat/ToolStatus.tsx

import { LucideIcon, Loader2, Check, AlertCircle, Wrench } from 'lucide-react'
import { cva } from 'class-variance-authority'

const toolStatusVariants = cva(
  'flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-medium',
  {
    variants: {
      status: {
        pending: 'bg-gray-100 text-gray-700',
        executing: 'bg-primary-100 text-primary-700',
        success: 'bg-success-100 text-success-700',
        error: 'bg-error-100 text-error-700',
      },
    },
    defaultVariants: {
      status: 'pending',
    },
  }
)

interface ToolStatusProps {
  tool: ToolExecution
  className?: string
}

const statusConfig: Record<string, { icon: LucideIcon; label: string }> = {
  pending: { icon: Wrench, label: 'Pending' },
  executing: { icon: Loader2, label: 'Executing...' },
  success: { icon: Check, label: 'Completed' },
  error: { icon: AlertCircle, label: 'Failed' },
}

export function ToolStatus({ tool, className }: ToolStatusProps) {
  const config = statusConfig[tool.status]
  const Icon = config.icon
  
  return (
    <div className={toolStatusVariants({ status: tool.status, className })}>
      <Icon className={`w-3.5 h-3.5 ${tool.status === 'executing' ? 'animate-spin' : ''}`} />
      <span>{tool.tool_name}</span>
      {tool.status === 'success' && tool.result && (
        <span className="text-xs opacity-75">
          {JSON.stringify(tool.result).slice(0, 50)}...
        </span>
      )}
      {tool.status === 'error' && tool.error && (
        <span className="text-xs opacity-75">{tool.error}</span>
      )}
    </div>
  )
}
```

---

## 4. Animation Variants

### Page Transition Variants

```typescript
// src/lib/animations.ts
import { Variants } from 'framer-motion'

export const pageTransition: Variants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.25,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.2,
    },
  },
}

export const fadeIn: Variants = {
  initial: { opacity: 0 },
  animate: { 
    opacity: 1,
    transition: { duration: 0.2 },
  },
}

export const slideUp: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { 
    opacity: 1,
    y: 0,
    transition: { duration: 0.25, ease: 'easeOut' },
  },
}
```

### List Item Variants (Staggered Animation)

```typescript
export const listItemVariants: Variants = {
  hidden: {
    opacity: 0,
    x: -20,
  },
  visible: (i: number) => ({
    opacity: 1,
    x: 0,
    transition: {
      delay: i * 0.05,
      duration: 0.2,
      ease: 'easeOut',
    },
  }),
  exit: {
    opacity: 0,
    x: 20,
    transition: { duration: 0.2 },
  },
}

// Usage
<motion.div variants={listItemVariants} custom={index}>
  <TaskCard />
</motion.div>
```

### Checkbox Animation

```typescript
export const checkboxVariants = {
  checked: {
    scale: [1, 1.2, 1],
    transition: { duration: 0.2 },
  },
  unchecked: {
    scale: 1,
  },
}
```

---

## 5. Responsive Breakpoint Strategy

### Mobile-First Classes

```typescript
// Pattern: Base (mobile) → md (tablet) → lg (desktop)

// Layout
<div className="
  flex flex-col              // Mobile: stacked
  md:flex-row md:gap-4       // Tablet: side-by-side
  lg:gap-6                   // Desktop: more gap
">

// Grid
<div className="
  grid grid-cols-1           // Mobile: 1 column
  md:grid-cols-2             // Tablet: 2 columns
  lg:grid-cols-3             // Desktop: 3 columns
  gap-4 md:gap-6 lg:gap-8
">

// Navigation
<nav className="
  fixed bottom-0 left-0 right-0    // Mobile: bottom nav
  md:static                        // Tablet+: sidebar
  md:w-64
">
```

### Touch Target Enforcement

```typescript
// All interactive elements must meet 44x44px minimum
const touchTarget = 'min-w-[44px] min-h-[44px]'

// Applied to buttons, links, inputs, etc.
<button className={`${touchTarget} p-3`}>
  <Icon className="w-5 h-5" />
</button>
```

---

## 6. Accessibility Contracts

### Focus Management

```typescript
// Global focus styles in globals.css
*:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

button:focus-visible,
a:focus-visible,
input:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
}
```

### ARIA Labels

```typescript
// Icon-only buttons MUST have aria-label
<IconButton aria-label="Delete task">
  <Trash2 />
</IconButton>

// Loading states MUST have aria-busy
<button aria-busy={isSubmitting} disabled={isSubmitting}>
  {isSubmitting ? <Loader2 /> : 'Submit'}
</button>

// Error messages MUST have role="alert"
<p role="alert" aria-live="polite">
  {error}
</p>
```

### Reduced Motion

```typescript
// Use Framer Motion's useReducedMotion
import { useReducedMotion } from 'framer-motion'

const shouldReduceMotion = useReducedMotion()

const variants = {
  initial: { 
    opacity: 0, 
    x: shouldReduceMotion ? 0 : -20 
  },
  animate: { 
    opacity: 1, 
    x: 0,
    transition: { 
      duration: shouldReduceMotion ? 0 : 0.2 
    }
  },
}
```

---

## 7. File Structure

```
src/
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Checkbox.tsx
│   │   ├── Badge.tsx
│   │   ├── Skeleton.tsx
│   │   ├── IconButton.tsx
│   │   └── index.ts
│   ├── tasks/
│   │   ├── TaskCard.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   ├── EmptyState.tsx
│   │   └── index.ts
│   └── chat/
│       ├── MessageBubble.tsx
│       ├── ToolStatus.tsx
│       ├── ChatInput.tsx
│       ├── TypingIndicator.tsx
│       └── index.ts
├── lib/
│   ├── animations.ts
│   ├── utils.ts
│   └── constants.ts
├── styles/
│   └── globals.css
└── types/
    └── ui.ts
```

---

## Summary

This document defines:
- ✅ Complete design token system (colors, spacing, typography, shadows)
- ✅ Component architecture with clear hierarchy
- ✅ Typed component contracts with variants
- ✅ Animation patterns for all interactions
- ✅ Responsive breakpoint strategy
- ✅ Accessibility requirements and patterns
- ✅ File organization for scalability

All components are designed to be:
- **Reusable**: Single responsibility, composable
- **Accessible**: WCAG 2.1 AA compliant
- **Responsive**: Mobile-first, touch-friendly
- **Performant**: Optimized animations, minimal re-renders
- **Type-safe**: Full TypeScript support
