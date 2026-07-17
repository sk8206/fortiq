import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import type { DashboardStats } from '@/types';

interface TierDistributionChartProps {
  stats: DashboardStats | null;
}

const TIER_COLORS = {
  critical: 'var(--r-critical)',
  high: 'var(--r-high)',
  medium: 'var(--r-medium)',
  low: 'var(--r-low)',
  unknown: 'var(--r-unknown)',
};


const TIER_LABELS = {
  critical: 'CRITICAL',
  high: 'HIGH',
  medium: 'MEDIUM',
  low: 'LOW',
  unknown: 'UNKNOWN',
};

export function TierDistributionChart({ stats }: TierDistributionChartProps) {
  if (!stats) {
    return (
      <div
        style={{
          background: 'var(--field)',
          padding: '32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRight: '1px solid var(--rule)',
          height: '100%',
        }}
      >
        <div
          style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '16px',
            fontStyle: 'italic',
            color: 'var(--cream-60)',
          }}
        >
          Loading tier data...
        </div>
      </div>
    );
  }

  const data = [
    { name: 'critical', value: stats.by_tier.critical, color: TIER_COLORS.critical },
    { name: 'high', value: stats.by_tier.high, color: TIER_COLORS.high },
    { name: 'medium', value: stats.by_tier.medium, color: TIER_COLORS.medium },
    { name: 'low', value: stats.by_tier.low, color: TIER_COLORS.low },
    { name: 'unknown', value: stats.by_tier.unknown, color: TIER_COLORS.unknown },
  ].filter(d => d.value > 0);

  const hasData = data.length > 0 && stats.total > 0;

  return (
    <div
      style={{
        background: 'var(--field)',
        padding: '24px',
        borderRight: '1px solid var(--rule)',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}
    >
      {/* Chart */}
      <div style={{ flex: 1, position: 'relative', minHeight: '160px' }}>
        {hasData ? (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={70}
                paddingAngle={2}
                dataKey="value"
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <div
              style={{
                width: '140px',
                height: '140px',
                borderRadius: '50%',
                border: '2px solid var(--rule)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <span
                style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: '14px',
                  fontStyle: 'italic',
                  color: 'var(--cream-60)',
                }}
              >
                No data
              </span>
            </div>
          </div>
        )}

        {/* Center label */}
        {hasData && (
          <div
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              textAlign: 'center',
              pointerEvents: 'none',
            }}
          >
            <div
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '36px',
                color: 'var(--cream)',
                lineHeight: 1,
              }}
            >
              {stats.total}
            </div>
            <div
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '0.12em',
                color: 'var(--cream-25)',
                textTransform: 'uppercase',
                marginTop: '4px',
              }}
            >
              ENDPOINTS
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {(['critical', 'high', 'medium', 'low'] as const).map((tier) => (
          <div
            key={tier}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <span
              style={{
                width: '8px',
                height: '8px',
                background: TIER_COLORS[tier],
                flexShrink: 0,
              }}
            />
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '11px',
                fontWeight: 700,
                letterSpacing: '0.08em',
                color: 'var(--cream-60)',
                textTransform: 'uppercase',
                flex: 1,
              }}
            >
              {TIER_LABELS[tier]}
            </span>
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '13px',
                fontWeight: 500,
                color: 'var(--cream)',
              }}
            >
              {stats.by_tier[tier]}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
