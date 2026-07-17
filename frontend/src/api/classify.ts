import { apiClient } from './client';
import type { ScanJob, ModelEvaluation } from '@/types';

interface BackendModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;  // Backend uses 'f1', not 'f1_score'
}

export const classifyApi = {
  startClassification: async () => {
    const { data } = await apiClient.post<{ data: { job_id: string } }>('/api/v1/classify');
    return data.data;
  },

  getJob: async (jobId: string) => {
    const { data } = await apiClient.get<{ data: ScanJob }>(`/api/v1/classify/jobs/${jobId}`);
    return data.data;
  },

  getModelEvaluations: async (): Promise<ModelEvaluation[]> => {
    const { data } = await apiClient.get<{ data: { vqc: BackendModelMetrics; svm: BackendModelMetrics } }>('/api/v1/classify/model-comparison');

    // Map backend 'f1' to frontend 'f1_score'
    return [
      {
        model_name: 'VQC',
        accuracy: data.data.vqc.accuracy,
        precision: data.data.vqc.precision,
        recall: data.data.vqc.recall,
        f1_score: data.data.vqc.f1,
      },
      {
        model_name: 'SVM',
        accuracy: data.data.svm.accuracy,
        precision: data.data.svm.precision,
        recall: data.data.svm.recall,
        f1_score: data.data.svm.f1,
      }
    ];
  },
};
