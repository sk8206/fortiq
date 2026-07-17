import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { SectionIndex } from '@/components/ui/SectionIndex';
import { ReticleMark } from '@/components/ui/ReticleMark';
import { authApi } from '@/api/auth';
import { useAuthStore } from '@/stores/useAuthStore';

export function LoginView() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { setUser, setToken } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await authApi.login(username, password);
      setToken(response.access_token);
      setUser(response.user);
      navigate('/');
    } catch (err) {
      setError('[ERR-001] Authentication failed. Check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      {/* Left panel - Hero */}
      <div
        style={{
          flex: 1,
          background: 'var(--field)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '48px',
        }}
      >
        <ReticleMark
          style={{
            width: '100px',
            height: '100px',
            color: 'var(--acid)',
            animation: 'reticle-spin 200s linear infinite',
            marginBottom: '32px',
          }}
        />
        <div
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '64px',
            color: 'var(--cream)',
            letterSpacing: '0.06em',
            marginBottom: '16px',
          }}
        >
          FORTIQ
        </div>
        <div
          style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '16px',
            fontStyle: 'italic',
            color: 'var(--cream-60)',
            marginBottom: '64px',
          }}
        >
          Quantum-Safe Migration Platform
        </div>
        <div
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '11px',
            color: 'var(--cream-25)',
            letterSpacing: '0.08em',
          }}
        >
          ML-KEM-768 · ML-DSA-65 · FIPS 203/204
        </div>
      </div>

      {/* Right panel - Form */}
      <div
        style={{
          flex: 1,
          background: 'var(--void)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '48px',
        }}
      >
        <div style={{ width: '100%', maxWidth: '340px' }}>
          <SectionIndex number="[01]" label="AUTHENTICATION" />

          <form onSubmit={handleSubmit}>
            <Input
              label="USERNAME"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="admin"
              required
            />
            <Input
              label="PASSWORD"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />

            {error && (
              <div
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '11px',
                  color: 'var(--r-critical)',
                  marginBottom: '16px',
                  padding: '12px',
                  background: 'var(--r-critical-bg)',
                  border: '1px solid var(--r-critical)',
                  borderRadius: '2px',
                }}
              >
                {error}
              </div>
            )}

            <Button
              variant="primary"
              type="submit"
              disabled={isLoading}
              style={{ width: '100%' }}
            >
              {isLoading ? 'AUTHENTICATING...' : 'AUTHENTICATE'}
            </Button>
          </form>

          <div
            style={{
              marginTop: '24px',
              padding: '12px',
              background: 'var(--recess)',
              border: '1px solid var(--rule)',
              borderRadius: '2px',
            }}
          >
            <div
              style={{
                fontFamily: 'var(--font-ui)',
                fontSize: '10px',
                fontWeight: 700,
                letterSpacing: '0.14em',
                color: 'var(--cream-25)',
                textTransform: 'uppercase',
                marginBottom: '8px',
              }}
            >
              Demo Credentials
            </div>
            <div
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '12px',
                color: 'var(--cream-60)',
              }}
            >
              admin / fortiq-demo-2024
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
