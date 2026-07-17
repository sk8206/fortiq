interface NetworkCoordOverlayProps {
  nodeCount: number;
  linkCount: number;
  scale?: number;
}

export function NetworkCoordOverlay({ nodeCount, linkCount, scale = 1 }: NetworkCoordOverlayProps) {
  return (
    <div style={{
      position: 'absolute',
      top: '16px',
      right: '16px',
      padding: '12px 16px',
      background: 'rgba(8,8,15,0.85)',
      border: '1px solid var(--rule)',
      fontFamily: 'var(--font-mono)',
      fontSize: '11px',
      color: 'var(--cream-60)',
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      lineHeight: '1.8',
      borderRadius: '2px',
      pointerEvents: 'none',
    }}>
      <div>NODES: {nodeCount}</div>
      <div>EDGES: {linkCount}</div>
      <div>SCALE: {scale.toFixed(2)}x</div>
    </div>
  );
}
