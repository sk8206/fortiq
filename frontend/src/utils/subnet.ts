export function getSubnetPrefix(ip: string): string {
  const parts = ip.split('.');
  if (parts.length === 4) {
    return parts.slice(0, 3).join('.');
  }
  return ip;
}
