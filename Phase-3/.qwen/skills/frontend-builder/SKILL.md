---
name: frontend-builder
description: Build responsive frontend pages and reusable components with clean layouts and modern styling. Use for UI development tasks.
---

# Frontend Page & Component Building

## Instructions

1. **Page structure**
   - Use semantic HTML (`header`, `main`, `section`, `footer`)
   - Clear content hierarchy
   - Reusable layout patterns (grid, flex)

2. **Components**
   - Break UI into small, reusable components
   - Single responsibility per component
   - Props/variants for flexibility (if using frameworks)

3. **Layout & styling**
   - Mobile-first responsive design
   - Flexbox and CSS Grid for layout
   - Consistent spacing, typography, and colors
   - Use design tokens or CSS variables

4. **Styling approach**
   - Prefer modern CSS (Flexbox, Grid)
   - Utility-first or component-scoped styles
   - Avoid inline styles unless necessary

5. **Accessibility**
   - Proper heading order
   - Sufficient color contrast
   - Keyboard-friendly interactions

## Best Practices
- Start with mobile, scale up
- Keep components small and composable
- Use consistent spacing (4px or 8px system)
- Avoid over-nesting HTML
- Optimize for readability and maintainability
- Test layout at multiple breakpoints

## Common Layout Patterns
- Navbar + content + footer
- Sidebar + main content
- Card-based grid layouts
- Responsive columns

## Example Structure

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Frontend Page</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header class="site-header">
      <h1 class="logo">My App</h1>
      <nav class="nav">
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Contact</a>
      </nav>
    </header>

    <main class="container">
      <section class="card-grid">
        <article class="card">
          <h2>Card Title</h2>
          <p>Card description content.</p>
          <button class="btn-primary">Action</button>
        </article>
        <article class="card">
          <h2>Another Card</h2>
          <p>More supporting content.</p>
          <button class="btn-primary">Action</button>
        </article>
      </section>
    </main>

    <footer class="site-footer">
      <p>&copy; 2026 My App</p>
    </footer>
  </body>
</html>
