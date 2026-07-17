import { useEffect, useState } from 'react';
import type { PQCAlgorithm } from '@/types';
import { migrateApi } from '@/api/migrate';
import { Skeleton } from '@/components/ui/Skeleton';

export function AlgorithmInfoPanel() {
  const [algorithms, setAlgorithms] = useState<{
    ml_kem_768: PQCAlgorithm | null;
    ml_dsa_65: PQCAlgorithm | null;
  }>({ ml_kem_768: null, ml_dsa_65: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await migrateApi.getPqcDemo();
        setAlgorithms(data);
        setError(null);
      } catch (err: any) {
        const errorMsg = err?.response?.data?.detail || err?.message || 'Failed to load PQC data';
        setError(errorMsg);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <Skeleton height={400} />;
  }

  if (error) {
    return (
      <div style={{
        border: '1px solid var(--rule)',
        background: 'var(--field)',
        padding: '32px',
        borderRadius: '4px',
      }}>
        <div style={{
          padding: '12px',
          background: 'rgba(255,53,53,0.1)',
          border: '1px solid var(--r-critical)',
          fontFamily: 'var(--font-mono)',
          fontSize: '12px',
          color: 'var(--r-critical)',
        }}>
          [ERR] Failed to load PQC demo: {error}
        </div>
      </div>
    );
  }

  const renderAlgorithm = (algo: PQCAlgorithm | null, title: string, description: string) => {
    if (!algo) return null;

    return (
      <div style={{
        padding: '32px',
        background: 'var(--field)',
      }}>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: '13px',
          color: 'var(--acid)',
          letterSpacing: '0.08em',
          marginBottom: '8px',
        }}>
          {algo.fips_standard}
        </div>

        <h3 style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '36px',
          fontStyle: 'italic',
          color: 'var(--cream)',
          marginBottom: '8px',
        }}>
          {title}
        </h3>

        <div style={{
          fontFamily: 'var(--font-ui)',
          fontSize: '11px',
          fontWeight: 700,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color: 'var(--cream-60)',
          marginBottom: '24px',
        }}>
          {algo.algorithm}
        </div>

        <div style={{ height: '1px', background: 'var(--rule)', margin: '24px 0' }} />

        <p style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '14px',
          fontStyle: 'italic',
          color: 'var(--cream-60)',
          lineHeight: '1.6',
          marginBottom: '24px',
        }}>
          {description}
        </p>

        <div style={{ height: '1px', background: 'var(--rule)', margin: '24px 0' }} />

        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '20px',
        }}>
          <MetricRow
            label="NIST Security Level"
            value={`${algo.nist_security_level}`}
            highlight
          />

          {algo.public_key_bytes && (
            <MetricRow
              label="Public Key"
              value={`${algo.public_key_bytes} B`}
            />
          )}

          {algo.ciphertext_bytes && (
            <MetricRow
              label="Ciphertext"
              value={`${algo.ciphertext_bytes} B`}
            />
          )}

          {algo.shared_secret_bytes && (
            <MetricRow
              label="Shared Secret"
              value={`${algo.shared_secret_bytes} B`}
            />
          )}

          {algo.signature_bytes && (
            <MetricRow
              label="Signature Size"
              value={`${algo.signature_bytes} B`}
            />
          )}
        </div>

        <div style={{ height: '1px', background: 'var(--rule)', margin: '24px 0' }} />

        <div style={{
          display: 'flex',
          gap: '8px',
          alignItems: 'center',
        }}>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '12px',
            color: 'var(--cream-60)',
            textTransform: 'uppercase',
          }}>
            VERIFICATION:
          </span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '12px',
            fontWeight: 500,
            color: (algo.encapsulation_ok ?? algo.verification_passed) ? 'var(--r-low)' : 'var(--r-critical)',
          }}>
            {(algo.encapsulation_ok ?? algo.verification_passed) ? 'PASSED' : 'FAILED'}
          </span>
        </div>
      </div>
    );
  };

  return (
    <div style={{
      border: '1px solid var(--rule)',
      background: 'var(--field)',
      borderRadius: '4px',
      overflow: 'hidden',
    }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '1px',
        background: 'var(--rule)',
      }}>
        {renderAlgorithm(
          algorithms.ml_kem_768,
          'ML-KEM-768',
          'Module-Lattice-Based Key Encapsulation Mechanism provides quantum-resistant key exchange for TLS and VPN protocols.'
        )}
        {renderAlgorithm(
          algorithms.ml_dsa_65,
          'ML-DSA-65',
          'Module-Lattice-Based Digital Signature Algorithm ensures quantum-resistant authentication and non-repudiation.'
        )}
      </div>
    </div>
  );
}

interface MetricRowProps {
  label: string;
  value: string;
  highlight?: boolean;
}

function MetricRow({ label, value, highlight }: MetricRowProps) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '4px',
    }}>
      <span style={{
        fontFamily: 'var(--font-ui)',
        fontSize: '10px',
        fontWeight: 700,
        letterSpacing: '0.14em',
        textTransform: 'uppercase',
        color: 'var(--cream-25)',
      }}>
        {label}
      </span>
      <span style={{
        fontFamily: highlight ? 'var(--font-display)' : 'var(--font-mono)',
        fontSize: highlight ? '28px' : '13px',
        color: highlight ? 'var(--acid)' : 'var(--cream)',
      }}>
        {value}
      </span>
    </div>
  );
}
