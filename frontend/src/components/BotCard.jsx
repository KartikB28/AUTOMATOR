import React from 'react';
import { Play, Pause, RefreshCw } from 'lucide-react';
import StatusDot from './StatusDot.jsx';
import { formatDistanceToNow } from 'date-fns';

export default function BotCard({ name, label, description, state = {}, onRun, onToggle }) {
  const status = state.status || 'idle';
  const enabled = state.enabled !== false;

  return (
    <div className="bg-dark-700 border border-dark-500 rounded-lg p-4">
      <div className="flex items-start justify-between mb-2">
        <div>
          <div className="flex items-center gap-2">
            <StatusDot status={status} />
            <span className="font-mono text-sm font-medium">{label}</span>
          </div>
          <div className="text-xs text-muted font-mono mt-1">{description}</div>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => onToggle(name)}
            className="p-1.5 rounded bg-dark-600 hover:bg-dark-500 transition-colors"
            title={enabled ? 'Pause' : 'Resume'}
          >
            <Pause size={12} className={enabled ? 'text-warn' : 'text-muted'} />
          </button>
          <button
            onClick={() => onRun(name)}
            disabled={status === 'running'}
            className="p-1.5 rounded bg-dark-600 hover:bg-dark-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            title="Run now"
          >
            {status === 'running'
              ? <RefreshCw size={12} className="animate-spin text-accent" />
              : <Play size={12} className="text-accent" />}
          </button>
        </div>
      </div>
      <div className="text-xs text-muted font-mono mt-2 space-y-1">
        <div>Last: {state.last_run ? formatDistanceToNow(new Date(state.last_run)) + ' ago' : 'Never'}</div>
        <div>Next: {state.next_run ? formatDistanceToNow(new Date(state.next_run)) : '—'}</div>
        <div className="uppercase text-xs">Status: {status}</div>
      </div>
    </div>
  );
}
