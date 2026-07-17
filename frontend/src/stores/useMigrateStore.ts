import { create } from 'zustand';
import type { ScanJob, RiskTier } from '@/types';
import { migrateApi } from '@/api/migrate';

interface MigrateState {
  selectedIds: Set<string>;
  currentJob: ScanJob | null;
  isRunning: boolean;
  tierFilter: RiskTier | 'all';
  error: string | null;

  setSelectedIds: (ids: Set<string>) => void;
  setTierFilter: (tier: RiskTier | 'all') => void;
  startMigration: (endpointIds: string[]) => Promise<void>;
  stopPolling: () => void;
  reset: () => void;
}

let pollInterval: ReturnType<typeof setInterval> | null = null;
let pollAttempts = 0;
const MAX_POLL_ATTEMPTS = 60; // 60 * 3s = 3 minutes max

export const useMigrateStore = create<MigrateState>((set, get) => ({
  selectedIds: new Set(),
  currentJob: null,
  isRunning: false,
  tierFilter: 'all',
  error: null,

  setSelectedIds: (ids) => set({ selectedIds: ids }),

  setTierFilter: (tier) => set({ tierFilter: tier }),

  startMigration: async (endpointIds) => {
    // Prevent duplicate starts
    if (get().isRunning) return;

    // Clear any existing interval
    get().stopPolling();
    pollAttempts = 0;

    try {
      set({ error: null, isRunning: true });
      const { job_id } = await migrateApi.startMigration(endpointIds);

      pollInterval = setInterval(async () => {
        pollAttempts++;

        // Check max attempts
        if (pollAttempts >= MAX_POLL_ATTEMPTS) {
          get().stopPolling();
          set({ error: 'Migration timed out', isRunning: false });
          return;
        }

        try {
          const job = await migrateApi.getJob(job_id);
          set({ currentJob: job });

          if (job.status === 'completed') {
            get().stopPolling();
            set({ isRunning: false, selectedIds: new Set() });
          } else if (job.status === 'failed') {
            get().stopPolling();
            set({ isRunning: false, error: job.error ?? 'Migration failed' });
          }
        } catch (error: any) {
          // Only stop on fatal errors, not transient network issues
          if (pollAttempts >= 3) {
            get().stopPolling();
            const errorMsg = error?.response?.data?.detail || error?.message || 'Migration polling failed';
            set({ error: errorMsg, isRunning: false });
          }
        }
      }, 3000);

    } catch (error: any) {
      const errorMsg = error?.response?.data?.detail || error?.message || 'Failed to start migration';
      set({ error: errorMsg, isRunning: false });
    }
  },

  stopPolling: () => {
    if (pollInterval) {
      clearInterval(pollInterval);
      pollInterval = null;
    }
    pollAttempts = 0;
  },

  reset: () => {
    get().stopPolling();
    set({
      selectedIds: new Set(),
      currentJob: null,
      isRunning: false,
      error: null
    });
  },
}));
