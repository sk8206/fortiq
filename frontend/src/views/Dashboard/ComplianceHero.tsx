
import CountUp from 'react-countup';
import { ReticleMark } from '@/components/ui/ReticleMark';
import { useComplianceColor } from '@/hooks/useComplianceColor';
import type { DashboardStats } from '@/types';

interface ComplianceHeroProps {
  stats: DashboardStats | null;
}

export function ComplianceHero({ stats }: ComplianceHeroProps) {
  const score = stats?.compliance_score ?? 0;
  const color = useComplianceColor(score);

  return (
    <div
      style={{
        background: 'var(--field)',
        padding: '32px',
        position: 'relative',
        overflow: 'hidden',
        borderRight: '1px solid var(--rule)',
      }}
    >
      {/* Reticle watermark */}
      <ReticleMark
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          opacity: 0.04,
          width: '200px',
          height: '200px',
          animation: 'reticle-spin 200s linear infinite',
        }}
      />

      {/* Number */}
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '96px',
          lineHeight: 1,
          color,
          position: 'relative',
          marginBottom: '16px',
        }}
      >
        <CountUp end={score} decimals={1} suffix="%" duration={1.2} />
      </div>

      {/* Divider */}
      <div style={{ height: '1px', background: 'var(--rule)', margin: '16px 0' }} />

      {/* Label */}
      <div
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '14px',
          fontStyle: 'italic',
          color: 'var(--cream-60)',
          marginBottom: '24px',
        }}
      >
        Cryptographic Compliance Score
      </div>

      {/* Mini tier breakdown */}
      {stats && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {[
            { tier: 'critical', count: stats.by_tier.critical, color: 'var(--r-critical)' },
            { tier: 'high', count: stats.by_tier.high, color: 'var(--r-high)' },
            { tier: 'medium', count: stats.by_tier.medium, color: 'var(--r-medium)' },
            { tier: 'low', count: stats.by_tier.low, color: 'var(--r-low)' },
          ].map(({ tier, count, color }) => (
            <div
              key={tier}
              style={{
                display: 'grid',
                gridTemplateColumns: '6px auto 1fr auto',
                gap: '8px',
                alignItems: 'center',
              }}
            >
              <span
                style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: color,
                }}
              />
              <span
                style={{
                  fontFamily: 'var(--font-ui)',
                  fontSize: '11px',
                  fontWeight: 700,
                  letterSpacing: '0.12em',
                  textTransform: 'uppercase',
                  color: 'var(--cream-60)',
                }}
              >
                {tier}
              </span>
              <div style={{ height: '2px', background: 'var(--rule)' }} />
              <span
                style={{
                  fontFamily: 'var(--font-display)',
                  fontSize: '18px',
                  color: 'var(--cream)',
                }}
              >
                {count}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
