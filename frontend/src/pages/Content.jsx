import React, { useState, useEffect } from 'react';
import { content as contentApi, niches as nichesApi } from '../api.js';
import { useStore } from '../store.js';
import ContentCard from '../components/ContentCard.jsx';
import Modal from '../components/Modal.jsx';
import { ChevronLeft, ChevronRight, ExternalLink, Trash2, Send } from 'lucide-react';
import toast from 'react-hot-toast';
import { useSearchParams } from 'react-router-dom';

const STATUS_OPTIONS = ['', 'pending', 'media_pending', 'media_ready', 'posting', 'posted', 'failed'];
const PLATFORMS = ['', 'instagram', 'tiktok', 'youtube', 'twitter', 'linkedin', 'facebook'];
const PAGE_SIZE = 50;

export default function Content() {
  const niches = useStore(s => s.niches);
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState({});
  const [filterNiche, setFilterNiche] = useState(searchParams.get('niche') || '');
  const [filterPlatform, setFilterPlatform] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [page, setPage] = useState(0);
  const [selected, setSelected] = useState(null);

  async function load() {
    try {
      const params = { limit: PAGE_SIZE, offset: page * PAGE_SIZE };
      if (filterNiche) params.niche_id = filterNiche;
      if (filterPlatform) params.platform = filterPlatform;
      if (filterStatus) params.status = filterStatus;
      const [data, s] = await Promise.all([contentApi.list(params), contentApi.stats()]);
      setItems(data);
      setStats(s);
    } catch (e) {
      console.error('Failed to load content:', e);
    }
  }

  useEffect(() => { load(); }, [filterNiche, filterPlatform, filterStatus, page]);

  async function handleDelete(id) {
    if (!confirm('Delete this content item?')) return;
    try {
      await contentApi.delete(id);
      toast.success('Deleted');
      setSelected(null);
      load();
    } catch (e) {
      toast.error('Delete failed');
    }
  }

  async function handlePostNow(item) {
    try {
      await contentApi.update(item.id, { status: 'media_ready' });
      toast.success('Marked for immediate posting');
      load();
    } catch (e) {
      toast.error('Failed to mark for posting');
    }
  }

  const byStatus = stats.by_status || {};

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-mono text-xl font-medium">Content Queue</h1>
        <p className="text-muted text-sm font-mono mt-1">{stats.total || 0} total items</p>
      </div>

      <div className="grid grid-cols-6 gap-3">
        {[
          { label: 'PENDING', value: byStatus.pending || 0, color: 'text-muted' },
          { label: 'BUILDING', value: (byStatus.building || 0) + (byStatus.media_pending || 0), color: 'text-info' },
          { label: 'READY', value: byStatus.media_ready || 0, color: 'text-warn' },
          { label: 'POSTING', value: byStatus.posting || 0, color: 'text-info' },
          { label: 'POSTED', value: byStatus.posted || 0, color: 'text-accent' },
          { label: 'FAILED', value: byStatus.failed || 0, color: 'text-danger' },
        ].map(s => (
          <div key={s.label} className="bg-dark-700 border border-dark-500 rounded p-3">
            <div className="text-xs font-mono text-muted">{s.label}</div>
            <div className={`text-2xl font-mono font-medium ${s.color}`}>{s.value}</div>
          </div>
        ))}
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg p-4">
        <div className="flex items-center gap-3 flex-wrap">
          <select
            value={filterNiche}
            onChange={(e) => { setFilterNiche(e.target.value); setPage(0); }}
            className="px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white font-mono text-xs"
          >
            <option value="">All Niches</option>
            {niches.map(n => <option key={n.id} value={n.id}>{n.name}</option>)}
          </select>
          <select
            value={filterPlatform}
            onChange={(e) => { setFilterPlatform(e.target.value); setPage(0); }}
            className="px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white font-mono text-xs capitalize"
          >
            {PLATFORMS.map(p => <option key={p} value={p}>{p || 'All Platforms'}</option>)}
          </select>
          <select
            value={filterStatus}
            onChange={(e) => { setFilterStatus(e.target.value); setPage(0); }}
            className="px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white font-mono text-xs capitalize"
          >
            {STATUS_OPTIONS.map(s => <option key={s} value={s}>{s || 'All Statuses'}</option>)}
          </select>
        </div>
      </div>

      {items.length === 0 ? (
        <div className="bg-dark-800 border border-dark-600 rounded-lg p-12 text-center">
          <p className="text-muted font-mono text-sm">No content found. Run the Builder Bot to generate content.</p>
        </div>
      ) : (
        <div className="grid grid-cols-4 gap-4">
          {items.map(item => (
            <ContentCard key={item.id} item={item} onClick={setSelected} />
          ))}
        </div>
      )}

      <div className="flex items-center justify-between font-mono text-xs">
        <button
          onClick={() => setPage(Math.max(0, page - 1))}
          disabled={page === 0}
          className="px-3 py-2 bg-dark-700 text-muted rounded flex items-center gap-1 disabled:opacity-40"
        >
          <ChevronLeft size={12} /> Previous
        </button>
        <span className="text-muted">Page {page + 1}</span>
        <button
          onClick={() => setPage(page + 1)}
          disabled={items.length < PAGE_SIZE}
          className="px-3 py-2 bg-dark-700 text-muted rounded flex items-center gap-1 disabled:opacity-40"
        >
          Next <ChevronRight size={12} />
        </button>
      </div>

      <Modal
        open={!!selected}
        onClose={() => setSelected(null)}
        title={selected ? selected.topic : ''}
        maxWidth="max-w-3xl"
      >
        {selected && (
          <div className="space-y-4 font-mono text-xs">
            <div className="grid grid-cols-3 gap-3">
              <div>
                <div className="text-muted">PLATFORM</div>
                <div className="text-white capitalize">{selected.platform}</div>
              </div>
              <div>
                <div className="text-muted">STATUS</div>
                <div className="text-white uppercase">{selected.status}</div>
              </div>
              <div>
                <div className="text-muted">TYPE</div>
                <div className="text-white capitalize">{selected.content_type}</div>
              </div>
            </div>

            {selected.hook && (
              <div>
                <div className="text-muted mb-1">HOOK</div>
                <div className="bg-dark-700 p-3 rounded text-white">{selected.hook}</div>
              </div>
            )}

            {selected.caption && (
              <div>
                <div className="text-muted mb-1">CAPTION</div>
                <div className="bg-dark-700 p-3 rounded text-white whitespace-pre-wrap max-h-48 overflow-y-auto">{selected.caption}</div>
              </div>
            )}

            {selected.script && (
              <div>
                <div className="text-muted mb-1">SCRIPT</div>
                <div className="bg-dark-700 p-3 rounded text-white whitespace-pre-wrap max-h-48 overflow-y-auto">{selected.script}</div>
              </div>
            )}

            {selected.hashtags && selected.hashtags.length > 0 && (
              <div>
                <div className="text-muted mb-1">HASHTAGS ({selected.hashtags.length})</div>
                <div className="flex flex-wrap gap-1">
                  {selected.hashtags.map(h => (
                    <span key={h} className="px-2 py-0.5 bg-warn/10 text-warn rounded text-xs">#{h.replace(/^#/, '')}</span>
                  ))}
                </div>
              </div>
            )}

            {selected.cta && (
              <div>
                <div className="text-muted mb-1">CALL TO ACTION</div>
                <div className="text-white">{selected.cta}</div>
              </div>
            )}

            {selected.error_message && (
              <div>
                <div className="text-danger mb-1">ERROR</div>
                <div className="bg-danger/10 border border-danger/20 p-3 rounded text-danger">{selected.error_message}</div>
              </div>
            )}

            {selected.post_url && (
              <div>
                <div className="text-muted mb-1">POSTED URL</div>
                <a
                  href={selected.post_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-accent flex items-center gap-1 hover:underline"
                >
                  {selected.post_url} <ExternalLink size={12} />
                </a>
              </div>
            )}

            <div className="flex gap-2 pt-4 border-t border-dark-600">
              {selected.status === 'media_ready' && (
                <button
                  onClick={() => handlePostNow(selected)}
                  className="px-4 py-2 bg-accent-muted text-accent border border-accent/20 rounded flex items-center gap-2"
                >
                  <Send size={12} /> Post Now
                </button>
              )}
              <button
                onClick={() => handleDelete(selected.id)}
                className="px-4 py-2 bg-danger/10 text-danger border border-danger/20 rounded flex items-center gap-2 ml-auto"
              >
                <Trash2 size={12} /> Delete
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
