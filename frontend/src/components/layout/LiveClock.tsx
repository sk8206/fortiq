import { useLiveClock } from '@/hooks/useLiveClock';

export function LiveClock() {
  const time = useLiveClock();

  return (
    <div
      style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '11px',
        textTransform: 'uppercase',
        color: 'var(--cream-25)',
        letterSpacing: '0.08em',
      }}
    >
      {time}
    </div>
  );
}
