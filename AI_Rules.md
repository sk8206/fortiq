# AI_Rules.md — Fortiq Coding Agent Ruleset (Design v3: Tactical Luxury)

> These rules are absolute. Read Section 4 (Design System) before touching a single component. The design direction is the most important thing that separates Fortiq from a generic dashboard.

---

## 0. Critical Research Findings (Unchanged — still mandatory)

1. Use `ML-KEM-768` and `ML-DSA-65` — NOT Kyber768/Dilithium3.
2. Use `lightning.qubit` — NOT `default.qubit`.
3. Use `react-force-graph-2d` — NOT raw D3 in React.
4. Celery tasks are `def` (sync). Use `asyncio.run()` only when needed.
5. JWT access token in memory (Zustand). Refresh token in HttpOnly cookie only.

---

## 1. Technology Stack (Unchanged)

Same as v2. See previous AI_Rules.md. No changes to backend or library choices.

---

## 2–3. Backend Architecture Rules (Unchanged)

Same layered architecture, same async rules, same PQC/QML module isolation. See v2.

---

## 4. DESIGN SYSTEM — "TACTICAL LUXURY" (Complete Rewrite)

This is the defining aesthetic update. Every component must breathe this language.

### 4.1 Design Philosophy & Inspiration

Fortiq's visual language fuses three references into one coherent identity:

**From darknode.army:**
Operational precision. Live telemetry feel. Coordinate readouts in the UI (`ENDPOINTS: 142 | CRITICAL: 15`). Crosshair and reticle SVG marks. Section index numbers styled like military designations — `[01]`, `[02]`. Timestamps and system clocks running in the corner. The entire interface feels like a classified ops briefing room — every number matters, nothing is decorative without also being functional.

**From detroit.paris:**
Editorial luxury. Compressed uppercase display type at extreme sizes. Horizontal rules as structural punctuation. Sparse composition — white (or in Fortiq's case, void black) space is an active design element, not absence. The confidence to let a 96px number sit alone and dominate a card. Asymmetric column layouts that break the boring 12-grid. Text mixed with visual data rather than separated from it.

**From GQ Extraordinary Lab:**
Magazine architecture applied to data. Section headers that read like chapter openers. Pull-quote-style callouts that isolate a single critical number. Sequential section numbers as editorial scaffolding. The sense that a skilled art director chose what was on each panel, not just a developer filling containers.

**The synthesis — "Ops Center Luxury":**
Imagine a classified intelligence briefing that has been art-directed by a Parisian design studio. Dark. Precise. Typographically bold. Every data point is a designed element, not just a rendered value.

---

### 4.2 Typography System (Complete Change)

Load these from Google Fonts / Fontsource. Add ALL to `index.html` preconnect.

```html
<!-- index.html head -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Syne:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

| Role | Font | Size | Weight | Case | Use |
|---|---|---|---|---|---|
| Hero numbers | **Bebas Neue** | 96px | 400 | UPPER | Compliance score, hero stats |
| Section markers | **Bebas Neue** | 48px | 400 | UPPER | `[01]` section numbers |
| Display headings | **Cormorant Garamond** | 28–36px | 600 | Title | Card titles, panel names |
| Display italic | **Cormorant Garamond** | 28px | 400 italic | Mixed | Secondary headings, sub-labels |
| UI labels | **Syne** | 11–13px | 700 | UPPER | Column headers, status labels, nav items |
| Body / descriptions | **Syne** | 14–15px | 400 | Sentence | Description text, panel body |
| Data values | **Syne** | 18–24px | 500 | — | Stat numbers (not hero-sized) |
| Tactical mono | **JetBrains Mono** | 11–13px | 500 | — | Coordinates, hashes, algorithm names, config content |
| Ticker / telemetry | **JetBrains Mono** | 11px | 400 | UPPER | Live readouts, timestamps, `X: 1393 Y: 0326` style |

**Typography Rules:**
- `Bebas Neue` is reserved for numbers and `[NN]` markers ONLY. Never for paragraph text.
- `Cormorant Garamond` is used for every heading — including card titles, section headings, panel names. The serif/data-mono contrast is the visual signature of this design.
- `Syne` handles all UI chrome — labels, badges, body text, navigation.
- `JetBrains Mono` handles every piece of data that is "system output" — hashes, algorithm names, byte counts, timestamps, coordinate-style readouts.
- Letter-spacing on `Syne` uppercase labels: `0.12em`. This is the luxury editorial detail.
- Never use Inter, Roboto, or system-ui. Never.

---

### 4.3 Color Palette (Updated)

```css
:root {
  /* ── Void ────────────────────────────────────────── */
  --void:         #020204;   /* absolute background — deeper than black */
  --field:        #08080F;   /* primary surface — cards, panels */
  --lift:         #0E0E18;   /* elevated layer — modals, dropdown, hover */
  --recess:       #14141F;   /* inset — table alternates, input backgrounds */

  /* ── Cream (primary text — warm, not harsh) ───────── */
  --cream:        #F2EFE6;   /* primary text — the detroit.paris off-white */
  --cream-60:     rgba(242,239,230,0.60);  /* secondary text */
  --cream-25:     rgba(242,239,230,0.25);  /* disabled / placeholder */
  --cream-10:     rgba(242,239,230,0.10);  /* subtle hover */
  --cream-05:     rgba(242,239,230,0.05);  /* faintest border / row alternates */

  /* ── Acid (single hero accent — tactical electric) ── */
  --acid:         #B8FF00;   /* primary action — buttons, active states, graph accent */
  --acid-15:      rgba(184,255,0,0.15);
  --acid-08:      rgba(184,255,0,0.08);
  --acid-border:  rgba(184,255,0,0.30);

  /* ── Risk Tier (semantic only) ──────────────────── */
  --r-critical:   #FF3535;
  --r-critical-bg:rgba(255,53,53,0.08);
  --r-high:       #FF7A00;
  --r-high-bg:    rgba(255,122,0,0.08);
  --r-medium:     #F5C400;
  --r-medium-bg:  rgba(245,196,0,0.08);
  --r-low:        #00CC6A;
  --r-low-bg:     rgba(0,204,106,0.08);
  --r-unknown:    rgba(242,239,230,0.20);
  --r-unknown-bg: rgba(242,239,230,0.04);

  /* ── Structural lines ────────────────────────────── */
  --rule:         rgba(242,239,230,0.08);   /* hairline rule — section dividers */
  --rule-strong:  rgba(242,239,230,0.18);   /* heavier rule on hover / active */
  --rule-accent:  rgba(184,255,0,0.25);     /* accent-coloured rule */

  /* ── Typography scale (referenced in Tailwind) ───── */
  --font-display: 'Bebas Neue', sans-serif;
  --font-serif:   'Cormorant Garamond', serif;
  --font-ui:      'Syne', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  /* ── Spacing (4px grid) ──────────────────────────── */
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px;
  --sp-5:20px; --sp-6:24px; --sp-8:32px; --sp-10:40px;
  --sp-12:48px; --sp-16:64px; --sp-24:96px;

  /* ── Transition ──────────────────────────────────── */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in:  cubic-bezier(0.4, 0, 1, 1);
  --t-fast:   120ms;
  --t-base:   220ms;
  --t-slow:   400ms;
}
```

---

### 4.4 Layout Architecture (Editorial Redesign)

**Navigation: Left Spine** (NOT a traditional sidebar)

The left edge is a 56px narrow vertical spine — not 240px. It contains only icons with a tooltip on hover. This keeps the content area dominant and editorial. The spine uses a subtle `1px solid var(--rule)` right border.

When a nav item is active: a 2px `var(--acid)` vertical bar appears on its left edge. No background fill. Just the bar.

```
[56px spine] [main content — full remaining width]
```

**Top Bar: Tactical Ticker**

The top bar is 48px tall. It contains:
- Left: Fortiq wordmark (Bebas Neue, 20px)
- Center: Live telemetry ticker in JetBrains Mono 11px — `ENDPOINTS: 100 ·· CRITICAL: 15 ·· COMPLIANCE: 0.0%` — these update in real time after classification/migration
- Right: Live clock `WED 13:58:12 UTC` + user avatar

**Grid Rules**

- Main content area: 40px horizontal padding
- Content max-width: 1440px centred
- Section dividers: `1px solid var(--rule)` horizontal rules, full width
- Panels use 24px padding, NO border-radius on outer containers (sharp edges = tactical)
- Cards use `4px` border-radius only (not 8–12px — those look corporate)
- Gap between panels: 1px (the rule itself acts as the separator, not gap + border)

**Z-index stack**: Base(0), Sticky(10), Dropdown(20), Drawer(30), Modal(40), Ticker(50)

---

### 4.5 Signature UI Patterns (New — Implement Exactly)

These are the distinguishing elements borrowed directly from the reference sites.

#### Pattern 1: Section Indexer `[NN]`

Every major panel or section must have a section index number.

```tsx
// Component: SectionIndex
<div className="section-index">
  <span className="section-number">[01]</span>  {/* Bebas Neue 14px, --acid color */}
  <span className="section-rule" />              {/* 1px horizontal line, flex-1 */}
  <span className="section-label">ASSET REGISTRY</span>  {/* Syne 11px uppercase, --cream-60 */}
</div>
```

CSS:
```css
.section-index {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.section-number {
  font-family: var(--font-display);
  font-size: 13px;
  color: var(--acid);
  letter-spacing: 0.08em;
  white-space: nowrap;
}
.section-rule {
  flex: 1;
  height: 1px;
  background: var(--rule);
}
.section-label {
  font-family: var(--font-ui);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--cream-60);
  text-transform: uppercase;
  white-space: nowrap;
}
```

Use this at the top of every panel: `[01] ─────────────── ASSET REGISTRY`

#### Pattern 2: Coordinate Readout

Borrowed from darknode.army's `X: 1393 Y: 0326` corner display. In Fortiq, use it to show live operational data.

```tsx
// Component: CoordinateReadout — lives in top bar center
<div className="coord-ticker">
  <CoordItem label="ENDPOINTS" value={stats.total} />
  <span className="coord-sep">··</span>
  <CoordItem label="CRITICAL" value={stats.by_tier.critical} color="var(--r-critical)" />
  <span className="coord-sep">··</span>
  <CoordItem label="MIGRATED" value={stats.by_status.complete} />
  <span className="coord-sep">··</span>
  <CoordItem label="COMPLIANCE" value={`${stats.compliance_score.toFixed(1)}%`} color={complianceColor} />
</div>

// CoordItem: JetBrains Mono 11px. Label in --cream-25, value in --cream.
// Example render: CRITICAL: 15
```

#### Pattern 3: Hero Stat Block

For the compliance score and main numbers — take inspiration from detroit.paris's bold single-number compositions.

```tsx
// In ComplianceGauge — no traditional circular gauge
// Instead: giant Bebas Neue number + editorial label below
<div className="hero-stat">
  <div className="hero-number">
    {/* Bebas Neue 96px, --cream, leading: 1.0 */}
    <CountUp end={score} suffix="%" duration={1.2} />
  </div>
  <div className="hero-divider" />   {/* 1px rule, 100% width */}
  <div className="hero-label">
    {/* Cormorant Garamond 14px italic, --cream-60 */}
    Cryptographic Compliance Score
  </div>
  {/* Below: 4 mini tier bars */}
  <MiniTierBreakdown />
</div>
```

The `96px` Bebas Neue compliance number IS the gauge. No SVG arc needed — the editorial number IS more powerful and more distinctive.

#### Pattern 4: Reticle Mark

A purely decorative but identity-defining SVG element borrowed from darknode.army. Used as:
- Subtle background element on the hero stat card (10% opacity)
- Cursor-following SVG in the network graph area (very subtle)
- Corner decoration on the migration status panel

```tsx
// Component: ReticleMark — purely decorative SVG
// 40×40px crosshair circle: outer ring + cross lines + center dot
// Rendered at 5% opacity as panel background watermark
// At 15% opacity as active section indicator
```

#### Pattern 5: Tactical Data Row

Table rows and list items use a military briefing aesthetic — not standard web tables.

```
[RETICLE DOT] [ENDPOINT NAME ────────────] [RSA-2048] [CRITICAL] [0.92] [PENDING →]
```

- Left: 6px solid dot in risk tier colour (not a full badge — a dot)
- Name: left-aligned, Syne 13px, `--cream`
- Algorithm: JetBrains Mono 12px, `--cream-25`
- Risk tier: text only, `--r-{tier}` colour, Syne 11px uppercase, no background pill
- Score: Syne 14px 500, `--cream`
- Status: Syne 11px uppercase + single right-arrow `→` for active states

Row height: 44px. No alternating backgrounds — use `1px solid var(--rule)` separator only.

#### Pattern 6: Editorial Panel Header

Every panel card has this exact structure at its top:

```tsx
<div className="panel-header">
  <SectionIndex number="[02]" label="RISK CLASSIFICATION" />
  <div className="panel-header-actions">
    {/* any action buttons here */}
  </div>
</div>
<div className="panel-rule" />  {/* 1px rule, --rule-strong */}
```

#### Pattern 7: Drawer — Editorial Detail Panel

When an endpoint is selected, the detail drawer slides in from the right — full height, 480px wide. BUT it doesn't overlay the content. It pushes the main content area to compress. This creates an editorial layout shift that feels intentional, not accidental.

The drawer has:
- **Top section**: Endpoint name in Cormorant Garamond 28px + host in JetBrains Mono 13px
- **Section divider**: full-width rule
- **Data grid**: 2-column grid, each field labeled in Syne 10px uppercase + value in Syne 14px
- **Feature profile**: Recharts RadarChart — but styled with `--acid` fill at 15% opacity, `--acid` stroke, custom labels in JetBrains Mono 11px
- **Footer**: "ADD TO MIGRATION QUEUE →" button — full width, `--acid-08` background, `--acid` border, `--acid` text

---

### 4.6 Component Anatomy (Updated)

**Panel Card:**
```
background: var(--field)
border: 1px solid var(--rule)
border-radius: 4px          ← sharp, not corporate
padding: 24px
```
No box-shadow. No glow. Structure comes from the rule borders alone.

**Risk Tier Display** (NOT a pill/badge — a text treatment):
```
font-family: var(--font-ui)
font-size: 11px
font-weight: 700
letter-spacing: 0.12em
text-transform: uppercase
color: var(--r-{tier})
```
No background colour. The text colour IS the indicator. Paired with a 6px dot (same colour) to the left for accessibility.

**Button (primary):**
```
font-family: var(--font-ui)
font-size: 12px
font-weight: 700
letter-spacing: 0.10em
text-transform: uppercase
color: var(--acid)
background: var(--acid-08)
border: 1px solid var(--acid-border)
border-radius: 2px           ← very tight radius — military utility
padding: 10px 20px
```
After label, include `→` (U+2192). Hover: `background: var(--acid-15)`.

**Button (ghost):**
Same sizing. `color: var(--cream-60)`, `border: 1px solid var(--rule)`, `background: transparent`. Hover: `background: var(--cream-05)`.

**Button (danger):**
`color: var(--r-critical)`, `border: 1px solid var(--r-critical-bg)`, `background: var(--r-critical-bg)`.

**Input:**
```
background: var(--recess)
border: none
border-bottom: 1px solid var(--rule-strong)   ← underline only — editorial
border-radius: 0                               ← no radius
padding: 10px 0px
font-family: var(--font-mono)
font-size: 13px
color: var(--cream)
```
Focus: `border-bottom-color: var(--acid)`. No box-shadow. The underline-only input is the luxury detail.

**Progress Bar:**
```
track: height 2px, background var(--rule)       ← hairline, not chunky
fill: background var(--r-{tier}) or var(--acid)
no border-radius
```
2px, not 4px or 8px. Ultra thin. It reads as data precision, not a loading bar.

**Tooltip:**
```
background: var(--lift)
border: 1px solid var(--rule-strong)
border-radius: 2px
padding: 8px 12px
font-family: var(--font-mono)
font-size: 11px
color: var(--cream)
```

**Network Graph Nodes:**
- Use `react-force-graph-2d` canvas rendering
- Node fill: risk tier colours
- Node outline: 1px cream at 20% opacity
- Graph canvas background: `var(--void)`
- Link colour: `rgba(242,239,230,0.05)`
- Selected node: `--acid` ring (2px outline, canvas drawArc)
- Node label: JetBrains Mono 10px, `--cream-60`

**Modal:**
```
background: var(--field)
border: 1px solid var(--rule-strong)
border-radius: 4px
backdrop: rgba(2,2,4,0.85) backdrop-filter: blur(8px)
```
Modal header: full-width rule below it. No modal close "×" — a "CLOSE →" text button.

**Toast:**
Fixed bottom-right. Width 300px. `background: var(--lift)`. Left border: `3px solid var(--r-{level})` or `var(--acid)`. Font: Syne 12px. Letter-spacing 0.08em. NO rounded corners. Slide in from right.

**Skeleton Loading:**
```
background: linear-gradient(
  90deg,
  var(--recess) 0%,
  rgba(242,239,230,0.04) 50%,
  var(--recess) 100%
)
background-size: 200% 100%
animation: skeleton-sweep 1.8s ease infinite
```

**CodeBlock (config viewer):**
```
background: var(--void)
border: 1px solid var(--rule)
border-radius: 2px
font-family: var(--font-mono)
font-size: 12px
line-height: 1.7
padding: 20px 24px
```
Syntax highlighting via highlight.js `github-dark` theme — but override the background to match `var(--void)`.

---

### 4.7 View-Level Layout Specs

#### Dashboard — "Intelligence Overview"

```
[TOPBAR: 48px — ticker + clock + user]
[SPINE: 56px] [MAIN CONTENT: remaining width, 40px h-padding]
              ├── [SectionIndex: [01] ─ INTELLIGENCE OVERVIEW]
              ├── [HERO ROW: 3 columns]
              │   ├── ComplianceHero (Bebas Neue 96px number, full height)
              │   ├── TierBreakdown (Recharts PieChart, editorial-styled)
              │   └── LiveFeed (last 8 audit entries, scrolling)
              ├── [1px rule]
              ├── [SectionIndex: [02] ─ ASSET REGISTRY]
              └── [MigrationProgressTable — full width]
```

**ComplianceHero card** occupies ~35% of the hero row width. The number is everything.

#### Scan View — "Network Discovery"

```
[SectionIndex: [01] ─ NETWORK TOPOLOGY]
[FULL WIDTH: NetworkGraph — 65% height of viewport]
  [CoordinateOverlay — top-right of graph canvas]
    NODES: 100 ·· EDGES: 34 ·· SCALE: 1.0×
[SectionIndex: [02] ─ CLASSIFICATION ENGINE]
[2 COLUMNS: ClassifyPanel (left 40%) | ModelComparison (right 60%)]
```

The network graph is the HERO of this view — full width, not trapped in a column.

#### Migrate View — "Orchestration"

```
[SectionIndex: [01] ─ MIGRATION QUEUE]
[3 COLUMNS: TierNav (left 20%) | EndpointList (center 40%) | JobStatus OR AlgoInfo (right 40%)]
[1px rule]
[SectionIndex: [02] ─ PQC ALGORITHMS]
[AlgorithmInfoPanel — full width, 2-card editorial layout]
[1px rule]
[SectionIndex: [03] ─ AUDIT LOG]
[AuditTrail — full width]
```

**AlgorithmInfoPanel**: The two PQC algorithm cards sit side by side at full width. Each card has:
- Large algorithm name in Cormorant Garamond italic 32px
- `[FIPS 203]` section marker in Bebas Neue + acid colour
- Byte metrics in two columns: label (Syne 10px uppercase) / value (Bebas Neue 28px)
- Bottom row: `VERIFICATION → PASSED ✓` in JetBrains Mono 12px, `--r-low` colour

This is the "magazine spread" moment of the app — two large editorial cards like a GQ feature layout.

---

### 4.8 Animation Rules (Updated)

- **No auto-playing decorative animations.** Fortiq is a professional ops tool. Motion serves data, not aesthetics.
- **Entrance**: `opacity: 0 → 1` + `transform: translateY(6px) → 0`. Duration 300ms. Stagger 40ms between sections.
- **Ticker update**: When a live counter changes (compliance score, endpoint count), flash the value — `color: var(--acid)` for 400ms then fade back to `var(--cream)`.
- **Drawer open**: `transform: translateX(480px) → translateX(0)`. Duration 280ms ease-out. Main content simultaneously `width: 100% → calc(100% - 480px)`.
- **Network graph nodes**: Fade in sequentially, 25ms stagger. Max 2s total animation time.
- **Reticle rotation**: The `ReticleMark` background watermark rotates at `0.3rpm` (very slow, barely perceptible). CSS: `animation: reticle-spin 200s linear infinite`. Only on the ComplianceHero card.
- **Compliance number CountUp**: 1.2s duration, easeOutExpo. Only on first mount.
- Always wrap in `@media (prefers-reduced-motion: reduce)`.

---

### 4.9 Tailwind Config (Updated)

```js
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        void:    'var(--void)',
        field:   'var(--field)',
        lift:    'var(--lift)',
        recess:  'var(--recess)',
        cream:   'var(--cream)',
        acid:    'var(--acid)',
        risk: {
          critical: 'var(--r-critical)',
          high:     'var(--r-high)',
          medium:   'var(--r-medium)',
          low:      'var(--r-low)',
          unknown:  'var(--r-unknown)',
        },
      },
      fontFamily: {
        display: ['Bebas Neue', 'sans-serif'],
        serif:   ['Cormorant Garamond', 'serif'],
        ui:      ['Syne', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '4px',   // tactical default
        sm: '2px',
        none: '0',
      },
      letterSpacing: {
        tactical: '0.12em',
        wide:     '0.08em',
      },
    },
  },
  plugins: [],
}
```

---

## 5. Frontend Architecture Rules (Unchanged from v2)

Same Zustand rules, same API client pattern, same strict TypeScript.

---

## 6. Cybersecurity Rules (Unchanged from v2)

Same JWT, CORS, rate limiting, Docker security rules.

---

## 7. Code Quality Rules (Unchanged from v2)

---

## 8. UI/UX Clarity Rules (Updated for new design)

- **Every piece of data has Syne or JetBrains Mono** — never mix serif for data values.
- **Cormorant Garamond is for panel titles and headings only** — not for any data value or label.
- **Bebas Neue is for numbers and `[NN]` markers only** — never for descriptive text.
- **Risk tier = text + dot** — the `RiskBadge` component always renders a `6px × 6px` solid circle in tier colour + uppercase text label. Never just a coloured pill.
- **Empty states use editorial typography**: "NO ENDPOINTS CLASSIFIED" in Bebas Neue 32px, below it: "Run the classification engine to assign risk tiers." in Cormorant Garamond 16px italic.
- **Confirmation modals** for migration: The input field is an underline-only input in JetBrains Mono. Placeholder: `TYPE CONFIRM TO PROCEED`. The confirm button is initially disabled (`--cream-25` colour), activates only when value equals "CONFIRM".
- **Jargon tooltips**: `(?)` hover trigger using Syne 10px uppercase label. Tooltip body in Syne 13px. Maximum 2 sentences.
- **Keyboard navigation**: Focus ring = `outline: 1px solid var(--acid); outline-offset: 3px`. Matches accent colour.
- **Error messages**: Format — `[ERR-001] Cannot connect to API server. Verify docker compose up is running.` The `[ERR-001]` prefix is in JetBrains Mono `--r-critical`, the rest in Syne `--cream-60`. Military error code format.