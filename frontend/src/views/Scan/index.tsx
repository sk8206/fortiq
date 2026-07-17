import { useEffect } from 'react';
import { SectionIndex } from '@/components/ui/SectionIndex';
import { NetworkGraph } from '@/components/data/NetworkGraph';
import { NetworkCoordOverlay } from '@/components/data/NetworkGraph/NetworkCoordOverlay';
import { ClassifyPanel } from '@/components/data/ClassifyPanel';
import { ModelComparisonTable } from '@/components/data/ModelComparisonTable';
import { useEndpointStore } from '@/stores/useEndpointStore';
import { useClassifyStore } from '@/stores/useClassifyStore';
import { useGraphData } from '@/hooks/useGraphData';

export function ScanView() {
  const { endpoints, selectedEndpoint, selectEndpoint, fetchEndpoints } = useEndpointStore();
  const { evaluations, fetchEvaluations, stopPolling } = useClassifyStore();
  const { nodes, links } = useGraphData(endpoints);

  useEffect(() => {
    fetchEndpoints();
    fetchEvaluations();

    // Cleanup polling on unmount
    return () => {
      stopPolling();
    };
  }, [fetchEndpoints, fetchEvaluations, stopPolling]);

  return (
    <div style={{ animation: 'fade-in-up 300ms var(--ease-out)' }}>
      <SectionIndex number="[01]" label="NETWORK TOPOLOGY" />

      <div
        style={{
          height: '55vh',
          border: '1px solid var(--rule)',
          background: 'var(--field)',
          marginBottom: '32px',
          position: 'relative',
          borderRadius: '4px',
          overflow: 'hidden',
        }}
      >
        <NetworkGraph
          endpoints={endpoints}
          onNodeClick={selectEndpoint}
          selectedId={selectedEndpoint?.id}
        />
        <NetworkCoordOverlay
          nodeCount={nodes.length}
          linkCount={links.length}
        />
      </div>

      <div style={{ height: '1px', background: 'var(--rule)', marginBottom: '32px' }} />

      <SectionIndex number="[02]" label="CLASSIFICATION ENGINE" />

      <ClassifyPanel />

      {evaluations.length > 0 && (
        <ModelComparisonTable evaluations={evaluations} />
      )}
    </div>
  );
}
