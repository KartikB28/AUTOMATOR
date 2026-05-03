import React, { useState, useEffect } from 'react';
import { bots as botsApi } from '../api.js';
import { Play, Pause, RefreshCw, ChevronDown, ChevronRight, CheckCircle, XCircle } from 'lucide-react';
import StatusDot from '../components/StatusDot.jsx';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

const BOT_CONFIGS = {
  scout: {
    label: 'Scout Bot',
    desc: 'Discovers trending topics from Google Trends, Reddit, Twitter, TikTok, YouTube, RSS feeds',
    interval: 'Every 2 hours',
    color: 'text-info'
  },
  builder: {
    label: 'Builder Bot',
    desc: 'Generates platform-specific content with hooks, captions, scripts, hashtags using Claude AI',
    interval: 'Every 1 hour',
    color: 'text-white'
  },
  creator: {
    label: 'Creator Bot',
    desc: 'Creates visuals via DALL-E 3, Stability AI, Pexels, Unsplash with branded thumbnails',
    interval: 'Every 1 hour',
    color: 'text-warn'
  },
  publisher: {
    label: 'Publisher Bot',
    desc: 'Posts to all platforms at scheduled times, handles rate limits and retries',
    interval: 'Every 15 minutes',
    color: 'text-accent'
  },
  analyst: {
    label: 'Analyst Bot',
    desc: 'Pulls metrics, calculates engagement, generates AI-powered weekly digests',
    interval: 'Every 6 hours',
    color: 'text-muted'
  },
};

export default function Bots() {
  const [botStatus, setBotStatus] = useState({});
  const [runs, setRuns] = useState({});
  const [expanded, setExpanded] = useState({});

  async function loadAll() {
    try {
      const status = await botsApi.getStatus();
      setBotStatus(status);
      const allRuns = {};
      for (const name of Object.keys(BOT_CONFIGS)) {
        try {
          allRuns[name] = await botsApi.getRuns(name, 20);
        } catch (e) {
          allRuns[name] = [];
        }
      }
      setRuns(allRuns);
    } catch (e) {
      console.error('Failed to load bots:', e);
    }
  }

  useEffect(() => {
    loadAll();
    const interval = setInterval(loadAll, 5000);
    return () => clearInterval(interval);
  }, []);

  async function handleRun(name) {
    try {
      await botsApi.trigger(name);
      toast.success(`${BOT_CONFIGS[name].label} triggered`);
      setTimeout(loadAll, 1000);
    } catch (e) {
      toast.error('Failed to trigger bot');
    }
  }

  async function handleToggle(name) {
    const state = botStatus[name];
    try {
      if (state?.enabled) {
        await botsApi.pause(name);
        toast.success(`${BOT_CONFIGS[name].label} paused`);
      } else {
        await botsApi.resume(name);
        toast.success(`${BOT_CONFIGS[name].label} resumed`);
      }
      loadAll();
    } catch (e) {
      toast.error('Failed to toggle bot');
    }
  }

  async function handlePauseAll() {
    try {
      await botsApi.pauseAll();
      toast.success('All bots paused');
      loadAll();
    } catch (e) {
      toast.error('Failed to pause');
    }
  }

  async function handleResumeAll() {
    try {
      await botsApi.resumeAll();
      toast.success('All bots resumed');
      loadAll();
    } catch (e) {
      toast.error('Failed to resume');
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-mono text-xl font-medium">Bots</h1>
          <p className="text-muted text-sm font-mono mt-1">Autonomous worker control panel</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handlePauseAll}
            className="px-4 py-2 bg-dark-700 hover:bg-dark-600 text-warn rounded-lg font-mono text-xs flex items-center gap-2"
          >
            <Pause size={12} /> Pause All
          </button>
          <button
            onClick={handleResumeAll}
            className="px-4 py-2 bg-dark-700 hover:bg-dark-600 text-accent rounded-lg font-mono text-xs flex items-center gap-2"
          >
            <Play size={12} /> Resume All
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {Object.entries(BOT_CONFIGS).map(([name, config]) => {
          const state = botStatus[name] || {};
          const botRuns = runs[name] || [];
          const status = state.status || 'idle';
          const isExpanded = expanded[name];

          const lastRun = botRuns[0];

          return (
            <div key={name} className="bg-dark-800 border border-dark-600 rounded-lg overflow-hidden">
              <div className="p-5">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    <StatusDot status={status} size="lg" />
                    <div className="flex-1">
                      <h3 className={`font-mono text-base font-medium ${config.color}`}>{config.label}</h3>
                      <p className="text-xs text-muted font-mono mt-1">{config.desc}</p>
                      <div className="flex items-center gap-4 mt-3 text-xs font-mono text-muted">
                        <span>Schedule: {config.interval}</span>
                        <span>Last: {state.last_run ? formatDistanceToNow(new Date(state.last_run)) + ' ago' : 'Never'}</span>
                        <span>Next: {state.next_run ? formatDistanceToNow(new Date(state.next_run)) : '—'}</span>
                      </div>
                      {lastRun && (
                        <div className="text-xs text-muted font-mono mt-2">
                          Last run: {lastRun.items_succeeded}/{lastRun.items_processed} succeeded
                          {lastRun.items_failed > 0 && <span className="text-danger"> ({lastRun.items_failed} failed)</span>}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleToggle(name)}
                      className="px-3 py-2 bg-dark-700 hover:bg-dark-600 rounded font-mono text-xs flex items-center gap-1"
                    >
                      {state.enabled !== false
                        ? <><Pause size={12} className="text-warn" /> Pause</>
                        : <><Play size={12} className="text-accent" /> Resume</>}
                    </button>
                    <button
                      onClick={() => handleRun(name)}
                      disabled={status === 'running'}
                      className="px-3 py-2 bg-accent-muted text-accent border border-accent/20 rounded font-mono text-xs flex items-center gap-1 disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                      {status === 'running'
                        ? <><RefreshCw size={12} className="animate-spin" /> Running</>
                        : <><Play size={12} /> Run Now</>}
                    </button>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setExpanded({ ...expanded, [name]: !isExpanded })}
                className="w-full px-5 py-2 bg-dark-700 hover:bg-dark-600 border-t border-dark-600 flex items-center gap-2 text-xs font-mono text-muted"
              >
                {isExpanded ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                Run History ({botRuns.length})
              </button>

              {isExpanded && (
                <div className="border-t border-dark-600 max-h-96 overflow-y-auto">
                  {botRuns.length === 0 ? (
                    <div className="p-4 text-center text-muted text-xs font-mono">No runs yet</div>
                  ) : (
                    <table className="w-full text-xs font-mono">
                      <thead className="bg-dark-700 sticky top-0">
                        <tr>
                          <th className="px-4 py-2 text-left text-muted">Status</th>
                          <th className="px-4 py-2 text-left text-muted">Started</th>
                          <th className="px-4 py-2 text-right text-muted">Processed</th>
                          <th className="px-4 py-2 text-right text-muted">Succeeded</th>
                          <th className="px-4 py-2 text-right text-muted">Failed</th>
                        </tr>
                      </thead>
                      <tbody>
                        {botRuns.map(run => (
                          <tr key={run.id} className="border-t border-dark-700">
                            <td className="px-4 py-2">
                              {run.status === 'completed'
                                ? <CheckCircle size={12} className="text-accent inline" />
                                : run.status === 'failed'
                                ? <XCircle size={12} className="text-danger inline" />
                                : <RefreshCw size={12} className="animate-spin text-warn inline" />}
                              <span className="ml-2">{run.status}</span>
                            </td>
                            <td className="px-4 py-2 text-muted">
                              {run.started_at ? formatDistanceToNow(new Date(run.started_at)) + ' ago' : '—'}
                            </td>
                            <td className="px-4 py-2 text-right">{run.items_processed}</td>
                            <td className="px-4 py-2 text-right text-accent">{run.items_succeeded}</td>
                            <td className="px-4 py-2 text-right text-danger">{run.items_failed}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
