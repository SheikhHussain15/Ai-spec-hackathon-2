# UI/UX Upgrade - Testing Checklist

**Feature**: 004-ui-ux-upgrade
**Created**: 2026-02-16
**Status**: In Progress

---

## Responsive Design Testing

### Breakpoints to Test

- [ ] **320px** (Small mobile)
  - [ ] Home page - no horizontal scroll
  - [ ] Login page - form usable
  - [ ] Signup page - all fields accessible
  - [ ] Dashboard - tasks readable

- [ ] **375px** (iPhone SE)
  - [ ] All pages layout correctly
  - [ ] Touch targets 44px minimum
  - [ ] Text readable without zoom

- [ ] **768px** (Tablet portrait)
  - [ ] Home page - buttons side-by-side or stacked
  - [ ] Forms - comfortable layout
  - [ ] Dashboard - 2-column task grid

- [ ] **1024px** (Tablet landscape)
  - [ ] Dashboard - 3-column layout
  - [ ] All content centered properly
  - [ ] No excessive whitespace

- [ ] **1440px** (Desktop)
  - [ ] All pages use space efficiently
  - [ ] Forms have appropriate max-width
  - [ ] Dashboard shows task grid effectively

---

## Visual Design Consistency

### Color Usage

- [ ] Primary actions use primary-500
- [ ] Hover states use primary-600
- [ ] Active states use primary-700
- [ ] Error states use error-500
- [ ] Success states use success-500
- [ ] Text uses gray-900 (headings), gray-700 (body), gray-500 (secondary)

### Typography Hierarchy

- [ ] H1: 36px (4xl), bold
- [ ] H2: 24px (2xl), semibold
- [ ] H3: 20px (xl), semibold
- [ ] Body: 16px (base), normal
- [ ] Secondary text: 14px (sm), gray-500
- [ ] Captions: 12px (xs), gray-500

### Spacing Consistency

- [ ] Component padding uses spacing tokens (4, 6, 8)
- [ ] Section margins use spacing tokens (12, 16, 24)
- [ ] Gap between elements follows 4px grid
- [ ] No random pixel values

---

## Component States

### Buttons

- [ ] Default state visible
- [ ] Hover state (darker, elevated shadow)
- [ ] Active state (pressed appearance)
- [ ] Focus state (2px ring with offset)
- [ ] Disabled state (gray, reduced opacity)
- [ ] Loading state (spinner, disabled)

### Inputs

- [ ] Default state (gray border)
- [ ] Focus state (primary border, ring)
- [ ] Error state (red border, error message)
- [ ] Disabled state (gray background)

### Interactive Elements

- [ ] All links have hover state
- [ ] All buttons have focus ring
- [ ] All checkboxes/radios have clear states
- [ ] Focus visible on keyboard navigation

---

## Accessibility Testing

### Keyboard Navigation

- [ ] Tab through all interactive elements
- [ ] Enter/Space activate buttons
- [ ] Escape closes modals/dropdowns
- [ ] Focus order logical (top to bottom, left to right)
- [ ] Focus indicator visible on all elements

### Screen Reader (Windows Narrator)

- [ ] All inputs have associated labels
- [ ] Error messages announced
- [ ] Button text descriptive
- [ ] Page titles meaningful
- [ ] Skip to main content link (if applicable)

### Color Contrast

- [ ] Normal text: 4.5:1 minimum ratio
- [ ] Large text (18px+): 3:1 minimum ratio
- [ ] UI components: 3:1 minimum ratio
- [ ] Focus indicators: visible on all backgrounds

### Focus Indicators

- [ ] 2px minimum width
- [ ] High contrast color
- [ ] Visible on all backgrounds
- [ ] Consistent across all elements

---

## Animation Testing

### Performance

- [ ] All transitions smooth (no jank)
- [ ] Animations complete in 200-300ms
- [ ] No layout shifts during animations
- [ ] 60fps during page transitions

### Reduced Motion

- [ ] Test with `prefers-reduced-motion: reduce` enabled
- [ ] All animations reduce to instant/no motion
- [ ] Functionality still works without animations

### Specific Animations

- [ ] Page transitions (fade in + slide up)
- [ ] Button hover (scale + shadow)
- [ ] Input focus (border color + ring)
- [ ] Task creation (fade in + slide up)
- [ ] Task deletion (fade out + scale down)
- [ ] Task completion toggle (pulse)
- [ ] Loading skeletons (shimmer)

---

## Form UX Testing

### Login Form

- [ ] Email field auto-focus on mount
- [ ] Labels clear and visible
- [ ] Placeholder text helpful
- [ ] Error messages inline near field
- [ ] Loading state during submit
- [ ] Button disabled during processing
- [ ] Success redirects to dashboard

### Signup Form

- [ ] All fields clearly labeled
- [ ] Password requirements clear (if any)
- [ ] Password match validation real-time
- [ ] Error messages specific and actionable
- [ ] Loading state during registration
- [ ] Success redirects to dashboard or login

### Error Handling

- [ ] Invalid email shows error
- [ ] Wrong password shows error
- [ ] Network errors show user-friendly message
- [ ] Errors clear on successful submission
- [ ] Focus moves to first error on submit failure

---

## Loading States

### Skeleton Loaders

- [ ] Skeleton matches content layout
- [ ] Shimmer animation subtle (not distracting)
- [ ] No layout shift when content loads
- [ ] Reduced motion respected

### Processing States

- [ ] Buttons show spinner during async operations
- [ ] Disabled state prevents double-submission
- [ ] Loading text clear (e.g., "Signing in...")
- [ ] Cursor changes to not-allowed when disabled

---

## Lighthouse Audits

### Performance

- [ ] Score ≥90
- [ ] First Contentful Paint <1.5s
- [ ] Time to Interactive <3.5s
- [ ] Cumulative Layout Shift = 0
- [ ] Total Blocking Time <200ms

### Accessibility

- [ ] Score ≥90
- [ ] No contrast errors
- [ ] All elements labeled
- [ ] Focus indicators present
- [ ] Keyboard navigation works

### Best Practices

- [ ] Score ≥90
- [ ] No deprecated APIs
- [ ] No browser errors
- [ ] HTTPS (in production)

### SEO

- [ ] Score ≥90 (if applicable)
- [ ] Meta descriptions present
- [ ] Page titles descriptive
- [ ] Headings in logical order

---

## Cross-Browser Testing

### Chrome

- [ ] All features work
- [ ] Animations smooth
- [ ] DevTools audit passes

### Firefox

- [ ] All features work
- [ ] Fonts render correctly
- [ ] Animations smooth

### Safari (if available)

- [ ] All features work
- [ ] Touch targets appropriate
- [ ] Animations smooth

### Edge

- [ ] All features work
- [ ] Consistent with Chrome
- [ ] DevTools audit passes

---

## Edge Cases

### Long Content

- [ ] Long task titles truncate with ellipsis
- [ ] Full text available on hover/focus
- [ ] Long descriptions wrap correctly
- [ ] No layout breaks with long content

### Empty States

- [ ] Empty dashboard shows friendly message
- [ ] Call-to-action button visible
- [ ] Illustration or icon present (if applicable)

### Error States

- [ ] Network error shows recovery option
- [ ] Server error shows user-friendly message
- [ ] 404 page helpful (if applicable)

### Window Resize

- [ ] Layout adapts smoothly
- [ ] No content lost during resize
- [ ] No JavaScript errors on resize

---

## Sign-Off

### Visual Design (US1)

- [ ] All pages follow design system
- [ ] Typography hierarchy consistent
- [ ] Color usage consistent
- [ ] Spacing follows 4px grid
- [ ] **Status**: PASS / FAIL

### Responsive Layout (US2)

- [ ] All breakpoints tested
- [ ] No horizontal scroll at 320px
- [ ] Touch targets 44px minimum
- [ ] Content readable at all sizes
- [ ] **Status**: PASS / FAIL

### Animations (US3)

- [ ] All transitions smooth
- [ ] Durations 200-300ms
- [ ] Reduced motion respected
- [ ] Performance 60fps
- [ ] **Status**: PASS / FAIL

### Form UX (US4)

- [ ] Labels clear
- [ ] Errors inline and helpful
- [ ] Loading states present
- [ ] Accessibility verified
- [ ] **Status**: PASS / FAIL

### Dashboard (US5)

- [ ] Task hierarchy clear
- [ ] Empty state helpful
- [ ] Actions accessible
- [ ] Loading states present
- [ ] **Status**: PASS / FAIL

---

**Overall Status**: PENDING / PASS / FAIL

**Tested By**: ________________
**Date**: ________________
**Browser/OS**: ________________
**Device**: ________________

**Notes**:

