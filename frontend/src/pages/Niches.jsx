import React, { useState, useEffect } from 'react';
import { niches as nichesApi } from '../api.js';
import { useStore } from '../store.js';
import { Plus, Edit2, Trash2, Layers, Power } from 'lucide-react';
import Modal from '../components/Modal.jsx';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

const PLATFORM_OPTIONS = ['instagram', 'tiktok', 'youtube', 'twitter', 'linkedin', 'facebook'];
const TONE_OPTIONS = ['engaging', 'professional', 'humorous', 'educational', 'inspirational', 'authoritative'];

const EMPTY_FORM = {
  name: '',
  description: '',
  keywords: [],
  hashtags: [],
  target_platforms: ['instagram', 'twitter'],
  posting_frequency: 3,
  content_tone: 'engaging',
  target_audience: '',
  brand_voice: '',
};

export default function Niches() {
  const navigate = useNavigate();
  const niches = useStore(s => s.niches);
  const setNiches = useStore(s => s.setNiches);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [keywordInput, setKeywordInput] = useState('');
  const [hashtagInput, setHashtagInput] = useState('');

  async function loadNiches() {
    try {
      const data = await nichesApi.list();
      setNiches(data);
    } catch (e) {
      console.error('Failed to load niches:', e);
    }
  }

  useEffect(() => { loadNiches(); }, []);

  function openCreate() {
    setEditing(null);
    setForm(EMPTY_FORM);
    setKeywordInput('');
    setHashtagInput('');
    setModalOpen(true);
  }

  function openEdit(niche) {
    setEditing(niche);
    setForm({
      name: niche.name || '',
      description: niche.description || '',
      keywords: niche.keywords || [],
      hashtags: niche.hashtags || [],
      target_platforms: niche.target_platforms || [],
      posting_frequency: niche.posting_frequency || 3,
      content_tone: niche.content_tone || 'engaging',
      target_audience: niche.target_audience || '',
      brand_voice: niche.brand_voice || '',
    });
    setModalOpen(true);
  }

  async function handleSave() {
    if (!form.name.trim()) {
      toast.error('Name is required');
      return;
    }
    try {
      if (editing) {
        await nichesApi.update(editing.id, form);
        toast.success('Niche updated');
      } else {
        await nichesApi.create(form);
        toast.success('Niche created');
      }
      setModalOpen(false);
      loadNiches();
    } catch (e) {
      toast.error('Save failed');
    }
  }

  async function handleDelete(niche) {
    if (!confirm(`Delete niche "${niche.name}"? This will also delete all associated content.`)) return;
    try {
      await nichesApi.delete(niche.id);
      toast.success('Niche deleted');
      loadNiches();
    } catch (e) {
      toast.error('Delete failed');
    }
  }

  async function handleToggleActive(niche) {
    try {
      await nichesApi.update(niche.id, { active: !niche.active });
      toast.success(niche.active ? 'Niche paused' : 'Niche activated');
      loadNiches();
    } catch (e) {
      toast.error('Failed to toggle');
    }
  }

  function addKeyword() {
    const k = keywordInput.trim();
    if (k && !form.keywords.includes(k)) {
      setForm({ ...form, keywords: [...form.keywords, k] });
      setKeywordInput('');
    }
  }

  function removeKeyword(k) {
    setForm({ ...form, keywords: form.keywords.filter(x => x !== k) });
  }

  function addHashtag() {
    let h = hashtagInput.trim();
    if (h && !h.startsWith('#')) h = '#' + h;
    if (h && h.length > 1 && !form.hashtags.includes(h)) {
      setForm({ ...form, hashtags: [...form.hashtags, h] });
      setHashtagInput('');
    }
  }

  function removeHashtag(h) {
    setForm({ ...form, hashtags: form.hashtags.filter(x => x !== h) });
  }

  function togglePlatform(p) {
    if (form.target_platforms.includes(p)) {
      setForm({ ...form, target_platforms: form.target_platforms.filter(x => x !== p) });
    } else {
      setForm({ ...form, target_platforms: [...form.target_platforms, p] });
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-mono text-xl font-medium">Niches</h1>
          <p className="text-muted text-sm font-mono mt-1">Configure your content focus areas</p>
        </div>
        <button
          onClick={openCreate}
          className="px-4 py-2 bg-accent-muted text-accent border border-accent/20 rounded-lg font-mono text-xs flex items-center gap-2"
        >
          <Plus size={14} /> Create Niche
        </button>
      </div>

      {niches.length === 0 ? (
        <div className="bg-dark-800 border border-dark-600 rounded-lg p-12 text-center">
          <Layers size={32} className="text-muted mx-auto mb-3" />
          <p className="text-muted font-mono text-sm">No niches yet. Create your first to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {niches.map(niche => (
            <div
              key={niche.id}
              className="bg-dark-800 border border-dark-600 rounded-lg p-5 hover:border-dark-400 transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1 cursor-pointer" onClick={() => navigate(`/content?niche=${niche.id}`)}>
                  <h3 className="font-mono text-base font-medium text-white">{niche.name}</h3>
                  {niche.description && <p className="text-xs text-muted font-mono mt-1 line-clamp-2">{niche.description}</p>}
                </div>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => handleToggleActive(niche)}
                    className={`p-1.5 rounded hover:bg-dark-600 ${niche.active ? 'text-accent' : 'text-muted'}`}
                    title={niche.active ? 'Active' : 'Inactive'}
                  >
                    <Power size={12} />
                  </button>
                  <button
                    onClick={() => openEdit(niche)}
                    className="p-1.5 rounded hover:bg-dark-600 text-info"
                  >
                    <Edit2 size={12} />
                  </button>
                  <button
                    onClick={() => handleDelete(niche)}
                    className="p-1.5 rounded hover:bg-dark-600 text-danger"
                  >
                    <Trash2 size={12} />
                  </button>
                </div>
              </div>

              <div className="space-y-2 text-xs font-mono">
                <div className="flex flex-wrap gap-1">
                  {(niche.target_platforms || []).map(p => (
                    <span key={p} className="px-2 py-0.5 bg-dark-600 text-muted rounded uppercase text-xs">{p}</span>
                  ))}
                </div>
                <div className="flex flex-wrap gap-1 mt-2">
                  {(niche.keywords || []).slice(0, 5).map(k => (
                    <span key={k} className="px-2 py-0.5 bg-info/10 text-info rounded text-xs">{k}</span>
                  ))}
                  {(niche.keywords || []).length > 5 && (
                    <span className="px-2 py-0.5 text-muted text-xs">+{niche.keywords.length - 5} more</span>
                  )}
                </div>
                <div className="text-muted text-xs mt-2 flex items-center gap-3">
                  <span>{niche.posting_frequency} posts/day</span>
                  <span>•</span>
                  <span>Tone: {niche.content_tone}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? 'Edit Niche' : 'Create Niche'}
        maxWidth="max-w-3xl"
      >
        <div className="space-y-4 font-mono text-xs">
          <div>
            <label className="block text-muted mb-1">Name *</label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              placeholder="e.g., Fitness, Tech Reviews, Cooking"
            />
          </div>

          <div>
            <label className="block text-muted mb-1">Description</label>
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white h-20"
              placeholder="A brief description of this niche"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-muted mb-1">Keywords</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                  className="flex-1 px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
                  placeholder="Add keyword"
                />
                <button onClick={addKeyword} className="px-3 py-2 bg-info/10 text-info border border-info/20 rounded">+</button>
              </div>
              <div className="flex flex-wrap gap-1">
                {form.keywords.map(k => (
                  <span key={k} className="px-2 py-0.5 bg-info/10 text-info rounded text-xs flex items-center gap-1">
                    {k}
                    <button onClick={() => removeKeyword(k)} className="hover:text-danger">×</button>
                  </span>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-muted mb-1">Hashtags</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={hashtagInput}
                  onChange={(e) => setHashtagInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addHashtag())}
                  className="flex-1 px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
                  placeholder="#example"
                />
                <button onClick={addHashtag} className="px-3 py-2 bg-warn/10 text-warn border border-warn/20 rounded">+</button>
              </div>
              <div className="flex flex-wrap gap-1">
                {form.hashtags.map(h => (
                  <span key={h} className="px-2 py-0.5 bg-warn/10 text-warn rounded text-xs flex items-center gap-1">
                    {h}
                    <button onClick={() => removeHashtag(h)} className="hover:text-danger">×</button>
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div>
            <label className="block text-muted mb-1">Target Platforms</label>
            <div className="grid grid-cols-3 gap-2">
              {PLATFORM_OPTIONS.map(p => (
                <label key={p} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={form.target_platforms.includes(p)}
                    onChange={() => togglePlatform(p)}
                    className="rounded"
                  />
                  <span className="capitalize">{p}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-muted mb-1">Posts per day</label>
              <input
                type="number"
                min="1"
                max="50"
                value={form.posting_frequency}
                onChange={(e) => setForm({ ...form, posting_frequency: parseInt(e.target.value) || 3 })}
                className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              />
            </div>
            <div>
              <label className="block text-muted mb-1">Content Tone</label>
              <select
                value={form.content_tone}
                onChange={(e) => setForm({ ...form, content_tone: e.target.value })}
                className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              >
                {TONE_OPTIONS.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-muted mb-1">Target Audience</label>
            <input
              type="text"
              value={form.target_audience}
              onChange={(e) => setForm({ ...form, target_audience: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              placeholder="e.g., Adults 25-40 interested in fitness"
            />
          </div>

          <div>
            <label className="block text-muted mb-1">Brand Voice</label>
            <textarea
              value={form.brand_voice}
              onChange={(e) => setForm({ ...form, brand_voice: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white h-20"
              placeholder="Describe your brand's voice and personality"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              onClick={() => setModalOpen(false)}
              className="px-4 py-2 bg-dark-700 text-muted rounded font-mono text-xs"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-accent-muted text-accent border border-accent/20 rounded font-mono text-xs"
            >
              {editing ? 'Save Changes' : 'Create Niche'}
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
