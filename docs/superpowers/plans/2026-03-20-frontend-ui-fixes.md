# Frontend UI Comprehensive Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix MigratePage blank screen, improve UI spacing/layout, add responsive sidebar, fix component overlaps and inconsistencies across all frontend pages.

**Architecture:** Systematic refactoring of React components with consistent spacing tokens, proper loading states, responsive sidebar with collapse functionality, and mobile-first responsive design.

**Tech Stack:** React 19, TypeScript, TailwindCSS, Zustand

---

## Task 1: Fix AppShell Sidebar - Add Responsive Toggle

**Files:**
- Modify: `frontend/src/components/layout/AppShell.tsx`
- Modify: `frontend/src/styles/tokens.css`

- [ ] **Step 1: Add mobile-responsive sidebar with toggle button**

Read the current AppShell to understand structure:

```bash
# Already read in exploration
```

Update AppShell component to use `sidebarCollapsed` state and add toggle button:

```tsx
// In AppShell.tsx, add this after imports
import { useUIStore } from '../../stores/authStore';

// Replace the entire return statement with:
const { sidebarCollapsed, toggleSidebar } = useUIStore();

return (
  <div className="flex min-h-screen" style={{ background: 'var(--bg-void)' }}>
    {/* Sidebar */}
    <aside
      className={`fixed left-0 top-0 h-full flex flex-col transition-all duration-300 z-40 ${
        sidebarCollapsed ? 'w-16' : 'w-64'
      }`}
      style={{
        background: 'var(--bg-surface)',
        borderRight: '1px solid var(--border-subtle)'
      }}
    >
      {/* Logo & Toggle */}
      <div
        className="h-16 flex items-center justify-between px-4"
        style={{ borderBottom: '1px solid var(--border-subtle)' }}
      >
        {!sidebarCollapsed && (
          <div className="flex items-center gap-3">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ background: 'var(--accent-dim)' }}
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="var(--accent)"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <span
              className="text-lg font-semibold"
              style={{ color: 'var(--text-primary)' }}
            >
              Fortiq
            </span>
          </div>
        )}
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-lg hover:bg-[var(--bg-elevated)] transition-colors"
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="var(--text-secondary)"
            viewBox="0 0 24 24"
          >
            {sidebarCollapsed ? (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 5l7 7-7 7M5 5l7 7-7 7"
              />
            ) : (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
              />
            )}
          </svg>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3 overflow-y-auto">
        <div className="space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors group"
              style={({ isActive }) => ({
                background: isActive ? 'var(--accent-dim)' : 'transparent',
                color: isActive ? 'var(--accent)' : 'var(--text-secondary)',
              })}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={item.icon} />
              </svg>
              {!sidebarCollapsed && <span>{item.label}</span>}
            </NavLink>
          ))}
        </div>
      </nav>

      {/* User section */}
      <div
        className="p-4"
        style={{ borderTop: '1px solid var(--border-subtle)' }}
      >
        <div className="flex items-center gap-3">
          <div
            className="w-9 h-9 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0"
            style={{
              background: 'var(--accent-dim)',
              color: 'var(--accent)'
            }}
          >
            {user?.username?.charAt(0).toUpperCase() || 'U'}
          </div>
          {!sidebarCollapsed && (
            <div className="flex-1 min-w-0">
              <p
                className="text-sm font-medium truncate"
                style={{ color: 'var(--text-primary)' }}
              >
                {user?.username || 'User'}
              </p>
              <button
                onClick={handleLogout}
                className="text-xs hover:underline"
                style={{ color: 'var(--text-muted)' }}
              >
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </aside>

    {/* Main content */}
    <main
      className={`flex-1 transition-all duration-300 ${
        sidebarCollapsed ? 'ml-16' : 'ml-64'
      }`}
    >
      <div className="p-6 md:p-8 max-w-7xl mx-auto w-full">
        <Outlet />
      </div>
    </main>
  </div>
);
```

- [ ] **Step 2: Fix import statement in AppShell**

The useUIStore import needs to come from the correct location:

```tsx
// Change line 2 in AppShell.tsx from:
import { useAuthStore } from '../../stores/authStore';
// To:
import { useAuthStore } from '../../stores/authStore';
import { useUIStore } from '../../stores/uiStore';
```

- [ ] **Step 3: Test sidebar toggle functionality**

```bash
cd frontend && npm run dev
```

Expected: Sidebar should collapse/expand when clicking the toggle button, main content should adjust margin accordingly.

- [ ] **Step 4: Commit sidebar toggle feature**

```bash
git add frontend/src/components/layout/AppShell.tsx
git commit -m "$(cat <<'EOF'
feat: add responsive sidebar toggle to AppShell

- Add collapse/expand functionality using useUIStore
- Implement smooth transitions for sidebar width changes
- Add toggle button with appropriate icons
- Adjust main content margin based on sidebar state
- Improve mobile responsiveness

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Fix MigratePage Blank Screen - Add Loading States

**Files:**
- Modify: `frontend/src/pages/MigratePage.tsx`

- [ ] **Step 1: Add comprehensive loading and error states**

Update MigratePage to handle loading states properly:

```tsx
// Add after the hooks declarations around line 14:
const { data: endpointsData, isLoading: endpointsLoading, isError: endpointsError } = useEndpoints({ per_page: 100 });
const { data: pqcDemo, isLoading: pqcLoading, isError: pqcError } = usePQCDemo();

// Add loading state check at the beginning of the component return:
if (endpointsLoading) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center space-y-4">
        <div
          className="w-12 h-12 border-4 border-t-transparent rounded-full animate-spin mx-auto"
          style={{ borderColor: 'var(--accent)', borderTopColor: 'transparent' }}
        />
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Loading migration data...
        </p>
      </div>
    </div>
  );
}

if (endpointsError) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div
        className="p-6 rounded-lg max-w-md text-center"
        style={{
          background: 'rgba(239, 68, 68, 0.12)',
          border: '1px solid rgba(239, 68, 68, 0.3)'
        }}
      >
        <svg
          className="w-12 h-12 mx-auto mb-4"
          fill="none"
          stroke="var(--status-error)"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--status-error)' }}>
          Failed to Load Migration Data
        </h2>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Unable to fetch endpoints. Please try refreshing the page.
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Update the main content with better null checks**

Add null/undefined checks for data throughout the component:

```tsx
// Replace line 32-34 with:
const pendingEndpoints = endpointsData?.endpoints?.filter(
  (e) => e.migration_status === 'pending'
) || [];

const totalEndpoints = endpointsData?.endpoints?.length || 0;
```

- [ ] **Step 3: Test MigratePage loading and error states**

```bash
cd frontend && npm run dev
```

Expected: Page should show loading spinner initially, then content or error message.

- [ ] **Step 4: Commit MigratePage fixes**

```bash
git add frontend/src/pages/MigratePage.tsx
git commit -m "$(cat <<'EOF'
fix: add loading and error states to MigratePage

- Add loading spinner for initial data fetch
- Add error state display for failed API calls
- Improve null/undefined data handling
- Prevent blank screen on page load

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Standardize Component Spacing

**Files:**
- Modify: `frontend/src/pages/DashboardPage.tsx`
- Modify: `frontend/src/pages/ClassifyPage.tsx`
- Modify: `frontend/src/pages/MigratePage.tsx`
- Modify: `frontend/src/pages/AdminPage.tsx`
- Modify: `frontend/src/pages/AboutPage.tsx`

- [ ] **Step 1: Update DashboardPage spacing**

Standardize spacing in DashboardPage:

```tsx
// Replace line 46's `space-y-6` with `space-y-8` for consistency
// Replace line 59's gap-4 with gap-6
// Replace line 92's gap-4 with gap-6

// Update the entire return statement spacing:
return (
  <div className="space-y-8">
    {/* Header */}
    <div>
      <h1 className="text-2xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
        Dashboard
      </h1>
      <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
        Post-quantum cryptography migration overview
      </p>
    </div>

    {/* Stat Cards */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {/* ... existing stat cards ... */}
    </div>

    {/* Charts */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* ... existing charts ... */}
    </div>

    {/* Recent Endpoints Table */}
    <div
      style={{
        background: 'var(--bg-surface)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-lg)',
        padding: '1.5rem'
      }}
    >
      {/* ... existing table ... */}
    </div>
  </div>
);
```

- [ ] **Step 2: Update ClassifyPage spacing**

```tsx
// In ClassifyPage.tsx, replace line 36's `space-y-6` with `space-y-8`
// Update header section to add mb-2 to h1:

<div className="space-y-8">
  {/* Header */}
  <div>
    <h1 className="text-2xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
      Risk Classification
    </h1>
    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
      Classify endpoints using VQC (Variational Quantum Classifier)
    </p>
  </div>

  {/* Rest of content with proper spacing */}
</div>
```

- [ ] **Step 3: Update MigratePage spacing**

```tsx
// In MigratePage.tsx, update main container and all sections:
// Change line 37 from space-y-8 to more consistent spacing
// Add proper margins to headers

<div className="space-y-8">
  {/* Header */}
  <div>
    <h1 className="text-2xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
      PQC Migration
    </h1>
    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
      Migrate endpoints to post-quantum cryptography (ML-KEM-768 + ML-DSA-65)
    </p>
  </div>
  {/* ... rest of content ... */}
</div>
```

- [ ] **Step 4: Update AdminPage spacing**

```tsx
// In AdminPage.tsx, update spacing:
<div className="space-y-8">
  {/* Header */}
  <div>
    <h1 className="text-2xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
      Admin Tools
    </h1>
    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
      Administrative functions for data generation and model training
    </p>
  </div>
  {/* ... sections with padding: '1.5rem' consistently ... */}
</div>
```

- [ ] **Step 5: Update AboutPage spacing**

```tsx
// In AboutPage.tsx, update spacing consistency:
<div className="space-y-10">
  {/* Header */}
  <div>
    <h1 className="text-2xl font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
      About Fortiq
    </h1>
    <p className="text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
      {/* ... existing description ... */}
    </p>
  </div>
  {/* ... rest with consistent spacing ... */}
</div>
```

- [ ] **Step 6: Test all pages for spacing consistency**

```bash
cd frontend && npm run dev
```

Expected: All pages should have consistent spacing between sections, proper margins on headers, and aligned card padding.

- [ ] **Step 7: Commit spacing standardization**

```bash
git add frontend/src/pages/*.tsx
git commit -m "$(cat <<'EOF'
refactor: standardize spacing across all pages

- Use consistent space-y-8 for main content sections
- Standardize header margins (mb-2 for h1 titles)
- Use gap-6 consistently for grids
- Standardize card padding to 1.5rem
- Improve visual hierarchy and breathing room

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Fix Card Component Inconsistencies

**Files:**
- Modify: `frontend/src/index.css`
- Modify: `frontend/src/pages/DashboardPage.tsx`
- Modify: `frontend/src/pages/ClassifyPage.tsx`
- Modify: `frontend/src/pages/MigratePage.tsx`
- Modify: `frontend/src/pages/AdminPage.tsx`
- Modify: `frontend/src/pages/AboutPage.tsx`

- [ ] **Step 1: Update card utility classes in index.css**

```css
/* In index.css, update .card class around line 71: */
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}

.card-compact {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
}

.card-header {
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}
```

- [ ] **Step 2: Replace inline card styles with utility classes**

Go through each page and replace inline card styles:

```tsx
// Before:
<div
  style={{
    background: 'var(--bg-surface)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-lg)',
    padding: '1.25rem'
  }}
>

// After:
<div className="card">
```

- [ ] **Step 3: Apply card classes to DashboardPage**

```tsx
// Update all cards in DashboardPage to use the class:
// Lines 94-100, 149-156, 205-212

<div className="card">
  <h2 className="card-title">Risk Tier Distribution</h2>
  {/* ... content ... */}
</div>
```

- [ ] **Step 4: Apply card classes to other pages**

Similarly update ClassifyPage, MigratePage, AdminPage, and AboutPage to use card utility classes instead of inline styles.

- [ ] **Step 5: Test visual consistency**

```bash
cd frontend && npm run dev
```

Expected: All cards should have consistent borders, shadows, padding, and radius across all pages.

- [ ] **Step 6: Commit card standardization**

```bash
git add frontend/src/index.css frontend/src/pages/*.tsx
git commit -m "$(cat <<'EOF'
refactor: standardize card components with utility classes

- Create .card, .card-compact, .card-header utility classes
- Replace inline card styles with utility classes
- Ensure consistent padding, borders, and radius
- Reduce code duplication across pages

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Add Loading States to All Pages

**Files:**
- Modify: `frontend/src/pages/DashboardPage.tsx`
- Modify: `frontend/src/pages/ClassifyPage.tsx`
- Create: `frontend/src/components/common/LoadingSpinner.tsx`
- Create: `frontend/src/components/common/ErrorMessage.tsx`

- [ ] **Step 1: Create LoadingSpinner component**

```tsx
// Create frontend/src/components/common/LoadingSpinner.tsx
export function LoadingSpinner({ message = 'Loading...' }: { message?: string }) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center space-y-4">
        <div
          className="w-12 h-12 border-4 border-t-transparent rounded-full animate-spin mx-auto"
          style={{ borderColor: 'var(--accent)', borderTopColor: 'transparent' }}
        />
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          {message}
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create ErrorMessage component**

```tsx
// Create frontend/src/components/common/ErrorMessage.tsx
export function ErrorMessage({
  title = 'Error',
  message = 'Something went wrong. Please try again.',
}: {
  title?: string;
  message?: string;
}) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div
        className="p-6 rounded-lg max-w-md text-center"
        style={{
          background: 'rgba(239, 68, 68, 0.12)',
          border: '1px solid rgba(239, 68, 68, 0.3)'
        }}
      >
        <svg
          className="w-12 h-12 mx-auto mb-4"
          fill="none"
          stroke="var(--status-error)"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--status-error)' }}>
          {title}
        </h2>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          {message}
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Update DashboardPage with loading components**

```tsx
// At the top of DashboardPage.tsx, import:
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';

// Add error handling to the existing loading check:
const { data: stats, isLoading: statsLoading, isError } = useDashboardStats();
const { data: endpointsData, isLoading: endpointsLoading } = useEndpoints({ per_page: 100 });

if (statsLoading || endpointsLoading) {
  return <LoadingSpinner message="Loading dashboard..." />;
}

if (isError) {
  return <ErrorMessage title="Failed to Load Dashboard" message="Unable to fetch dashboard statistics." />;
}
```

- [ ] **Step 4: Update ClassifyPage with loading components**

```tsx
// Similarly update ClassifyPage.tsx:
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';

// Update the hooks to capture error state:
const { data: endpointsData, isLoading, isError } = useEndpoints({ per_page: 100 });

// Add before the main return:
if (isLoading) {
  return <LoadingSpinner message="Loading endpoints..." />;
}

if (isError) {
  return <ErrorMessage title="Failed to Load Endpoints" />;
}
```

- [ ] **Step 5: Ensure MigratePage uses new components**

```tsx
// Update MigratePage imports to use the new components:
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';

// Replace the loading/error JSX with:
if (endpointsLoading) {
  return <LoadingSpinner message="Loading migration data..." />;
}

if (endpointsError) {
  return <ErrorMessage title="Failed to Load Migration Data" message="Unable to fetch endpoints. Please try refreshing the page." />;
}
```

- [ ] **Step 6: Test loading states**

```bash
cd frontend && npm run dev
```

Expected: All pages show consistent loading spinners, all error states display properly.

- [ ] **Step 7: Commit loading state components**

```bash
git add frontend/src/components/common/*.tsx frontend/src/pages/*.tsx
git commit -m "$(cat <<'EOF'
feat: add reusable loading and error components

- Create LoadingSpinner component for consistent loading states
- Create ErrorMessage component for error handling
- Apply to Dashboard, Classify, and Migrate pages
- Improve user experience with clear feedback

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Improve Mobile Responsiveness

**Files:**
- Modify: `frontend/src/components/layout/AppShell.tsx`
- Modify: `frontend/src/pages/DashboardPage.tsx`
- Modify: `frontend/src/pages/ClassifyPage.tsx`
- Modify: `frontend/src/pages/MigratePage.tsx`
- Modify: `frontend/src/index.css`

- [ ] **Step 1: Add mobile overlay to sidebar**

```tsx
// In AppShell.tsx, add mobile overlay when sidebar is open:
return (
  <div className="flex min-h-screen" style={{ background: 'var(--bg-void)' }}>
    {/* Mobile overlay - only show on small screens when sidebar not collapsed */}
    {!sidebarCollapsed && (
      <div
        className="fixed inset-0 bg-black/50 z-30 lg:hidden"
        onClick={toggleSidebar}
        aria-hidden="true"
      />
    )}

    {/* Sidebar */}
    <aside
      className={`fixed left-0 top-0 h-full flex flex-col transition-all duration-300 z-40 ${
        sidebarCollapsed ? 'w-16' : 'w-64'
      } lg:translate-x-0 ${
        sidebarCollapsed ? '-translate-x-full lg:translate-x-0' : 'translate-x-0'
      }`}
      style={{
        background: 'var(--bg-surface)',
        borderRight: '1px solid var(--border-subtle)'
      }}
    >
      {/* ... existing sidebar content ... */}
    </aside>

    {/* Main content */}
    <main
      className={`flex-1 transition-all duration-300 ${
        sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-64'
      }`}
    >
      {/* Add hamburger menu for mobile */}
      <div className="lg:hidden sticky top-0 z-20 flex items-center gap-4 px-4 h-16" style={{ background: 'var(--bg-surface)', borderBottom: '1px solid var(--border-subtle)' }}>
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-lg hover:bg-[var(--bg-elevated)] transition-colors"
          aria-label="Toggle menu"
        >
          <svg className="w-6 h-6" fill="none" stroke="var(--text-primary)" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <span className="text-lg font-semibold" style={{ color: 'var(--text-primary)' }}>
          Fortiq
        </span>
      </div>

      <div className="p-4 md:p-6 lg:p-8 max-w-7xl mx-auto w-full">
        <Outlet />
      </div>
    </main>
  </div>
);
```

- [ ] **Step 2: Add mobile menu auto-close behavior**

```tsx
// In AppShell.tsx, update the useUIStore to auto-collapse on mobile:
// Add this effect after the component function starts:
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const location = useLocation();

// Auto-close sidebar on mobile when route changes
useEffect(() => {
  if (window.innerWidth < 1024 && !sidebarCollapsed) {
    toggleSidebar();
  }
}, [location.pathname]);
```

- [ ] **Step 3: Make tables responsive**

```css
/* Add to index.css */
@layer components {
  /* ... existing styles ... */

  /* Responsive table wrapper */
  .table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  @media (max-width: 768px) {
    .table {
      font-size: 0.8125rem;
    }

    .table th,
    .table td {
      padding: 0.625rem 0.75rem;
    }
  }
}
```

- [ ] **Step 4: Update table wrappers in pages**

```tsx
// In DashboardPage.tsx, wrap table:
<div className="table-responsive">
  <table className="w-full">
    {/* ... table content ... */}
  </table>
</div>

// Do the same for ClassifyPage model comparison table
```

- [ ] **Step 5: Test mobile responsiveness**

```bash
cd frontend && npm run dev
# Test at different viewport sizes: 375px, 768px, 1024px, 1440px
```

Expected: Sidebar should overlay on mobile, hamburger menu appears, tables scroll horizontally on small screens.

- [ ] **Step 6: Commit mobile responsiveness**

```bash
git add frontend/src/components/layout/AppShell.tsx frontend/src/pages/*.tsx frontend/src/index.css
git commit -m "$(cat <<'EOF'
feat: improve mobile responsiveness across application

- Add mobile overlay for sidebar with tap-to-close
- Add hamburger menu for mobile navigation
- Auto-close sidebar on route change (mobile only)
- Make tables horizontally scrollable on small screens
- Responsive padding adjustments for all pages

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Polish Button and Input Consistency

**Files:**
- Modify: `frontend/src/index.css`
- Modify: `frontend/src/pages/MigratePage.tsx`
- Modify: `frontend/src/pages/ClassifyPage.tsx`
- Modify: `frontend/src/pages/AdminPage.tsx`

- [ ] **Step 1: Update button styles for consistency**

```css
/* In index.css, update button utilities: */
@layer components {
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    border-radius: var(--radius-md);
    font-weight: 500;
    font-size: 0.875rem;
    line-height: 1.25rem;
    transition: all 0.15s ease;
    cursor: pointer;
    border: none;
    white-space: nowrap;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-primary {
    background: var(--accent);
    color: var(--text-inverse);
    min-height: 2.5rem;
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--accent-solid);
    transform: translateY(-1px);
  }

  .btn-secondary {
    background: var(--bg-elevated);
    color: var(--text-primary);
    border: 1px solid var(--border-default);
    min-height: 2.5rem;
  }

  .btn-secondary:hover:not(:disabled) {
    background: var(--bg-subtle);
    border-color: var(--border-active);
  }

  .btn-ghost {
    background: transparent;
    color: var(--text-secondary);
    min-height: 2.5rem;
  }

  .btn-ghost:hover:not(:disabled) {
    background: var(--bg-subtle);
    color: var(--text-primary);
  }
}
```

- [ ] **Step 2: Replace inline button styles with utility classes**

```tsx
// In MigratePage.tsx, replace button around line 48-56:
<button
  onClick={() => setShowConfirm(true)}
  disabled={migrateMutation.isPending || jobStatus?.status === 'running'}
  className="btn-primary"
>
  {migrateMutation.isPending || jobStatus?.status === 'running'
    ? 'Migrating...'
    : `Migrate ${migrationQueue.length > 0 ? `(${migrationQueue.length})` : 'All'}`}
</button>

// Similarly update other buttons in the file to use btn-* classes
```

- [ ] **Step 3: Update ClassifyPage buttons**

```tsx
// In ClassifyPage.tsx, update the classify button around line 47-59:
<button
  onClick={handleClassify}
  disabled={classifyMutation.isPending || (jobStatus?.status === 'running')}
  className="btn-primary"
>
  {classifyMutation.isPending || jobStatus?.status === 'running'
    ? 'Classifying...'
    : 'Run Classification'}
</button>
```

- [ ] **Step 4: Update AdminPage buttons**

```tsx
// In AdminPage.tsx, update buttons to use utility classes:
<button
  onClick={handleGenerateData}
  disabled={generateStatus.running}
  className="btn-primary"
>
  {generateStatus.running ? 'Generating...' : 'Generate Data'}
</button>

<button
  onClick={handleTrainModels}
  disabled={trainStatus.running}
  className="btn-primary"
>
  {trainStatus.running ? 'Training Models...' : 'Start Training'}
</button>
```

- [ ] **Step 5: Test button consistency**

```bash
cd frontend && npm run dev
```

Expected: All buttons should have consistent height, padding, hover states, and disabled states.

- [ ] **Step 6: Commit button polish**

```bash
git add frontend/src/index.css frontend/src/pages/*.tsx
git commit -m "$(cat <<'EOF'
refactor: polish button styling and consistency

- Add min-height to all button variants
- Add subtle transform on hover for better feedback
- Replace inline button styles with utility classes
- Ensure consistent disabled states across all buttons

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Final Visual Polish and Testing

**Files:**
- Modify: `frontend/src/styles/tokens.css`
- Test: All pages

- [ ] **Step 1: Enhance focus states for accessibility**

```css
/* In tokens.css, add enhanced focus visible: */
/* At the bottom of the file, update the focus-visible section around line 126: */

/* Focus styles */
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 4px;
}

button:focus-visible,
a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

- [ ] **Step 2: Test all pages systematically**

Test checklist:
- Dashboard: Charts render, cards are properly spaced, table is readable
- Classify: Endpoint list loads, detail panel works, model comparison table displays
- Migrate: PQC demo cards show, migration queue works, confirmation modal appears
- Admin: Generate data works, train models works, status messages display
- About: All sections render with proper spacing
- Login: Form is centered, inputs work, error states display

```bash
cd frontend && npm run dev
# Navigate through each page and verify functionality
```

- [ ] **Step 3: Test responsive behavior**

```bash
# Open DevTools, test at:
# - 375px (mobile)
# - 768px (tablet)
# - 1024px (desktop)
# - 1440px (large desktop)
```

Expected: No overlaps, proper text wrapping, sidebar behaves correctly, tables scroll on mobile.

- [ ] **Step 4: Test sidebar collapse/expand**

Test:
- Click toggle button on desktop
- Verify main content margin adjusts
- Verify nav labels hide/show
- Test on mobile - sidebar should overlay
- Test route changes auto-close sidebar on mobile

- [ ] **Step 5: Test loading and error states**

```bash
# Temporarily break API connection or add artificial delays
# Verify loading spinners appear
# Verify error messages display properly
```

- [ ] **Step 6: Document changes**

```bash
# Create or update CHANGELOG.md or similar
```

- [ ] **Step 7: Final commit**

```bash
git add frontend/src/styles/tokens.css
git commit -m "$(cat <<'EOF'
style: enhance focus states for accessibility

- Improve keyboard navigation focus indicators
- Add rounded corners to focus outlines
- Ensure consistent focus-visible across interactive elements

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Create Common Components Directory

**Files:**
- Create: `frontend/src/components/common/index.ts`

- [ ] **Step 1: Create barrel export for common components**

```tsx
// Create frontend/src/components/common/index.ts
export { LoadingSpinner } from './LoadingSpinner';
export { ErrorMessage } from './ErrorMessage';
```

- [ ] **Step 2: Update imports across pages**

```tsx
// Update all pages to use barrel import:
// Before:
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';

// After:
import { LoadingSpinner, ErrorMessage } from '../components/common';
```

- [ ] **Step 3: Test imports**

```bash
cd frontend && npm run build
```

Expected: Build succeeds without errors.

- [ ] **Step 4: Commit common components organization**

```bash
git add frontend/src/components/common/index.ts frontend/src/pages/*.tsx
git commit -m "$(cat <<'EOF'
refactor: organize common components with barrel exports

- Create index.ts for common components
- Update imports to use barrel exports
- Improve code organization and maintainability

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Review and Verification

After completing all tasks:

1. **Visual Review**: Navigate through all pages and verify spacing, alignment, and consistency
2. **Functional Review**: Test all interactive features (sidebar toggle, buttons, forms, navigation)
3. **Responsive Review**: Test at multiple viewport sizes
4. **Performance Review**: Check for smooth animations and transitions
5. **Accessibility Review**: Test keyboard navigation and screen reader compatibility

**Success Criteria:**
- ✅ MigratePage loads without blank screen
- ✅ Sidebar toggles correctly on all screen sizes
- ✅ All pages have consistent spacing and card styles
- ✅ Loading and error states work properly
- ✅ Mobile responsive design functions correctly
- ✅ No component overlaps or layout issues
- ✅ Buttons and inputs have consistent styling
- ✅ All pages are accessible via keyboard navigation
