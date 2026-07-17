import { useState, useEffect } from 'react';
import { formatDayTime } from '@/utils/formatters';

export function useLiveClock() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return formatDayTime(time);
}
