import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '@/stores/useAuthStore';

export function UserMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const { user, logout } = useAuthStore();

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  // Get user initials for avatar
  const getInitials = () => {
    if (!user?.username) return 'A';
    return user.username.charAt(0).toUpperCase();
  };

  const handleLogout = () => {
    logout();
    setIsOpen(false);
  };

  return (
    <div style={{ position: 'relative' }} ref={menuRef}>
      {/* Avatar Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '28px',
          height: '28px',
          borderRadius: '50%',
          background: 'var(--recess)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'var(--font-ui)',
          fontSize: '11px',
          fontWeight: 700,
          color: 'var(--cream-60)',
          border: 'none',
          cursor: 'pointer',
          transition: 'background var(--t-fast) var(--ease-out)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'var(--lift)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'var(--recess)';
        }}
      >
        {getInitials()}
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          style={{
            position: 'absolute',
            top: 'calc(100% + 8px)',
            right: 0,
            width: '200px',
            background: 'var(--lift)',
            border: '1px solid var(--rule-strong)',
            borderRadius: '2px',
            overflow: 'hidden',
            zIndex: 50,
            boxShadow: '0 8px 24px rgba(0,0,0,0.4)',
          }}
        >
          {/* User Info Section */}
          {user && (
            <div
              style={{
                padding: '12px 16px',
                borderBottom: '1px solid var(--rule)',
              }}
            >
              <div
                style={{
                  fontFamily: 'var(--font-ui)',
                  fontSize: '13px',
                  fontWeight: 500,
                  color: 'var(--cream)',
                  marginBottom: '4px',
                }}
              >
                {user.username}
              </div>
              <div
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '10px',
                  color: 'var(--cream-60)',
                  letterSpacing: '0.04em',
                }}
              >
                ID: {user.id.slice(0, 8)}
              </div>
            </div>
          )}

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            style={{
              width: '100%',
              padding: '12px 16px',
              border: 'none',
              background: 'transparent',
              fontFamily: 'var(--font-ui)',
              fontSize: '12px',
              fontWeight: 700,
              letterSpacing: '0.10em',
              textTransform: 'uppercase',
              color: 'var(--cream)',
              textAlign: 'left',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              transition: 'all var(--t-fast) var(--ease-out)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'var(--cream-05)';
              e.currentTarget.style.color = 'var(--acid)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent';
              e.currentTarget.style.color = 'var(--cream)';
            }}
          >
            <span>Logout</span>
            <span>→</span>
          </button>
        </div>
      )}
    </div>
  );
}
