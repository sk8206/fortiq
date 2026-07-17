import { create } from 'zustand';
import type { Endpoint, DashboardStats } from '@/types';
import { endpointsApi } from '@/api/endpoints';

interface EndpointState {
  endpoints: Endpoint[];
  stats: DashboardStats | null;
  selectedEndpoint: Endpoint | null;
  isLoading: boolean;
  error: string | null;
  fetchEndpoints: () => Promise<void>;
  fetchStats: () => Promise<void>;
  selectEndpoint: (endpoint: Endpoint | null) => void;
}

export const useEndpointStore = create<EndpointState>((set) => ({
  endpoints: [],
  stats: null,
  selectedEndpoint: null,
  isLoading: false,
  error: null,

  fetchEndpoints: async () => {
    try {
      set({ isLoading: true, error: null });
      const endpoints = await endpointsApi.getAll();
      set({ endpoints, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchStats: async () => {
    try {
      const stats = await endpointsApi.getStats();
      set({ stats });
    } catch (error) {
      set({ error: (error as Error).message });
    }
  },

  selectEndpoint: (endpoint) => set({ selectedEndpoint: endpoint }),
}));
