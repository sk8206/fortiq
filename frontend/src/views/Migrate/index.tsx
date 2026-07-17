import { useEffect } from 'react';
import { SectionIndex } from '@/components/ui/SectionIndex';
import { MigrationQueue } from '@/components/data/MigrationQueue';
import { AlgorithmInfoPanel } from '@/components/data/AlgorithmInfoPanel';
import { useEndpointStore } from '@/stores/useEndpointStore';
import { useMigrateStore } from '@/stores/useMigrateStore';

export function MigrateView() {
  const { fetchEndpoints } = useEndpointStore();
  const { stopPolling } = useMigrateStore();

  useEffect(() => {
    fetchEndpoints();

    // Cleanup polling on unmount
    return () => {
      stopPolling();
    };
  }, [fetchEndpoints, stopPolling]);

  return (
    <div style={{ animation: 'fade-in-up 300ms var(--ease-out)' }}>
      <SectionIndex number="[01]" label="MIGRATION QUEUE" />

      <MigrationQueue />

      <div style={{ height: '1px', background: 'var(--rule)', margin: '32px 0' }} />

      <SectionIndex number="[02]" label="PQC ALGORITHMS" />

      <AlgorithmInfoPanel />
    </div>
  );
}
