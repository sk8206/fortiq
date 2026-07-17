import { useEffect } from 'react';
import { SectionIndex } from '@/components/ui/SectionIndex';
import { DataTable } from '@/components/data/DataTable';
import { ComplianceHero } from './ComplianceHero';
import { useEndpointStore } from '@/stores/useEndpointStore';

export function DashboardView() {
  const { endpoints, stats, fetchEndpoints, fetchStats, selectEndpoint } = useEndpointStore();

  useEffect(() => {
    fetchEndpoints();
    fetchStats();

    const interval = setInterval(() => {
      fetchStats();
    }, 5000);

    return () => clearInterval(interval);
  }, [fetchEndpoints, fetchStats]);

  return (
    <div style={{ animation: 'fade-in-up 300ms var(--ease-out)' }}>
      <SectionIndex number="[01]" label="INTELLIGENCE OVERVIEW" />

      {/* Hero row */}
      <div
        style={{
          marginBottom: '32px',
          border: '1px solid var(--rule)',
        }}
      >
        <ComplianceHero stats={stats} />
      </div>

      <div style={{ height: '1px', background: 'var(--rule)', margin: '32px 0' }} />

      <SectionIndex number="[02]" label="ASSET REGISTRY" />
      <DataTable
        endpoints={endpoints}
        onRowClick={(endpoint) => selectEndpoint(endpoint)}
      />
    </div>
  );
}
