import { useEffect, useState } from 'react';
import { SectionIndex } from '@/components/ui/SectionIndex';
import { migrateApi } from '@/api/migrate';
import type { AuditEntry } from '@/types';

const STATUS_COLORS: Record<string, string> = {
  complete: 'var(--r-low)',
  rollback: 'var(--r-critical)',
  hybrid: 'var(--r-medium)',
  in_progress: 'var(--acid)',
  pending: 'var(--cream-60)',
};

export function RecentActivityFeed() {
  const [entries, setEntries] = useState<AuditEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAuditLog = async () => {
      try {
        const data = await migrateApi.getAuditLog();
        setEntries(data.slice(0, 8));
      } catch {
        // Silent fail - show empty state
      } finally {
        setLoading(false);
      }
    };

    fetchAuditLog();
    const interval = setInterval(fetchAuditLog, 5000);
    return () => clearInterval(interval);
  }, []);

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  if (loading) {
    return (
      <div
        style={{
          background: 'var(--field)',
          padding: '24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
        }}
      >
        <div
          style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '14px',
            fontStyle: 'italic',
            color: 'var(--cream-60)',
          }}
        >
          Loading activity...
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        background: 'var(--field)',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        overflow: 'hidden',
      }}
    >
      <SectionIndex number="[03]" label="RECENT ACTIVITY" />

      {entries.length === 0 ? (
        <div
          style={{
            flex: 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <div
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '14px',
              fontStyle: 'italic',
              color: 'var(--cream-60)',
              textAlign: 'center',
            }}
          >
            Awaiting migration activity...
          </div>
        </div>
      ) : (
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {entries.map((entry, index) => (
            <div
              key={entry.id || index}
              style={{
                padding: '10px 0',
                borderBottom: index < entries.length - 1 ? '1px solid var(--rule)' : 'none',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '10px',
                    color: 'var(--cream-25)',
                    flexShrink: 0,
                  }}
                >
                  {entry.created_at ? formatTime(entry.created_at) : '--:--:--'}
                </span>
                <span
                  style={{
                    fontFamily: 'var(--font-ui)',
                    fontSize: '12px',
                    color: 'var(--cream-60)',
                  }}
                >
                  {entry.endpoint_name || 'Unknown'}
                </span>
              </div>
              <div
                style={{
                  marginTop: '4px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  marginLeft: '62px',
                }}
              >
                <span
                  style={{
                    fontFamily: 'var(--font-ui)',
                    fontSize: '10px',
                    fontWeight: 700,
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                    color: 'var(--cream-25)',
                  }}
                >
                  {entry.from_status?.replace('_', ' ') || 'UNKNOWN'}
                </span>
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '10px',
                    color: 'var(--cream-25)',
                  }}
                >
                  {'\u2192'}
                </span>
                <span
                  style={{
                    fontFamily: 'var(--font-ui)',
                    fontSize: '10px',
                    fontWeight: 700,
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                    color: STATUS_COLORS[entry.to_status] || 'var(--cream-60)',
                  }}
                >
                  {entry.to_status?.replace('_', ' ') || 'UNKNOWN'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
