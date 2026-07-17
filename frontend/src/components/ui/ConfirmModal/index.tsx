import { useState } from 'react';
import { Button } from '../Button';
import { Input } from '../Input';
import { Modal } from '../Modal';

interface ConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  description: string;
  confirmText?: string;
}

export function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmText = 'CONFIRM',
}: ConfirmModalProps) {
  const [input, setInput] = useState('');

  const handleConfirm = () => {
    if (input === confirmText) {
      onConfirm();
      setInput('');
      onClose();
    }
  };

  const handleClose = () => {
    setInput('');
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title={title}>
      <div style={{ marginBottom: '24px' }}>
        <p
          style={{
            fontFamily: 'var(--font-ui)',
            fontSize: '14px',
            color: 'var(--cream-60)',
            lineHeight: 1.6,
          }}
        >
          {description}
        </p>
      </div>
      <Input
        placeholder={`TYPE ${confirmText} TO PROCEED`}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ marginBottom: '20px' }}
      />
      <div style={{ display: 'flex', gap: '12px' }}>
        <Button
          variant="primary"
          disabled={input !== confirmText}
          onClick={handleConfirm}
          style={{ flex: 1 }}
        >
          PROCEED
        </Button>
        <Button variant="ghost" onClick={handleClose} style={{ flex: 1 }}>
          CANCEL
        </Button>
      </div>
    </Modal>
  );
}
