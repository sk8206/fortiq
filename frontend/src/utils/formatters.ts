export function formatNumber(num: number): string {
  return new Intl.NumberFormat('en-US').format(num);
}

export function formatPercent(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`;
}

export function formatTimestamp(date: string): string {
  const d = new Date(date);
  return d.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

export function formatTimeHHMMSS(date: Date): string {
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
}

export function formatDayTime(date: Date): string {
  const day = date.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
  const time = formatTimeHHMMSS(date);
  return `${day} ${time} UTC`;
}
