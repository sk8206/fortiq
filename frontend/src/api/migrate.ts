import { apiClient } from './client';
import type { ScanJob, PQCAlgorithm, MigrationConfig, AuditEntry } from '@/types';

export const migrateApi = {
  startMigration: async (endpointIds: string[]) => {
    const { data } = await apiClient.post<{ data: { job_id: string } }>('/api/v1/migrate', {
      endpoint_ids: endpointIds,
    });
    return data.data;
  },

  getJob: async (jobId: string) => {
    const { data } = await apiClient.get<{ data: ScanJob }>(`/api/v1/migrate/jobs/${jobId}`);
    return data.data;
  },

  getPqcDemo: async () => {
    const { data } = await apiClient.get<{ data: { ml_kem_768: PQCAlgorithm; ml_dsa_65: PQCAlgorithm } }>(
      '/api/v1/migrate/pqc-demo'
    );
    return data.data;
  },

  getConfigs: async (endpointId: string) => {
    const { data } = await apiClient.get<{ data: { configs: MigrationConfig[] } }>(
      `/api/v1/migrate/configs/${endpointId}`
    );
    return data.data.configs;
  },

  getAuditLog: async (endpointId?: string) => {
    const { data } = await apiClient.get<{ data: AuditEntry[] }>('/api/v1/migrate/audit-log', {
      params: endpointId ? { endpoint_id: endpointId } : {},
    });
    return data.data;
  },
};
