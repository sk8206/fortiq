import { useRef, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import type { Endpoint, RiskTier } from '@/types';
import { useGraphData } from '@/hooks/useGraphData';
import { TIER_HEX } from '@/utils/riskColors';

interface NetworkGraphProps {
  endpoints: Endpoint[];
  onNodeClick?: (endpoint: Endpoint) => void;
  selectedId?: string | null;
}

export function NetworkGraph({ endpoints, onNodeClick, selectedId }: NetworkGraphProps) {
  const { nodes, links } = useGraphData(endpoints);
  const graphRef = useRef<any>(null);

  const handleNodeClick = useCallback((node: any) => {
    const endpoint = endpoints.find(e => e.id === node.id);
    if (endpoint && onNodeClick) {
      onNodeClick(endpoint);
    }
  }, [endpoints, onNodeClick]);

  const getNodeColor = useCallback((node: any) => {
    return TIER_HEX[node.risk_tier as RiskTier] ?? TIER_HEX.unknown;
  }, []);

  const getNodeSize = useCallback((node: any) => {
    const sizeMap: Record<string, number> = {
      low: 4,
      medium: 6,
      high: 8,
      critical: 10
    };
    return sizeMap[node.traffic_volume] ?? 4;
  }, []);

  if (endpoints.length === 0) {
    return (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'var(--font-serif)',
        fontSize: '16px',
        fontStyle: 'italic',
        color: 'var(--cream-60)',
      }}>
        No endpoints to visualize
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <ForceGraph2D
        ref={graphRef}
        graphData={{ nodes, links }}
        backgroundColor="transparent"
        nodeLabel={(node: any) => `${node.name}\n${node.host}\n${node.risk_tier.toUpperCase()}`}
        nodeColor={getNodeColor}
        nodeVal={getNodeSize}
        linkColor={() => 'rgba(27, 26, 23, 0.08)'}
        linkWidth={0.5}
        onNodeClick={handleNodeClick}
        enableNodeDrag={true}
        enableZoomInteraction={true}
        enablePanInteraction={true}
        d3VelocityDecay={0.3}
        cooldownTicks={150}
        warmupTicks={40}
        nodeCanvasObject={(node: any, ctx, globalScale) => {
          const size = getNodeSize(node);
          const x = node.x ?? 0;
          const y = node.y ?? 0;

          ctx.beginPath();
          ctx.arc(x, y, size, 0, 2 * Math.PI);
          ctx.fillStyle = getNodeColor(node);
          ctx.fill();

          if (selectedId === node.id) {
            ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--acid').trim() || '#1E4637';
            ctx.lineWidth = 2 / globalScale;
            ctx.beginPath();
            ctx.arc(x, y, size + 3, 0, 2 * Math.PI);
            ctx.stroke();
          }
        }}
        nodeCanvasObjectMode={() => 'replace'}
      />
    </div>
  );
}
