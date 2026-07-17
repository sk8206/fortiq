import { useState, useMemo, useEffect, useRef } from 'react';
import { DataTable } from '@/components/data/DataTable';
import { Button } from '@/components/ui/Button';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { ConfirmModal } from '@/components/ui/ConfirmModal';
import { useEndpointStore } from '@/stores/useEndpointStore';
import { useMigrateStore } from '@/stores/useMigrateStore';
import type { RiskTier } from '@/types';

export function MigrationQueue() {
  const { endpoints, fetchEndpoints } = useEndpointStore();
  const {
    selectedIds,
    setSelectedIds,
    tierFilter,
    setTierFilter,
    currentJob,
    isRunning,
    startMigration,
    error
  } = useMigrateStore();

  const [showConfirm, setShowConfirm] = useState(false);
  const wasRunning = useRef(false);

  // Refresh endpoints when migration completes
  useEffect(() => {
    if (wasRunning.current && !isRunning && currentJob?.status === 'completed') {
      fetchEndpoints();
    }
    wasRunning.current = isRunning;
  }, [isRunning, currentJob?.status, fetchEndpoints]);

  const filteredEndpoints = useMemo(() => {
    let filtered = endpoints.filter(ep => ep.migration_status === 'pending');
    if (tierFilter !== 'all') {
      filtered = filtered.filter(ep => ep.risk_tier === tierFilter);
    }
    return filtered;
  }, [endpoints, tierFilter]);

  const handleMigrate = () => {
    if (selectedIds.size === 0) return;
    setShowConfirm(true);
  };

  const confirmMigration = () => {
    setShowConfirm(false);
    startMigration(Array.from(selectedIds));
  };

  return (
    <div style={{
      border: '1px solid var(--rule)',
      background: 'var(--field)',
      padding: '32px',
      borderRadius: '4px',
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '24px',
      }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <h3 style={{
            fontFamily: 'var(--font-ui)',
            fontSize: '16px',
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: 'var(--cream)',
          }}>
            MIGRATION QUEUE
          </h3>

          <select
            value={tierFilter}
            onChange={(e) => setTierFilter(e.target.value as RiskTier | 'all')}
            disabled={isRunning}
            style={{
              fontFamily: 'var(--font-ui)',
              fontSize: '11px',
              fontWeight: 700,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              padding: '8px 12px',
              background: 'var(--recess)',
              border: '1px solid var(--rule)',
              borderBottom: '1px solid var(--rule-strong)',
              color: 'var(--cream)',
              borderRadius: '2px',
              cursor: 'pointer',
            }}
          >
            <option value="all">ALL TIERS</option>
            <option value="critical">CRITICAL</option>
            <option value="high">HIGH</option>
            <option value="medium">MEDIUM</option>
            <option value="low">LOW</option>
          </select>
        </div>

        <Button
          onClick={handleMigrate}
          disabled={selectedIds.size === 0 || isRunning}
        >
          MIGRATE SELECTED ({selectedIds.size})
        </Button>
      </div>

      {currentJob && (
        <div style={{ marginBottom: '24px' }}>
          <ProgressBar value={currentJob.progress_pct} max={100} variant="accent" />
          <div style={{
            marginTop: '12px',
            fontFamily: 'var(--font-mono)',
            fontSize: '11px',
            color: 'var(--cream-60)',
            textTransform: 'uppercase',
          }}>
            {isRunning
              ? `MIGRATING: ${currentJob.processed}/${currentJob.total} ENDPOINTS (${currentJob.progress_pct.toFixed(1)}%)`
              : `STATUS: ${currentJob.status.toUpperCase()}`
            }
          </div>
        </div>
      )}

      {error && (
        <div style={{
          marginBottom: '24px',
          padding: '12px',
          background: 'rgba(255,53,53,0.1)',
          border: '1px solid var(--r-critical)',
          fontFamily: 'var(--font-mono)',
          fontSize: '12px',
          color: 'var(--r-critical)',
          borderRadius: '2px',
        }}>
          [ERR] {error}
        </div>
      )}

      <DataTable
        endpoints={filteredEndpoints}
        selectable={true}
        selectedIds={selectedIds}
        onSelectionChange={setSelectedIds}
      />

      {filteredEndpoints.length === 0 && (
        <div style={{
          padding: '48px 24px',
          textAlign: 'center',
          fontFamily: 'var(--font-serif)',
          fontSize: '16px',
          fontStyle: 'italic',
          color: 'var(--cream-60)',
        }}>
          No pending endpoints found. All endpoints have been processed.
        </div>
      )}

      <ConfirmModal
        isOpen={showConfirm}
        onClose={() => setShowConfirm(false)}
        onConfirm={confirmMigration}
        title="CONFIRM MIGRATION"
        description={`You are about to migrate ${selectedIds.size} endpoint(s) to post-quantum cryptography. This will generate ML-KEM-768 and ML-DSA-65 configurations.`}
        confirmText="CONFIRM"
      />
    </div>
  );
}
