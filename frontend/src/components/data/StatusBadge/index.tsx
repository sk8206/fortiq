
import type { MigrationStatus } from '@/types';

interface StatusBadgeProps {
  status: MigrationStatus;
  className?: string;
}

export function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  const color = status === 'complete' ? 'var(--r-low)' :
                status === 'rollback' ? 'var(--r-critical)' :
                status === 'hybrid' ? 'var(--r-medium)' :
                status === 'in_progress' ? 'var(--acid)' :
                'var(--cream-60)';

  return (
    <span
      className={className}
      style={{
        fontFamily: 'var(--font-ui)',
        fontSize: '11px',
        fontWeight: 700,
        letterSpacing: '0.12em',
        textTransform: 'uppercase',
        color,
      }}
    >
      {status.replace('_', ' ')}
      {(status === 'in_progress' || status === 'pending') && ' →'}
    </span>
  );
}
