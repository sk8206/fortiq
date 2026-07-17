import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'ghost' | 'danger';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', children, className = '', style, ...props }: ButtonProps) {
  const baseStyles = {
    fontFamily: 'var(--font-ui)',
    fontSize: '12px',
    fontWeight: 700,
    letterSpacing: '0.10em',
    textTransform: 'uppercase' as const,
    borderRadius: '2px',
    padding: '10px 20px',
    border: '1px solid',
    cursor: props.disabled ? 'not-allowed' : 'pointer',
    transition: 'all var(--t-base) var(--ease-out)',
    opacity: props.disabled ? 0.5 : 1,
  };

  const variantStyles = {
    primary: {
      color: 'var(--acid)',
      background: 'var(--acid-08)',
      borderColor: 'var(--acid-border)',
    },
    ghost: {
      color: 'var(--cream-60)',
      background: 'transparent',
      borderColor: 'var(--rule)',
    },
    danger: {
      color: 'var(--r-critical)',
      background: 'var(--r-critical-bg)',
      borderColor: 'var(--r-critical)',
    },
  };

  const hoverStyles = variant === 'primary'
    ? { background: 'var(--acid-15)' }
    : variant === 'ghost'
    ? { background: 'var(--cream-05)' }
    : { background: 'rgba(255,53,53,0.15)' };

  return (
    <button
      className={className}
      style={{ ...baseStyles, ...variantStyles[variant], ...style }}
      onMouseEnter={(e) => {
        if (!props.disabled) {
          Object.assign(e.currentTarget.style, hoverStyles);
        }
      }}
      onMouseLeave={(e) => {
        if (!props.disabled) {
          Object.assign(e.currentTarget.style, variantStyles[variant]);
        }
      }}
      {...props}
    >
      {children} →
    </button>
  );
}
