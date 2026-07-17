import { useLocation, Link } from 'react-router-dom';
import { LayoutDashboard, ScanLine, ArrowRightLeft } from 'lucide-react';
import { ReticleMark } from '../ui/ReticleMark';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/scan', icon: ScanLine, label: 'Scan' },
  { path: '/migrate', icon: ArrowRightLeft, label: 'Migrate' },
];

export function Spine() {
  const location = useLocation();

  return (
    <div
      style={{
        width: 'var(--sidebar-w)',
        background: 'var(--field)',
        borderRight: '1px solid var(--rule)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '16px 0',
        gap: '8px',
      }}
    >
      {/* Logo */}
      <div style={{ marginBottom: '24px' }}>
        <ReticleMark
          style={{
            width: '32px',
            height: '32px',
            color: 'var(--acid)',
          }}
        />
      </div>

      {/* Nav items */}
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = location.pathname === item.path;

        return (
          <Link
            key={item.path}
            to={item.path}
            style={{
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
              cursor: 'pointer',
              transition: 'all var(--t-base) var(--ease-out)',
              textDecoration: 'none',
            }}
            title={item.label}
          >
            {isActive && (
              <div
                style={{
                  position: 'absolute',
                  left: 0,
                  top: 0,
                  width: '2px',
                  height: '100%',
                  background: 'var(--acid)',
                }}
              />
            )}
            <Icon
              size={20}
              style={{
                color: isActive ? 'var(--acid)' : 'var(--cream-25)',
                transition: 'color var(--t-base) var(--ease-out)',
              }}
            />
          </Link>
        );
      })}
    </div>
  );
}
