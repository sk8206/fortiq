export type RiskTier = 'critical' | 'high' | 'medium' | 'low' | 'unknown';
export type MigrationStatus = 'pending' | 'in_progress' | 'hybrid' | 'complete' | 'rollback';
export type EndpointType = 'api' | 'database' | 'iot' | 'firmware' | 'web';
export type AlgorithmType = 'RSA-2048' | 'RSA-4096' | 'ECC-256' | 'ECC-384';
export type ExposureSurface = 'internet-facing' | 'internal' | 'air-gapped';
export type TrafficVolume = 'low' | 'medium' | 'high' | 'critical';

export interface Endpoint {
  id: string;
  name: string;
  host: string;
  port: number;
  endpoint_type: EndpointType;
  algorithm: AlgorithmType;
  key_length: number;
  data_sensitivity: number;
  exposure_surface: ExposureSurface;
  traffic_volume: TrafficVolume;
  cert_expiry_days: number;
  risk_tier: RiskTier;
  risk_score: number | null;
  migration_status: MigrationStatus;
  created_at?: string;
  updated_at?: string;
}

export interface DashboardStats {
  total: number;
  by_tier: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    unknown: number;
  };
  by_status: {
    pending: number;
    in_progress: number;
    hybrid: number;
    complete: number;
    rollback: number;
  };
  compliance_score: number;
}

export interface ScanJob {
  id: string;
  job_type: 'classify' | 'migrate';
  status: 'pending' | 'running' | 'completed' | 'failed';
  total: number;
  processed: number;
  progress_pct: number;
  created_at: string;
  completed_at?: string;
  error?: string;
}

export interface ModelEvaluation {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
}

export interface PQCAlgorithm {
  algorithm: string;
  fips_standard: string;
  nist_security_level: number;
  public_key_bytes?: number;
  ciphertext_bytes?: number;
  shared_secret_bytes?: number;
  signature_bytes?: number;
  encapsulation_ok?: boolean;
  decapsulation_ok?: boolean;
  verification_passed?: boolean;
}

export interface MigrationConfig {
  id: string;
  endpoint_id: string;
  config_type: string;
  content: string;
  created_at: string;
}

export interface AuditEntry {
  id: string;
  endpoint_id: string;
  endpoint_name: string;
  from_status: MigrationStatus;
  to_status: MigrationStatus;
  created_at: string;
}

export interface User {
  id: string;
  username: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}
