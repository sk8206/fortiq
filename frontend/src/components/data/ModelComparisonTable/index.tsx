import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { ModelEvaluation } from '@/types';

interface ModelComparisonTableProps {
  evaluations: ModelEvaluation[];
}

export function ModelComparisonTable({ evaluations }: ModelComparisonTableProps) {
  if (evaluations.length === 0) {
    return null;
  }

  const chartData = [
    {
      metric: 'Accuracy',
      VQC: evaluations.find(e => e.model_name === 'VQC')?.accuracy ?? 0,
      SVM: evaluations.find(e => e.model_name === 'SVM')?.accuracy ?? 0,
    },
    {
      metric: 'Precision',
      VQC: evaluations.find(e => e.model_name === 'VQC')?.precision ?? 0,
      SVM: evaluations.find(e => e.model_name === 'SVM')?.precision ?? 0,
    },
    {
      metric: 'Recall',
      VQC: evaluations.find(e => e.model_name === 'VQC')?.recall ?? 0,
      SVM: evaluations.find(e => e.model_name === 'SVM')?.recall ?? 0,
    },
    {
      metric: 'F1 Score',
      VQC: evaluations.find(e => e.model_name === 'VQC')?.f1_score ?? 0,
      SVM: evaluations.find(e => e.model_name === 'SVM')?.f1_score ?? 0,
    },
  ];

  return (
    <div style={{
      border: '1px solid var(--rule)',
      background: 'var(--field)',
      padding: '32px',
      marginTop: '32px',
      borderRadius: '4px',
    }}>
      <h3 style={{
        fontFamily: 'var(--font-ui)',
        fontSize: '16px',
        fontWeight: 700,
        letterSpacing: '0.08em',
        textTransform: 'uppercase',
        color: 'var(--cream)',
        marginBottom: '24px',
      }}>
        MODEL PERFORMANCE COMPARISON
      </h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} barGap={8}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--rule)" />
          <XAxis
            dataKey="metric"
            stroke="var(--cream-60)"
            tick={{ fontFamily: 'JetBrains Mono', fontSize: 11, fill: 'var(--cream-60)' }}
          />
          <YAxis
            stroke="var(--cream-60)"
            tick={{ fontFamily: 'JetBrains Mono', fontSize: 11, fill: 'var(--cream-60)' }}
            domain={[0, 1]}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--lift)',
              border: '1px solid var(--rule)',
              fontFamily: 'JetBrains Mono',
              fontSize: 11,
              color: 'var(--cream)',
              borderRadius: '2px',
            }}
            itemStyle={{ color: 'var(--cream)' }}
            labelStyle={{ color: 'var(--cream)' }}
            formatter={(value: number) => value.toFixed(3)}
          />
          <Legend
            wrapperStyle={{
              fontFamily: 'Syne',
              fontSize: 11,
            }}
          />
          <Bar dataKey="VQC" fill="var(--acid)" />
          <Bar dataKey="SVM" fill="var(--r-medium)" />
        </BarChart>
      </ResponsiveContainer>

      <div style={{
        marginTop: '24px',
        paddingTop: '24px',
        borderTop: '1px solid var(--rule)',
        fontFamily: 'var(--font-serif)',
        fontSize: '14px',
        fontStyle: 'italic',
        color: 'var(--cream-60)',
        lineHeight: '1.6',
      }}>
        Quantum advantage is architectural — forward-compatible as hardware scales.
      </div>
    </div>
  );
}
