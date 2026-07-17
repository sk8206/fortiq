export function useComplianceColor(score: number): string {
  if (score >= 80) return 'var(--r-low)';
  if (score >= 40) return 'var(--r-medium)';
  return 'var(--r-critical)';
}
