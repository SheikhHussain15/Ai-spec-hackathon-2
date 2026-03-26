# Quickstart Guide - UI/UX Upgrade

**Feature**: UI/UX Upgrade
**Branch**: 004-ui-ux-upgrade
**Date**: 2026-02-16

## Overview

This guide provides setup instructions and development workflow for implementing the UI/UX upgrade. Follow these steps to get started with development.

---

## Prerequisites

Ensure you have the following installed:

- **Node.js**: v18.17 or later (v20 recommended)
- **npm**: v9 or later (comes with Node.js)
- **Git**: Latest version
- **Code Editor**: VS Code recommended
- **Browser**: Chrome/Edge for DevTools testing

---

## Project Setup

### 1. Clone and Navigate

```bash
# Navigate to project root
cd C:\Users\hr773\Desktop\Ai-hackathon-2\Phase-2

# Ensure you're on the correct branch
git checkout 004-ui-ux-upgrade
```

### 2. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Verify installation
npm list --depth=0
```

**Expected Output**:
```
├── next@14.2.35
├── react@18.3.1
├── tailwindcss@3.3.0
├── typescript@5.3.3
└── ... (other dependencies)
```

### 3. Environment Setup

```bash
# Create .env.local if it doesn't exist
# File should contain:
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Verify Backend is Running

```bash
# Backend should be running on port 8000
# Test with:
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

---

## Development Workflow

### Start Development Server

```bash
# From frontend directory
npm run dev

# Server starts on http://localhost:3000
```

**Expected Output**:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
event - compiled client and server successfully in 2.1s
wait  - compiling...
```

### Hot Reload

- Changes to components automatically reload
- Changes to global styles may require manual refresh (Ctrl+R)
- TypeScript errors shown in browser console

---

## Implementation Order

### Week 1: Design System Foundation

**Day 1-2: Design Tokens**
1. Create `frontend/src/styles/globals.css`
2. Add CSS custom properties for all tokens
3. Update `tailwind.config.js` with token references
4. Test tokens in browser DevTools

**Day 3-4: Base Components**
1. Create `frontend/src/components/ui/Button.tsx`
2. Create `frontend/src/components/ui/Input.tsx`
3. Create `frontend/src/components/ui/Card.tsx`
4. Storybook-style testing page (optional)

**Day 5: Layout Components**
1. Create `frontend/src/components/layout/Container.tsx`
2. Create `frontend/src/components/layout/Grid.tsx`
3. Update `frontend/app/layout.tsx` with design system

---

### Week 2: Task Components

**Day 1-2: Task Display**
1. Create `frontend/src/components/tasks/TaskCard.tsx`
2. Create `frontend/src/components/tasks/TaskList.tsx`
3. Create `frontend/src/components/tasks/EmptyState.tsx`
4. Integrate into `frontend/app/dashboard/page.tsx`

**Day 3-4: Task Forms**
1. Create `frontend/src/components/tasks/TaskForm.tsx`
2. Add form validation logic
3. Integrate create/edit functionality
4. Test with backend API

**Day 5: Utility Components**
1. Create `frontend/src/components/ui/Badge.tsx`
2. Create `frontend/src/components/ui/Skeleton.tsx`
3. Add loading states to all async operations

---

### Week 3: Polish & Testing

**Day 1-2: Animations**
1. Create `frontend/src/lib/animations.ts`
2. Implement page transitions
3. Add task creation/deletion animations
4. Implement completion toggle animation

**Day 3: Accessibility Audit**
1. Test keyboard navigation
2. Verify focus indicators
3. Check color contrast ratios
4. Test with screen reader (Narrator/NVDA)

**Day 4: Responsive Testing**
1. Test at 320px, 768px, 1024px, 1440px
2. Fix any layout issues
3. Verify touch targets on mobile
4. Test orientation changes

**Day 5: Performance**
1. Run Lighthouse audit
2. Optimize animations if needed
3. Check bundle size
4. Fix any CLS issues

---

## Testing Guidelines

### Manual Testing Checklist

**For each component**:
- [ ] Renders correctly in all states
- [ ] Hover states work
- [ ] Focus states visible
- [ ] Disabled states clear
- [ ] Mobile responsive
- [ ] Keyboard accessible
- [ ] Screen reader friendly

**For each page**:
- [ ] Loads without errors
- [ ] Responsive at all breakpoints
- [ ] Forms validate correctly
- [ ] Errors display properly
- [ ] Loading states show
- [ ] Animations smooth (no jank)

---

### Browser DevTools Testing

**Chrome DevTools**:
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test responsive modes:
   - iPhone SE (375px)
   - iPad (768px)
   - iPad Pro (1024px)
   - Desktop (1440px)

**Lighthouse Audit**:
1. Open DevTools
2. Go to Lighthouse tab
3. Select: Performance, Accessibility, Best Practices, SEO
4. Run audit
5. Target scores: All ≥90

**Performance Panel**:
1. Record page load
2. Check for layout shifts
3. Verify animations are GPU-accelerated
4. Look for long tasks (>50ms)

---

### Accessibility Testing

**Automated Tools**:
```bash
# Install axe-core (optional)
npm install -g @axe-core/cli

# Run accessibility audit
axe http://localhost:3000
```

**Manual Testing**:
1. **Keyboard Navigation**:
   - Tab through all interactive elements
   - Enter/Space activate buttons
   - Escape closes modals
   - Arrow keys navigate menus

2. **Focus Indicators**:
   - All focus rings visible
   - 2px minimum width
   - High contrast color

3. **Screen Reader** (Windows Narrator):
   - Press Win+Ctrl+Enter to start
   - Navigate with Tab
   - Verify labels read correctly
   - Check state announcements

4. **Color Contrast**:
   - Use WebAIM Contrast Checker
   - Test all text/background combinations
   - Verify 4.5:1 ratio for normal text
   - Verify 3:1 ratio for large text

---

## Common Development Tasks

### Adding a New Component

```bash
# 1. Create component file
New-Item -Path "frontend/src/components/ui/NewComponent.tsx" -ItemType File

# 2. Add component code (use template)
# 3. Export from components/index.ts (if using)
# 4. Test in isolation
# 5. Integrate into pages
```

### Updating Design Tokens

```css
/* 1. Update globals.css */
:root {
  --color-new-token: #value;
}

/* 2. Update tailwind.config.js */
module.exports = {
  theme: {
    extend: {
      colors: {
        'new-token': 'var(--color-new-token)',
      }
    }
  }
}

/* 3. Restart dev server if needed */
npm run dev
```

### Adding Animations

```css
/* 1. Define keyframe in globals.css */
@keyframes myAnimation {
  from { /* start state */ }
  to { /* end state */ }
}

/* 2. Create utility class */
.animate-my-animation {
  animation: myAnimation 300ms ease-out;
}

/* 3. Use in component */
<div className="animate-my-animation">
  Content
</div>
```

---

## Troubleshooting

### Issue: Styles Not Updating

**Solution**:
```bash
# Clear Next.js cache
rm -rf .next

# Restart dev server
npm run dev
```

### Issue: TypeScript Errors

**Solution**:
```bash
# Check TypeScript config
cat tsconfig.json

# Verify types are installed
npm list @types/react @types/node

# Reinstall if needed
npm install --save-dev @types/react @types/node
```

### Issue: Tailwind Classes Not Working

**Solution**:
```bash
# Check tailwind.config.js content paths
# Should include:
# './app/**/*.{js,ts,jsx,tsx,mdx}',
# './src/**/*.{js,ts,jsx,tsx,mdx}',

# Restart dev server
npm run dev
```

### Issue: Animations Not Smooth

**Solution**:
```css
/* Ensure using GPU-accelerated properties */
/* Good: transform, opacity */
/* Bad: top, left, width, height */

.element {
  transform: translateY(0); /* ✓ */
  opacity: 1; /* ✓ */
}
```

---

## Code Quality

### ESLint Configuration

```bash
# Run linter
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

### Prettier Formatting

```bash
# Format all files
npx prettier --write "src/**/*.{ts,tsx}"

# Or configure VS Code to format on save
```

### TypeScript Strict Mode

Ensure `tsconfig.json` has:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  }
}
```

---

## Deployment Preview

### Build for Production

```bash
# Create production build
npm run build

# Analyze bundle size
npm run build -- --stats

# Preview production build
npm run start
```

**Expected Output**:
```
✓ Compiled successfully
✓ Building pages...
✓ Generating static pages
✓ Collecting page data
✓ Finalizing page optimization

Route (app)                              Size     First Load JS
┌ ○ /                                    2.1 kB        85.3 kB
├ ○ /login                               1.8 kB        82.1 kB
├ ○ /signup                              1.9 kB        82.2 kB
└ ● /dashboard                           3.2 kB        95.4 kB
```

---

## Resources

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Docs](https://react.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs)

### Design Systems
- [Material Design 3](https://m3.material.io)
- [Tailwind UI](https://tailwindui.com)
- [IBM Carbon](https://carbondesignsystem.com)

### Accessibility
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker)
- [A11y Project](https://www.a11yproject.com)

### Performance
- [Web.dev](https://web.dev)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools)
- [Core Web Vitals](https://web.dev/vitals)

---

## Getting Help

**During Implementation**:
1. Check specification documents in `specs/004-ui-ux-upgrade/`
2. Review component contracts in `contracts/components.md`
3. Reference design tokens in `data-model.md`
4. Consult research decisions in `research.md`

**Common Issues**:
- Component not rendering: Check imports and exports
- Styles not applying: Verify Tailwind config and CSS imports
- Animations not working: Check CSS syntax and browser support
- Accessibility failures: Use automated tools + manual testing

---

**Status**: ✅ Ready for Development

**Next Step**: Begin Week 1 implementation (Design System Foundation)

**Success Metrics**:
- All design tokens implemented
- Base components created and tested
- Tailwind configuration updated
- Development environment stable
