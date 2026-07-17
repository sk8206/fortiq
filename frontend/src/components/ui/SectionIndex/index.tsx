interface SectionIndexProps {
  number: string;
  label: string;
}

export function SectionIndex({ number, label }: SectionIndexProps) {
  return (
    <div className="section-index">
      <span className="si-num">{number}</span>
      <span className="si-rule" />
      <span className="si-label">{label}</span>
    </div>
  );
}
