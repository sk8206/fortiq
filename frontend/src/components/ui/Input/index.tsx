import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({ label, className = '', style, ...props }: InputProps) {
  const inputStyles = {
    background: 'var(--recess)',
    border: 'none',
    borderBottom: '1px solid var(--rule-strong)',
    borderRadius: '0',
    padding: '10px 0px',
    fontFamily: 'var(--font-mono)',
    fontSize: '13px',
    color: 'var(--cream)',
    width: '100%',
    transition: 'border-color var(--t-base) var(--ease-out)',
  };

  return (
    <div style={{ marginBottom: label ? '20px' : '0' }}>
      {label && (
        <label
          style={{
            display: 'block',
            fontFamily: 'var(--font-ui)',
            fontSize: '10px',
            fontWeight: 700,
            letterSpacing: '0.14em',
            color: 'var(--cream-60)',
            textTransform: 'uppercase',
            marginBottom: '8px',
          }}
        >
          {label}
        </label>
      )}
      <input
        className={className}
        style={{ ...inputStyles, ...style }}
        onFocus={(e) => {
          e.currentTarget.style.borderBottomColor = 'var(--acid)';
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderBottomColor = 'var(--rule-strong)';
        }}
        {...props}
      />
    </div>
  );
}
