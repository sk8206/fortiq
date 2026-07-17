

interface SkeletonProps {
  width?: number | string;
  height?: number | string;
  className?: string;
}

export function Skeleton({ width = '100%', height = '20px', className = '' }: SkeletonProps) {
  return (
    <div
      className={className}
      style={{
        background: `linear-gradient(90deg, var(--recess) 0%, var(--cream-05) 50%, var(--recess) 100%)`,
        backgroundSize: '200% 100%',
        animation: 'skeleton-sweep 1.8s ease infinite',
        borderRadius: '2px',
        height,
        width,
      }}
    />

  );
}
