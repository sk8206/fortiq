# PRD.md — Fortiq Product Requirements Document (Research-Informed v2)

**Version**: 2.0.0 | **Status**: Approved for Implementation | **Scope**: QC² Hackathon, 36-hour prototype

> This document defines exactly what Fortiq is and what it must do. Features not listed under Functional Requirements are **out of scope**. When scope questions arise, the answer is always: "Is it in the PRD?" If not, it does not get built.

---

## 1. Product Overview

### 1.1 Problem Statement

Enterprise digital infrastructure depends on RSA and ECC encryption. A cryptographically relevant quantum computer running Shor's Algorithm will render both obsolete. Major institutions (NIST, IBM, Google, NSA) estimate this arrives 2030–2035. Nation-state adversaries are already executing "Harvest Now, Decrypt Later" — collecting encrypted traffic today to decrypt once quantum hardware arrives.

NIST finalised three post-quantum standards in August 2024:
- **FIPS 203**: ML-KEM (Module-Lattice Key Encapsulation Mechanism) — formerly CRYSTALS-Kyber
- **FIPS 204**: ML-DSA (Module-Lattice Digital Signature Algorithm) — formerly CRYSTALS-Dilithium
- **FIPS 205**: SLH-DSA (Stateless Hash-Based Digital Signature Algorithm) — formerly SPHINCS+

The bottleneck is not knowing *which* standard to adopt. The bottleneck is executing the migration across thousands of enterprise endpoints without the tooling to do so.

### 1.2 Product Vision

Fortiq is an automated three-stage pipeline: it discovers every cryptographic endpoint in an enterprise network, uses a Variational Quantum Classifier (VQC) to risk-rank them in priority order, and automatically generates the migration artefacts needed to transition each endpoint to NIST-approved post-quantum encryption — with zero-downtime hybrid mode and deterministic rollback.

### 1.3 Prototype Scope Statement

This PRD describes a **hackathon prototype** demonstrating the complete pipeline end-to-end with 100 synthetic endpoints. Production concerns (real network scanning, real cert issuance, multi-tenant SaaS, SOC 2) are explicitly excluded.

---

## 2. Terminology Glossary

Use these terms exactly and consistently throughout all code, UI copy, and documentation. Do not use synonyms.

| Term | Precise Definition |
|---|---|
| **Endpoint** | A single cryptographic service or asset identified during discovery: an API gateway, database connection, IoT device, firmware system, or web server. The atomic unit of the Fortiq system. |
| **Asset Registry** | The complete database of all Endpoints, with their cryptographic metadata and current migration status. |
| **Risk Tier** | One of four classification levels assigned by the VQC: Critical, High, Medium, Low. |
| **Risk Score** | A continuous float [0.0, 1.0] representing risk level. 1.0 = highest risk. |
| **VQC** | Variational Quantum Classifier. The quantum machine learning model that assigns Risk Tiers to Endpoints. |
| **SVM** | Support Vector Machine. The classical ML baseline used for comparison against the VQC. |
| **ML-KEM-768** | Module-Lattice Key Encapsulation Mechanism, Security Level 3. FIPS 203 finalised standard. Replaces CRYSTALS-Kyber. **This is the correct name** — `Kyber768` is deprecated in liboqs 0.14.0+. |
| **ML-DSA-65** | Module-Lattice Digital Signature Algorithm, Security Level 3. FIPS 204 finalised standard. Replaces CRYSTALS-Dilithium. **This is the correct name** — `Dilithium3` is deprecated in liboqs 0.14.0+. |
| **Migration Config** | A generated configuration file (nginx, OpenSSL, PostgreSQL SSL, YAML plan) that implements PQC for a specific Endpoint. Illustrative text only — not executed by the prototype. |
| **Hybrid Mode** | A transition state where both the original encryption and the new PQC encryption run simultaneously on an Endpoint. |
| **Rollback** | The deterministic reversion of a failed migration attempt. Outcome is seeded by Endpoint ID for reproducibility. |
| **Compliance Score** | The percentage of Endpoints that have reached `complete` migration status: `(complete count / total count) × 100`. |
| **Audit Log** | An immutable, append-only record of all migration state transitions for each Endpoint. |
| **Scan Job** | An asynchronous background Celery task performing either endpoint classification or migration. |
| **Harvest Now, Decrypt Later** | The nation-state threat strategy of collecting encrypted data today for decryption once quantum hardware arrives. |

---

## 3. User Personas

### 3.1 Primary — Enterprise Security Engineer

**Name**: Priya, Senior Security Engineer, Financial Services
**Goal**: Understand which of her 200+ endpoints are most vulnerable to quantum attacks and get a prioritised migration plan — without spending $1M on an external audit.
**Technical level**: High. Understands RSA, ECC, TLS, PKI. Does not know PennyLane or liboqs.
**Key need**: A ranked list of Endpoints with Risk Scores, plus ready-to-use Migration Configs for the most critical ones.

### 3.2 Secondary — Hackathon Judge / Technical Evaluator

**Name**: Dr. Arun, Quantum Computing Track Judge
**Goal**: Verify that the QML component is technically credible and that PQC uses correct NIST 2024 final standards.
**Technical level**: Very high. Understands quantum circuits, VQC architecture, ML-KEM/ML-DSA.
**Key need**: The model comparison panel (VQC vs SVM), circuit architecture explanation, and evidence that liboqs uses the finalised FIPS 203/204 algorithm names (`ML-KEM-768`, `ML-DSA-65`), not deprecated Round 3 names.

---

## 4. Functional Requirements

Priority levels: **P0** = must ship (demo is broken without it), **P1** = should ship (demo is weaker without it), **P2** = skip if time pressure.

---

### Module 1: Asset Discovery & Registry

**FR-1.1 — Synthetic Asset Registry** [P0]
The system contains a pre-populated Asset Registry of exactly 100 synthetic Endpoints. Each Endpoint has all fields defined in §5.1.
*Acceptance*: `GET /api/v1/endpoints` returns 100 records. All required fields are non-null. Label distribution: ~15 Critical, ~30 High, ~35 Medium, ~20 Low (±5 per tier acceptable).

**FR-1.2 — Endpoint Listing with Filters** [P0]
A table displays all Endpoints. User can sort by Risk Score, Risk Tier, Algorithm, and Migration Status. User can filter by Risk Tier and Migration Status simultaneously.
*Acceptance*: Applying `tier=critical` filter shows only Critical tier endpoints. Applying `status=complete` shows only completed endpoints. Combined filters work correctly.

**FR-1.3 — Endpoint Detail** [P0]
Clicking any Endpoint opens a detail view showing all fields from §5.1, the Risk Tier badge, Risk Score, Migration Status, and generated Migration Configs (if any).
*Acceptance*: Detail opens in < 200ms. All 14 fields visible and labelled using Glossary terminology.

**FR-1.4 — Dashboard Statistics** [P0]
The dashboard displays: total Endpoint count, count per Risk Tier (4 tiles), Compliance Score (%), and count per Migration Status.
*Acceptance*: All counts match the actual database. Compliance Score = `(complete / total) × 100`, rounded to 1 decimal.

**FR-1.5 — Network Graph Visualisation** [P1]
A force-directed graph visualises all 100 Endpoints as nodes. Node colour encodes Risk Tier using the design system's `--risk-*` tokens. Node size encodes traffic volume. Edges connect Endpoints sharing the same `/24` subnet prefix. Zoom and pan work.
*Acceptance*: 100 nodes rendered. Critical nodes are `--risk-critical` colour. Click opens Endpoint detail. Graph stabilises within 3 seconds.

---

### Module 2: Risk Classification (VQC)

**FR-2.1 — Pre-Trained VQC Model** [P0]
A trained VQC model loads at Celery worker startup. `models/vqc_params.npy` and `models/normalizer.pkl` exist after running `train_models.py`.
*Acceptance*: Worker starts without model-loading errors. VQC training accuracy documented in the UI's Model Comparison panel.

**FR-2.2 — Classification Job** [P0]
User triggers a classification job from the Scan view. The job classifies all Endpoints using the VQC and writes `risk_tier` and `risk_score` to the database.
*Acceptance*: "Run Classification" creates a job and returns a `job_id` within 500ms. Progress bar polls every 2 seconds and shows incremental increase. On completion (< 5 min), all 100 Endpoints have non-null `risk_tier`. Network graph node colours update automatically after completion.

**FR-2.3 — VQC vs SVM Model Comparison** [P0]
The UI displays side-by-side evaluation metrics for VQC and SVM: accuracy, precision, recall, F1. VQC circuit architecture is described (4 qubits, 3 layers, amplitude encoding, `lightning.qubit` device).
*Acceptance*: All 8 metrics (4 per model) are displayed. Values match the `model_evaluations` table. Architecture description uses correct PennyLane terminology.

**FR-2.4 — Risk Score Display** [P0]
Each Endpoint displays its Risk Score as `X.XX / 1.00` and as a proportional progress bar coloured with the Endpoint's Risk Tier colour.
*Acceptance*: Score format matches spec. Bar fill percentage = `risk_score × 100`.

**FR-2.5 — Feature Breakdown Radar Chart** [P1]
Endpoint detail includes a radar chart showing the 6 input features: Algorithm Risk, Data Sensitivity, Exposure Risk, Traffic Risk, Certificate Urgency, Composite Risk.
*Acceptance*: Recharts `RadarChart` renders 6 axes. Values match the computed feature vector for the selected Endpoint.

---

### Module 3: PQC Migration

**FR-3.1 — Migration Job Trigger** [P0]
User can select Endpoints (by tier filter or individual checkbox) and trigger a migration job. Triggering requires confirmation modal with typed `CONFIRM`.
*Acceptance*: "All Critical" selection adds all Critical Endpoints to the queue. Confirmation modal prevents accidental trigger. Confirming creates a job and returns `job_id`.

**FR-3.2 — Risk-Ordered Migration Processing** [P0]
Migration processes Endpoints in Risk Tier order: Critical first, then High, Medium, Low. Within a tier, ordered by Risk Score descending.
*Acceptance*: Audit log records show all Critical Endpoints have earlier `created_at` timestamps than all High Endpoints for the same job.

**FR-3.3 — PQC Algorithm Demonstration** [P0]
The system demonstrates that ML-KEM-768 and ML-DSA-65 function correctly via liboqs 0.15.0.
*Acceptance*: Algorithm Info panel shows:
- ML-KEM-768: `public_key_bytes=1184`, `ciphertext_bytes=1088`, `shared_secret_bytes=32`, `fips_standard="FIPS 203"`.
- ML-DSA-65: `signature_bytes=3293`, `verification_passed=true`, `fips_standard="FIPS 204"`.
- NIST security level badge: Level 3 for both.

**FR-3.4 — Migration Config Generation** [P0]
For each Endpoint processed by a migration job, at least one Migration Config is generated and stored.
*Acceptance*: Every Endpoint with `migration_status` of `complete` or `rollback` has ≥1 record in `migration_configs`. Config text is non-empty and references the Endpoint's `name` and `host`.

**FR-3.5 — Hybrid Mode Transition** [P0]
Every migration attempt transitions through a `hybrid` state before reaching `complete` or `rollback`.
*Acceptance*: Audit log for every migrated Endpoint shows: `pending → in_progress → hybrid → (complete | rollback)`. No Endpoint goes directly from `in_progress` to `complete`.

**FR-3.6 — Deterministic Rollback Simulation** [P0]
Approximately 20% of migration attempts reach `rollback`. The outcome for each Endpoint is deterministic (seeded by Endpoint ID) — running the same migration job twice produces the same complete/rollback outcomes.
*Acceptance*: Between 15–25 Endpoints reach `rollback` in a full 100-Endpoint migration run. Running the migration twice on the same Endpoints produces identical outcomes per Endpoint.

**FR-3.7 — Migration Config Viewer** [P1]
User can view generated Migration Configs for a completed Endpoint. Configs are displayed with syntax highlighting. Multiple config types shown in tabs.
*Acceptance*: At least 2 config tabs per completed Endpoint. `highlight.js` applies syntax highlighting. Content is readable and references the correct Endpoint.

**FR-3.8 — Audit Trail** [P0]
Every migration state transition is written to the Audit Log. The UI shows the Audit Log filterable by Endpoint.
*Acceptance*: Audit log table shows ≥4 entries per migrated Endpoint (one per state transition). Filtering by a specific Endpoint name shows only that Endpoint's entries.

---

### Module 4: Authentication

**FR-4.1 — Login Required** [P0]
All features require authentication. Default demo account: `admin` / `fortiq-demo-2024`.
*Acceptance*: Unauthenticated `GET /api/v1/endpoints` returns 401. Login page redirects to Dashboard on success.

**FR-4.2 — Session Persistence** [P1]
Session persists across browser refreshes for up to 7 days via HttpOnly refresh token cookie.
*Acceptance*: After login, refreshing the page does not require re-login. Closing and reopening the browser requires re-login (cookie not persistent across browser sessions unless explicitly configured).

---

## 5. Data Specifications

### 5.1 Endpoint Entity — Required Fields

| # | Field | Type | Constraints | Description |
|---|---|---|---|---|
| 1 | `id` | UUID | PK | Auto-generated |
| 2 | `name` | string | 3–80 chars | Human-readable name (e.g., `api-gateway-prod`) |
| 3 | `host` | string | valid IP or FQDN | Network address |
| 4 | `port` | integer | 1–65535 | Service port |
| 5 | `endpoint_type` | enum | api \| database \| iot \| firmware \| web | Category |
| 6 | `algorithm` | enum | RSA-2048 \| RSA-4096 \| ECC-256 \| ECC-384 | Current encryption |
| 7 | `key_length` | integer | 2048 \| 4096 \| 256 \| 384 | Key length in bits |
| 8 | `data_sensitivity` | integer | 1–5 | 5 = most sensitive |
| 9 | `exposure_surface` | enum | internet-facing \| internal \| air-gapped | Network exposure |
| 10 | `traffic_volume` | enum | low \| medium \| high \| critical | Traffic load |
| 11 | `cert_expiry_days` | integer | unbounded (neg = expired) | Days until cert expiry |
| 12 | `risk_tier` | enum | critical \| high \| medium \| low \| unknown | VQC output |
| 13 | `risk_score` | float \| null | [0.0, 1.0] | VQC confidence score |
| 14 | `migration_status` | enum | pending \| in_progress \| hybrid \| complete \| rollback | Migration state |

### 5.2 VQC Feature Vector

6 features, all normalised to [0, 1]:

| # | Feature | Encoding | Notes |
|---|---|---|---|
| 1 | algorithm_risk | RSA-2048→0.60, RSA-4096→0.30, ECC-256→0.50, ECC-384→0.20 | Higher = more urgent |
| 2 | data_sensitivity_norm | raw / 5.0 | Direct normalisation |
| 3 | exposure_risk | internet→1.0, internal→0.40, air-gapped→0.10 | |
| 4 | traffic_risk | critical→1.0, high→0.70, medium→0.40, low→0.10 | |
| 5 | cert_urgency | `clamp((730 - days) / 760, 0.0, 1.0)` | Higher = expiring sooner |
| 6 | composite_risk | `mean(features 1–5)` | Derived aggregate |

Features 1–6 are padded to 16 elements (2^4) for `qml.AmplitudeEmbedding` with `normalize=True`.

### 5.3 PQC Algorithm Metadata

Expected output from `GET /migrate/pqc-demo`:
```json
{
  "ml_kem_768": {
    "algorithm": "ML-KEM-768",
    "fips_standard": "FIPS 203",
    "nist_security_level": 3,
    "public_key_bytes": 1184,
    "ciphertext_bytes": 1088,
    "shared_secret_bytes": 32,
    "encapsulation_ok": true,
    "decapsulation_ok": true
  },
  "ml_dsa_65": {
    "algorithm": "ML-DSA-65",
    "fips_standard": "FIPS 204",
    "nist_security_level": 3,
    "public_key_bytes": 1952,
    "signature_bytes": 3293,
    "verification_passed": true
  }
}
```

### 5.4 API Pagination Standard

All list endpoints: `?page=1&per_page=20`. Response `meta`: `{total, page, per_page, total_pages}`.

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target |
|---|---|
| `GET /endpoints` (100 records) | < 200ms p95 |
| `GET /endpoints/stats/dashboard` | < 100ms p95 |
| `POST /classify` (job creation) | < 500ms |
| `GET /migrate/pqc-demo` | < 5 seconds |
| Classification job (100 endpoints) | < 5 minutes |
| Migration job (100 endpoints) | < 2 minutes |
| Frontend initial paint | < 3 seconds (Vite dev) |
| Network graph first nodes visible | < 1 second |

### 6.2 Reliability

- Restart of any single service must not cause data loss.
- An interrupted migration job is resumable (progress tracked in `scan_jobs.processed`).
- VQC model loads from disk on Celery worker start without requiring retraining.

### 6.3 Security

- JWT auth on all non-health write routes.
- No real private keys or shared secrets stored anywhere.
- CORS restricted to `http://localhost:5173` in development.
- Rate limiting on auth endpoints (5/min).
- `.env` with secrets never committed.

### 6.4 Accuracy (Research-Based Targets)

| Model | Metric | Target | Basis |
|---|---|---|---|
| VQC (each binary classifier) | Accuracy | ≥ 60% | Realistic for 4-qubit simulator on 80-sample train set |
| SVM (multiclass) | Accuracy | ≥ 75% | Standard RBF SVM on this feature dimensionality |
| Overall | Rollback rate | 15–25% | Seeded deterministic simulation |

### 6.5 Browser Support

Chrome 120+, Firefox 120+, Safari 17+. No IE11. No mobile. Minimum viewport 1024px wide.

---

## 7. Explicit Out of Scope

These are NOT part of this prototype. Do not implement even partially.

| Item | Reason |
|---|---|
| Real network scanning / passive agent | Requires enterprise infrastructure |
| Real certificate issuance or renewal | Requires CA integration |
| Execution of generated Migration Configs | Safety — configs are illustrative only |
| Multi-tenant / multi-organisation | Single-admin prototype |
| Real quantum hardware (IBM Cloud, AWS Braket) | Uses local `lightning.qubit` simulator |
| PQC operations in browser JavaScript | Server-side Celery only |
| User management / RBAC | Single hardcoded admin account |
| WebSocket real-time updates | React Query polling only |
| Mobile / tablet responsive design | Desktop (≥1024px) only |
| Multi-language / i18n | English only |
| Data export (CSV, PDF reports) | Not in prototype |
| SIEM/SOAR integrations | Not in prototype |
| SLH-DSA / SPHINCS+ (FIPS 205) | ML-KEM-768 + ML-DSA-65 only |
| More than 100 synthetic endpoints | Exactly 100 for performance |
| Celery Beat / scheduled tasks | On-demand trigger only |
| Flower monitoring dashboard | Not in prototype |
| Deployment to cloud (AWS/GCP/Azure) | Docker Compose local only |

---

## 8. Acceptance Criteria — End-to-End Demo Flows

The prototype is complete when all P0 requirements pass AND all four demo flows execute without errors.

### Demo Flow 1: Discovery & Overview
1. `docker compose up` starts all services.
2. `alembic upgrade head` + `python scripts/generate_dataset.py` + `python scripts/train_models.py`.
3. `python scripts/create_admin.py` creates the demo account.
4. User navigates to `http://localhost:5173`, login with `admin` / `fortiq-demo-2024`.
5. Dashboard shows: 100 total Endpoints, 4 tier counts (or unknown if not yet classified), 0% Compliance.
6. Scan view shows network graph with 100 grey nodes (`--risk-unknown`).

### Demo Flow 2: Classification
1. User clicks "Run Classification" in Scan view.
2. Progress bar starts from 0 and reaches 100% (< 5 minutes).
3. Network graph node colours update to reflect Risk Tiers.
4. Dashboard tier counts update correctly.
5. Model Comparison panel shows VQC and SVM accuracy/F1 with circuit architecture description.

### Demo Flow 3: Migration
1. User navigates to Migrate view.
2. User selects "All Critical" (15 endpoints).
3. Confirmation modal appears. User types `CONFIRM`.
4. Migration job runs. Status timeline shows each state transition.
5. ~80% of Critical endpoints reach `complete`. ~20% reach `rollback`.
6. Compliance Score on Dashboard updates after completion.
7. User clicks a `complete` endpoint → views 2+ Migration Config tabs with syntax-highlighted text.
8. User clicks Audit Trail → sees ≥4 entries per endpoint in order.

### Demo Flow 4: PQC Algorithm Demo
1. User opens Algorithm Info panel.
2. ML-KEM-768 metadata shows: key=1184B, ciphertext=1088B, FIPS 203, Level 3.
3. ML-DSA-65 metadata shows: signature=3293B, `verification_passed: true`, FIPS 204, Level 3.
4. No deprecated algorithm names (`Kyber768`, `Dilithium3`) appear anywhere in the UI.
