

interface EmptyStateProps {
  title: string;
  description?: string;
}

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div
      style={{
        padding: '64px 24px',
        textAlign: 'center',
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '32px',
          color: 'var(--cream-25)',
          marginBottom: '12px',
          letterSpacing: '0.06em',
        }}
      >
        {title}
      </div>
      {description && (
        <div
          style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '16px',
            fontStyle: 'italic',
            color: 'var(--cream-60)',
          }}
        >
          {description}
        </div>
      )}
    </div>
  );
}
