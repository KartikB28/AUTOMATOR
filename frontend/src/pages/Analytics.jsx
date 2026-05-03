import React, { useState, useEffect } from 'react';
import { analytics as analyticsApi } from '../api.js';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import { Eye, Heart, Users, TrendingUp, RefreshCw, FileText } from 'lucide-react';
import { getMediaUrl } from '../api.js';
import toast from 'react-hot-toast';

const RANGES = [
  { label: '7 Days', value: 7 },
  { label: '30 Days', value: 30 },
  { label: '90 Days', value: 90 },
];

export default function Analytics() {
  const [range, setRange] = useState(30);
  const [overview, setOverview] = useState(null);
  const [timeseries, setTimeseries] = useState([]);
  const [digest, setDigest] = useState(null);

  async function load() {
    try {
      const [o, ts, d] = await Promise.all([
        analyticsApi.overview(range),
        analyticsApi.timeseries('views', range),
        analyticsApi.digest(),
      ]);
      setOverview(o);
      setTimeseries(ts);
      setDigest(d);
    } catch (e) {
      console.error('Failed to load analytics:', e);
    }
  }

  useEffect(() => { load(); }, [range]);

  const platformData = overview ? Object.entries(overview.by_platform || {}).map(([platform, d]) => ({
    platform: platform.charAt(0).toUpperCase() + platform.slice(1),
    likes: d.likes || 0,
    views: d.views || 0,
    posts: d.posts || 0,
  })) : [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-mono text-xl font-medium">Analytics</h1>
          <p className="text-muted text-sm font-mono mt-1">Performance insights across all platforms</p>
        </div>
        <div className="flex gap-1 bg-dark-700 p-1 rounded-lg">
          {RANGES.map(r => (
            <button
              key={r.value}
              onClick={() => setRange(r.value)}
              className={`px-3 py-1.5 rounded font-mono text-xs ${
                range === r.value ? 'bg-accent-muted text-accent' : 'text-muted hover:text-white'
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-dark-700 border border-dark-500 rounded-lg p-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono text-muted">TOTAL POSTS</span>
            <FileText size={14} className="text-info" />
          </div>
          <div className="text-3xl font-mono font-medium text-white">
            {(overview?.total_posts || 0).toLocaleString()}
          </div>
        </div>
        <div className="bg-dark-700 border border-dark-500 rounded-lg p-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono text-muted">TOTAL VIEWS</span>
            <Eye size={14} className="text-info" />
          </div>
          <div className="text-3xl font-mono font-medium text-info">
            {(overview?.total_views || 0).toLocaleString()}
          </div>
        </div>
        <div className="bg-dark-700 border border-dark-500 rounded-lg p-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono text-muted">TOTAL LIKES</span>
            <Heart size={14} className="text-danger" />
          </div>
          <div className="text-3xl font-mono font-medium text-danger">
            {(overview?.total_likes || 0).toLocaleString()}
          </div>
        </div>
        <div className="bg-dark-700 border border-dark-500 rounded-lg p-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono text-muted">AVG ENGAGEMENT</span>
            <TrendingUp size={14} className="text-accent" />
          </div>
          <div className="text-3xl font-mono font-medium text-accent">
            {(overview?.avg_engagement_rate || 0).toFixed(2)}%
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-dark-800 border border-dark-600 rounded-lg p-4">
          <div className="text-xs font-mono text-muted mb-3">VIEWS OVER TIME</div>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={timeseries}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="date" tick={{ fill: '#666', fontSize: 10 }} />
              <YAxis tick={{ fill: '#666', fontSize: 10 }} />
              <Tooltip
                contentStyle={{ background: '#1a1a1a', border: '1px solid #333', fontSize: 12 }}
                labelStyle={{ color: '#888' }}
              />
              <Line type="monotone" dataKey="value" stroke="#00ff88" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-dark-800 border border-dark-600 rounded-lg p-4">
          <div className="text-xs font-mono text-muted mb-3">PERFORMANCE BY PLATFORM</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={platformData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="platform" tick={{ fill: '#666', fontSize: 10 }} />
              <YAxis tick={{ fill: '#666', fontSize: 10 }} />
              <Tooltip
                contentStyle={{ background: '#1a1a1a', border: '1px solid #333', fontSize: 12 }}
                labelStyle={{ color: '#888' }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="likes" fill="#ff4444" />
              <Bar dataKey="views" fill="#4488ff" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg">
        <div className="p-4 border-b border-dark-600">
          <span className="font-mono text-xs text-muted">TOP CONTENT BY ENGAGEMENT</span>
        </div>
        <div className="p-4 grid grid-cols-5 gap-3">
          {overview?.top_content?.length > 0 ? (
            overview.top_content.map(c => (
              <div key={c.content_id} className="bg-dark-700 rounded-lg overflow-hidden">
                <div className="aspect-square bg-dark-600">
                  {c.thumbnail_path && (
                    <img
                      src={getMediaUrl(c.thumbnail_path)}
                      alt={c.topic}
                      className="w-full h-full object-cover"
                      onError={(e) => { e.target.style.display = 'none'; }}
                    />
                  )}
                </div>
                <div className="p-2">
                  <div className="text-xs font-mono text-white truncate" title={c.topic}>{c.topic}</div>
                  <div className="text-xs font-mono text-muted mt-1 capitalize">{c.platform}</div>
                  <div className="text-xs font-mono text-accent mt-1">{c.engagement_rate?.toFixed(2)}% engagement</div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-5 text-center text-muted text-xs font-mono py-8">
              No data yet. Posts will appear here after the Analyst Bot runs.
            </div>
          )}
        </div>
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg">
        <div className="p-4 border-b border-dark-600 flex items-center justify-between">
          <span className="font-mono text-xs text-muted">WEEKLY AI DIGEST</span>
          <button
            onClick={load}
            className="p-1.5 rounded bg-dark-700 hover:bg-dark-600 text-muted"
          >
            <RefreshCw size={12} />
          </button>
        </div>
        <div className="p-4">
          {digest?.digest ? (
            <pre className="text-xs font-mono text-white whitespace-pre-wrap leading-relaxed">{digest.digest}</pre>
          ) : (
            <div className="text-muted text-xs font-mono">
              No digest available yet. The Analyst Bot generates a weekly digest every Monday morning.
            </div>
          )}
          {digest?.updated_at && (
            <div className="text-xs text-muted font-mono mt-3 pt-3 border-t border-dark-700">
              Generated: {new Date(digest.updated_at).toLocaleString()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
