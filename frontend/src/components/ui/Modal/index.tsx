import React from 'react';
import { Button } from '../Button';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
}

export function Modal({ isOpen, onClose, children, title }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(2,2,4,0.85)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 40,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'var(--field)',
          border: '1px solid var(--rule-strong)',
          borderRadius: '4px',
          maxWidth: '500px',
          width: '90%',
          maxHeight: '90vh',
          overflow: 'auto',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {title && (
          <>
            <div
              style={{
                padding: '24px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <h2
                style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: '22px',
                  color: 'var(--cream)',
                }}
              >
                {title}
              </h2>
              <Button variant="ghost" onClick={onClose} style={{ padding: '6px 12px' }}>
                CLOSE
              </Button>
            </div>
            <div style={{ height: '1px', background: 'var(--rule)' }} />
          </>
        )}
        <div style={{ padding: '24px' }}>{children}</div>
      </div>
    </div>
  );
}
