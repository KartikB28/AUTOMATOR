import React from 'react';

const STATUS_COLORS = {
  idle: 'bg-muted',
  running: 'bg-accent animate-pulse',
  error: 'bg-danger',
  paused: 'bg-warn',
  ok: 'bg-accent',
  off: 'bg-muted',
};

export default function StatusDot({ status = 'idle', size = 'sm' }) {
  const sizeClass = size === 'lg' ? 'w-3 h-3' : 'w-2 h-2';
  return (
    <span className={`inline-block rounded-full ${sizeClass} ${STATUS_COLORS[status] || 'bg-muted'}`} />
  );
}
