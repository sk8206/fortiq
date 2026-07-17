import { useEffect, useRef } from 'react';
import { Button } from '@/components/ui/Button';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { useClassifyStore } from '@/stores/useClassifyStore';
import { useEndpointStore } from '@/stores/useEndpointStore';

export function ClassifyPanel() {
  const { currentJob, isRunning, error, startClassification } = useClassifyStore();
  const { fetchEndpoints } = useEndpointStore();
  const wasRunning = useRef(false);

  // Refresh endpoints when classification completes
  useEffect(() => {
    if (wasRunning.current && !isRunning && currentJob?.status === 'completed') {
      fetchEndpoints();
    }
    wasRunning.current = isRunning;
  }, [isRunning, currentJob?.status, fetchEndpoints]);

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
        alignItems: 'flex-start',
        marginBottom: '24px',
      }}>
        <div>
          <h3 style={{
            fontFamily: 'var(--font-ui)',
            fontSize: '16px',
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: 'var(--cream)',
            marginBottom: '8px',
          }}>
            VQC CLASSIFIER
          </h3>
          <p style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '14px',
            fontStyle: 'italic',
            color: 'var(--cream-60)',
          }}>
            Variational Quantum Classifier for risk assessment
          </p>
        </div>

        <Button onClick={startClassification} disabled={isRunning}>
          {isRunning ? 'CLASSIFYING' : 'START CLASSIFICATION'}
        </Button>
      </div>

      {currentJob && (
        <div>
          <ProgressBar value={currentJob.progress_pct} max={100} variant="accent" />
          <div style={{
            marginTop: '12px',
            fontFamily: 'var(--font-mono)',
            fontSize: '11px',
            color: 'var(--cream-60)',
          }}>
            {isRunning
              ? `PROCESSING: ${currentJob.processed}/${currentJob.total} ENDPOINTS (${currentJob.progress_pct.toFixed(1)}%)`
              : `STATUS: ${currentJob.status.toUpperCase()}`
            }
          </div>
        </div>
      )}

      {error && (
        <div style={{
          marginTop: '16px',
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

      <div style={{
        marginTop: '32px',
        paddingTop: '24px',
        borderTop: '1px solid var(--rule)',
      }}>
        <div style={{
          fontFamily: 'var(--font-ui)',
          fontSize: '10px',
          fontWeight: 700,
          letterSpacing: '0.14em',
          textTransform: 'uppercase',
          color: 'var(--cream-25)',
          marginBottom: '12px',
        }}>
          CIRCUIT ARCHITECTURE
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '11px',
          color: 'var(--cream-60)',
          lineHeight: '2',
        }}>
          <div>DEVICE   lightning.qubit</div>
          <div>QUBITS   4</div>
          <div>LAYERS   3 x [RY / RZ / CNOT]</div>
          <div>ENCODING amplitude</div>
          <div>DIFF     adjoint</div>
        </div>
      </div>
    </div>
  );
}
