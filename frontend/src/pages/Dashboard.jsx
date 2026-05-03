import React, { useState, useEffect } from 'react';
import { bots as botsApi, content as contentApi, system } from '../api.js';
import { Play, RefreshCw, Activity, CheckCircle, XCircle, Clock } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

const BOT_CONFIGS = {
  scout: { label: 'Scout Bot', desc: 'Trend hunting', color: 'text-info' },
  builder: { label: 'Builder Bot', desc: 'Content generation', color: 'text-white' },
  creator: { label: 'Creator Bot', desc: 'Media generation', color: 'text-warn' },
  publisher: { label: 'Publisher Bot', desc: '24/7 posting', color: 'text-accent' },
  analyst: { label: 'Analyst Bot', desc: 'Performance tracking', color: 'text-muted' },
};

export default function Dashboard() {
  const [botStatus, setBotStatus] = useState({});
  const [botRuns, setBotRuns] = useState([]);
  const [contentStats, setContentStats] = useState({});
  const [sysStats, setSysStats] = useState({});
  const [loading, setLoading] = useState(true);

  async function loadAll() {
    try {
      const [bs, runs, cs, ss] = await Promise.all([
        botsApi.getStatus(),
        botsApi.getRuns(null, 10),
        contentApi.stats(),
        system.stats()
      ]);
      setBotStatus(bs);
      setBotRuns(runs);
      setContentStats(cs);
      setSysStats(ss);
    } catch (e) {
      console.error('Dashboard load failed:', e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAll();
    const interval = setInterval(loadAll, 10000);
    return () => clearInterval(interval);
  }, []);

  async function handleRunBot(name) {
    try {
      await botsApi.trigger(name);
      toast.success(`${BOT_CONFIGS[name].label} triggered`);
      setTimeout(loadAll, 1000);
    } catch (e) {
      toast.error(`Failed to trigger bot: ${e}`);
    }
  }

  const statusColors = {
    idle: 'text-muted',
    running: 'text-accent',
    error: 'text-danger',
    paused: 'text-warn',
  };

  const byStatus = contentStats.by_status || {};
  const pipelineStages = [
    { label: 'Pending', value: byStatus.pending || 0, color: 'bg-muted' },
    { label: 'Building', value: byStatus.building || 0, color: 'bg-info' },
    { label: 'Media Ready', value: (byStatus.media_ready || 0) + (byStatus.media_pending || 0), color: 'bg-warn' },
    { label: 'Posted', value: byStatus.posted || 0, color: 'bg-accent' },
    { label: 'Failed', value: byStatus.failed || 0, color: 'bg-danger' },
  ];

  if (loading) return <div className="text-muted font-mono text-sm p-8">Initializing...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-mono text-xl font-medium">Command Center</h1>
        <p className="text-muted text-sm font-mono mt-1">System overview - auto-refreshing every 10s</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'POSTED', value: sysStats.posted_content || 0, color: 'text-accent' },
          { label: 'PENDING', value: sysStats.pending_content || 0, color: 'text-warn' },
          { label: 'NICHES', value: sysStats.niches || 0, color: 'text-info' },
          { label: 'TOTAL CONTENT', value: sysStats.total_content || 0, color: 'text-white' },
        ].map(card => (
          <div key={card.label} className="bg-dark-700 border border-dark-500 rounded-lg p-4">
            <div className="text-xs font-mono text-muted mb-1">{card.label}</div>
            <div className={`text-3xl font-mono font-medium ${card.color}`}>{card.value.toLocaleString()}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-dark-800 border border-dark-600 rounded-lg">
          <div className="p-4 border-b border-dark-600 flex items-center gap-2">
            <Activity size={14} className="text-accent" />
            <span className="font-mono text-sm font-medium">BOT STATUS</span>
          </div>
          <div className="divide-y divide-dark-600">
            {Object.entries(BOT_CONFIGS).map(([name, config]) => {
              const state = botStatus[name] || {};
              const status = state.status || 'idle';
              return (
                <div key={name} className="p-4 flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-mono ${statusColors[status] || 'text-muted'}`}>*</span>
                      <span className={`font-mono text-sm ${config.color}`}>{config.label}</span>
                    </div>
                    <div className="text-xs text-muted font-mono mt-1">
                      {state.last_run ? `Last: ${formatDistanceToNow(new Date(state.last_run))} ago` : 'Never run'}
                      {state.next_run && ` - Next: ${formatDistanceToNow(new Date(state.next_run))}`}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-mono uppercase ${statusColors[status] || 'text-muted'}`}>{status}</span>
                    <button
                      onClick={() => handleRunBot(name)}
                      disabled={status === 'running'}
                      className="p-1.5 rounded bg-dark-600 hover:bg-dark-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                    >
                      {status === 'running'
                        ? <RefreshCw size={12} className="animate-spin text-accent" />
                        : <Play size={12} className="text-accent" />}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-dark-800 border border-dark-600 rounded-lg p-4">
            <div className="font-mono text-xs text-muted mb-3">CONTENT PIPELINE</div>
            <div className="space-y-2">
              {pipelineStages.map(stage => (
                <div key={stage.label} className="flex items-center gap-3">
                  <div className="text-xs font-mono text-muted w-20">{stage.label}</div>
                  <div className="flex-1 bg-dark-600 rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full ${stage.color}`}
                      style={{ width: `${Math.min(100, stage.value * 5)}%`, minWidth: stage.value > 0 ? '4px' : '0' }}
                    />
                  </div>
                  <div className="text-xs font-mono text-white w-8 text-right">{stage.value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-dark-800 border border-dark-600 rounded-lg">
            <div className="p-3 border-b border-dark-600">
              <span className="font-mono text-xs text-muted">RECENT BOT RUNS</span>
            </div>
            <div className="divide-y divide-dark-700 max-h-52 overflow-y-auto">
              {botRuns.slice(0, 8).map(run => (
                <div key={run.id} className="px-3 py-2 flex items-center gap-3">
                  {run.status === 'completed'
                    ? <CheckCircle size={12} className="text-accent flex-shrink-0" />
                    : run.status === 'failed'
                    ? <XCircle size={12} className="text-danger flex-shrink-0" />
                    : <Clock size={12} className="text-warn flex-shrink-0" />}
                  <div className="flex-1 min-w-0">
                    <span className="font-mono text-xs text-white">{run.bot_name}</span>
                    <span className="font-mono text-xs text-muted ml-2">{run.items_processed} items</span>
                  </div>
                  <div className="text-xs text-muted font-mono flex-shrink-0">
                    {run.started_at ? formatDistanceToNow(new Date(run.started_at)) + ' ago' : ''}
                  </div>
                </div>
              ))}
              {botRuns.length === 0 && (
                <div className="px-3 py-4 text-center text-muted text-xs font-mono">No runs yet</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
