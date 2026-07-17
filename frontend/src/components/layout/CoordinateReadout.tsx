
import type { DashboardStats } from '@/types';
import { formatNumber } from '@/utils/formatters';

interface CoordinateReadoutProps {
  stats: DashboardStats | null;
}

export function CoordinateReadout({ stats }: CoordinateReadoutProps) {
  return (
    <div
      style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '11px',
        letterSpacing: '0.08em',
        color: 'var(--cream-60)',
        display: 'flex',
        gap: '20px',
        alignItems: 'center',
      }}
    >
      <span>ENDPOINTS: {stats ? formatNumber(stats.total) : '—'}</span>
      <span style={{ color: 'var(--rule-strong)' }}>··</span>
      <span style={{ color: stats?.by_tier.critical ? 'var(--r-critical)' : 'inherit' }}>
        CRITICAL: {stats ? formatNumber(stats.by_tier.critical) : '—'}
      </span>
      <span style={{ color: 'var(--rule-strong)' }}>··</span>
      <span>MIGRATED: {stats ? formatNumber(stats.by_status.complete) : '—'}</span>
      <span style={{ color: 'var(--rule-strong)' }}>··</span>
      <span>
        COMPLIANCE: {stats ? `${stats.compliance_score.toFixed(1)}%` : '—'}
      </span>
    </div>
  );
}
