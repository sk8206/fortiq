import { create } from 'zustand';
import type { ScanJob, ModelEvaluation } from '@/types';
import { classifyApi } from '@/api/classify';

interface ClassifyState {
  currentJob: ScanJob | null;
  isRunning: boolean;
  evaluations: ModelEvaluation[];
  error: string | null;

  startClassification: () => Promise<void>;
  stopPolling: () => void;
  fetchEvaluations: () => Promise<void>;
  reset: () => void;
}

let pollInterval: ReturnType<typeof setInterval> | null = null;
let pollAttempts = 0;
const MAX_POLL_ATTEMPTS = 120; // 120 * 2s = 4 minutes max

export const useClassifyStore = create<ClassifyState>((set, get) => ({
  currentJob: null,
  isRunning: false,
  evaluations: [],
  error: null,

  startClassification: async () => {
    // Prevent duplicate starts
    if (get().isRunning) return;

    // Clear any existing interval
    get().stopPolling();
    pollAttempts = 0;

    try {
      set({ error: null, isRunning: true });
      const { job_id } = await classifyApi.startClassification();

      pollInterval = setInterval(async () => {
        pollAttempts++;

        // Check max attempts
        if (pollAttempts >= MAX_POLL_ATTEMPTS) {
          get().stopPolling();
          set({ error: 'Classification timed out', isRunning: false });
          return;
        }

        try {
          const job = await classifyApi.getJob(job_id);
          set({ currentJob: job });

          if (job.status === 'completed') {
            get().stopPolling();
            await get().fetchEvaluations();
            set({ isRunning: false });
          } else if (job.status === 'failed') {
            get().stopPolling();
            set({ isRunning: false, error: job.error ?? 'Classification failed' });
          }
        } catch (error: any) {
          // Only stop on fatal errors, not transient network issues
          if (pollAttempts >= 3) {
            get().stopPolling();
            const errorMsg = error?.response?.data?.detail || error?.message || 'Classification polling failed';
            set({ error: errorMsg, isRunning: false });
          }
        }
      }, 2000);

    } catch (error: any) {
      const errorMsg = error?.response?.data?.detail || error?.message || 'Failed to start classification';
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

  fetchEvaluations: async () => {
    try {
      const evaluations = await classifyApi.getModelEvaluations();
      set({ evaluations, error: null });
    } catch (error: any) {
      // Don't show error if evaluations just aren't available yet (404 or empty response)
      if (error?.response?.status === 404 || error?.response?.data?.data?.message) {
        set({ evaluations: [] });
      } else {
        set({ error: error?.response?.data?.detail || error?.message || 'Failed to load evaluations' });
      }
    }
  },

  reset: () => {
    get().stopPolling();
    set({ currentJob: null, isRunning: false, error: null });
  },
}));
