import { LiveClock } from './LiveClock';
import { CoordinateReadout } from './CoordinateReadout';
import { UserMenu } from './UserMenu';
import type { DashboardStats } from '@/types';

interface TopBarProps {
  stats: DashboardStats | null;
}

export function TopBar({ stats }: TopBarProps) {
  return (
    <div
      style={{
        height: 'var(--topbar-h)',
        background: 'var(--field)',
        borderBottom: '1px solid var(--rule)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 24px',
      }}
    >
      {/* Left: Wordmark */}
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '18px',
          color: 'var(--cream)',
          letterSpacing: '0.06em',
        }}
      >
        FORTIQ
      </div>

      {/* Center: Ticker */}
      <CoordinateReadout stats={stats} />

      {/* Right: Clock + User */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <LiveClock />
        <UserMenu />
      </div>
    </div>
  );
}
