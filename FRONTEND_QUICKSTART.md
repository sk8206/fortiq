# Fortiq Frontend - Quick Start

The frontend has been completely rebuilt with the Tactical Luxury design system.

## Install Dependencies

```bash
cd frontend
npm install
```

## Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Design System Highlights

### Typography (4-font system)
- **Bebas Neue** - Display numbers (96px compliance score, section markers)
- **Cormorant Garamond** - Serif headings (panel titles, editorial text)
- **Syne** - UI elements (labels, buttons, body text)
- **JetBrains Mono** - Data/code (algorithms, coordinates, hashes)

### Layout
- **56px narrow spine** - Icon-only vertical navigation (not traditional sidebar)
- **48px top bar** - Live ticker with operational stats + clock
- **Tactical patterns** - Section indexers `[01] ──── LABEL`, coordinate readouts, editorial panels

### Colors
- **Void** (#020204) - Absolute background
- **Cream** (#F2EFE6) - Warm primary text (not harsh white)
- **Acid** (#B8FF00) - Tactical electric accent
- **Risk tiers** - Critical/High/Medium/Low semantic colors

### Key Components Built
- ✅ AppShell with Spine + TopBar + live ticker
- ✅ SectionIndex pattern (used everywhere)
- ✅ ReticleMark SVG (signature decorative element)
- ✅ Button, Input, Modal, ConfirmModal
- ✅ ProgressBar (2px hairline, not chunky)
- ✅ RiskBadge (dot + text, no pill background)
- ✅ DataTable (tactical data rows)
- ✅ ComplianceHero with 96px Bebas Neue number + rotating reticle watermark
- ✅ Login view (split panel hero design)
- ✅ Dashboard, Scan, Migrate views (basic structure)

### What's Included
- Full routing with React Router
- Authentication with Zustand store
- API client with Axios + interceptors
- Type-safe TypeScript throughout
- Tailwind configured with design tokens
- All CSS animations (fade-in-up, reticle-spin, skeleton-sweep, etc.)

### Default Credentials
```
Username: admin
Password: fortiq-demo-2024
```

## Next Steps

The core structure is complete. You can now:
1. Add NetworkGraph with react-force-graph-2d
2. Add Recharts visualizations (PieChart, RadarChart)
3. Implement classification and migration job polling
4. Add AlgorithmInfoPanel editorial spread
5. Add audit log and migration config viewers

## File Structure
```
frontend/src/
├── components/
│   ├── ui/          - Primitive components
│   ├── layout/      - AppShell, Spine, TopBar
│   └── data/        - RiskBadge, DataTable
├── views/           - Page components
├── api/             - API clients
├── stores/          - Zustand state
├── hooks/           - Custom hooks
├── styles/          - CSS tokens & animations
└── types/           - TypeScript definitions
```
