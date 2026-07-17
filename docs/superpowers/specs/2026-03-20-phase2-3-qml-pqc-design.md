# Phase 2 & 3 Implementation Design

**Date:** 2026-03-20
**Scope:** QML Risk Engine (Phase 2) + PQC Migration Layer (Phase 3)
**Approach:** Sequential with testing (Approach A)

---

## Phase 2: QML Risk Engine

### 1. Feature Engineering (`app/qml/features.py`)

**Purpose:** Transform endpoint attributes into normalized 6-feature vectors for quantum ML.

**Features (normalized to [0, 1]):**
1. `algorithm_risk`: RSA-2048→0.60, RSA-4096→0.30, ECC-256→0.50, ECC-384→0.20
2. `data_sensitivity_norm`: raw_value / 5.0
3. `exposure_risk`: internet→1.0, internal→0.40, air-gapped→0.10
4. `traffic_risk`: critical→1.0, high→0.70, medium→0.40, low→0.10
5. `cert_urgency`: clamp((730 - cert_expiry_days) / 760, 0.0, 1.0)
6. `composite_risk`: mean(features 1-5)

**Components:**
- `endpoint_to_features(endpoint: Endpoint) -> np.ndarray[6]`: Extract features from DB model
- `FeatureNormalizer`: Wrapper around sklearn StandardScaler
  - `fit_transform(X)`: Fit and normalize training data
  - `transform(X)`: Normalize inference data (no refitting)
  - `save(path)`, `load(path)`: Pickle serialization
- `prepare_for_amplitude_encoding(features: np.ndarray[6]) -> np.ndarray[16]`: Zero-pad to 2^4 for 4-qubit circuit

**Testing:**
- Unit test: known endpoint → expected 6-feature vector
- Test: normalizer fit/transform consistency
- Test: padding produces 16-element array

---

### 2. VQC Classifier (`app/qml/vqc.py`)

**Architecture:** 4-qubit variational quantum circuit with amplitude encoding

**Device:** `default.qubit` (Python 3.14 compatible; lightning.qubit unavailable)

**Circuit Structure:**
```python
@qml.qnode(dev, diff_method="parameter-shift")  # adjoint not available on default.qubit
def vqc_circuit(features: np.ndarray[16], params: np.ndarray[3, 4, 2]) -> float:
    qml.AmplitudeEmbedding(features, wires=range(4), normalize=True)
    for layer in range(3):
        for qubit in range(4):
            qml.RY(params[layer, qubit, 0], wires=qubit)
            qml.RZ(params[layer, qubit, 1], wires=qubit)
        for qubit in range(4):
            qml.CNOT(wires=[qubit, (qubit + 1) % 4])
    return qml.expval(qml.PauliZ(0))
```

**VQCClassifier:**
- One-vs-rest strategy: 3 binary classifiers (critical, high, medium). "low" is residual.
- Loss: Binary cross-entropy
- Optimizer: Gradient descent (manual implementation)
- Params: Shape `(3_layers, 4_qubits, 2_angles)` per class
- Init: Uniform(-0.01, 0.01) to avoid barren plateaus

**Methods:**
- `fit(X, y, max_iter=100, lr=0.01)`: Train all 3 classifiers
- `predict(X)`: Argmax of confidence scores
- `predict_proba(X)`: Shape (n_samples, 4) probabilities
- `save(path)`, `load(path)`: Save/load params dict

**Testing:**
- Unit test: circuit output in [-1, 1]
- Test: fitting improves loss
- Test: predict returns valid class labels
- Integration test: train on synthetic data, accuracy > 60%

---

### 3. SVM Baseline (`app/qml/classical_baseline.py`)

**Purpose:** Classical baseline for comparison

**Implementation:**
- sklearn `SVC(kernel='rbf', C=1.0, probability=True, random_state=42)`
- Identical interface to VQCClassifier (fit, predict, predict_proba, save, load)

**Testing:**
- Test: fitting completes without error
- Test: predict returns valid labels
- Test: accuracy on synthetic data > 70%

---

### 4. Training Script (`scripts/train_models.py`)

**Flow:**
1. Load all endpoints from DB (sync session)
2. Extract 6 features → normalize with FeatureNormalizer
3. Stratified 80/20 train/test split
4. Train VQCClassifier (log loss every 10 iterations)
5. Train SVMClassifier
6. Evaluate both on test set → accuracy, precision, recall, F1
7. Insert evaluation metrics into `model_evaluations` table
8. Save: `models/vqc_params.npy`, `models/svm_model.pkl`, `models/normalizer.pkl`

**Testing:**
- Execute script, verify model files created
- Check model_evaluations table has 2 rows (VQC + SVM)
- Load models and predict on sample endpoint

---

### 5. Celery Classification Task (`app/tasks/classify_task.py`)

**Task:** `classify_endpoints_task(job_id: str)`

**Flow (SYNC):**
1. Load job from DB (SyncSessionLocal)
2. Update job status → 'running'
3. Load VQC model + normalizer from disk
4. Query endpoints with `risk_tier='unknown'` or force reclassify all
5. For each endpoint:
   - Extract features → normalize → predict tier + score
   - Update endpoint.risk_tier, endpoint.risk_score
   - Commit every 10 endpoints, update job.processed
6. Update job status → 'complete'

**Testing:**
- Create job, trigger task
- Verify endpoints updated with tier/score
- Check job.processed increments correctly
- Test error handling (missing model file)

---

## Phase 3: PQC Migration Layer

### 6. PQC Operations (`app/pqc/operations.py`)

**Note:** liboqs not installed. Implementing demo/stub functions.

**Functions:**
- `demo_ml_kem_768() -> dict`: Returns metadata (algorithm, FIPS standard, key/ciphertext sizes)
  - No actual key generation, just returns expected byte counts
  - `encapsulation_ok=False`, `decapsulation_ok=False` (stub)
- `demo_ml_dsa_65() -> dict`: Returns metadata (algorithm, FIPS standard, signature size)
  - `verification_passed=False` (stub)

**Testing:**
- Test: functions return expected structure
- Test: byte sizes match NIST specifications

---

### 7. Config Generator (`app/pqc/config_generator.py`)

**Purpose:** Generate migration config text per endpoint type

**Function:** `generate_migration_configs(endpoint: Endpoint) -> list[str]`

**Config templates:**
- `api`: Nginx TLS config snippet
- `database`: PostgreSQL ssl_ciphers config
- `iot`: MQTT TLS settings
- `firmware`: Certificate chain format
- `web`: Apache/Node.js TLS config

**Testing:**
- Test: each endpoint_type produces non-empty config
- Test: configs contain algorithm names (ML-KEM-768, ML-DSA-65)

---

### 8. Migration Celery Task (`app/tasks/migrate_task.py`)

**Task:** `run_migration_task(job_id: str, endpoint_ids: list[str])`

**Flow (SYNC):**
1. Load job, update status → 'running'
2. Query endpoints, sort by (tier_priority DESC, risk_score DESC)
3. For each endpoint:
   - Update migration_status → 'in_progress'
   - Write audit_log: 'migration_started'
   - Call demo_ml_kem_768(), demo_ml_dsa_65()
   - Generate configs → insert into migration_configs table
   - Update migration_status → 'hybrid'
   - Deterministic pass/fail (80% pass rate, seeded by endpoint.id):
     - Pass: status → 'complete', migrated_algorithm → 'ML-KEM-768 + ML-DSA-65'
     - Fail: status → 'rollback', write audit reason
   - Commit, update job.processed
4. Update job status → 'complete'

**Testing:**
- Trigger migration, verify ~80% complete, ~20% rollback
- Check audit_log has ≥4 entries per endpoint
- Test: same endpoint_ids produce same outcome (determinism)
- Test: critical endpoints processed before high

---

### 9. API Routes Updates

**`/api/v1/classify`:**
- `POST /`: Trigger classification task via Celery
- `GET /jobs/{job_id}`: Poll job status
- `GET /model-comparison`: Return VQC vs SVM metrics from model_evaluations table

**`/api/v1/migrate`:**
- `POST /`: Trigger migration task (body: `{endpoint_ids: [...]}` or `{tier: "critical"}`)
- `GET /jobs/{job_id}`: Poll job status
- `GET /pqc-demo`: Call demo functions, return combined result
- `GET /audit-log`: Paginated audit log with filters

**Testing:**
- Integration test: POST /classify → poll job → verify endpoints updated
- Integration test: POST /migrate → poll job → verify audit logs created
- Test: GET /pqc-demo responds < 5 seconds

---

## Testing Strategy

**Unit Tests:**
- Feature extraction correctness
- VQC circuit output range
- SVM baseline training
- Config generator templates

**Integration Tests:**
- Training script end-to-end
- Classify task updates DB correctly
- Migrate task creates audit logs
- API routes return expected formats

**Verification:**
- Run training script, check model files exist
- Trigger classify job, verify tier updates
- Trigger migrate job, check 80/20 split
- Query model_evaluations table for metrics

---

## Implementation Order (Approach A)

1. ✅ Feature engineering + unit tests
2. ✅ VQC implementation + unit tests
3. ✅ SVM baseline + tests
4. ✅ Training script + execution verification
5. ✅ Classify Celery task + integration test
6. ✅ PQC operations (stubs) + tests
7. ✅ Config generator + tests
8. ✅ Migrate Celery task + integration test
9. ✅ API route updates + E2E tests

---

## Success Criteria

**Phase 2:**
- [ ] Training script produces model files
- [ ] VQC accuracy > 60% on test set
- [ ] SVM accuracy > 70% on test set
- [ ] Classify task updates all endpoints
- [ ] model_evaluations table populated

**Phase 3:**
- [ ] PQC demo returns expected byte sizes
- [ ] Migration task: ~80% complete, ~20% rollback (±5%)
- [ ] Audit log has ≥4 entries per migrated endpoint
- [ ] Config generator produces text for all endpoint types
- [ ] Same endpoint IDs = same migration outcome

**Integration:**
- [ ] POST /classify → successful job execution
- [ ] POST /migrate → successful job execution
- [ ] GET /model-comparison returns VQC vs SVM metrics
- [ ] GET /pqc-demo responds < 5s
