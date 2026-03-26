# Quickstart Guide: Advanced UX & Visual Experience

**Feature**: 007-advanced-ux  
**Date**: 2026-03-06  
**Purpose**: Get developers up and running with the advanced UX implementation

---

## Prerequisites

- Node.js 18+ installed
- Existing Phase-3 project setup (frontend directory)
- Git branch: `007-advanced-ux`

---

## 1. Install Dependencies

```bash
cd frontend

# Install animation library and component utilities
npm install framer-motion class-variance-authority

# Verify installation
npm list framer-motion class-variance-authority
```

**Expected Output**:
```
├── framer-motion@10.16.4
└── class-variance-authority@0.7.0
```

---

## 2. Update Tailwind Configuration

Extend `tailwind.config.js` with the design system:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Custom color palette
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
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
      },
      
      // Animation durations
      transitionDuration: {
        75: '75ms',
        100: '100ms',
        150: '150ms',
        200: '200ms',
        250: '250ms',
        300: '300ms',
        500: '500ms',
      },
      
      // Custom animations
      animation: {
        'fade-in': 'fadeIn 0.25s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
    },
  },
  plugins: [],
}
```

---

## 3. Update Global Styles

Add to `src/styles/globals.css` or `app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Focus styles for accessibility */
*:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

button:focus-visible,
a:focus-visible,
input:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Base typography */
body {
  @apply text-gray-900 antialiased;
  font-feature-settings: "cv11", "ss01";
  font-optical-sizing: auto;
}

/* Custom utilities */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

---

## 4. Create UI Component Library

Create the base components in `src/components/ui/`:

### Button Component

```typescript
// src/components/ui/Button.tsx
import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { Loader2, type LucideIcon } from 'lucide-react'

const buttonVariants = cva(
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

export interface ButtonProps
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

export { buttonVariants }
```

### Input Component

```typescript
// src/components/ui/Input.tsx
import * as React from 'react'
import { type LucideIcon } from 'lucide-react'
import { AlertCircle } from 'lucide-react'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
  hint?: string
  leftIcon?: LucideIcon
  rightElement?: React.ReactNode
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, leftIcon: LeftIcon, rightElement, className, id, ...props }, ref) => {
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
            ref={ref}
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
)

Input.displayName = 'Input'
```

### Create Component Index

```typescript
// src/components/ui/index.ts
export { Button, type ButtonProps, buttonVariants } from './Button'
export { Input, type InputProps } from './Input'
export { Checkbox } from './Checkbox'
export { Badge, type BadgeProps } from './Badge'
export { Skeleton, TaskCardSkeleton, DashboardSkeleton } from './Skeleton'
export { IconButton, type IconButtonProps } from './IconButton'
```

---

## 5. Create Animation Utilities

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
```

---

## 6. Set Up Page Transitions

Create `app/template.tsx` for consistent page transitions:

```typescript
// app/template.tsx
'use client'

import { motion } from 'framer-motion'
import { pageTransition } from '@/lib/animations'

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageTransition}
    >
      {children}
    </motion.div>
  )
}
```

---

## 7. Verify Installation

### Test Animation Library

Create a test component:

```typescript
// src/components/TestAnimation.tsx
'use client'

import { motion } from 'framer-motion'
import { Button } from './ui'

export function TestAnimation() {
  return (
    <div className="p-8 space-y-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="space-y-4"
      >
        <h1 className="text-2xl font-bold">Animation Test</h1>
        <p className="text-gray-600">If you see this fade in, animations are working!</p>
        
        <Button variant="primary">
          Test Button
        </Button>
        
        <Button variant="secondary" loading>
          Loading Button
        </Button>
      </motion.div>
    </div>
  )
}
```

### Run Development Server

```bash
npm run dev
```

Navigate to `http://localhost:3000` and verify:
- ✅ Page transitions work smoothly
- ✅ Buttons have hover states
- ✅ Loading states show spinner
- ✅ Focus indicators are visible
- ✅ No console errors

---

## 8. Implementation Checklist

Use this checklist when implementing each component:

### Component Standards

- [ ] Component is typed with TypeScript
- [ ] Variants use `class-variance-authority`
- [ ] Supports all required sizes (sm, md, lg)
- [ ] Supports all required states (default, hover, focus, disabled, loading)
- [ ] Meets WCAG 2.1 AA contrast requirements
- [ ] Has visible focus indicator
- [ ] Touch targets are minimum 44x44px
- [ ] Supports keyboard navigation
- [ ] Includes ARIA labels where needed
- [ ] Respects `prefers-reduced-motion`

### Animation Standards

- [ ] Duration between 150-300ms
- [ ] Uses appropriate easing (easeOut for entrances)
- [ ] Animates only `transform` and `opacity`
- [ ] Does not block user interaction
- [ ] Provides clear visual feedback
- [ ] Maintains 60 FPS (tested in DevTools)

### Responsive Standards

- [ ] Mobile-first implementation
- [ ] Tested at 320px, 768px, 1024px, 1440px
- [ ] No horizontal scrolling on mobile
- [ ] Touch targets meet 44x44px minimum
- [ ] Layout adapts smoothly at breakpoints

---

## 9. Testing Commands

```bash
# Run Lighthouse accessibility audit
npm run build
npx serve .next

# In Chrome DevTools:
# 1. Open Lighthouse tab
# 2. Select "Accessibility" category
# 3. Run analysis
# 4. Verify score >= 95

# Test responsive design
# In Chrome DevTools:
# 1. Toggle device toolbar (Ctrl+Shift+M)
# 2. Test at: iPhone SE (375px), iPad (768px), Desktop (1440px)

# Test keyboard navigation
# Tab through all interactive elements
# Verify focus is visible and logical
# Test Enter and Escape keys

# Test reduced motion
# In Chrome DevTools:
# 1. Rendering tab
# 2. Check "Emulate CSS prefers-reduced-motion"
# 3. Verify animations are disabled
```

---

## 10. Common Patterns

### Form with Validation

```typescript
'use client'

import { useState } from 'react'
import { Button, Input } from '@/components/ui'

export function SignupForm() {
  const [email, setEmail] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // Validation
    if (!email.includes('@')) {
      setErrors({ email: 'Please enter a valid email address' })
      setIsSubmitting(false)
      return
    }
    
    // Submit...
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={errors.email}
        placeholder="you@example.com"
      />
      
      <Button 
        type="submit" 
        variant="primary" 
        loading={isSubmitting}
      >
        {isSubmitting ? 'Creating account...' : 'Create account'}
      </Button>
    </form>
  )
}
```

### Animated Task List

```typescript
'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { listItemVariants } from '@/lib/animations'
import { TaskCard } from '@/components/tasks'

export function TaskList({ tasks }) {
  return (
    <div className="space-y-3">
      <AnimatePresence>
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            variants={listItemVariants}
            custom={index}
          >
            <TaskCard task={task} />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
```

### Loading State

```typescript
import { DashboardSkeleton } from '@/components/ui'
import { TaskList } from '@/components/tasks'

export function Dashboard({ tasks, isLoading }) {
  if (isLoading) {
    return <DashboardSkeleton />
  }
  
  if (tasks.length === 0) {
    return <EmptyState />
  }
  
  return <TaskList tasks={tasks} />
}
```

---

## 11. Troubleshooting

### Issue: Animations not working

**Solution**:
- Ensure component has `'use client'` directive
- Check that Framer Motion is installed: `npm list framer-motion`
- Verify no errors in browser console

### Issue: Styles not applying

**Solution**:
- Check Tailwind content paths in `tailwind.config.js`
- Restart dev server after config changes
- Run `npm run build` to check for errors

### Issue: Focus styles not showing

**Solution**:
- Verify global CSS is imported in `layout.tsx`
- Check that `:focus-visible` is used (not `:focus`)
- Test with keyboard navigation (Tab key)

### Issue: Layout shift during loading

**Solution**:
- Use skeleton loaders matching exact content dimensions
- Add `min-height` to containers
- Check CLS score in Lighthouse

---

## 12. Next Steps

After completing setup:

1. ✅ Implement remaining UI components (Checkbox, Badge, IconButton)
2. ✅ Create task-specific components (TaskCard, TaskList, EmptyState)
3. ✅ Create chat components (MessageBubble, ToolStatus, ChatInput)
4. ✅ Add animations to all user interactions
5. ✅ Test across all breakpoints
6. ✅ Run accessibility audit
7. ✅ Optimize performance (bundle size, animation FPS)

---

## Resources

- **Framer Motion Docs**: https://www.framer.com/motion/
- **TailwindCSS Docs**: https://tailwindcss.com/docs
- **CVA Docs**: https://cva.style/
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **Lucide Icons**: https://lucide.dev/icons/
