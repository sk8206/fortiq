import { useMemo } from 'react';
import type { Endpoint } from '@/types';
import { getSubnetPrefix } from '@/utils/subnet';

interface GraphNode {
  id: string;
  name: string;
  risk_tier: string;
  risk_score: number | null;
  traffic_volume: string;
  endpoint_type: string;
  migration_status: string;
  host: string;
}

interface GraphLink {
  source: string;
  target: string;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export function useGraphData(endpoints: Endpoint[]): GraphData {
  return useMemo(() => {
    const nodes: GraphNode[] = endpoints.map((ep) => ({
      id: ep.id,
      name: ep.name,
      risk_tier: ep.risk_tier,
      risk_score: ep.risk_score,
      traffic_volume: ep.traffic_volume,
      endpoint_type: ep.endpoint_type,
      migration_status: ep.migration_status,
      host: ep.host,
    }));

    const links: GraphLink[] = [];
    const subnetGroups = new Map<string, string[]>();

    for (const ep of endpoints) {
      const prefix = getSubnetPrefix(ep.host);
      const group = subnetGroups.get(prefix) ?? [];
      group.push(ep.id);
      subnetGroups.set(prefix, group);
    }

    for (const ids of subnetGroups.values()) {
      const maxConnections = Math.min(ids.length, 6);
      for (let i = 0; i < maxConnections; i++) {
        for (let j = i + 1; j < maxConnections; j++) {
          links.push({ source: ids[i], target: ids[j] });
        }
      }
    }

    return { nodes, links };
  }, [endpoints]);
}
