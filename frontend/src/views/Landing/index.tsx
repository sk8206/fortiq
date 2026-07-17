import { useNavigate } from 'react-router-dom';
import { ReticleMark } from '@/components/ui/ReticleMark';
import { Button } from '@/components/ui/Button';

export function LandingView() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'var(--void)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Hero Section */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '64px 40px',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Background Reticle */}
        <ReticleMark
          style={{
            position: 'absolute',
            width: '600px',
            height: '600px',
            color: 'var(--acid)',
            opacity: 0.03,
            animation: 'reticle-spin 200s linear infinite',
          }}
        />

        {/* Logo and Title */}
        <div style={{ position: 'relative', textAlign: 'center', marginBottom: '48px' }}>
          <ReticleMark
            style={{
              width: '80px',
              height: '80px',
              color: 'var(--acid)',
              marginBottom: '24px',
            }}
          />
          <h1
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '72px',
              color: 'var(--cream)',
              letterSpacing: '0.04em',
              lineHeight: 1,
              marginBottom: '16px',
            }}
          >
            FORTIQ
          </h1>
          <p
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '20px',
              fontStyle: 'italic',
              color: 'var(--cream-60)',
            }}
          >
            Post-Quantum Cryptographic Migration Platform
          </p>
        </div>

        {/* Login Button */}
        <Button onClick={() => navigate('/login')} style={{ marginBottom: '64px' }}>
          ACCESS PLATFORM
        </Button>

        {/* Main Description */}
        <div
          style={{
            maxWidth: '800px',
            textAlign: 'center',
            position: 'relative',
          }}
        >
          <p
            style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '18px',
              lineHeight: 1.8,
              color: 'var(--cream-60)',
              marginBottom: '32px',
            }}
          >
            Quantum computers running Shor's Algorithm will break RSA and ECC encryption
            by 2030-2035. Fortiq automates the transition to NIST-approved post-quantum
            cryptography, protecting your infrastructure from "Harvest Now, Decrypt Later"
            attacks.
          </p>
        </div>
      </div>

      {/* Features Section */}
      <div
        style={{
          borderTop: '1px solid var(--rule)',
          padding: '64px 40px',
          background: 'var(--field)',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {/* Section Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '48px' }}>
            <span
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '13px',
                color: 'var(--acid)',
                letterSpacing: '0.08em',
              }}
            >
              [01]
            </span>
            <span style={{ flex: 1, height: '1px', background: 'var(--rule)' }} />
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '0.14em',
                color: 'var(--cream-60)',
                textTransform: 'uppercase',
              }}
            >
              HOW IT WORKS
            </span>
          </div>

          {/* Three Steps */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '32px',
            }}
          >
            <FeatureCard
              step="01"
              title="Discover"
              description="Automatically scan and inventory all cryptographic endpoints across your infrastructure. Identify RSA, ECC, and legacy encryption systems requiring migration."
            />
            <FeatureCard
              step="02"
              title="Classify"
              description="Our Variational Quantum Classifier (VQC) analyzes each endpoint's risk profile, prioritizing migration based on data sensitivity, exposure, and certificate urgency."
            />
            <FeatureCard
              step="03"
              title="Migrate"
              description="Generate ML-KEM-768 and ML-DSA-65 configurations (FIPS 203/204) with hybrid mode transitions and deterministic rollback for zero-downtime deployment."
            />
          </div>
        </div>
      </div>

      {/* Technology Section */}
      <div
        style={{
          borderTop: '1px solid var(--rule)',
          padding: '64px 40px',
          background: 'var(--void)',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {/* Section Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '48px' }}>
            <span
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '13px',
                color: 'var(--acid)',
                letterSpacing: '0.08em',
              }}
            >
              [02]
            </span>
            <span style={{ flex: 1, height: '1px', background: 'var(--rule)' }} />
            <span
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '0.14em',
                color: 'var(--cream-60)',
                textTransform: 'uppercase',
              }}
            >
              NIST POST-QUANTUM STANDARDS
            </span>
          </div>

          {/* Algorithm Cards */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: '1px',
              background: 'var(--rule)',
              border: '1px solid var(--rule)',
            }}
          >
            <AlgorithmCard
              standard="FIPS 203"
              name="ML-KEM-768"
              type="Key Encapsulation"
              description="Quantum-resistant key exchange replacing RSA and ECDH. NIST Security Level 3."
            />
            <AlgorithmCard
              standard="FIPS 204"
              name="ML-DSA-65"
              type="Digital Signature"
              description="Quantum-resistant authentication replacing RSA and ECDSA signatures. NIST Security Level 3."
            />
          </div>
        </div>
      </div>

      {/* Footer */}
      <div
        style={{
          borderTop: '1px solid var(--rule)',
          padding: '32px 40px',
          background: 'var(--field)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '11px',
            color: 'var(--cream-25)',
            letterSpacing: '0.08em',
          }}
        >
          ML-KEM-768 {'\u00B7'} ML-DSA-65 {'\u00B7'} FIPS 203/204 {'\u00B7'} NIST LEVEL 3
        </div>
        <Button variant="ghost" onClick={() => navigate('/login')}>
          LOGIN
        </Button>
      </div>
    </div>
  );
}

interface FeatureCardProps {
  step: string;
  title: string;
  description: string;
}

function FeatureCard({ step, title, description }: FeatureCardProps) {
  return (
    <div
      style={{
        padding: '32px',
        background: 'var(--void)',
        border: '1px solid var(--rule)',
        borderRadius: '4px',
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '48px',
          color: 'var(--acid)',
          lineHeight: 1,
          marginBottom: '16px',
        }}
      >
        {step}
      </div>
      <h3
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '24px',
          color: 'var(--cream)',
          marginBottom: '12px',
        }}
      >
        {title}
      </h3>
      <p
        style={{
          fontFamily: 'var(--font-ui)',
          fontSize: '14px',
          lineHeight: 1.6,
          color: 'var(--cream-60)',
        }}
      >
        {description}
      </p>
    </div>
  );
}

interface AlgorithmCardProps {
  standard: string;
  name: string;
  type: string;
  description: string;
}

function AlgorithmCard({ standard, name, type, description }: AlgorithmCardProps) {
  return (
    <div
      style={{
        padding: '32px',
        background: 'var(--field)',
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: '13px',
          color: 'var(--acid)',
          letterSpacing: '0.08em',
          marginBottom: '8px',
        }}
      >
        [{standard}]
      </div>
      <h3
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '32px',
          fontStyle: 'italic',
          color: 'var(--cream)',
          marginBottom: '8px',
        }}
      >
        {name}
      </h3>
      <div
        style={{
          fontFamily: 'var(--font-ui)',
          fontSize: '11px',
          fontWeight: 700,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color: 'var(--cream-60)',
          marginBottom: '16px',
        }}
      >
        {type}
      </div>
      <p
        style={{
          fontFamily: 'var(--font-serif)',
          fontSize: '14px',
          fontStyle: 'italic',
          lineHeight: 1.6,
          color: 'var(--cream-60)',
        }}
      >
        {description}
      </p>
    </div>
  );
}
