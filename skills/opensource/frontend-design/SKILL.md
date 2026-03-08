---
name: frontend-design
description: Generate modern, responsive frontend UI designs and components. Supports React, Vue, Angular, and plain HTML/CSS/JS with Tailwind CSS, Material UI, and Ant Design.
author: openclaw
version: 1.0.0
---

# Frontend Design Skill

## Overview

Generate modern, responsive frontend UI designs and components:
- **Component Generation**: React, Vue, Angular, Svelte components
- **Styling**: Tailwind CSS, Material UI, Ant Design, styled-components
- **Responsive Design**: Mobile-first, adaptive layouts
- **Accessibility**: WCAG 2.1 compliance, ARIA attributes
- **Best Practices**: Performance, SEO, modern patterns

## Supported Frameworks

| Framework | Version | Components | Styling |
|-----------|---------|------------|---------|
| React | 18+ | Functional, Hooks | Tailwind, MUI, CSS Modules |
| Vue | 3+ | Composition API | Tailwind, Element Plus |
| Angular | 15+ | Standalone Components | Angular Material, Tailwind |
| Svelte | 4+ | Svelte Components | Tailwind, native CSS |
| Plain HTML/CSS | HTML5, CSS3 | Semantic HTML | Tailwind, Bootstrap, custom |

## Design Categories

### 1. Layout Components

| Component | Description | Use Case |
|-----------|-------------|----------|
| Container | Responsive wrapper | Page layout |
| Grid/Flex | Layout systems | Content arrangement |
| Header/Nav | Navigation | Site navigation |
| Sidebar | Side navigation | Admin panels, docs |
| Footer | Page footer | Links, copyright |

### 2. Form Components

| Component | Description | Use Case |
|-----------|-------------|----------|
| Input | Text, number, email | User input |
| Select | Dropdown selection | Options selection |
| Checkbox/Radio | Boolean/multiple choice | Preferences |
| Textarea | Multi-line input | Comments, descriptions |
| File Upload | File selection | Document upload |
| Form Validation | Error handling | Input validation |

### 3. Data Display

| Component | Description | Use Case |
|-----------|-------------|----------|
| Table | Data tables | Data grids |
| Card | Content cards | Product cards, posts |
| List | Item lists | Feed, inventory |
| Modal | Dialog overlays | Confirmations, forms |
| Tooltip | Hover hints | Help text |
| Badge | Status indicators | Notifications |

### 4. Navigation

| Component | Description | Use Case |
|-----------|-------------|----------|
| Button | Action triggers | Submit, navigate |
| Link | Navigation links | Internal/external links |
| Breadcrumb | Path navigation | Hierarchical navigation |
| Pagination | Page navigation | Large datasets |
| Tabs | Tabbed navigation | Content sections |
| Menu | Dropdown menus | Action menus |

### 5. Feedback

| Component | Description | Use Case |
|-----------|-------------|----------|
| Alert | Notifications | Success, error, warning |
| Toast | Temporary messages | Action feedback |
| Progress | Loading indicators | Progress bars, spinners |
| Skeleton | Loading placeholders | Content loading |

## Usage

### Generate a Component

```bash
# Generate React component
Create a React login form with Tailwind CSS

# Generate Vue component
Create a Vue 3 data table with sorting and pagination

# Generate Angular component
Create an Angular dashboard with sidebar navigation
```

### Generate a Page

```bash
# Full page design
Design a responsive product landing page

# Admin dashboard
Create an admin dashboard with charts and data tables

# E-commerce page
Design a product listing page with filters
```

### Redesign Existing UI

```bash
# Improve existing component
Modernize this login form: [paste code]

# Make responsive
Make this layout mobile-responsive: [paste code]

# Improve accessibility
Add WCAG compliance to this component: [paste code]
```

## Component Templates

### React + Tailwind CSS

```tsx
// components/Button.tsx
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  children,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
    ghost: 'text-gray-600 hover:bg-gray-100 focus:ring-gray-500',
  };
  
  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      )}
      {children}
    </button>
  );
};
```

### Vue 3 + Tailwind CSS

```vue
<!-- components/Card.vue -->
<template>
  <div :class="['bg-white rounded-xl shadow-lg overflow-hidden', cardClass]">
    <div v-if="$slots.header" class="px-6 py-4 border-b border-gray-200">
      <slot name="header" />
    </div>
    
    <div :class="['px-6 py-4', contentClass]">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="px-6 py-4 bg-gray-50 border-t border-gray-200">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  cardClass?: string;
  contentClass?: string;
}

withDefaults(defineProps<Props>(), {
  cardClass: '',
  contentClass: '',
});
</script>
```

### Angular + Material

```typescript
// components/data-table/data-table.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';

export interface Column<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  template?: (item: T) => string;
}

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent<T> {
  @Input() data: T[] = [];
  @Input() columns: Column<T>[] = [];
  @Input() pageSize = 10;
  @Output() rowClick = new EventEmitter<T>();
  
  dataSource = new MatTableDataSource<T>();
  displayedColumns: string[] = [];
  
  ngOnInit() {
    this.displayedColumns = this.columns.map(c => c.key as string);
    this.dataSource.data = this.data;
  }
  
  onRowClick(row: T) {
    this.rowClick.emit(row);
  }
}
```

```html
<!-- data-table.component.html -->
<table mat-table [dataSource]="dataSource" class="mat-elevation-z8">
  <ng-container *ngFor="let column of columns" [matColumnDef]="column.key">
    <th mat-header-cell *matHeaderCellDef [class.sortable]="column.sortable">
      {{ column.label }}
    </th>
    <td mat-cell *matCellDef="let item">
      {{ column.template ? column.template(item) : item[column.key] }}
    </td>
  </ng-container>
  
  <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
  <tr mat-row *matRowDef="let row; columns: displayedColumns;" 
      (click)="onRowClick(row)"
      class="cursor-pointer hover:bg-gray-50">
  </tr>
</table>

<mat-paginator [pageSize]="pageSize" showFirstLastButtons></mat-paginator>
```

## Design Principles

### 1. Responsive Design

```css
/* Mobile-first approach */
.container {
  @apply w-full px-4;
}

@media (min-width: 640px) {
  .container {
    @apply max-w-screen-sm mx-auto;
  }
}

@media (min-width: 768px) {
  .container {
    @apply max-w-screen-md;
  }
}

@media (min-width: 1024px) {
  .container {
    @apply max-w-screen-lg;
  }
}

@media (min-width: 1280px) {
  .container {
    @apply max-w-screen-xl;
  }
}
```

### 2. Accessibility (WCAG 2.1)

```tsx
// Accessible Modal Component
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      return () => { document.body.style.overflow = 'unset'; };
    }
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center"
    >
      <div className="fixed inset-0 bg-black/50" onClick={onClose} aria-hidden="true" />
      
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 id="modal-title" className="text-lg font-semibold">{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close modal"
            className="p-1 hover:bg-gray-100 rounded"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-4">{children}</div>
      </div>
    </div>
  );
};
```

### 3. Performance Optimization

```tsx
// Lazy loaded component
const HeavyChart = lazy(() => import('./HeavyChart'));

// Memoized component
const ExpensiveComponent = memo(({ data }) => {
  return (
    <div>
      {data.map(item => (
        <Item key={item.id} item={item} />
      ))}
    </div>
  );
});

// Virtualized list for large datasets
import { FixedSizeList } from 'react-window';

const VirtualList = ({ items }) => (
  <FixedSizeList
    height={600}
    itemCount={items.length}
    itemSize={50}
  >
    {({ index, style }) => (
      <div style={style}>
        <Item item={items[index]} />
      </div>
    )}
  </FixedSizeList>
);
```

## Integration

Works with:
- `code-review` - Review generated components
- `code-simplifier` - Simplify complex components
- `test-case-generator` - Generate component tests
- `xiaohongshu-mcp` - Design social media content pages

## Best Practices

### Code Organization

```
src/
├── components/
│   ├── ui/           # Reusable UI components
│   │   ├── Button/
│   │   ├── Card/
│   │   └── Modal/
│   ├── forms/        # Form components
│   ├── layout/       # Layout components
│   └── features/     # Feature-specific components
├── hooks/            # Custom hooks
├── styles/           # Global styles
├── utils/            # Utility functions
└── types/            # TypeScript types
```

### Naming Conventions

- **Components**: PascalCase (`UserProfile`, `DataTable`)
- **Files**: Match component name (`UserProfile.tsx`)
- **Props**: TypeScript interfaces (`UserProfileProps`)
- **CSS**: BEM or utility classes (`user-profile__avatar`, `bg-blue-500`)

### Testing

```tsx
// __tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('shows loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Commands

| Command | Description |
|---------|-------------|
| `generate-component <name>` | Generate a new component |
| `generate-page <name>` | Generate a full page |
| `redesign <code>` | Improve existing UI code |
| `make-responsive <code>` | Add responsive design |
| `add-accessibility <code>` | Add WCAG compliance |

## Color Palettes

### Modern Color Schemes

```css
/* Professional Blue */
--primary: #2563eb;
--primary-dark: #1d4ed8;
--primary-light: #3b82f6;

/* Success Green */
--success: #10b981;
--success-dark: #059669;

/* Warning Yellow */
--warning: #f59e0b;
--warning-dark: #d97706;

/* Error Red */
--error: #ef4444;
--error-dark: #dc2626;

/* Neutral Grays */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;
```

## Examples

### Login Form (React + Tailwind)

```tsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">Email address</label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Password"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```
