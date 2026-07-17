import { apiClient } from './client';
import type { Endpoint, DashboardStats } from '@/types';

export const endpointsApi = {
  getAll: async () => {
    const { data } = await apiClient.get<{ data: Endpoint[] }>('/api/v1/endpoints', {
      params: { per_page: 100 }
    });
    return data.data;
  },

  getById: async (id: string) => {
    const { data } = await apiClient.get<{ data: Endpoint }>(`/api/v1/endpoints/${id}`);
    return data.data;
  },

  getStats: async () => {
    const { data } = await apiClient.get<{ data: DashboardStats }>('/api/v1/endpoints/stats/dashboard');
    return data.data;
  },
};
