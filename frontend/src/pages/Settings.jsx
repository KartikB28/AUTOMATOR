import React, { useState, useEffect } from 'react';
import { settings as settingsApi, content as contentApi } from '../api.js';
import { CheckCircle, XCircle, ExternalLink, FolderOpen, AlertTriangle } from 'lucide-react';
import StatusDot from '../components/StatusDot.jsx';
import toast from 'react-hot-toast';

const SERVICES = [
  {
    key: 'has_anthropic',
    label: 'Anthropic (Claude)',
    desc: 'Required for content generation',
    url: 'https://console.anthropic.com/',
    required: true,
  },
  {
    key: 'has_openai',
    label: 'OpenAI (DALL-E 3)',
    desc: 'Optional - primary image generation',
    url: 'https://platform.openai.com/api-keys',
    required: false,
  },
  {
    key: 'has_stability',
    label: 'Stability AI',
    desc: 'Optional - fallback image generation',
    url: 'https://platform.stability.ai/account/keys',
    required: false,
  },
  {
    key: 'has_pexels',
    label: 'Pexels',
    desc: 'Optional - free stock photos',
    url: 'https://www.pexels.com/api/',
    required: false,
  },
  {
    key: 'has_unsplash',
    label: 'Unsplash',
    desc: 'Optional - free stock photos',
    url: 'https://unsplash.com/developers',
    required: false,
  },
  {
    key: 'has_instagram',
    label: 'Instagram',
    desc: 'For posting to Instagram (Business Account required)',
    url: 'https://developers.facebook.com/apps/',
    required: false,
  },
  {
    key: 'has_tiktok',
    label: 'TikTok',
    desc: 'For posting to TikTok',
    url: 'https://developers.tiktok.com/',
    required: false,
  },
  {
    key: 'has_youtube',
    label: 'YouTube',
    desc: 'For posting YouTube Shorts',
    url: 'https://console.cloud.google.com/',
    required: false,
  },
  {
    key: 'has_twitter',
    label: 'Twitter / X',
    desc: 'For posting tweets',
    url: 'https://developer.twitter.com/',
    required: false,
  },
  {
    key: 'has_linkedin',
    label: 'LinkedIn',
    desc: 'For posting to LinkedIn',
    url: 'https://www.linkedin.com/developers/apps',
    required: false,
  },
  {
    key: 'has_facebook',
    label: 'Facebook',
    desc: 'For posting to Facebook Pages',
    url: 'https://developers.facebook.com/apps/',
    required: false,
  },
  {
    key: 'has_supabase',
    label: 'Supabase',
    desc: 'Optional - cloud sync of data',
    url: 'https://supabase.com/',
    required: false,
  },
];

export default function Settings() {
  const [config, setConfig] = useState(null);
  const [envPath, setEnvPath] = useState(null);

  async function load() {
    try {
      const [c, p] = await Promise.all([
        settingsApi.get(),
        settingsApi.getEnvPath(),
      ]);
      setConfig(c);
      setEnvPath(p);
    } catch (e) {
      console.error('Failed to load settings:', e);
    }
  }

  useEffect(() => { load(); }, []);

  function openEnvFile() {
    if (envPath?.path && window.electron) {
      window.electron.openExternalLink('file://' + envPath.path);
    } else if (envPath?.path) {
      navigator.clipboard?.writeText(envPath.path);
      toast.success('Path copied to clipboard');
    }
  }

  function openDocsUrl(url) {
    if (window.electron) {
      window.electron.openExternalLink(url);
    } else {
      window.open(url, '_blank');
    }
  }

  async function handleClearAllData() {
    if (!confirm('This will delete ALL content (not niches). Continue?')) return;
    if (!confirm('Are you absolutely sure? This cannot be undone.')) return;
    try {
      const items = await contentApi.list({ limit: 200 });
      for (const item of items) {
        await contentApi.delete(item.id);
      }
      toast.success('All content data cleared');
    } catch (e) {
      toast.error('Clear failed');
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-mono text-xl font-medium">Settings</h1>
        <p className="text-muted text-sm font-mono mt-1">API connections and system configuration</p>
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg">
        <div className="p-4 border-b border-dark-600">
          <span className="font-mono text-xs text-muted">.ENV FILE LOCATION</span>
        </div>
        <div className="p-4">
          <div className="flex items-center gap-3">
            <div className="flex-1 px-3 py-2 bg-dark-700 border border-dark-500 rounded font-mono text-xs text-white truncate">
              {envPath?.path || 'Loading...'}
            </div>
            <button
              onClick={openEnvFile}
              className="px-3 py-2 bg-info/10 text-info border border-info/20 rounded font-mono text-xs flex items-center gap-1"
            >
              <FolderOpen size={12} /> Open
            </button>
          </div>
          <div className="mt-2 flex items-center gap-2 text-xs font-mono">
            <StatusDot status={envPath?.exists ? 'ok' : 'error'} />
            <span className="text-muted">
              {envPath?.exists ? 'File exists' : 'File missing - copy .env.example to .env'}
            </span>
          </div>
        </div>
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg">
        <div className="p-4 border-b border-dark-600">
          <span className="font-mono text-xs text-muted">API CONNECTION STATUS</span>
        </div>
        <div className="divide-y divide-dark-700">
          {SERVICES.map(svc => {
            const connected = config?.[svc.key];
            return (
              <div key={svc.key} className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-3 flex-1">
                  {connected
                    ? <CheckCircle size={16} className="text-accent flex-shrink-0" />
                    : <XCircle size={16} className="text-muted flex-shrink-0" />}
                  <div className="flex-1">
                    <div className="font-mono text-sm text-white flex items-center gap-2">
                      {svc.label}
                      {svc.required && !connected && (
                        <span className="text-xs px-2 py-0.5 bg-danger/10 text-danger rounded">REQUIRED</span>
                      )}
                    </div>
                    <div className="text-xs text-muted font-mono">{svc.desc}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs font-mono uppercase ${connected ? 'text-accent' : 'text-muted'}`}>
                    {connected ? 'Connected' : 'Not Configured'}
                  </span>
                  <button
                    onClick={() => openDocsUrl(svc.url)}
                    className="p-1.5 rounded bg-dark-700 hover:bg-dark-600 text-muted"
                    title="Open developer portal"
                  >
                    <ExternalLink size={12} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg p-4">
        <div className="text-xs font-mono text-muted mb-2">SYSTEM PATHS</div>
        <div className="grid grid-cols-2 gap-3 text-xs font-mono">
          <div>
            <div className="text-muted">App Data:</div>
            <div className="text-white truncate">{config?.app_data_path || '—'}</div>
          </div>
          <div>
            <div className="text-muted">Media Path:</div>
            <div className="text-white truncate">{config?.media_path || '—'}</div>
          </div>
        </div>
      </div>

      <div className="bg-danger/5 border border-danger/20 rounded-lg p-4">
        <div className="flex items-center gap-2 mb-2">
          <AlertTriangle size={14} className="text-danger" />
          <span className="font-mono text-xs text-danger">DANGER ZONE</span>
        </div>
        <p className="text-xs text-muted font-mono mb-3">
          Permanently delete all content data. Niches, schedules, and settings will be preserved.
        </p>
        <button
          onClick={handleClearAllData}
          className="px-4 py-2 bg-danger/10 text-danger border border-danger/20 rounded font-mono text-xs"
        >
          Clear All Content Data
        </button>
      </div>
    </div>
  );
}
