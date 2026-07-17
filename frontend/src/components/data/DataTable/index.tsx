
import type { Endpoint } from '@/types';
import { RiskBadge } from '../RiskBadge';
import { StatusBadge } from '../StatusBadge';

interface DataTableProps {
  endpoints: Endpoint[];
  onRowClick?: (endpoint: Endpoint) => void;
  selectable?: boolean;
  selectedIds?: Set<string>;
  onSelectionChange?: (ids: Set<string>) => void;
}

export function DataTable({
  endpoints,
  onRowClick,
  selectable = false,
  selectedIds = new Set(),
  onSelectionChange,
}: DataTableProps) {
  const handleToggle = (id: string) => {
    if (!onSelectionChange) return;
    const newSet = new Set(selectedIds);
    if (newSet.has(id)) {
      newSet.delete(id);
    } else {
      newSet.add(id);
    }
    onSelectionChange(newSet);
  };

  const handleToggleAll = () => {
    if (!onSelectionChange) return;
    if (selectedIds.size === endpoints.length) {
      onSelectionChange(new Set());
    } else {
      onSelectionChange(new Set(endpoints.map((e) => e.id)));
    }
  };

  return (
    <div
      style={{
        background: 'var(--field)',
        border: '1px solid var(--rule)',
        borderRadius: '4px',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: selectable
            ? '40px 6px 1fr 80px 100px 100px 80px 120px'
            : '6px 1fr 80px 100px 100px 80px 120px',
          padding: '12px 24px',
          borderBottom: '1px solid var(--rule)',
          fontFamily: 'var(--font-ui)',
          fontSize: '10px',
          fontWeight: 700,
          letterSpacing: '0.14em',
          color: 'var(--cream-25)',
          textTransform: 'uppercase',
        }}
      >
        {selectable && (
          <input
            type="checkbox"
            checked={selectedIds.size === endpoints.length && endpoints.length > 0}
            onChange={handleToggleAll}
            style={{ cursor: 'pointer' }}
          />
        )}
        <span></span>
        <span>NAME</span>
        <span>TYPE</span>
        <span>ALGORITHM</span>
        <span>TIER</span>
        <span>SCORE</span>
        <span>STATUS</span>
      </div>

      {/* Rows */}
      {endpoints.length === 0 ? (
        <div
          style={{
            padding: '48px 24px',
            textAlign: 'center',
            fontFamily: 'var(--font-serif)',
            fontSize: '16px',
            fontStyle: 'italic',
            color: 'var(--cream-60)',
          }}
        >
          No endpoints found
        </div>
      ) : (
        endpoints.map((endpoint) => (
          <div
            key={endpoint.id}
            style={{
              display: 'grid',
              gridTemplateColumns: selectable
                ? '40px 6px 1fr 80px 100px 100px 80px 120px'
                : '6px 1fr 80px 100px 100px 80px 120px',
              padding: '12px 24px',
              borderBottom: '1px solid var(--rule)',
              cursor: onRowClick ? 'pointer' : 'default',
              transition: 'background var(--t-fast) var(--ease-out)',
              alignItems: 'center',
            }}
            onClick={() => onRowClick?.(endpoint)}
            onMouseEnter={(e) => {
              if (onRowClick) e.currentTarget.style.background = 'var(--cream-05)';
            }}
            onMouseLeave={(e) => {
              if (onRowClick) e.currentTarget.style.background = 'transparent';
            }}
          >
            {selectable && (
              <input
                type="checkbox"
                checked={selectedIds.has(endpoint.id)}
                onChange={(e) => {
                  e.stopPropagation();
                  handleToggle(endpoint.id);
                }}
                onClick={(e) => e.stopPropagation()}
                style={{ cursor: 'pointer' }}
              />
            )}
            <span
              style={{
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                background: `var(--r-${endpoint.risk_tier})`,
              }}
            />
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '13px',
                color: 'var(--cream)',
              }}
            >
              {endpoint.name}
            </span>
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '11px',
                color: 'var(--cream-25)',
                textTransform: 'uppercase',
              }}
            >
              {endpoint.endpoint_type}
            </span>
            <span
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '12px',
                color: 'var(--cream-25)',
              }}
            >
              {endpoint.algorithm}
            </span>
            <RiskBadge tier={endpoint.risk_tier} />
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '14px',
                fontWeight: 500,
                color: 'var(--cream)',
              }}
            >
              {endpoint.risk_score !== null ? endpoint.risk_score.toFixed(2) : '—'}
            </span>
            <StatusBadge status={endpoint.migration_status} />
          </div>
        ))
      )}
    </div>
  );
}
