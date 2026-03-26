# Frontend Application - Advanced UX Edition

**Feature**: 007-advanced-ux - Premium Modern SaaS-Quality UI
**Status**: ✅ Complete (All 9 Phases)

This is the frontend for the multi-user todo web application built with Next.js 14+ and React 18+, featuring a premium modern UI with smooth animations, responsive design, and excellent accessibility.

## ✨ Features

### Core Features
- Next.js 14+ with App Router
- TypeScript 5+ support
- Better Auth integration for authentication
- Tailwind CSS for styling
- Responsive, mobile-first design
- Task management functionality

### Advanced UX Features (Phase 3-8)

#### 🎨 Premium Visual Design (US1)
- Cohesive design system with custom color palette
- Professional spacing scale (4px base unit)
- Typography hierarchy (title, body, metadata)
- Consistent visual states (hover, focus, active, disabled)
- Modern SaaS-quality aesthetic

#### 🎬 Smooth Animations (US2)
- Page transitions (250ms, ease-out)
- Micro-interactions (150ms duration)
- Staggered list animations
- Checkbox toggle animations
- Button hover/tap effects
- **Reduced motion support** for accessibility

#### 📱 Responsive Design (US3)
- Mobile-first breakpoints (320px, 768px, 1024px, 1440px)
- Touch-friendly 44x44px minimum targets
- Adaptive layouts for all screen sizes
- No horizontal scrolling on mobile
- Optimized for iPhone SE, iPad, Desktop

#### 📋 Enhanced Task Visualization (US4)
- Clear visual hierarchy (title > description > metadata)
- Color-coded status indicators
- Interactive action buttons (edit, delete)
- Empty state with call-to-action
- Smooth task completion toggle

#### ⏳ Loading States (US5)
- Skeleton loaders matching content layout
- Prevents layout shifts (CLS optimization)
- Loading spinners on form submissions
- Dashboard and task card skeletons
- Smooth transitions from loading to content

#### ✅ Form Validation (US6)
- Clear labels on all form fields
- Inline error messages with icons
- Success states and validation feedback
- Focus management and indicators
- Accessible ARIA labels and live regions

### Accessibility Features (Phase 9)

#### ♿ WCAG 2.1 AA Compliance
- Visible focus indicators (2px blue outline)
- Keyboard navigation support
- ARIA labels and roles
- Semantic HTML structure
- Color contrast ratios ≥4.5:1
- Screen reader friendly

#### 🎯 Reduced Motion Support
- Respects `prefers-reduced-motion` preference
- Instant transitions when enabled
- Toggle in DevTools for testing
- No animations for users with vestibular disorders

#### ⌨️ Keyboard Navigation
- Full tab navigation support
- Enter/Space key activation
- Logical focus order
- No keyboard traps
- Focus visible on all interactive elements

## 🛠 Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | Next.js | 14.2.x |
| Language | TypeScript | 5.x |
| Styling | Tailwind CSS | 3.3.x |
| Animations | Framer Motion | 12.35.x |
| Component Utils | class-variance-authority | 0.7.x |
| Icons | Lucide React | 0.294.x |
| Auth | Better Auth | Latest |

## 📦 Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Modern browser (Chrome, Firefox, Safari, Edge)

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Variables

Create a `.env.local` file in the frontend root directory:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### 4. Build for Production

```bash
npm run build
npm start
```

## 📁 Project Structure

```
frontend/
├── app/                     # Next.js App Router
│   ├── page.tsx            # Home page (landing)
│   ├── layout.tsx          # Root layout
│   ├── template.tsx        # Page transitions wrapper
│   ├── dashboard/          # Dashboard page
│   ├── login/              # Login page
│   ├── register/           # Registration page
│   ├── signup/             # Signup page
│   └── chat/               # AI Chat page
├── src/
│   ├── components/
│   │   ├── ui/             # Base UI components
│   │   │   ├── Button.tsx        # Multi-variant button
│   │   │   ├── Input.tsx         # Form input with validation
│   │   │   ├── Checkbox.tsx      # Animated checkbox
│   │   │   ├── Badge.tsx         # Status badges
│   │   │   ├── IconButton.tsx    # Icon-only button
│   │   │   ├── Skeleton.tsx      # Loading skeletons
│   │   │   └── index.ts          # Component exports
│   │   ├── tasks/          # Task-specific components
│   │   │   ├── TaskCard.tsx      # Individual task card
│   │   │   ├── TaskList.tsx      # Task list with animations
│   │   │   └── EmptyState.tsx    # Empty state component
│   │   ├── chat/           # Chat components
│   │   └── layout/         # Layout components
│   ├── lib/
│   │   └── animations.ts   # Animation variants library
│   ├── styles/
│   │   └── globals.css     # Global styles & focus states
│   └── types/              # TypeScript type definitions
├── public/                 # Static assets
├── tests/                  # Test files
└── package.json
```

## 🎨 Design System

### Color Palette

```typescript
colors: {
  primary: { /* Blue scale */ 50-900 },
  success: { /* Green scale */ 50-900 },
  warning: { /* Amber scale */ 50-900 },
  error: { /* Red scale */ 50-900 },
  gray: { /* Neutral scale */ 50-900 },
}
```

### Animation Durations

```typescript
transitionDuration: {
  75: '75ms',    // Micro-interactions
  150: '150ms',  // Hover effects
  200: '200ms',  // Standard transitions
  250: '250ms',  // Page transitions
  300: '300ms',  // Complex animations
  500: '500ms',  // Extended transitions
}
```

### Typography Hierarchy

- **Heading 1**: 2xl-4xl, font-bold (Page titles)
- **Heading 2**: xl-2xl, font-semibold (Section titles)
- **Heading 3**: lg-xl, font-semibold (Card titles)
- **Body**: base, text-gray-900 (Primary content)
- **Secondary**: sm, text-gray-600 (Descriptions)
- **Metadata**: xs, text-gray-500 (Timestamps, labels)

### Spacing Scale

Based on 4px unit:
- `1` = 4px
- `2` = 8px
- `3` = 12px
- `4` = 16px
- `5` = 20px
- `6` = 24px
- `8` = 32px
- `10` = 40px
- `12` = 48px

## 🧪 Testing

### Run Lighthouse Accessibility Audit

```bash
npm run build
npx serve .next

# In Chrome DevTools:
# 1. Open Lighthouse tab
# 2. Select "Accessibility" category
# 3. Run analysis
# Target: Score ≥95
```

### Test Reduced Motion

```
1. Open Chrome DevTools (F12)
2. Go to Rendering tab (Ctrl+Shift+P → "Rendering")
3. Check "Emulate CSS prefers-reduced-motion"
4. Navigate between pages
5. Verify instant transitions (no animations)
```

### Test Keyboard Navigation

```
1. Press Tab to navigate through elements
2. Verify focus visible on each element
3. Press Enter/Space to activate buttons
4. Test form submission with Enter
5. Verify no keyboard traps
```

### Test Responsive Design

```
1. Open Chrome DevTools
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test at breakpoints:
   - iPhone SE (375px)
   - iPad (768px)
   - Desktop (1024px+)
4. Verify no horizontal scrolling
5. Check touch targets ≥44x44px
```

### Test Animation Performance

```
1. Open Chrome DevTools Performance tab
2. Start recording
3. Navigate through app, interact with components
4. Stop recording
5. Verify 60 FPS maintained
6. Check for layout shifts
```

## 📚 Component Usage Examples

### Button Component

```tsx
import { Button } from '@/components/ui'

// Primary button
<Button variant="primary" size="md">Create Task</Button>

// Loading button
<Button variant="secondary" loading>Saving...</Button>

// Button with icon
<Button variant="destructive" icon={Trash2}>Delete</Button>

// Icon-only button
<Button variant="ghost" size="icon" aria-label="Edit">
  <Edit2 className="w-5 h-5" />
</Button>
```

### Input Component

```tsx
import { Input } from '@/components/ui'

// Basic input
<Input label="Email" value={email} onChange={setEmail} />

// Input with error
<Input
  label="Email"
  value={email}
  error="Please enter a valid email"
/>

// Input with success state
<Input
  label="Email"
  value={email}
  success
  successMessage="Email is valid"
/>

// Input with icon
<Input
  label="Search"
  leftIcon={Search}
  value={query}
  onChange={setQuery}
/>
```

### Animation Variants

```tsx
import { motion } from 'framer-motion'
import { pageTransition, slideUp } from '@/lib/animations'

// Page transition
<motion.div variants={pageTransition}>
  {/* Content */}
</motion.div>

// Custom animation
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {/* Content */}
</motion.div>
```

## 🔧 Available Scripts

```bash
# Development
npm run dev          # Start development server

# Production
npm run build        # Build for production
npm start            # Start production server

# Code Quality
npm run lint         # Run ESLint
```

## 🌐 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | ✅ Full support |
| Firefox | Latest | ✅ Full support |
| Safari | Latest | ✅ Full support |
| Edge | Latest | ✅ Full support |

**Mobile Browsers**:
- iOS Safari (iOS 15+)
- Chrome Mobile (Android 10+)

## 📊 Performance Metrics

### Bundle Size

- **First Load JS**: 87.3 kB (shared)
- **Framer Motion**: ~30-35 kB (tree-shaken)
- **class-variance-authority**: ~2-3 kB
- **Total added**: ~40-45 kB (under 50kb target)

### Animation Performance

- **Target**: 60 FPS
- **Duration**: 150-300ms
- **Properties**: transform, opacity only (GPU-accelerated)
- **Easing**: ease-out for natural feel

### Accessibility

- **Target Lighthouse Score**: ≥95
- **WCAG Level**: AA
- **Focus Indicators**: Visible 2px outline
- **Touch Targets**: Minimum 44x44px

## 🐛 Troubleshooting

### Animations Not Working

**Solution**:
- Ensure component has `'use client'` directive
- Check Framer Motion installed: `npm list framer-motion`
- Verify no console errors

### Focus Styles Not Showing

**Solution**:
- Verify global CSS imported in `layout.tsx`
- Use `:focus-visible` (not `:focus`)
- Test with keyboard navigation (Tab key)

### Layout Shift During Loading

**Solution**:
- Use skeleton loaders (DashboardSkeleton, TaskCardSkeleton)
- Add `min-height` to containers
- Check CLS in Lighthouse

### Reduced Motion Not Working

**Solution**:
- Enable "Emulate CSS prefers-reduced-motion" in DevTools Rendering
- Verify `useReducedMotionPreference()` hook usage
- Check `getMotionVariants()` helper implementation

## 📖 Additional Resources

- **Framer Motion Docs**: https://www.framer.com/motion/
- **TailwindCSS Docs**: https://tailwindcss.com/docs
- **CVA Docs**: https://cva.style/
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **Lucide Icons**: https://lucide.dev/icons/

## 📝 License

This project is part of the AI Hackathon 2026 Phase-3 implementation.

---

**Last Updated**: 2026-03-26
**Feature**: 007-advanced-ux (All Phases Complete)
**Status**: ✅ Production Ready