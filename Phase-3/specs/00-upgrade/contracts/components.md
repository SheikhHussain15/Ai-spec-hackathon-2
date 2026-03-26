# UI Component Contracts

**Feature**: UI/UX Upgrade
**Branch**: 004-ui-ux-upgrade
**Date**: 2026-02-16

## Overview

This document defines the API contracts for reusable UI components. Each component specification includes props, states, accessibility requirements, and usage examples.

---

## Base Components

### Button Component

**File**: `frontend/src/components/ui/Button.tsx`

**Purpose**: Primary interactive element for actions

**Props**:
```typescript
interface ButtonProps {
  // Content
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  
  // State
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  
  // Behavior
  type?: 'button' | 'submit' | 'reset';
  onClick?: (e: React.MouseEvent) => void;
  
  // Accessibility
  'aria-label'?: string;
  'aria-disabled'?: boolean;
  
  // Styling
  className?: string;
  style?: React.CSSProperties;
}
```

**Visual States**:
- **Default**: Primary color background, white text, subtle shadow
- **Hover**: Darker shade, elevated shadow
- **Active**: Even darker shade, pressed appearance
- **Focus**: 2px ring with offset
- **Disabled**: Gray background, reduced opacity, not-allowed cursor
- **Loading**: Spinner replaces icon, disabled interaction

**Accessibility**:
- Keyboard accessible (Enter/Space to activate)
- Clear focus indicator
- Loading state announced to screen readers
- Disabled state properly marked

**Usage Example**:
```tsx
<Button 
  variant="primary" 
  size="md"
  onClick={handleClick}
  loading={isSubmitting}
>
  Submit
</Button>
```

---

### Input Component

**File**: `frontend/src/components/ui/Input.tsx`

**Purpose**: Form input field with validation

**Props**:
```typescript
interface InputProps {
  // Content
  label: string;
  placeholder?: string;
  type?: 'text' | 'email' | 'password' | 'number';
  
  // State
  value: string;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  
  // Behavior
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent) => void;
  onFocus?: (e: React.FocusEvent) => void;
  
  // Accessibility
  'aria-describedby'?: string;
  'aria-invalid'?: boolean;
  id: string;
  
  // Styling
  className?: string;
  icon?: React.ReactNode;
}
```

**Visual States**:
- **Default**: Gray border, dark text
- **Focus**: Primary color border, ring
- **Error**: Red border, error message below
- **Disabled**: Gray background, not-allowed cursor
- **With Icon**: Icon on left side, proper padding

**Accessibility**:
- Associated label via htmlFor
- Error messages linked via aria-describedby
- Required fields marked
- Invalid state announced

**Usage Example**:
```tsx
<Input
  id="email"
  label="Email Address"
  type="email"
  value={email}
  onChange={setEmail}
  error={errors.email}
  required
/>
```

---

### Card Component

**File**: `frontend/src/components/ui/Card.tsx`

**Purpose**: Container for grouping related content

**Props**:
```typescript
interface CardProps {
  // Content
  children: React.ReactNode;
  title?: string;
  description?: string;
  
  // State
  clickable?: boolean;
  selected?: boolean;
  
  // Behavior
  onClick?: () => void;
  
  // Styling
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  shadow?: 'none' | 'sm' | 'md' | 'lg';
}
```

**Visual States**:
- **Default**: White background, subtle border, shadow
- **Hover** (if clickable): Elevated shadow, cursor pointer
- **Selected**: Primary color border, subtle background tint

**Accessibility**:
- Semantic HTML (article or div with role)
- Clickable cards keyboard accessible
- Selected state visually distinct

**Usage Example**:
```tsx
<Card
  title="Task Title"
  description="Task description"
  clickable
  onClick={handleCardClick}
>
  {children}
</Card>
```

---

### Badge Component

**File**: `frontend/src/components/ui/Badge.tsx`

**Purpose**: Status indicator or label

**Props**:
```typescript
interface BadgeProps {
  // Content
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md';
  
  // Styling
  className?: string;
  icon?: React.ReactNode;
}
```

**Visual States**:
- **Default**: Gray background, dark text
- **Success**: Green background, dark green text
- **Warning**: Yellow background, dark yellow text
- **Error**: Red background, dark red text
- **Info**: Blue background, dark blue text

**Accessibility**:
- Sufficient contrast ratio
- Icon + text for status (not icon alone)

**Usage Example**:
```tsx
<Badge variant="success">
  <CheckIcon className="w-3 h-3 mr-1" />
  Completed
</Badge>
```

---

### Skeleton Component

**File**: `frontend/src/components/ui/Skeleton.tsx`

**Purpose**: Loading placeholder for content

**Props**:
```typescript
interface SkeletonProps {
  // Shape
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded';
  
  // Sizing
  width?: string | number;
  height?: string | number;
  lines?: number;  // For text variant
  
  // Styling
  className?: string;
  animation?: 'shimmer' | 'pulse' | 'none';
}
```

**Visual States**:
- **Default**: Gray background with shimmer animation
- **Pulse**: Opacity animation
- **Shimmer**: Gradient sweep animation

**Accessibility**:
- aria-busy="true" on loading container
- Screen readers announce loading state
- Reduced motion respected

**Usage Example**:
```tsx
<Skeleton variant="text" lines={3} height={20} />
```

---

## Layout Components

### Container Component

**File**: `frontend/src/components/layout/Container.tsx`

**Purpose**: Responsive content container

**Props**:
```typescript
interface ContainerProps {
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  centered?: boolean;
  className?: string;
}
```

**Behavior**:
- Applies max-width based on size prop
- Centers content horizontally
- Responsive padding (mobile: 16px, desktop: 24px)

**Usage Example**:
```tsx
<Container size="lg" centered>
  {children}
</Container>
```

---

### Grid Component

**File**: `frontend/src/components/layout/Grid.tsx`

**Purpose**: Responsive grid layout

**Props**:
```typescript
interface GridProps {
  children: React.ReactNode;
  columns?: 1 | 2 | 3 | 4 | 6 | 12;
  gap?: 'sm' | 'md' | 'lg' | 'xl';
  responsive?: boolean;
  className?: string;
}
```

**Behavior**:
- Creates grid with specified columns
- Responsive: stacks on mobile, expands on desktop
- Consistent gap between items

**Usage Example**:
```tsx
<Grid columns={3} gap="md" responsive>
  {items.map(item => <Card key={item.id}>{item}</Card>)}
</Grid>
```

---

## Task-Specific Components

### TaskCard Component

**File**: `frontend/src/components/tasks/TaskCard.tsx`

**Purpose**: Display individual task with actions

**Props**:
```typescript
interface TaskCardProps {
  // Data
  task: {
    id: string;
    title: string;
    description: string;
    completed: boolean;
    createdAt: string;
    updatedAt: string;
  };
  
  // Behavior
  onToggle: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  
  // State
  loading?: boolean;
  
  // Styling
  className?: string;
}
```

**Layout**:
```
┌─────────────────────────────────────────────┐
│ ☐ Task Title                    [Pending]  │
│    Task description text...                 │
│    Feb 16, 2026            [Edit] [Delete] │
└─────────────────────────────────────────────┘
```

**Visual Hierarchy**:
1. **Title**: Bold, prominent (16px, gray-900)
2. **Description**: Regular weight (14px, gray-600)
3. **Metadata**: Small, muted (12px, gray-500)
4. **Actions**: Icon buttons, right-aligned

**Animations**:
- Fade in on creation
- Slide out on deletion
- Smooth toggle transition

**Accessibility**:
- Checkbox labeled with task title
- Actions keyboard accessible
- Completed state announced

**Usage Example**:
```tsx
<TaskCard
  task={task}
  onToggle={handleToggle}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

---

### TaskList Component

**File**: `frontend/src/components/tasks/TaskList.tsx`

**Purpose**: Container for task cards with animations

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  onToggle: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}
```

**Behavior**:
- Renders empty state if no tasks
- Shows skeleton loaders while loading
- Animates task entry/exit
- Groups completed/pending (optional)

**Usage Example**:
```tsx
<TaskList
  tasks={tasks}
  loading={isLoading}
  onToggle={toggleTask}
  onEdit={editTask}
  onDelete={deleteTask}
/>
```

---

### TaskForm Component

**File**: `frontend/src/components/tasks/TaskForm.tsx`

**Purpose**: Create or edit task form

**Props**:
```typescript
interface TaskFormProps {
  // Mode
  mode?: 'create' | 'edit';
  
  // Data
  initialData?: Task;
  
  // Behavior
  onSubmit: (data: CreateTaskInput | UpdateTaskInput) => void;
  onCancel: () => void;
  
  // State
  loading?: boolean;
  errors?: FormErrors;
}
```

**Fields**:
- Title (required, max 100 chars)
- Description (optional, max 500 chars)

**Validation**:
- Title required
- Title max length
- Real-time validation on blur

**Usage Example**:
```tsx
<TaskForm
  mode="create"
  onSubmit={createTask}
  onCancel={closeModal}
  loading={isSubmitting}
/>
```

---

### EmptyState Component

**File**: `frontend/src/components/tasks/EmptyState.tsx`

**Purpose**: Display when no tasks exist

**Props**:
```typescript
interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel: string;
  onAction: () => void;
  icon?: React.ReactNode;
}
```

**Layout**:
```
┌─────────────────────────┐
│      [Icon/Illustration]│
│                         │
│    No Tasks Yet         │
│    Create your first    │
│    task to get started  │
│                         │
│    [+ Create Task]      │
└─────────────────────────┘
```

**Accessibility**:
- Clear, friendly language
- Action button prominent
- Icon decorative (aria-hidden)

**Usage Example**:
```tsx
<EmptyState
  title="No Tasks Yet"
  description="Create your first task to get started"
  actionLabel="Create Task"
  onAction={openCreateForm}
  icon={<PlusCircleIcon className="w-16 h-16" />}
/>
```

---

## Page Components

### Header Component

**File**: `frontend/src/components/layout/Header.tsx`

**Purpose**: Page header with navigation

**Props**:
```typescript
interface HeaderProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  onBack?: () => void;
}
```

**Usage Example**:
```tsx
<Header
  title="Your Tasks"
  subtitle="Manage your daily goals"
  actions={
    <Button onClick={handleLogout}>Logout</Button>
  }
/>
```

---

## Animation Specifications

### Page Transitions

**Implementation**: CSS transitions on page mount/unmount

```css
.page-enter {
  opacity: 0;
  transform: translateY(8px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms ease-out, transform 300ms ease-out;
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 200ms ease-in;
}
```

---

### Task Creation Animation

**Sequence**:
1. Form submits
2. Optimistic UI update
3. New task fades in with slide up
4. List reflows smoothly

```css
@keyframes taskEnter {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.task-enter {
  animation: taskEnter 300ms ease-out;
}
```

---

### Task Deletion Animation

**Sequence**:
1. User confirms delete
2. Task fades out with scale down
3. Remaining tasks slide up
4. Empty state appears if needed

```css
@keyframes taskExit {
  from {
    opacity: 1;
    transform: scale(1);
    max-height: 200px;
  }
  to {
    opacity: 0;
    transform: scale(0.95);
    max-height: 0;
    margin: 0;
    padding: 0;
  }
}

.task-exit {
  animation: taskExit 300ms ease-in forwards;
}
```

---

### Completion Toggle Animation

**Sequence**:
1. User clicks checkbox
2. Checkbox animates (checkmark draws)
3. Title gets strikethrough
4. Badge changes color
5. Subtle scale pulse

```css
.task-complete {
  animation: completePulse 200ms ease-out;
}

@keyframes completePulse {
  0% { transform: scale(1); }
  50% { transform: scale(0.98); }
  100% { transform: scale(1); }
}
```

---

## Component Testing Guidelines

### Visual Regression Testing

**Checklist for each component**:
- [ ] All variants render correctly
- [ ] All states visible and distinct
- [ ] Responsive breakpoints work
- [ ] Dark mode compatible (if applicable)
- [ ] Focus indicators visible
- [ ] Disabled states clear

### Accessibility Testing

**Checklist for each component**:
- [ ] Keyboard navigable
- [ ] Focus indicators visible
- [ ] Screen reader announcements correct
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets 44px minimum
- [ ] Reduced motion respected

### Performance Testing

**Checklist for each component**:
- [ ] No layout shift on render
- [ ] Animations GPU-accelerated
- [ ] No unnecessary re-renders
- [ ] Lazy loaded if not critical
- [ ] Bundle size impact acceptable

---

## Implementation Priority

**Phase 1 - Foundation** (Week 1):
1. Button, Input, Card (base components)
2. Container, Grid (layout)
3. Design tokens implementation

**Phase 2 - Task Components** (Week 2):
1. TaskCard, TaskList
2. TaskForm, EmptyState
3. Badge, Skeleton

**Phase 3 - Polish** (Week 3):
1. Animations and transitions
2. Accessibility audit
3. Performance optimization
4. Cross-browser testing

---

**Status**: ✅ Complete - Component contracts ready for implementation

**Next**: quickstart.md for setup and development guide
