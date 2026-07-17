import React from 'react';
import { Spine } from './Spine';
import { TopBar } from './TopBar';
import type { DashboardStats } from '@/types';

interface AppShellProps {
  children: React.ReactNode;
  stats: DashboardStats | null;
}

export function AppShell({ children, stats }: AppShellProps) {
  return (
    <div
      style={{
        display: 'flex',
        height: '100vh',
        background: 'var(--void)',
        overflow: 'hidden',
      }}
    >
      <Spine />
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        <TopBar stats={stats} />
        <main
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '32px 40px',
            maxWidth: '1440px',
            width: '100%',
            margin: '0 auto',
          }}
        >
          {children}
        </main>
      </div>
    </div>
  );
}
