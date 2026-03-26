# Research & Technology Decisions: Advanced UX & Visual Experience

**Feature**: 007-advanced-ux  
**Date**: 2026-03-06  
**Purpose**: Document technology choices, best practices, and implementation patterns for premium UX implementation

---

## 1. Animation & Motion Library

### Decision: Use Framer Motion

**Rationale**:
- Industry-standard animation library for React with excellent Next.js integration
- Provides declarative API for complex animations and gestures
- Built-in support for layout animations, shared layout transitions, and gesture handling
- Automatic optimization for performance (60 FPS animations)
- Supports `prefers-reduced-motion` media query out of the box
- Small bundle size (~14kb gzipped) compared to alternatives
- Excellent TypeScript support and documentation

**Alternatives Considered**:
- **CSS Transitions/Animations**: Native browser support but limited for complex sequences, harder to coordinate multiple animations
- **React Spring**: Physics-based animations (overkill for UI transitions), steeper learning curve
- **GSAP**: Powerful but heavier bundle size, more complex API, better for marketing sites than web apps

**Implementation Pattern**:
```typescript
import { motion, AnimatePresence } from 'framer-motion'

// Page transitions
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.25, ease: "easeOut" }}
/>

// Task list animations
<AnimatePresence>
  {tasks.map(task => (
    <motion.div
      key={task.id}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20, transition: { duration: 0.2 } }}
      layout
    />
  ))}
</AnimatePresence>
```

**Best Practices**:
- Use `layout` prop for automatic layout animations
- Wrap conditional rendering with `AnimatePresence` for exit animations
- Keep animation durations between 150-300ms for UI feedback
- Use `easeOut` for entrances, `easeInOut` for balanced transitions
- Respect `prefers-reduced-motion` using Framer Motion's `useReducedMotion` hook

---

## 2. Design System & Styling

### Decision: Enhance Existing TailwindCSS Configuration

**Rationale**:
- Already integrated in project (no additional dependencies)
- Utility-first approach enables rapid iteration
- Highly customizable via `tailwind.config.js`
- Excellent responsive design support with mobile-first breakpoints
- Small production bundle size (purges unused styles)
- Strong TypeScript integration via `tailwindcss/types`

**Enhancements Required**:
- Define custom color palette (primary, secondary, success, warning, error)
- Create spacing scale based on 4px unit (already default in Tailwind)
- Extend typography scale with custom heading sizes
- Add custom shadows for elevation system
- Create component variants using Tailwind's `variants` or `cva` library

**Recommended Addition: class-variance-authority (CVA)**
- Lightweight utility for creating typed component variants
- Perfect for button variants (primary/secondary/destructive)
- Integrates seamlessly with Tailwind
- Bundle size: ~2kb gzipped

**Alternatives Considered**:
- **Styled Components**: Runtime CSS-in-JS (slower), larger bundle, not compatible with server components
- **CSS Modules**: Built into Next.js but less flexible for theming, harder to create reusable variants
- **Chakra UI / MUI**: Component libraries (too opinionated), larger bundles, would require replacing existing components

**Implementation Pattern**:
```typescript
// tailwind.config.js extension
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
      },
      animation: {
        'fade-in': 'fadeIn 0.25s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
}

// Component with CVA
import { cva } from 'class-variance-authority'

const buttonVariants = cva(
  'px-4 py-2 rounded-lg font-medium transition-all duration-200',
  {
    variants: {
      variant: {
        primary: 'bg-primary-600 text-white hover:bg-primary-700',
        secondary: 'border border-gray-300 hover:bg-gray-50',
        destructive: 'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2',
        lg: 'px-6 py-3 text-lg',
      },
    },
  }
)
```

---

## 3. Iconography

### Decision: Continue Using Lucide React (Already Installed)

**Rationale**:
- Already installed in project (`lucide-react` in package.json)
- Consistent, modern icon design with 1000+ icons
- Lightweight (~2kb per icon, tree-shakeable)
- Excellent TypeScript support
- Simple API: `import { Check, Trash2 } from 'lucide-react'`
- Icons are SVG-based and scale perfectly
- Consistent stroke width and visual style

**Implementation Pattern**:
```typescript
import { Check, Trash2, Edit2, Plus, Loader2 } from 'lucide-react'

// Usage with consistent sizing
<Check className="w-5 h-5 text-success" />
<Loader2 className="w-5 h-5 animate-spin" />
```

**Best Practices**:
- Use consistent icon sizes (w-5 h-5 = 20px for most UI, w-6 h-6 for emphasis)
- Pair icons with text labels for clarity (FR-019)
- Use `animate-spin` for loading states
- Apply color utilities to convey meaning (success, warning, error)

---

## 4. Responsive Breakpoint Strategy

### Decision: Use Tailwind's Default Breakpoints (Mobile-First)

**Breakpoints** (aligned with spec FR-002):
- `sm`: 640px (mobile landscape / small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops / small desktops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large desktops)

**Mobile-First Approach**:
```typescript
// Default styles = mobile (320-639px)
<div className="flex flex-col">
  {/* Stacked on mobile */}
  
  {/* Side-by-side on tablet+ */}
  <div className="md:flex md:gap-4">
    <div>Content 1</div>
    <div>Content 2</div>
  </div>
</div>
```

**Touch Target Compliance** (FR-012):
```typescript
// Minimum 44x44px touch target
<button className="min-w-[44px] min-h-[44px] p-3">
  <Icon className="w-5 h-5" />
</button>
```

---

## 5. Loading States & Skeleton Screens

### Decision: Custom Skeleton Components with Tailwind

**Rationale**:
- Full control over skeleton appearance and layout
- No additional dependencies
- Can match exact content dimensions (prevents CLS per FR-007)
- Reusable skeleton components for consistency

**Implementation Pattern**:
```typescript
// Reusable skeleton component
const Skeleton = ({ className }: { className: string }) => (
  <div className={`animate-pulse bg-gray-200 rounded ${className}`} />
)

// Task card skeleton
const TaskCardSkeleton = () => (
  <div className="p-4 border rounded-lg space-y-3">
    <Skeleton className="h-5 w-3/4" /> {/* Title */}
    <Skeleton className="h-4 w-full" />  {/* Description line 1 */}
    <Skeleton className="h-4 w-2/3" />  {/* Description line 2 */}
    <div className="flex gap-2">
      <Skeleton className="h-8 w-20" />  {/* Status badge */}
      <Skeleton className="h-8 w-8" />   {/* Action button */}
    </div>
  </div>
)
```

**Best Practices**:
- Use `animate-pulse` for loading state (Tailwind utility)
- Match skeleton dimensions to actual content (prevents layout shift)
- Show skeletons immediately (no delay) for perceived performance
- Add `aria-busy="true"` for accessibility

---

## 6. Form Validation & Feedback

### Decision: Client-Side Validation with HTML5 + React State

**Rationale**:
- HTML5 validation provides immediate feedback (required, type, pattern)
- React state management for custom validation rules
- No heavy form libraries needed for current complexity
- Can add `react-hook-form` later if forms become more complex

**Implementation Pattern**:
```typescript
const [errors, setErrors] = useState<Record<string, string>>({})
const [isSubmitting, setIsSubmitting] = useState(false)

// Inline error display
<div>
  <label className="block text-sm font-medium">Email</label>
  <input
    type="email"
    required
    className={`input ${errors.email ? 'border-error' : 'border-gray-300'}`}
  />
  {errors.email && (
    <p className="text-error text-sm mt-1">{errors.email}</p>
  )}
</div>

// Submit button with loading state
<button
  type="submit"
  disabled={isSubmitting}
  className="btn-primary disabled:opacity-50"
>
  {isSubmitting ? <Loader2 className="animate-spin" /> : 'Submit'}
</button>
```

**Accessibility**:
- Associate errors with inputs using `aria-describedby`
- Use `role="alert"` for error messages
- Focus first error field on failed submission

---

## 7. Page Transitions (Next.js App Router)

### Decision: Use Next.js 14 App Router with Framer Motion

**Challenge**: Next.js 14 App Router uses React Server Components by default, but Framer Motion requires client components.

**Solution**:
```typescript
// app/layout.tsx - Wrap with client component
'use client'
import { motion } from 'framer-motion'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          {children}
        </motion.div>
      </body>
    </html>
  )
}

// For page-specific transitions, use template.tsx
// app/template.tsx
'use client'
import { motion } from 'framer-motion'

export default function Template({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  )
}
```

**Best Practices**:
- Keep transitions subtle (opacity + slight movement)
- Duration: 200-300ms for page transitions
- Use `template.tsx` for consistent page transitions across routes
- Ensure transitions don't block interactivity

---

## 8. Accessibility Compliance

### Decision: WCAG 2.1 AA Standards

**Key Requirements** (per FR-008, FR-013):
- Contrast ratio: 4.5:1 for normal text, 3:1 for large text
- Focus indicators: Visible 2-3px outline on all interactive elements
- Keyboard navigation: All functionality accessible via keyboard
- Screen reader support: Proper ARIA labels and roles

**Implementation Checklist**:
- [ ] Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<article>`)
- [ ] Add `aria-label` to icon-only buttons
- [ ] Implement skip-to-content link
- [ ] Ensure focus order matches visual order
- [ ] Test with keyboard only (Tab, Enter, Escape)
- [ ] Verify with screen reader (NVDA or VoiceOver)
- [ ] Use `prefers-reduced-motion` media query

**Focus Indicator Example**:
```typescript
// Global focus styles in globals.css
*:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

button:focus-visible,
a:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
}
```

---

## 9. Performance Optimization

### Decision: Bundle Size & Animation Performance Budget

**Targets** (per SC-011):
- Maintain 60 FPS during animations
- Keep bundle size increase < 50kb
- First Contentful Paint < 1.5s on 3G

**Strategies**:
1. **Tree Shaking**: Import only used Framer Motion components
   ```typescript
   import { motion, AnimatePresence } from 'framer-motion'
   // NOT: import * as motion from 'framer-motion'
   ```

2. **Code Splitting**: Next.js automatic route-based splitting
   ```typescript
   // Dynamic imports for heavy components
   const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
     loading: () => <Skeleton className="h-40" />
   })
   ```

3. **CSS Optimization**: Tailwind purges unused styles automatically

4. **Animation Performance**:
   - Animate `transform` and `opacity` only (GPU-accelerated)
   - Avoid animating `width`, `height`, `top`, `left`
   - Use `will-change` sparingly for complex animations

---

## 10. MCP Tool Action Feedback in Chat

### Decision: Visual Status Indicators for Tool Execution

**Implementation Pattern**:
```typescript
type ToolStatus = 'pending' | 'executing' | 'success' | 'error'

const ToolMessage = ({ status, toolName, result }) => (
  <div className={`tool-message ${status}`}>
    {status === 'executing' && <Loader2 className="animate-spin" />}
    {status === 'success' && <Check className="text-success" />}
    {status === 'error' && <AlertCircle className="text-error" />}
    
    <span>{toolName}</span>
    {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
  </div>
)
```

**Visual States**:
- **Pending**: Gray background, spinner
- **Executing**: Blue background, animated spinner, tool name
- **Success**: Green tint, checkmark icon, result preview
- **Error**: Red tint, error icon, error message

---

## Summary of Technology Choices

| Category | Technology | Purpose | Bundle Impact |
|----------|-----------|---------|---------------|
| Animations | Framer Motion | Page transitions, micro-interactions, layout animations | ~14kb |
| Styling | TailwindCSS (existing) | Design system, responsive layouts, utilities | Already included |
| Variants | class-variance-authority | Component variant management | ~2kb |
| Icons | Lucide React (existing) | Iconography throughout UI | Already included |
| Forms | React + HTML5 | Validation, state management | No additional |
| Accessibility | Native HTML + ARIA | WCAG 2.1 AA compliance | No additional |

**Total Additional Bundle Size**: ~16kb gzipped (well under reasonable budget)

---

## Next Steps

1. ✅ Update `package.json` with Framer Motion and CVA dependencies
2. ✅ Extend `tailwind.config.js` with custom design tokens
3. ✅ Create reusable component library (Button, Input, Card, etc.)
4. ✅ Implement animation variants for common patterns
5. ✅ Build skeleton loader components
6. ✅ Add focus management and accessibility features
7. ✅ Test across breakpoints and browsers
