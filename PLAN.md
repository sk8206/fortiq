# PLAN.md — Phase 5 Design Implementation (Tactical Luxury Addendum)

> This document **extends** PLAN.md v2. Phases 0–4 (backend, QML, PQC, API) are unchanged. This addendum fully replaces the Phase 5 section with precise Tactical Luxury implementation instructions for every component.

---

## Phase 5 — React Dashboard: Tactical Luxury Implementation

### Pre-Phase 5: Style Foundation Setup

Before building any components, establish the complete style foundation.

**5.0.1 CSS Files — exact content**

`src/styles/tokens.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Syne:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --void:       #020204;
  --field:      #08080F;
  --lift:       #0E0E18;
  --recess:     #14141F;
  --cream:      #F2EFE6;
  --cream-60:   rgba(242,239,230,0.60);
  --cream-25:   rgba(242,239,230,0.25);
  --cream-10:   rgba(242,239,230,0.10);
  --cream-05:   rgba(242,239,230,0.05);
  --acid:       #B8FF00;
  --acid-15:    rgba(184,255,0,0.15);
  --acid-08:    rgba(184,255,0,0.08);
  --acid-border:rgba(184,255,0,0.30);
  --r-critical: #FF3535;
  --r-critical-bg:rgba(255,53,53,0.08);
  --r-high:     #FF7A00;
  --r-high-bg:  rgba(255,122,0,0.08);
  --r-medium:   #F5C400;
  --r-medium-bg:rgba(245,196,0,0.08);
  --r-low:      #00CC6A;
  --r-low-bg:   rgba(0,204,106,0.08);
  --r-unknown:  rgba(242,239,230,0.20);
  --rule:       rgba(242,239,230,0.08);
  --rule-strong:rgba(242,239,230,0.18);
  --rule-accent:rgba(184,255,0,0.25);
  --font-display:'Bebas Neue', sans-serif;
  --font-serif:  'Cormorant Garamond', serif;
  --font-ui:     'Syne', sans-serif;
  --font-mono:   'JetBrains Mono', monospace;
  --sidebar-w:   56px;
  --topbar-h:    48px;
}
```

`src/styles/global.css`:
```css
@import './tokens.css';

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { background: var(--void); color: var(--cream); }

body {
  font-family: var(--font-ui);
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  background: var(--void);
  overflow-x: hidden;
}

/* Scrollbar styling */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: var(--rule-strong); border-radius: 0; }

/* Focus ring — all interactive elements */
:focus-visible {
  outline: 1px solid var(--acid);
  outline-offset: 3px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Utility: section-index pattern */
.section-index {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.si-num {
  font-family: var(--font-display);
  font-size: 13px;
  color: var(--acid);
  letter-spacing: 0.08em;
  flex-shrink: 0;
}
.si-rule {
  flex: 1;
  height: 1px;
  background: var(--rule);
}
.si-label {
  font-family: var(--font-ui);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--cream-60);
  text-transform: uppercase;
  flex-shrink: 0;
}
```

`src/styles/animations.css`:
```css
@keyframes skeleton-sweep {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes reticle-spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in-right {
  from { transform: translateX(480px); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}

@keyframes ticker-flash {
  0%, 100% { color: var(--cream); }
  30%       { color: var(--acid); }
}

@keyframes drawer-push {
  from { width: 100%; }
  to   { width: calc(100% - 480px); }
}
```

---

### 5.1 Application Shell (`src/components/layout/AppShell.tsx`)

```tsx
// Exact layout structure:
//
// ┌─[56px spine]─┬──────────────[main]──────────────────┐
// │              │ ┌─────────────[topbar: 48px]─────────┐│
// │  [nav icons] │ │ FORTIQ · ticker · clock · user     ││
// │              │ └────────────────────────────────────┘│
// │  active:     │ ┌─────────────[content]──────────────┐│
// │  │ accent    │ │ 40px h-padding                      ││
// │  bar on left │ │ route outlet renders here           ││
// │              │ └────────────────────────────────────┘│
// └──────────────┴─────────────────────────────────────-─┘

export function AppShell({ children }) {
  return (
    <div style={{ display: 'flex', height: '100vh', background: 'var(--void)' }}>
      <Spine />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <TopBar />
        <main style={{
          flex: 1,
          overflowY: 'auto',
          padding: '32px 40px',
        }}>
          {children}
        </main>
      </div>
    </div>
  );
}
```

**Spine** (`src/components/layout/Spine.tsx`):
- Width: 56px, `background: var(--field)`, `border-right: 1px solid var(--rule)`
- Contains: Fortiq logo mark (top, 40px × 40px, acid green SVG icon — a simple reticle circle), then 3 nav icon buttons
- Nav icon: 40px × 40px, centered. Icon in `var(--cream-25)`. On hover: `var(--cream-60)`. On active route: `var(--acid)` icon + `position: absolute; left: 0; top: 0; width: 2px; height: 40px; background: var(--acid)` bar
- Icons: use Lucide icons — `LayoutDashboard`, `ScanLine`, `ArrowRightLeft`
- Tooltip on hover: rendered via CSS `::after` pseudo-element, not JS portal. Position: `left: 64px`. JetBrains Mono 11px uppercase.

**TopBar** (`src/components/layout/TopBar.tsx`):
- Height 48px, `background: var(--field)`, `border-bottom: 1px solid var(--rule)`
- Left: `FORTIQ` wordmark — Bebas Neue 18px, `var(--cream)`, letter-spacing 0.06em
- Center: `<CoordinateReadout />` — live ticker (see Pattern 2 in AI_Rules.md)
- Right: `<LiveClock />` + user initial avatar (28px circle, `var(--recess)` bg, `var(--cream-60)` text)

**LiveClock**: updates every second. JetBrains Mono 11px uppercase. Format: `THU 14:23:07 UTC`. Colour: `var(--cream-25)`.

**CoordinateReadout** implementation:
```tsx
function CoordinateReadout() {
  const stats = useEndpointStore(s => s.stats);
  // Flash each value when it changes
  return (
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11,
                  letterSpacing: '0.08em', color: 'var(--cream-60)',
                  display: 'flex', gap: 20, alignItems: 'center' }}>
      <CoordItem label="ENDPOINTS" value={stats?.total ?? '—'} />
      <span style={{ color: 'var(--rule-strong)' }}>··</span>
      <CoordItem label="CRITICAL" value={stats?.by_tier.critical ?? '—'} flash color="var(--r-critical)" />
      <span style={{ color: 'var(--rule-strong)' }}>··</span>
      <CoordItem label="MIGRATED" value={stats?.by_status.complete ?? '—'} />
      <span style={{ color: 'var(--rule-strong)' }}>··</span>
      <CoordItem label="COMPLIANCE" value={stats ? `${stats.compliance_score.toFixed(1)}%` : '—'} flash />
    </div>
  );
}
```

---

### 5.2 SectionIndex Component (`src/components/ui/SectionIndex/`)

```tsx
interface SectionIndexProps {
  number: string;  // e.g. "[01]"
  label: string;   // e.g. "ASSET REGISTRY"
}

export function SectionIndex({ number, label }: SectionIndexProps) {
  return (
    <div className="section-index">
      <span className="si-num">{number}</span>
      <span className="si-rule" />
      <span className="si-label">{label}</span>
    </div>
  );
}
```

Usage: `<SectionIndex number="[01]" label="ASSET REGISTRY" />`

This must appear at the start of every major panel.

---

### 5.3 Dashboard View (`src/views/Dashboard/DashboardView.tsx`)

```tsx
// Layout:
// SectionIndex [01] INTELLIGENCE OVERVIEW
// [HERO ROW — 3 panels at equal height ~280px]
//   [ComplianceHero — 35%] [TierBreakdown — 35%] [LiveFeed — 30%]
// [1px rule]
// SectionIndex [02] ASSET REGISTRY
// [MigrationProgressTable — full width]

export function DashboardView() {
  const stats = useEndpointStore(s => s.stats);
  const endpoints = useEndpointStore(s => s.endpoints);

  useEffect(() => {
    useEndpointStore.getState().fetchStats();
    useEndpointStore.getState().fetchEndpoints();
  }, []);

  return (
    <div style={{ animation: 'fade-in-up 300ms var(--ease-out)' }}>
      <SectionIndex number="[01]" label="INTELLIGENCE OVERVIEW" />
      <div style={{ display: 'grid', gridTemplateColumns: '35fr 35fr 30fr', gap: 1,
                    marginBottom: 1, border: '1px solid var(--rule)' }}>
        <ComplianceHero score={stats?.compliance_score ?? 0} />
        <TierBreakdown stats={stats} />
        <LiveFeed />
      </div>
      <div style={{ height: 1, background: 'var(--rule)', margin: '32px 0' }} />
      <SectionIndex number="[02]" label="ASSET REGISTRY" />
      <MigrationProgressTable endpoints={endpoints} />
    </div>
  );
}
```

**ComplianceHero** (`ComplianceHero.tsx`):
```tsx
// Position: relative overflow: hidden
// Background watermark: ReticleMark SVG at 5% opacity, position: absolute center
// Content stacked:
//   - Bebas Neue 96px compliance number (CountUp animated)
//   - 1px rule full width
//   - Cormorant Garamond 14px italic label: "Cryptographic Compliance Score"
//   - MiniTierBreakdown: 4 mini bars (2px height each, labelled)

function ComplianceHero({ score }: { score: number }) {
  const colour = score >= 80 ? 'var(--r-low)' : score >= 40 ? 'var(--r-medium)' : 'var(--r-critical)';
  return (
    <div style={{ background: 'var(--field)', padding: 32, position: 'relative',
                  overflow: 'hidden', borderRight: '1px solid var(--rule)' }}>
      {/* Reticle watermark */}
      <ReticleMark style={{ position: 'absolute', top: '50%', left: '50%',
        transform: 'translate(-50%,-50%)', opacity: 0.04, width: 200, height: 200,
        animation: 'reticle-spin 200s linear infinite' }} />
      {/* Number */}
      <div style={{ fontFamily: 'var(--font-display)', fontSize: 96, lineHeight: 1,
                    color: colour, position: 'relative' }}>
        <CountUp end={score} decimals={1} suffix="%" duration={1.2} />
      </div>
      {/* Divider */}
      <div style={{ height: 1, background: 'var(--rule)', margin: '16px 0' }} />
      {/* Label */}
      <div style={{ fontFamily: 'var(--font-serif)', fontSize: 14, fontStyle: 'italic',
                    color: 'var(--cream-60)' }}>
        Cryptographic Compliance Score
      </div>
      <MiniTierBreakdown stats={stats} />
    </div>
  );
}
```

**MiniTierBreakdown**: 4 rows, each `[DOT] [TIER LABEL] ─────── [COUNT]`. Dot is 6px. Label Syne 11px uppercase. Count Bebas Neue 18px. Each row separated by `1px var(--rule)`.

**TierBreakdown** (`TierBreakdown.tsx`):
```tsx
// Recharts PieChart — CUSTOM STYLED
// innerRadius: 60, outerRadius: 90
// No default legend — custom below chart
// Cell colours: var(--r-critical/high/medium/low)
// Center of donut: total endpoint count in Bebas Neue 36px + "ENDPOINTS" Syne 10px

// Custom legend: 4 rows vertical
// Each: [colored 8px square] [tier name Syne 12px uppercase --cream-60] [count Syne 14px --cream]
// Spacing between rows: 8px
```

**LiveFeed** (`RecentActivityFeed.tsx`):
- Title: `SectionIndex number="[03]" label="RECENT ACTIVITY"` inside card
- List of last 8 audit entries
- Each entry: `[timestamp JetBrains Mono 10px --cream-25] [action Syne 12px --cream-60]`
- Entry format: `14:22:07 — api-gateway-prod → COMPLETE`
- Entry separator: `1px var(--rule)`
- Empty state: Cormorant Garamond italic 16px "Awaiting migration activity..."

**MigrationProgressTable**:
Uses the `DataTable` component. Columns exactly as specified in "Tactical Data Row" (Pattern 5 from AI_Rules.md):

| Col | Content | Font |
|---|---|---|
| Status dot | 6px circle, tier color | SVG circle |
| Name | endpoint name | Syne 13px |
| Type | api / database / iot | Syne 11px uppercase `--cream-25` |
| Algorithm | RSA-2048 etc | JetBrains Mono 12px `--cream-25` |
| Tier | CRITICAL | Syne 11px uppercase `--r-{tier}` |
| Score | 0.92 | Syne 14px 500 |
| Status | PENDING → | Syne 11px uppercase |

No alternating row backgrounds. `1px var(--rule)` row separator. Row hover: `background: var(--cream-05)`.

---

### 5.4 Scan View (`src/views/Scan/ScanView.tsx`)

```tsx
// Layout:
// SectionIndex [01] NETWORK TOPOLOGY
// [NetworkGraph — FULL WIDTH, height: 55vh] with CoordOverlay inside
// [1px rule]
// SectionIndex [02] CLASSIFICATION ENGINE
// [COLUMNS: ClassifyPanel (left 42%) | ModelComparisonTable (right 58%)]
// [EndpointDetailPanel — drawer, conditionally rendered, pushes layout]

export function ScanView() {
  const selected = useEndpointStore(s => s.selectedEndpoint);
  return (
    <div style={{ display: 'flex', gap: 0, animation: 'fade-in-up 300ms var(--ease-out)' }}>
      {/* MAIN CONTENT — compresses when drawer opens */}
      <div style={{
        flex: 1,
        width: selected ? 'calc(100% - 480px)' : '100%',
        transition: 'width 280ms var(--ease-out)',
      }}>
        <SectionIndex number="[01]" label="NETWORK TOPOLOGY" />
        <div style={{ position: 'relative', height: '55vh',
                      border: '1px solid var(--rule)', marginBottom: 32 }}>
          <NetworkGraph />
          <NetworkCoordOverlay />
        </div>
        <div style={{ height: 1, background: 'var(--rule)', marginBottom: 32 }} />
        <SectionIndex number="[02]" label="CLASSIFICATION ENGINE" />
        <div style={{ display: 'grid', gridTemplateColumns: '42fr 58fr', gap: 1 }}>
          <ClassifyPanel />
          <ModelComparisonTable />
        </div>
      </div>
      {/* DETAIL DRAWER */}
      {selected && <EndpointDetailPanel />}
    </div>
  );
}
```

**NetworkCoordOverlay** (positioned absolute, top-right of graph container):
```tsx
<div style={{
  position: 'absolute', top: 12, right: 16,
  fontFamily: 'var(--font-mono)', fontSize: 11, letterSpacing: '0.08em',
  color: 'var(--cream-25)', pointerEvents: 'none',
  display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4,
}}>
  <span>NODES: {nodes.length}</span>
  <span>EDGES: {links.length}</span>
  <span>SCALE: {zoom.toFixed(2)}×</span>
</div>
```

**NetworkGraph** — `react-force-graph-2d` implementation:
```tsx
import ForceGraph2D from 'react-force-graph-2d';

const TIER_HEX = {
  critical: '#FF3535', high: '#FF7A00', medium: '#F5C400',
  low: '#00CC6A', unknown: 'rgba(242,239,230,0.20)'
};

<ForceGraph2D
  ref={graphRef}
  graphData={graphData}
  width={containerWidth}
  height={containerHeight}
  backgroundColor="transparent"
  nodeColor={n => TIER_HEX[n.risk_tier] ?? TIER_HEX.unknown}
  nodeVal={n => ({ low: 1.5, medium: 3, high: 5, critical: 7 }[n.traffic_volume] ?? 1.5)}
  nodeLabel=""                               // we render custom tooltip
  linkColor={() => 'rgba(242,239,230,0.04)'}
  linkWidth={0.5}
  onNodeClick={n => selectEndpoint(n.id)}
  onNodeHover={setHoveredNode}
  cooldownTicks={150}
  warmupTicks={40}
  onEngineStop={() => setSimDone(true)}
  onZoom={z => setZoom(z.k)}
  nodeCanvasObject={(node, ctx, globalScale) => {
    // Draw node: filled circle + selected ring if active
    const r = node.__radius ?? 4;
    ctx.beginPath();
    ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
    ctx.fillStyle = TIER_HEX[node.risk_tier] ?? TIER_HEX.unknown;
    ctx.fill();
    if (selectedId === node.id) {
      ctx.strokeStyle = '#B8FF00';  // --acid
      ctx.lineWidth = 1.5 / globalScale;
      ctx.stroke();
    }
  }}
  nodeCanvasObjectMode={() => 'replace'}
/>
```

Custom HTML tooltip (not D3): absolute-positioned div that follows `hoveredNode` coordinates, shows name + algorithm + tier + score. JetBrains Mono 11px inside `var(--lift)` background + 1px `var(--rule-strong)` border.

**ClassifyPanel**:
```tsx
<div style={{ background: 'var(--field)', border: '1px solid var(--rule)', padding: 24 }}>
  <SectionIndex number="[02A]" label="VQC ENGINE" />
  <Button variant="primary" onClick={triggerClassify} disabled={classifying}>
    {classifying ? 'CLASSIFYING...' : 'RUN CLASSIFICATION →'}
  </Button>
  {classifyJob && (
    <div style={{ marginTop: 20 }}>
      {/* Progress: thin 2px bar */}
      <ProgressBar value={classifyJob.progress_pct} max={100} />
      {/* Monospace counter */}
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--cream-60)',
                    marginTop: 8 }}>
        {classifyJob.processed} / {classifyJob.total} ENDPOINTS CLASSIFIED
      </div>
    </div>
  )}
  {/* VQC circuit info */}
  <div style={{ marginTop: 24, borderTop: '1px solid var(--rule)', paddingTop: 16 }}>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--cream-25)',
                  lineHeight: 2 }}>
      <div>DEVICE   lightning.qubit</div>
      <div>QUBITS   4</div>
      <div>LAYERS   3 × [RY · RZ · CNOT]</div>
      <div>ENCODING amplitude</div>
      <div>DIFF     adjoint</div>
    </div>
  </div>
</div>
```

**ModelComparisonTable**:
```tsx
// Two-column comparison: VQC | SVM
// Header: "VARIATIONAL QUANTUM CLASSIFIER" vs "SUPPORT VECTOR MACHINE"
//   in Cormorant Garamond 16px italic
// Metrics as rows:
//   [METRIC Syne 10px uppercase --cream-25] [VQC value] [SVM value]
// Each metric in its own row with 1px rule separator
// VQC value: if higher, colour = --r-low. If lower, --cream. Never both highlighted.
// Bottom note in Cormorant Garamond italic 13px:
//   "Quantum advantage is architectural — forward-compatible as hardware scales."
```

**EndpointDetailPanel** (`EndpointDetailPanel.tsx`) — the drawer:
```tsx
<div style={{
  width: 480, flexShrink: 0,
  background: 'var(--field)',
  borderLeft: '1px solid var(--rule)',
  animation: 'slide-in-right 280ms var(--ease-out)',
  overflowY: 'auto',
  display: 'flex', flexDirection: 'column',
}}>
  {/* Header */}
  <div style={{ padding: '24px 24px 0' }}>
    <div style={{ fontFamily: 'var(--font-serif)', fontSize: 22, color: 'var(--cream)',
                  marginBottom: 4 }}>
      {endpoint.name}
    </div>
    <div style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--cream-25)' }}>
      {endpoint.host}:{endpoint.port}
    </div>
  </div>
  <div style={{ height: 1, background: 'var(--rule)', margin: '20px 0' }} />
  {/* Feature data grid */}
  <div style={{ padding: '0 24px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
    {FEATURE_FIELDS.map(f => (
      <div key={f.key}>
        <div style={{ fontFamily: 'var(--font-ui)', fontSize: 10, fontWeight: 700,
                      letterSpacing: '0.14em', color: 'var(--cream-25)',
                      textTransform: 'uppercase', marginBottom: 4 }}>
          {f.label}
        </div>
        <div style={{ fontFamily: f.mono ? 'var(--font-mono)' : 'var(--font-ui)',
                      fontSize: 13, color: 'var(--cream)' }}>
          {f.format(endpoint[f.key])}
        </div>
      </div>
    ))}
  </div>
  <div style={{ height: 1, background: 'var(--rule)', margin: '20px 0' }} />
  {/* Feature radar */}
  <div style={{ padding: '0 24px' }}>
    <SectionIndex number="" label="VQC FEATURE PROFILE" />
    <FeatureRadarChart endpoint={endpoint} />
  </div>
  <div style={{ height: 1, background: 'var(--rule)', margin: '20px 0' }} />
  {/* Action */}
  <div style={{ padding: '0 24px 24px' }}>
    <Button variant="primary" style={{ width: '100%' }}
            onClick={() => addToQueue(endpoint.id)}>
      ADD TO MIGRATION QUEUE →
    </Button>
    <Button variant="ghost" style={{ width: '100%', marginTop: 8 }}
            onClick={clearSelection}>
      CLOSE →
    </Button>
  </div>
</div>
```

**FeatureRadarChart** (Recharts RadarChart — tactical styling):
```tsx
// Custom dot: none. Lines only. No background fill.
// Stroke: var(--acid) at full opacity for active line
// PolarGrid: stroke var(--rule), strokeWidth 0.5
// PolarAngleAxis: tick in JetBrains Mono 10px, fill var(--cream-25)
// No legend
// Area fill: var(--acid) at 8% opacity
```

---

### 5.5 Migrate View (`src/views/Migrate/MigrateView.tsx`)

```tsx
// Layout:
// SectionIndex [01] MIGRATION QUEUE
// [GRID: TierNav (20%) | EndpointList (40%) | Status/Info panel (40%)]
// [1px rule at 32px margin]
// SectionIndex [02] PQC ALGORITHMS
// [AlgorithmInfoPanel — full width, 2-card editorial]
// [1px rule]
// SectionIndex [03] AUDIT LOG
// [AuditTrail — full width]
```

**TierNav** — vertical pill nav for tier filter:
```tsx
// Items: ALL | CRITICAL | HIGH | MEDIUM | LOW
// Each item: Syne 11px uppercase, padding 10px 0
// Active: --acid left bar (2px) + --acid text
// Inactive: --cream-25 text
// No background on any item
// Bottom item: count in JetBrains Mono 12px --cream-25
```

**MigrationQueuePanel** — endpoint list:
Uses `DataTable`. Same Tactical Data Row spec. Adds left-side checkbox (custom styled: 14px square, `border: 1px solid var(--rule-strong)`, checked = `background: var(--acid)` with a tick mark in black).

Footer of panel: "RUN MIGRATION →" button (disabled unless ≥ 1 selected). Also "CLEAR SELECTION" ghost button.

**MigrationJobStatus** — right panel when job running:
```tsx
// SectionIndex number="" label="JOB STATUS"
// Large central: Bebas Neue 48px processed count + "/" + total
// Progress: 2px hairline progress bar, full width
// Below: StatusTimeline
```

**StatusTimeline**:
```tsx
// Scrollable vertical list of status events
// Each event:
//   [JetBrains Mono 10px --cream-25 timestamp]
//   [6px dot — tier colour or acid if complete, red if rollback]
//   [Syne 12px --cream endpoint name] → [Syne 11px status text]
// 
// Most recent event at TOP
// Currently active endpoint: dot pulses (CSS animation, 1s ease)
// Rollback entries: entire row has --r-critical-bg background tint
```

**AlgorithmInfoPanel** (`AlgorithmInfoPanel.tsx`) — "The Magazine Spread":

```tsx
// Two full-width cards side by side, equal height, 1px rule between them
// This is the editorial "hero" of the Migrate view — treat it like a magazine feature spread

<div style={{
  display: 'grid', gridTemplateColumns: '1fr 1fr',
  border: '1px solid var(--rule)', gap: 0,
}}>
  <AlgorithmCard
    tag="[FIPS 203]"
    name="ML-KEM-768"
    subtitle="Module Lattice Key Encapsulation"
    description="Post-quantum key exchange. Replaces RSA and ECDH. NIST Security Level 3."
    metrics={[
      { label: 'PUBLIC KEY', value: '1,184' },
      { label: 'CIPHERTEXT', value: '1,088' },
      { label: 'SHARED SECRET', value: '32' },
      { label: 'NIST LEVEL', value: '3' },
    ]}
    unit="BYTES"
    status={{ label: 'KEM ROUND-TRIP', value: 'VERIFIED →', ok: true }}
  />
  <AlgorithmCard
    tag="[FIPS 204]"
    name="ML-DSA-65"
    subtitle="Module Lattice Digital Signature"
    description="Post-quantum digital authentication. Replaces RSA and ECDSA signatures."
    metrics={[
      { label: 'PUBLIC KEY', value: '1,952' },
      { label: 'SIGNATURE', value: '3,309' },
      { label: 'SECURITY', value: 'Level 3' },
      { label: 'SCHEME', value: 'Lattice' },
    ]}
    unit="BYTES"
    status={{ label: 'SIGNATURE VERIFY', value: 'PASSED →', ok: true }}
    borderLeft
  />
</div>
```

`AlgorithmCard` internal layout:
```
[tag: "[FIPS 203]" — Bebas Neue 13px --acid, letter-spacing 0.08em]
[name: "ML-KEM-768" — Cormorant Garamond italic 36px --cream, mt: 8px]
[subtitle: Syne 11px uppercase --cream-60, mt: 4px]
[1px rule, mt/mb: 20px]
[description: Cormorant Garamond 15px --cream-60]
[1px rule, mt/mb: 20px]
[metrics: 2×2 grid]
  each metric cell:
    [label: Syne 10px uppercase --cream-25]
    [value: Bebas Neue 32px --cream]
    [unit: Syne 10px uppercase --cream-25]
[1px rule, mt: 20px]
[status row: JetBrains Mono 12px. "SIGNATURE VERIFY: PASSED →" in --r-low if ok]
```

This card layout is the visual centrepiece of the whole Migrate view. The `36px` Cormorant Garamond italic algorithm name vs the `32px` Bebas Neue metric numbers creates the luxury-data tension the design is built on.

**AuditTrail** (`AuditTrail.tsx`):
```tsx
// Search/filter: underline-only input, JetBrains Mono, placeholder "FILTER BY ENDPOINT..."
// Table using AuditLogTable component
// Each row:
//   [JetBrains Mono 11px --cream-25 timestamp]
//   [Syne 12px --cream endpoint name]
//   [→ arrow --cream-25]
//   [Syne 12px from_status → to_status, to_status coloured by --r-{tier} or --r-low/--r-critical]
```

---

### 5.6 Login View (`src/views/Auth/LoginView.tsx`)

Full-screen. Split layout: Left 50% is the visual hero. Right 50% is the form.

```
LEFT PANEL (background: var(--field)):
  Centered vertically:
  - ReticleMark SVG at 100×100, --acid, slowly rotating
  - "FORTIQ" Bebas Neue 64px --cream below
  - Cormorant Garamond 16px italic --cream-60: "Quantum-Safe Migration Platform"
  - JetBrains Mono 11px --cream-25 at bottom: "ML-KEM-768 · ML-DSA-65 · FIPS 203/204"

RIGHT PANEL (background: var(--void)):
  Centered vertically, max-width 340px:
  - SectionIndex "[01]" "AUTHENTICATION"
  - Two underline-only inputs: USERNAME, PASSWORD
  - "AUTHENTICATE →" primary button, full width
  - Error in [ERR-001] format below button if failed
```

---

### 5.7 Primitive Components

**`Button.tsx`**:
Three variants (`primary`, `ghost`, `danger`). Always letter-spaced Syne uppercase. Always ends with ` →` suffix (render as `{children} →`). Border-radius: 2px.

**`RiskBadge.tsx`**:
```tsx
<span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
  <span style={{ width: 6, height: 6, borderRadius: '50%',
                 background: `var(--r-${tier})`, flexShrink: 0 }} />
  <span style={{ fontFamily: 'var(--font-ui)', fontSize: 11, fontWeight: 700,
                 letterSpacing: '0.12em', textTransform: 'uppercase',
                 color: `var(--r-${tier})` }}>
    {tier}
  </span>
</span>
```

**`ProgressBar.tsx`**:
```tsx
<div style={{ height: 2, background: 'var(--rule)', position: 'relative', overflow: 'hidden' }}>
  <div style={{
    height: '100%',
    width: `${value}%`,
    background: tierColor ?? 'var(--acid)',
    transition: 'width var(--t-slow) var(--ease-out)',
  }} />
</div>
```

**`Skeleton.tsx`**:
```tsx
<div style={{
  background: `linear-gradient(90deg, var(--recess) 0%, rgba(242,239,230,0.04) 50%, var(--recess) 100%)`,
  backgroundSize: '200% 100%',
  animation: 'skeleton-sweep 1.8s ease infinite',
  borderRadius: 2,
  height,
  width,
}} />
```

**`Modal.tsx`**:
No rounded corners on modal itself (border-radius: 4px only). Header line immediately below title. Backdrop is `rgba(2,2,4,0.85)` with `backdrop-filter: blur(8px)`. Close button is `CLOSE →` text, top-right.

**`ConfirmModal.tsx`** (for migration trigger):
- Title in Cormorant Garamond 22px
- Description in Syne 14px `--cream-60`
- Underline-only input. JetBrains Mono 13px. Placeholder: `TYPE CONFIRM TO PROCEED`
- Confirm button: disabled and `--cream-25` coloured until value === "CONFIRM"
- On valid input: button activates to `--acid` coloured primary

**`ReticleMark.tsx`** — the signature decorative SVG:
```tsx
export function ReticleMark({ style }: { style?: React.CSSProperties }) {
  return (
    <svg viewBox="0 0 40 40" fill="none" style={style} xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="0.5" />
      <circle cx="20" cy="20" r="10" stroke="currentColor" strokeWidth="0.5" />
      <circle cx="20" cy="20" r="2" fill="currentColor" />
      <line x1="0" y1="20" x2="8" y2="20" stroke="currentColor" strokeWidth="0.5" />
      <line x1="32" y1="20" x2="40" y2="20" stroke="currentColor" strokeWidth="0.5" />
      <line x1="20" y1="0" x2="20" y2="8" stroke="currentColor" strokeWidth="0.5" />
      <line x1="20" y1="32" x2="20" y2="40" stroke="currentColor" strokeWidth="0.5" />
    </svg>
  );
}
```

---

### Phase 5 Checklist (Updated)

- [ ] Bebas Neue renders at 96px for compliance score. Cormorant Garamond renders at 36px for algorithm card names
- [ ] CoordinateReadout in TopBar shows live ticker with `··` separators in JetBrains Mono
- [ ] LiveClock in TopBar updates every second
- [ ] SectionIndex `[NN] ─────── LABEL` appears at top of every panel
- [ ] Left spine is 56px, not 240px. Active nav item has acid left bar, not filled background
- [ ] NetworkGraph fills full width at 55vh height with CoordOverlay in top-right
- [ ] Endpoint detail drawer pushes (compresses) main content — does NOT overlay
- [ ] AlgorithmInfoPanel shows ML-KEM-768 + ML-DSA-65 in full editorial card format
- [ ] Bebas Neue metric numbers (32px) visible in algorithm cards
- [ ] Cormorant Garamond italic algorithm names (36px) visible in algorithm cards
- [ ] All inputs are underline-only (no box border)
- [ ] Progress bars are 2px height (not 8px)
- [ ] RiskBadge uses dot + text, no coloured pill background
- [ ] Login view has left-panel hero with reticle + right-panel form
- [ ] ConfirmModal input activates button only when typed value === "CONFIRM"
- [ ] ReticleMark SVG appears as watermark in ComplianceHero at 4–5% opacity
- [ ] Empty state uses Bebas Neue 32px + Cormorant Garamond italic — not generic placeholder text
- [ ] Error messages use `[ERR-NNN]` format in JetBrains Mono
- [ ] No Inter, Roboto, or system-ui anywhere in the codebase