
import type { RiskTier } from '@/types';
import { getRiskColorVar } from '@/utils/riskColors';

interface ProgressBarProps {
  value: number;
  max?: number;
  variant?: 'accent' | 'tier';
  tier?: RiskTier;
  className?: string;
}

export function ProgressBar({ value, max = 100, variant = 'accent', tier, className = '' }: ProgressBarProps) {
  const percentage = Math.min(100, (value / max) * 100);
  const color = variant === 'tier' && tier ? getRiskColorVar(tier) : 'var(--acid)';

  return (
    <div
      className={className}
      style={{
        height: '2px',
        background: 'var(--rule)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          height: '100%',
          width: `${percentage}%`,
          background: color,
          transition: 'width var(--t-slow) var(--ease-out)',
        }}
      />
    </div>
  );
}
