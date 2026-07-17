
import type { RiskTier } from '@/types';
import { getRiskColorVar } from '@/utils/riskColors';

interface RiskBadgeProps {
  tier: RiskTier;
  className?: string;
}

export function RiskBadge({ tier, className = '' }: RiskBadgeProps) {
  const color = getRiskColorVar(tier);

  return (
    <span
      className={className}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
      }}
    >
      <span
        style={{
          width: '6px',
          height: '6px',
          borderRadius: '50%',
          background: color,
          flexShrink: 0,
        }}
      />
      <span
        style={{
          fontFamily: 'var(--font-ui)',
          fontSize: '11px',
          fontWeight: 700,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color,
        }}
      >
        {tier}
      </span>
    </span>
  );
}
