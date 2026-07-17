# Project_Architecture.md — Fortiq System Architecture (Research-Informed v2)

**Stack**: Python 3.11 · FastAPI · PennyLane `lightning.qubit` · liboqs 0.15.0 (ML-KEM-768, ML-DSA-65) · PostgreSQL 16 · Redis 7 · Celery 5 · React 18 · Vite 5 · TailwindCSS · React Query v5 · Zustand · react-force-graph-2d · Recharts

---

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FORTIQ SYSTEM                           │
│                                                                 │
│  ┌──────────────────┐   HTTP/REST    ┌───────────────────────┐  │
│  │   React SPA      │ ─────────────▶ │    FastAPI Backend    │  │
│  │   (Vite Dev)     │                │  Router→Service→Repo  │  │
│  │   Port 5173      │ ◀──────────── │    Port 8000           │  │
│  └──────────────────┘   JSON Env.   └──────────┬────────────┘  │
│                                                │                │
│                              ┌─────────────────┤               │
│                              │                 │               │
│                    ┌─────────▼──────┐  ┌───────▼────────────┐  │
│                    │  PostgreSQL 16  │  │  Celery Workers    │  │
│                    │  Port 5432      │  │  (QML + PQC Jobs)  │  │
│                    │  Async: asyncpg │  │  SYNC SQLAlchemy   │  │
│                    │  Sync: psycopg2 │  │  Port n/a          │  │
│                    └────────────────┘  └───────────┬─────────┘  │
│                                                    │            │
│                                         ┌──────────▼────────┐  │
│                                         │     Redis 7       │  │
│                                         │     Port 6379     │  │
│                                         │  Broker + Results │  │
│                                         └───────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Architectural Notes

1. **Dual session architecture**: FastAPI uses `AsyncSession` (asyncpg). Celery uses `Session` (psycopg2). Never mixed.
2. **Celery is sync**: All tasks are `def`, never `async def`. liboqs and PennyLane run in Celery only.
3. **React Query owns server state**: Endpoints, stats, job status — all React Query. Zustand holds UI state only.
4. **react-force-graph-2d** for the network graph: WebGL canvas, not D3 VDOM.

---

## 2. Repository Structure

```
fortiq/
├── .env.example
├── .env                            ← gitignored
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml                  ← ruff, mypy, black config
├── docker-compose.yml
├── README.md
│
├── AI_Rules.md
├── PLAN.md
├── PRD.md
├── Project_Architecture.md
│
├── docs/
│   ├── environment-notes.md        ← liboqs build notes, OS-specific issues
│   └── api-examples.http           ← REST Client examples for manual testing
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt            ← pinned production deps
│   ├── requirements-dev.txt        ← pytest, mypy, black, ruff, etc.
│   ├── alembic.ini
│   │
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 0001_initial_schema.py
│   │       └── 0002_seed_admin_user.py
│   │
│   ├── models/                     ← gitignored (binary model artefacts)
│   │   ├── .gitkeep
│   │   ├── vqc_params.npy          ← created by train_models.py
│   │   ├── svm_model.pkl           ← created by train_models.py
│   │   └── normalizer.pkl          ← created by train_models.py
│   │
│   ├── data/
│   │   ├── .gitkeep
│   │   └── endpoints_synthetic.csv ← created by generate_dataset.py
│   │
│   ├── migrations_generated/       ← gitignored (text config files)
│   │   └── .gitkeep
│   │
│   ├── scripts/
│   │   ├── generate_dataset.py     ← creates 100 synthetic endpoints in DB
│   │   ├── train_models.py         ← trains VQC + SVM, saves to models/
│   │   └── create_admin.py         ← creates default admin account
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py                 ← FastAPI app factory with lifespan
│       ├── celery_app.py           ← Celery instance configuration
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py           ← pydantic-settings BaseSettings
│       │   ├── database.py         ← DUAL SESSION: async (FastAPI) + sync (Celery)
│       │   ├── logging.py          ← structlog JSON config + request middleware
│       │   ├── security.py         ← JWT encode/decode, BCrypt hashing
│       │   └── dependencies.py     ← FastAPI Depends(): get_db, get_current_user
│       │
│       ├── models/                 ← SQLAlchemy ORM models (table definitions)
│       │   ├── __init__.py
│       │   ├── base.py             ← declarative_base(), common timestamp mixin
│       │   ├── endpoint.py
│       │   ├── scan_job.py
│       │   ├── migration_config.py
│       │   ├── audit_log.py
│       │   ├── model_evaluation.py
│       │   └── user.py
│       │
│       ├── schemas/                ← Pydantic v2 request/response models
│       │   ├── __init__.py
│       │   ├── common.py           ← ResponseEnvelope[T], ErrorDetail, PaginationMeta
│       │   ├── endpoint.py         ← EndpointListItem, EndpointDetail, EndpointFilters
│       │   ├── job.py              ← JobStatus, JobCreate
│       │   ├── auth.py             ← LoginRequest, TokenResponse, UserResponse
│       │   └── migration.py        ← MigrateRequest, MigrationConfigDTO, PQCDemoResult
│       │
│       ├── repositories/           ← DB access layer (async, FastAPI context)
│       │   ├── __init__.py
│       │   ├── endpoint_repository.py
│       │   ├── job_repository.py
│       │   ├── migration_repository.py
│       │   └── audit_repository.py
│       │
│       ├── services/               ← Business logic (calls repositories)
│       │   ├── __init__.py
│       │   ├── endpoint_service.py
│       │   ├── classification_service.py
│       │   ├── migration_service.py
│       │   └── auth_service.py
│       │
│       ├── routers/                ← FastAPI route handlers
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── endpoints.py
│       │   ├── classify.py
│       │   └── migrate.py
│       │
│       ├── qml/                    ← Quantum ML components
│       │   ├── __init__.py
│       │   ├── features.py         ← FeatureNormalizer + 6-feature encoding
│       │   ├── vqc.py              ← VQCClassifier (lightning.qubit + adjoint)
│       │   └── classical_baseline.py  ← SVMClassifier (sklearn RBF SVM)
│       │
│       ├── pqc/                    ← Post-Quantum Cryptography
│       │   ├── __init__.py
│       │   ├── operations.py       ← ML-KEM-768 + ML-DSA-65 demo operations
│       │   └── config_generator.py ← Migration config text generation
│       │
│       └── tasks/                  ← Celery tasks (ALL are def, not async def)
│           ├── __init__.py
│           ├── classify_task.py    ← classify_endpoints_task (sync, uses SyncSession)
│           └── migrate_task.py     ← run_migration_task (sync, uses SyncSession)
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json               ← "strict": true
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   │
│   └── src/
│       ├── main.tsx                ← ReactDOM.createRoot, QueryClientProvider, Router
│       ├── App.tsx                 ← Route definitions, ProtectedRoute wrapper
│       ├── vite-env.d.ts
│       │
│       ├── styles/
│       │   ├── tokens.css          ← All CSS custom properties (design system)
│       │   ├── global.css          ← Reset, base styles, Google Font import
│       │   └── animations.css      ← @keyframes definitions
│       │
│       ├── api/                    ← Axios API modules
│       │   ├── client.ts           ← Axios instance + auth/refresh interceptors
│       │   ├── endpoints.ts        ← /endpoints routes
│       │   ├── classify.ts         ← /classify routes
│       │   ├── migrate.ts          ← /migrate routes
│       │   └── auth.ts             ← /auth routes
│       │
│       ├── stores/                 ← Zustand (UI state only)
│       │   ├── useAuthStore.ts     ← accessToken, user (in-memory only)
│       │   └── useEndpointUIStore.ts ← selectedEndpointId, migrationQueue, sidebarCollapsed
│       │
│       ├── hooks/                  ← React Query hooks (server state)
│       │   ├── useEndpoints.ts
│       │   ├── useDashboardStats.ts
│       │   ├── useJobStatus.ts     ← polling with refetchInterval
│       │   ├── useAuditLog.ts
│       │   └── usePQCDemo.ts
│       │
│       ├── types/                  ← TypeScript interfaces
│       │   ├── endpoint.ts
│       │   ├── job.ts
│       │   ├── api.ts              ← ResponseEnvelope<T>, PaginationMeta
│       │   └── index.ts
│       │
│       ├── utils/
│       │   ├── formatters.ts       ← bytes, dates, numbers formatters
│       │   ├── riskColors.ts       ← tier → CSS var mapping
│       │   ├── queryKeys.ts        ← QUERY_KEYS constants
│       │   └── cn.ts               ← classnames helper
│       │
│       ├── components/             ← Shared reusable components
│       │   ├── layout/
│       │   │   ├── AppShell.tsx
│       │   │   ├── Sidebar.tsx
│       │   │   └── PageHeader.tsx
│       │   │
│       │   └── ui/
│       │       ├── Badge/
│       │       │   ├── index.tsx
│       │       │   └── RiskBadge.tsx        ← tier → colour badge
│       │       ├── Button/
│       │       │   └── index.tsx
│       │       ├── Card/
│       │       │   └── index.tsx
│       │       ├── StatCard/
│       │       │   └── index.tsx
│       │       ├── ProgressBar/
│       │       │   └── index.tsx
│       │       ├── Modal/
│       │       │   ├── index.tsx
│       │       │   └── ConfirmModal.tsx     ← typed CONFIRM modal
│       │       ├── Toast/
│       │       │   └── index.tsx
│       │       ├── Spinner/
│       │       │   └── index.tsx
│       │       ├── Tooltip/
│       │       │   └── index.tsx            ← PQC jargon tooltips
│       │       ├── CodeBlock/
│       │       │   └── index.tsx            ← highlight.js wrapper
│       │       ├── DataTable/
│       │       │   ├── index.tsx
│       │       │   └── types.ts
│       │       └── EmptyState/
│       │           └── index.tsx
│       │
│       └── views/                  ← Page-level views
│           ├── Auth/
│           │   └── LoginView.tsx
│           │
│           ├── Dashboard/
│           │   ├── index.tsx
│           │   ├── DashboardView.tsx
│           │   ├── ComplianceGauge.tsx      ← SVG arc gauge
│           │   ├── RiskTierBreakdown.tsx    ← Recharts PieChart
│           │   ├── StatCards.tsx
│           │   ├── RecentActivityFeed.tsx
│           │   └── MigrationProgressTable.tsx
│           │
│           ├── Scan/
│           │   ├── index.tsx
│           │   ├── ScanView.tsx
│           │   ├── ScanTriggerPanel.tsx
│           │   ├── NetworkGraph.tsx         ← react-force-graph-2d
│           │   ├── ClassifyPanel.tsx
│           │   ├── ModelComparisonTable.tsx
│           │   ├── EndpointDetailPanel.tsx  ← slide-in drawer
│           │   └── FeatureRadarChart.tsx    ← Recharts RadarChart
│           │
│           └── Migrate/
│               ├── index.tsx
│               ├── MigrateView.tsx
│               ├── MigrationQueuePanel.tsx
│               ├── MigrationJobStatus.tsx   ← status timeline + progress
│               ├── AlgorithmInfoPanel.tsx   ← ML-KEM-768 + ML-DSA-65 metadata
│               ├── MigrationConfigViewer.tsx
│               └── AuditTrail.tsx
```

---

## 3. Backend Component Architecture

### 3.1 Dependency Graph

```
Router (HTTP parse → call service → return envelope)
    │
    ▼
Service (business logic + orchestration)
    │          │
    ▼          ▼
Repository   [Celery task trigger only — no direct QML/PQC calls]
    │
    ▼
SQLAlchemy Model → PostgreSQL (ASYNC session)

─── separate process boundary ─────────────────────────────────

Celery Worker
    │          │
    ▼          ▼
qml/          pqc/
VQCClassifier  operations.py  ← ML-KEM-768 + ML-DSA-65
    │
    ▼
PennyLane lightning.qubit

SQLAlchemy Model → PostgreSQL (SYNC session via psycopg2)
```

### 3.2 Configuration (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database — two separate URLs
    DATABASE_URL: str           # postgresql+asyncpg://... (FastAPI)
    SYNC_DATABASE_URL: str      # postgresql+psycopg2://... (Celery)

    # Redis
    REDIS_URL: str

    # Auth
    SECRET_KEY: str             # min 32 bytes
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Model paths
    VQC_PARAMS_PATH: str = "models/vqc_params.npy"
    SVM_MODEL_PATH: str = "models/svm_model.pkl"
    NORMALIZER_PATH: str = "models/normalizer.pkl"

    model_config = {"env_file": ".env", "case_sensitive": True}

settings = Settings()  # raises ValidationError on startup if required vars missing
```

### 3.3 Celery App (`app/celery_app.py`)

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "fortiq",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.classify_task", "app.tasks.migrate_task"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,          # at-least-once delivery
    worker_prefetch_multiplier=1, # process one task at a time — predictable memory
    task_soft_time_limit=600,     # 10-minute soft timeout
    task_time_limit=660,          # 11-minute hard kill
)
```

---

## 4. API Route Map

All routes prefixed with `/api/v1`.

### Auth (`/auth`)

| Method | Path | Auth Required | Description |
|---|---|---|---|
| POST | `/auth/login` | No | Returns access token; sets refresh cookie |
| POST | `/auth/logout` | Cookie | Clears refresh cookie |
| POST | `/auth/refresh` | Cookie | Issues new access token from refresh cookie |
| GET | `/auth/me` | Bearer | Returns current user object |

### Endpoints (`/endpoints`)

| Method | Path | Auth Required | Description |
|---|---|---|---|
| GET | `/endpoints` | Bearer | Paginated list with `?tier&status&algorithm&page&per_page` |
| GET | `/endpoints/{id}` | Bearer | Full endpoint detail (14 fields) |
| GET | `/endpoints/stats/dashboard` | Bearer | Aggregate counts + compliance % |
| GET | `/endpoints/{id}/migration-config` | Bearer | Generated config text (list) |

### Classify (`/classify`)

| Method | Path | Auth Required | Description |
|---|---|---|---|
| POST | `/classify` | Bearer | Triggers VQC classification Celery task; returns `{job_id}` |
| GET | `/classify/jobs/{job_id}` | Bearer | Job status + `progress_pct` |
| GET | `/classify/model-comparison` | Bearer | VQC vs SVM evaluation metrics |

### Migrate (`/migrate`)

| Method | Path | Auth Required | Description |
|---|---|---|---|
| POST | `/migrate` | Bearer | Body: `{endpoint_ids: [...]}` or `{tier: "critical"}`. Returns `{job_id}` |
| GET | `/migrate/jobs/{job_id}` | Bearer | Migration job status + `current_endpoint` |
| GET | `/migrate/pqc-demo` | Bearer | ML-KEM-768 + ML-DSA-65 metadata demo |
| GET | `/migrate/audit-log` | Bearer | Paginated audit log; `?endpoint_id=&page=` |

### Health

| Method | Path | Auth Required | Description |
|---|---|---|---|
| GET | `/health` | No | `{"status": "ok"}` for Docker healthcheck |

---

## 5. Key Schema Definitions

### 5.1 Common (`schemas/common.py`)

```python
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')

class PaginationMeta(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int

class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: Any = None

class ResponseEnvelope(BaseModel, Generic[T]):
    data: Optional[T] = None
    meta: Optional[PaginationMeta] = None
    error: Optional[ErrorDetail] = None
```

### 5.2 Endpoint Schemas (`schemas/endpoint.py`)

```python
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class EndpointListItem(BaseModel):
    id: UUID
    name: str
    host: str
    algorithm: str
    risk_tier: str
    risk_score: Optional[float]
    migration_status: str
    endpoint_type: str
    data_sensitivity: int
    exposure_surface: str
    traffic_volume: str

class EndpointDetail(EndpointListItem):
    port: int
    key_length: int
    cert_expiry_days: int
    last_scanned_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class DashboardStats(BaseModel):
    total: int
    by_tier: dict[str, int]       # {"critical": 15, "high": 30, ...}
    by_status: dict[str, int]     # {"pending": 60, "complete": 25, ...}
    compliance_score: float       # 0.0 to 100.0 (one decimal)
```

### 5.3 Job Schema (`schemas/job.py`)

```python
class JobStatus(BaseModel):
    id: UUID
    status: str               # pending|running|complete|failed
    job_type: str             # classify|migrate
    total: int
    processed: int
    progress_pct: float       # processed / total * 100, rounded 1 decimal
    current_endpoint: Optional[str]  # name of endpoint being processed
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error: Optional[str]
```

### 5.4 PQC Demo Schema (`schemas/migration.py`)

```python
class KEMResult(BaseModel):
    algorithm: str          # "ML-KEM-768"
    fips_standard: str      # "FIPS 203"
    nist_security_level: int
    public_key_bytes: int
    ciphertext_bytes: int
    shared_secret_bytes: int
    encapsulation_ok: bool
    decapsulation_ok: bool

class SignatureResult(BaseModel):
    algorithm: str          # "ML-DSA-65"
    fips_standard: str      # "FIPS 204"
    nist_security_level: int
    public_key_bytes: int
    signature_bytes: int
    verification_passed: bool

class PQCDemoResult(BaseModel):
    ml_kem_768: KEMResult
    ml_dsa_65: SignatureResult
```

---

## 6. Frontend State Architecture

### 6.1 React Query — Query Keys

```typescript
// src/utils/queryKeys.ts
export const QUERY_KEYS = {
  endpoints: (filters: EndpointFilters) => ['endpoints', filters] as const,
  endpoint: (id: string) => ['endpoint', id] as const,
  dashboardStats: () => ['dashboard', 'stats'] as const,
  classifyJob: (id: string) => ['classify-job', id] as const,
  migrateJob: (id: string) => ['migrate-job', id] as const,
  modelComparison: () => ['model', 'comparison'] as const,
  pqcDemo: () => ['pqc', 'demo'] as const,
  auditLog: (filters: AuditFilters) => ['audit', filters] as const,
} as const;
```

### 6.2 Zustand — UI State Only

```typescript
// src/stores/useEndpointUIStore.ts
interface EndpointUIState {
  selectedEndpointId: string | null;
  migrationQueue: string[];         // list of endpoint IDs the user has queued
  activeJobId: string | null;       // currently running classify or migrate job

  setSelected: (id: string | null) => void;
  addToQueue: (id: string) => void;
  addTierToQueue: (tier: string, endpoints: EndpointListItem[]) => void;
  removeFromQueue: (id: string) => void;
  clearQueue: () => void;
  setActiveJobId: (id: string | null) => void;
}

// src/stores/useAuthStore.ts
interface AuthState {
  accessToken: string | null;       // in-memory only, never localStorage
  user: User | null;
  sidebarCollapsed: boolean;

  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
  toggleSidebar: () => void;
  logout: () => void;               // clears token + user
}
```

### 6.3 React Query — Key Hooks

```typescript
// src/hooks/useEndpoints.ts
export const useEndpoints = (filters: EndpointFilters) =>
  useQuery({
    queryKey: QUERY_KEYS.endpoints(filters),
    queryFn: () => endpointsApi.list(filters),
    staleTime: 30_000,
  });

// src/hooks/useJobStatus.ts
export const useJobStatus = (jobId: string | null, jobType: 'classify' | 'migrate') =>
  useQuery({
    queryKey: jobType === 'classify'
      ? QUERY_KEYS.classifyJob(jobId!)
      : QUERY_KEYS.migrateJob(jobId!),
    queryFn: () => jobsApi.getJob(jobId!, jobType),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const terminal = ['complete', 'failed', 'rollback'];
      return terminal.includes(query.state.data?.status ?? '') ? false : 2000;
    },
  });

// When a job completes, invalidate endpoint data:
// queryClient.invalidateQueries({ queryKey: ['endpoints'] })
// queryClient.invalidateQueries({ queryKey: ['dashboard', 'stats'] })
```

---

## 7. Data Flow Diagrams

### 7.1 Classification Flow

```
User: "Run Classification"
         │
         ▼
useEndpointUIStore.setActiveJobId(null)  ← clear previous
         │
         ▼
classifyApi.trigger()
→ POST /api/v1/classify
         │
         ▼ (FastAPI)
classification_service.trigger_job()
→ ScanJob row inserted (status=pending)
→ classify_endpoints_task.delay(job_id)
→ returns {job_id}
         │
         ▼ (React)
useEndpointUIStore.setActiveJobId(job_id)
useJobStatus(job_id, 'classify') starts polling every 2s
         │
         ▼ (Celery worker — separate process, sync)
classify_endpoints_task(job_id):
  with get_sync_db() as db:
    vqc = VQCClassifier.load('models/vqc_params.npy')
    for each endpoint:
      risk_tier, risk_score = vqc.predict(features)
      endpoint.risk_tier = risk_tier
      every 10: db.commit(), update_state(PROGRESS)
    job.status = 'complete'
    db.commit()
         │
         ▼ (polling detects terminal state)
refetchInterval returns false → polling stops
queryClient.invalidateQueries(['endpoints'])
queryClient.invalidateQueries(['dashboard', 'stats'])
Network graph node colours update via re-render
```

### 7.2 Migration Flow

```
User: selects "All Critical" → clicks "Run Migration"
         │
         ▼
ConfirmModal shows "Type CONFIRM to proceed"
User types CONFIRM → submits
         │
         ▼
migrateApi.trigger({ endpoint_ids: criticalIds })
→ POST /api/v1/migrate
         │
         ▼ (FastAPI)
migration_service.trigger_job(endpoint_ids)
→ ScanJob row inserted
→ run_migration_task.delay(job_id, endpoint_ids)
→ returns {job_id}
         │
         ▼ (React)
useJobStatus(job_id, 'migrate') starts polling every 2s
MigrationJobStatus component shows timeline
         │
         ▼ (Celery worker — sync)
run_migration_task(job_id, endpoint_ids):
  Sort by (tier_order DESC, risk_score DESC)
  For each endpoint:
    status: pending → in_progress  → write audit_log
    _run_ml_kem_768_demo()  ← SYNC, blocks until done
    _run_ml_dsa_65_demo()   ← SYNC, blocks until done
    generate_migration_configs(endpoint)  → DB
    status: in_progress → hybrid → write audit_log
    seed = hash(endpoint.id)[:8] → random(seed)
    if random() < 0.80:
      status: hybrid → complete, migrated_algorithm = 'ML-KEM-768 + ML-DSA-65'
    else:
      status: hybrid → rollback, reason = 'Hybrid validation timeout (simulated)'
    write audit_log
    job.processed += 1; db.commit()
    update_state(PROGRESS, {processed, total, current: endpoint.name})
  job.status = 'complete'; db.commit()
         │
         ▼ (polling detects completion)
queryClient.invalidateQueries(['endpoints'])
queryClient.invalidateQueries(['dashboard', 'stats'])
Compliance gauge animates to new value
```

### 7.3 Authentication Flow

```
App loads → App.tsx checks auth state
         │
         ├── accessToken in memory? No
         │         ▼
         │    authApi.refresh()  ← sends HttpOnly cookie
         │         ├── Cookie valid → new accessToken → isAuthenticated = true
         │         └── Cookie missing/expired → redirect to /login
         │
         └── accessToken in memory? Yes → render app
                   ▼
Login page (if needed):
  POST /auth/login {username, password}
  → response: {access_token, user}
  → cookie set: refresh_token (HttpOnly, SameSite=Strict)
  → useAuthStore.setToken(access_token)
  → useAuthStore.setUser(user)
  → navigate('/')

Axios interceptor (on 401):
  → authApi.refresh()  ← try silent refresh
  → if success: retry original request with new token
  → if fail: useAuthStore.logout() → navigate('/login')
```

---

## 8. Network Graph Node/Edge Specification

### Node Data Model

```typescript
interface GraphNode {
  id: string;
  name: string;
  risk_tier: 'critical' | 'high' | 'medium' | 'low' | 'unknown';
  risk_score: number | null;
  traffic_volume: 'critical' | 'high' | 'medium' | 'low';
  endpoint_type: string;
  migration_status: string;
  host: string;
  // Added by react-force-graph-2d simulation:
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
}

interface GraphLink {
  source: string;  // endpoint id
  target: string;  // endpoint id
  // Edge = shared /24 subnet prefix
}
```

### Edge Generation Logic

```typescript
function buildGraphLinks(endpoints: EndpointListItem[]): GraphLink[] {
  const links: GraphLink[] = [];
  const subnetGroups = new Map<string, string[]>();

  for (const ep of endpoints) {
    // Extract /24 prefix: "192.168.1.42" → "192.168.1"
    const parts = ep.host.split('.');
    if (parts.length === 4) {
      const prefix = parts.slice(0, 3).join('.');
      const group = subnetGroups.get(prefix) ?? [];
      group.push(ep.id);
      subnetGroups.set(prefix, group);
    }
  }

  for (const [, ids] of subnetGroups) {
    // Connect pairs within same subnet (max 5 edges per node to avoid clutter)
    for (let i = 0; i < Math.min(ids.length, 6); i++) {
      for (let j = i + 1; j < Math.min(ids.length, 6); j++) {
        links.push({ source: ids[i], target: ids[j] });
      }
    }
  }

  return links;
}
```

---

## 9. Docker Compose — Full Specification

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: fortiq-postgres
    restart: unless-stopped
    env_file: .env
    environment:
      POSTGRES_DB: fortiq
      POSTGRES_USER: fortiq
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fortiq -d fortiq"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 10s

  redis:
    image: redis:7-alpine
    container_name: fortiq-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: fortiq-backend
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./backend/models:/app/models          # model files persist
      - ./backend/migrations_generated:/app/migrations_generated
    ports:
      - "8000:8000"
    depends_on:
      postgres: { condition: service_healthy }
      redis:    { condition: service_healthy }
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: fortiq-celery
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./backend/models:/app/models
      - ./backend/migrations_generated:/app/migrations_generated
    depends_on:
      postgres: { condition: service_healthy }
      redis:    { condition: service_healthy }
    command: >
      celery -A app.celery_app worker
      --loglevel=info
      --concurrency=1
      --queues=fortiq

volumes:
  postgres_data:
    driver: local
```

---

## 10. Backend Dockerfile

```dockerfile
FROM python:3.11-slim-bookworm

# ── [RESEARCH] liboqs requires cmake + ninja + libssl to compile the C library
# This is the #1 environment setup failure point — install BEFORE pip install pyoqs
RUN apt-get update && apt-get install -y \
    cmake \
    ninja-build \
    libssl-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (maximise Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY scripts/ ./scripts/

# Non-root user for security
RUN useradd -m -u 1000 fortiq && chown -R fortiq:fortiq /app
USER fortiq

EXPOSE 8000
```

---

## 11. Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | `postgresql+asyncpg://fortiq:pw@postgres:5432/fortiq` |
| `SYNC_DATABASE_URL` | Yes | — | `postgresql+psycopg2://fortiq:pw@postgres:5432/fortiq` |
| `POSTGRES_PASSWORD` | Yes | — | DB password (also used by Docker postgres service) |
| `REDIS_URL` | Yes | — | `redis://redis:6379/0` |
| `SECRET_KEY` | Yes | — | 32+ byte random string for JWT signing |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | JWT access token TTL |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Refresh token TTL |
| `ALLOWED_ORIGINS` | No | `["http://localhost:5173"]` | CORS |
| `ENVIRONMENT` | No | `development` | Controls SQLAlchemy echo, log verbosity |
| `LOG_LEVEL` | No | `INFO` | structlog level |
| `VQC_PARAMS_PATH` | No | `models/vqc_params.npy` | Trained VQC weights |
| `SVM_MODEL_PATH` | No | `models/svm_model.pkl` | Trained SVM |
| `NORMALIZER_PATH` | No | `models/normalizer.pkl` | Feature normalizer |

---

## 12. Pre-Commit Configuration

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
        args: ['--line-length', '100']
        files: ^backend/

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        files: ^backend/

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        files: ^backend/

  - repo: local
    hooks:
      - id: mypy
        name: mypy (backend)
        entry: bash -c 'cd backend && mypy app/ --strict'
        language: system
        pass_filenames: false
        types: [python]

      - id: eslint
        name: eslint (frontend)
        entry: bash -c 'cd frontend && npx eslint src/ --ext .ts,.tsx'
        language: system
        pass_filenames: false

      - id: typescript
        name: tsc (frontend)
        entry: bash -c 'cd frontend && npx tsc --noEmit'
        language: system
        pass_filenames: false
```

---

## 13. Research Summary — Key Decisions Made

| Decision | Old Approach | Research Finding | New Approach |
|---|---|---|---|
| PQC algorithm names | `Kyber768`, `Dilithium3` | Removed from liboqs 0.14.0 (June 2025) | `ML-KEM-768`, `ML-DSA-65` |
| PennyLane device | `default.qubit` | `lightning.qubit` with adjoint is 5-10x faster | `lightning.qubit` + `diff_method="adjoint"` |
| Celery + SQLAlchemy | Async session in tasks | Celery tasks are sync; `asyncpg` deadlocks | Dual session: async for FastAPI, sync for Celery |
| Network graph | Raw D3 in React | D3 fights React VDOM; `react-force-graph-2d` uses WebGL canvas | `react-force-graph-2d` |
| Server state | Zustand polling | React Query v5 handles polling, caching, invalidation natively | React Query v5 with `refetchInterval` |
| VQC params init | Random large angles | Near-zero init prevents barren plateaus | `uniform(-0.01, 0.01)` |
| liboqs system deps | Not documented | `cmake`, `ninja-build`, `libssl-dev`, `pkg-config` required before `pip install pyoqs` | Added to Dockerfile |

# Project_Architecture.md — Fortiq (Design v3: Tactical Luxury Addendum)

> This document extends Project_Architecture.md v2. Backend structure (Sections 1–9) is unchanged. This addendum replaces the frontend directory tree and adds the new component hierarchy.

---

## Frontend Directory Tree (Design v3 — Complete Replacement)

```
frontend/src/
├── main.tsx
├── App.tsx                  ← BrowserRouter + AppShell + routes
├── vite-env.d.ts
│
├── styles/
│   ├── tokens.css           ← ALL CSS custom properties (Tactical Luxury system)
│   ├── global.css           ← reset, base styles, .section-index utility, scrollbar
│   └── animations.css       ← skeleton-sweep, reticle-spin, fade-in-up,
│                               slide-in-right, ticker-flash, drawer-push
│
├── api/                     ← Unchanged from v2
│   ├── client.ts
│   ├── endpoints.ts
│   ├── classify.ts
│   ├── migrate.ts
│   └── auth.ts
│
├── stores/                  ← Unchanged from v2
│   ├── useEndpointStore.ts
│   ├── useJobStore.ts
│   ├── useScanStore.ts
│   └── useAuthStore.ts
│
├── hooks/
│   ├── useGraphData.ts      ← endpoints[] → { nodes, links } (subnet edge logic)
│   ├── useComplianceColor.ts ← score → CSS var string
│   ├── useLiveClock.ts      ← setInterval 1s, formats "THU 14:22:07 UTC"
│   └── useTickerFlash.ts    ← watches value changes, returns flashing className
│
├── types/                   ← Unchanged from v2
│
├── utils/
│   ├── formatters.ts
│   ├── riskColors.ts        ← TIER_HEX, TIER_CSS_VAR maps
│   ├── subnet.ts            ← getSubnetPrefix(ip) for graph edges
│   └── cn.ts
│
├── components/
│   ├── layout/
│   │   ├── AppShell.tsx     ← Spine + TopBar + main content area
│   │   ├── Spine.tsx        ← 56px vertical nav with acid active-bar
│   │   ├── TopBar.tsx       ← FORTIQ wordmark + CoordinateReadout + LiveClock + user
│   │   ├── CoordinateReadout.tsx  ← live ticker: ENDPOINTS: N ·· CRITICAL: N ··
│   │   ├── LiveClock.tsx    ← "THU 14:22:07 UTC" updating every second
│   │   └── PageTransition.tsx     ← fade-in-up wrapper for view mounts
│   │
│   ├── ui/                  ← Primitive components — TACTICAL LUXURY styled
│   │   │
│   │   ├── Button/
│   │   │   ├── index.tsx
│   │   │   └── Button.tsx   ← variant: primary | ghost | danger
│   │   │                       Always: Syne uppercase + → suffix + 2px radius
│   │   │
│   │   ├── SectionIndex/
│   │   │   └── index.tsx    ← [NN] ─────────── LABEL pattern
│   │   │                       MOST USED component — top of every panel
│   │   │
│   │   ├── ReticleMark/
│   │   │   └── index.tsx    ← Signature crosshair SVG; accepts style prop
│   │   │                       Used as watermark in ComplianceHero + Login
│   │   │
│   │   ├── Input/
│   │   │   └── index.tsx    ← Underline-only. No box border. JetBrains Mono.
│   │   │
│   │   ├── ProgressBar/
│   │   │   └── index.tsx    ← 2px hairline. variant: accent | tier
│   │   │
│   │   ├── Modal/
│   │   │   └── index.tsx    ← 4px radius, blur backdrop, CLOSE → text button
│   │   │
│   │   ├── ConfirmModal/
│   │   │   └── index.tsx    ← Typed confirmation "CONFIRM" + activates button
│   │   │
│   │   ├── Toast/
│   │   │   └── index.tsx    ← Slide-from-right, left-border semantic colour
│   │   │
│   │   ├── Skeleton/
│   │   │   └── index.tsx    ← Sweeping shimmer on --recess background
│   │   │
│   │   ├── Tooltip/
│   │   │   └── index.tsx    ← JetBrains Mono content, --lift bg, 2px radius
│   │   │
│   │   ├── EmptyState/
│   │   │   └── index.tsx    ← Bebas Neue 32px label + Cormorant italic body
│   │   │
│   │   └── CodeBlock/
│   │       └── index.tsx    ← highlight.js, --void bg, JetBrains Mono 12px
│   │
│   └── data/
│       ├── DataTable/
│       │   ├── index.tsx
│       │   ├── DataTable.tsx    ← Tactical Data Row pattern (dot + text only)
│       │   └── types.ts
│       │
│       ├── RiskBadge/
│       │   └── index.tsx    ← dot (6px) + Syne uppercase text. NO pill background.
│       │
│       ├── StatusBadge/
│       │   └── index.tsx    ← Syne uppercase + → for active states
│       │
│       ├── MiniTierBreakdown/
│       │   └── index.tsx    ← 4 rows: dot + label + 2px bar + count. In ComplianceHero.
│       │
│       └── AuditLogTable/
│           └── index.tsx    ← Mono timestamps + Syne names + coloured status
│
└── views/
    ├── Auth/
    │   ├── index.tsx
    │   └── LoginView.tsx    ← Split: left hero (Reticle + FORTIQ + tagline)
    │                           Right form (SectionIndex + underline inputs)
    │
    ├── Dashboard/
    │   ├── index.tsx
    │   ├── DashboardView.tsx     ← [01] hero row + [02] full-width table
    │   ├── ComplianceHero.tsx    ← Bebas Neue 96px + Reticle watermark + MiniTierBreakdown
    │   ├── TierBreakdown.tsx     ← Recharts PieChart (donut) + custom vertical legend
    │   ├── LiveFeed.tsx          ← Last 8 audit entries, mono timestamps
    │   └── MigrationProgressTable.tsx  ← DataTable, all columns per spec
    │
    ├── Scan/
    │   ├── index.tsx
    │   ├── ScanView.tsx          ← Full-width graph + 2-col classify section
    │   │                            Main content compresses when drawer open
    │   ├── NetworkGraph.tsx      ← react-force-graph-2d, custom nodeCanvasObject
    │   ├── NetworkCoordOverlay.tsx  ← NODES·EDGES·SCALE in top-right of graph
    │   ├── ClassifyPanel.tsx     ← Run button + thin progress + VQC specs in mono
    │   ├── ModelComparisonTable.tsx  ← VQC vs SVM, Cormorant headings, coloured winners
    │   ├── EndpointDetailPanel.tsx   ← 480px drawer, compresses layout
    │   └── FeatureRadarChart.tsx     ← Recharts RadarChart, --acid stroke, minimal
    │
    └── Migrate/
        ├── index.tsx
        ├── MigrateView.tsx           ← [01] 3-col + [02] algo spread + [03] audit
        ├── TierNav.tsx               ← Vertical filter: ALL|CRITICAL|HIGH|MEDIUM|LOW
        │                                Active = acid left bar + acid text, no background
        ├── MigrationQueuePanel.tsx   ← Custom checkbox DataTable + RUN button
        ├── MigrationJobStatus.tsx    ← Bebas Neue processed/total + thin bar
        ├── StatusTimeline.tsx        ← Scrollable event list, pulsing active dot
        ├── AlgorithmInfoPanel.tsx    ← THE editorial spread — 2 full-width AlgorithmCards
        ├── AlgorithmCard.tsx         ← [FIPS NNN] tag + Cormorant 36px italic name
        │                                + 2×2 Bebas Neue metric grid + verify status
        ├── MigrationConfigViewer.tsx ← Tabbed CodeBlock viewer
        └── AuditTrail.tsx            ← Underline filter input + AuditLogTable
```

---

## Component Visual Reference

A quick visual reference for the most important layout decisions:

### Spine (56px) — Not a sidebar
```
┌────┐
│ ◎  │  ← Reticle logomark (acid)
│────│
│ ▦  │  ← Dashboard icon (cream-25 inactive / acid active)
│    │  ← 2px acid left bar when active
│ ⊹  │  ← Scan icon
│ ⇄  │  ← Migrate icon
│    │
└────┘
```

### TopBar (48px)
```
FORTIQ │ ENDPOINTS: 100 ·· CRITICAL: 15 ·· MIGRATED: 0 ·· COMPLIANCE: 0.0% │ THU 14:22:07 UTC  [A]
```

### SectionIndex (every panel)
```
[01] ──────────────────────────────────────────────── ASSET REGISTRY
  ↑           ↑ 1px --rule line                          ↑
  Bebas 13px acid                                   Syne 10px uppercase --cream-60
```

### ComplianceHero card
```
┌─────────────────────────────┐
│        ◎ (watermark,        │
│         5% opacity,         │
│         slowly rotating)    │
│                             │
│  87.0%                      │← Bebas Neue 96px, coloured by tier
│  ─────────────────────      │← 1px rule
│  Cryptographic              │← Cormorant Garamond 14px italic
│  Compliance Score           │
│                             │
│  ● CRITICAL ──── 15         │← MiniTierBreakdown
│  ● HIGH     ──── 30         │
│  ● MEDIUM   ──── 35         │
│  ● LOW      ──── 20         │
└─────────────────────────────┘
```

### AlgorithmCard (editorial spread)
```
┌─────────────────────────────────────────────────────┐
│ [FIPS 203]                       ← Bebas Neue 13px --acid
│                                                     │
│ ML-KEM-768                       ← Cormorant 36px italic
│ MODULE LATTICE KEY ENCAPSULATION ← Syne 11px uppercase --cream-60
│ ─────────────────────────────────                   │
│ Post-quantum key exchange.       ← Cormorant 15px --cream-60
│ Replaces RSA and ECDH.           │
│ ─────────────────────────────────                   │
│  PUBLIC KEY    CIPHERTEXT         │
│  1,184         1,088              ← Bebas Neue 32px --cream
│  BYTES         BYTES              ← Syne 10px uppercase --cream-25
│                                   │
│  SHARED SECRET  NIST LEVEL        │
│  32             3                 │
│  BYTES                            │
│ ─────────────────────────────────                   │
│  KEM ROUND-TRIP: VERIFIED →      ← JetBrains Mono 12px --r-low
└─────────────────────────────────────────────────────┘
```

### Tactical Data Row (table)
```
● api-gateway-prod  api  RSA-2048   CRITICAL   0.92   PENDING →
↑                   ↑    ↑          ↑          ↑      ↑
6px dot             Syne JetBrains  Syne upper Syne   Syne 11px
--r-critical        13px mono 12px  11px       14px   uppercase
                         --cream-25 --r-crit   500
```

### EndpointDetailPanel (480px drawer, pushes layout)
```
[main content: 100% → calc(100% - 480px)] [drawer: 480px]
                                           ← slide-in-right animation
─────────────────────────────────────────│ api-gateway-prod
                                         │ 192.168.1.10:443
                                         │ ─────────────────
                                         │ ALGORITHM  TYPE
                                         │ RSA-2048   api
                                         │ SENSITIVITY EXPOSURE
                                         │ ★★★★☆      INTERNET
                                         │ ─────────────────
                                         │ [RadarChart]
                                         │ ─────────────────
                                         │ ADD TO MIGRATION QUEUE →
                                         │ CLOSE →
```

---

## Tailwind Config (Updated for v3 Design)

```js
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        void:  'var(--void)',
        field: 'var(--field)',
        lift:  'var(--lift)',
        recess:'var(--recess)',
        cream: 'var(--cream)',
        acid:  'var(--acid)',
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
        DEFAULT: '4px',
        sm: '2px',
        none: '0px',
      },
      letterSpacing: {
        tactical: '0.12em',
        wide:     '0.08em',
        loose:    '0.14em',
      },
      fontSize: {
        // Custom sizes not in default Tailwind scale
        '10': '10px',
        '11': '11px',
        '96': '96px',
      },
    },
  },
  plugins: [],
}
```

---

## Key Design Decision Record

| Decision | Choice | Reason |
|---|---|---|
| Sidebar width | 56px spine, not 240px | darknode.army influence: content dominates, not chrome |
| Compliance display | Bebas Neue 96px number | detroit.paris: confident single number over decorative gauge |
| Text colour | Warm cream #F2EFE6 | Not harsh white — luxury editorial warmth |
| Accent colour | Acid green #B8FF00 | Tactical/military electric; not corporate cyan |
| Section markers | `[01]` Bebas Neue 13px | darknode.army military designation aesthetic |
| Algorithm card layout | Full-width editorial | GQ Extraordinary Lab magazine feature spread |
| Table rows | Text-only, no pill badges | Pure information density, not traffic-light UI |
| Input style | Underline-only | High-fashion restraint, not form-fill utility |
| Progress bar | 2px hairline | Precision instrument, not progress indicator |
| Network graph | Full viewport width | The data IS the hero — no column constraints |
| Drawer behaviour | Pushes content | Intentional editorial layout shift, not overlaying |
| Font pairing | Bebas+Cormorant+Syne+JetBrains Mono | 4-font system: display / serif / ui / data |
| Error format | `[ERR-001] message` | Military ops error code aesthetic |
| Empty state | Bebas 32px + Cormorant italic | Designed empty states, not afterthoughts |