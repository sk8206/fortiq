import React from 'react';

interface ReticleMarkProps {
  style?: React.CSSProperties;
  className?: string;
}

export function ReticleMark({ style, className }: ReticleMarkProps) {
  return (
    <svg
      viewBox="0 0 40 40"
      fill="none"
      style={style}
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="0.5" />
      <circle cx="20" cy="20" r="10" stroke="currentColor" strokeWidth="0.5" />
      <circle cx="20" cy="20" r="2" fill="currentColor" />
      <line x1="0" y1="20" x2="8" y2="20" stroke="currentColor" strokeWidth="0.5" />
      <line x1="32" y1="20" x2="40" y2="20" stroke="currentColor" strokeWidth="0.5" />
      <line x1="20" y1="0" x2="20" y2="8" stroke="currentColor" strokeWidth="0.5" />
      <line x1="20" y1="32" x2="20" y2="40" stroke="currentColor" strokeWidth="0.5" />
    </svg>
  );
}
