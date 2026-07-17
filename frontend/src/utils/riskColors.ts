import type { RiskTier } from '@/types';

export const TIER_HEX: Record<RiskTier, string> = {
  critical: '#C22F2F',
  high: '#D35400',
  medium: '#B58900',
  low: '#2A7B4C',
  unknown: 'rgba(27, 26, 23, 0.20)',
};


export const TIER_CSS_VAR: Record<RiskTier, string> = {
  critical: 'var(--r-critical)',
  high: 'var(--r-high)',
  medium: 'var(--r-medium)',
  low: 'var(--r-low)',
  unknown: 'var(--r-unknown)',
};

export function getRiskColor(tier: RiskTier): string {
  return TIER_HEX[tier];
}

export function getRiskColorVar(tier: RiskTier): string {
  return TIER_CSS_VAR[tier];
}
