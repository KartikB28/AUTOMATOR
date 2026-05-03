import React, { useState, useEffect } from 'react';
import { schedule as scheduleApi } from '../api.js';
import { useStore } from '../store.js';
import { Plus, X, Power } from 'lucide-react';
import Modal from '../components/Modal.jsx';
import toast from 'react-hot-toast';

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const PLATFORMS = ['instagram', 'tiktok', 'youtube', 'twitter', 'linkedin', 'facebook'];

export default function Schedule() {
  const niches = useStore(s => s.niches);
  const [selectedNiche, setSelectedNiche] = useState('');
  const [schedules, setSchedules] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({
    platform: 'instagram',
    day_of_week: '',
    hour: 12,
    minute: 0,
    timezone: 'UTC',
  });

  useEffect(() => {
    if (niches.length > 0 && !selectedNiche) {
      setSelectedNiche(niches[0].id);
    }
  }, [niches]);

  async function load() {
    if (!selectedNiche) { setSchedules([]); return; }
    try {
      const data = await scheduleApi.get(selectedNiche);
      setSchedules(data);
    } catch (e) {
      console.error('Failed to load schedules:', e);
    }
  }

  useEffect(() => { load(); }, [selectedNiche]);

  async function handleAddSlot() {
    try {
      await scheduleApi.create({
        niche_id: selectedNiche,
        platform: form.platform,
        day_of_week: form.day_of_week === '' ? null : parseInt(form.day_of_week),
        hour: parseInt(form.hour),
        minute: parseInt(form.minute),
        active: true,
        timezone: form.timezone,
      });
      toast.success('Schedule added');
      setModalOpen(false);
      load();
    } catch (e) {
      toast.error('Failed to add schedule');
    }
  }

  async function handleDelete(id) {
    try {
      await scheduleApi.delete(id);
      toast.success('Schedule removed');
      load();
    } catch (e) {
      toast.error('Delete failed');
    }
  }

  async function handleToggle(id) {
    try {
      await scheduleApi.toggle(id);
      load();
    } catch (e) {
      toast.error('Toggle failed');
    }
  }

  function getSlots(platform, day) {
    return schedules.filter(s =>
      s.platform === platform &&
      (s.day_of_week === day || s.day_of_week === null)
    );
  }

  function formatTime(s) {
    return `${String(s.hour).padStart(2, '0')}:${String(s.minute).padStart(2, '0')}`;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-mono text-xl font-medium">Schedule</h1>
          <p className="text-muted text-sm font-mono mt-1">When each niche posts to each platform</p>
        </div>
        <button
          onClick={() => selectedNiche && setModalOpen(true)}
          disabled={!selectedNiche}
          className="px-4 py-2 bg-accent-muted text-accent border border-accent/20 rounded-lg font-mono text-xs flex items-center gap-2 disabled:opacity-40"
        >
          <Plus size={14} /> Add Time Slot
        </button>
      </div>

      <div className="bg-dark-800 border border-dark-600 rounded-lg p-4">
        <label className="block text-muted text-xs font-mono mb-2">SELECT NICHE</label>
        <select
          value={selectedNiche}
          onChange={(e) => setSelectedNiche(e.target.value)}
          className="px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white font-mono text-xs"
        >
          <option value="">Select a niche...</option>
          {niches.map(n => <option key={n.id} value={n.id}>{n.name}</option>)}
        </select>
      </div>

      {selectedNiche && (
        <div className="bg-dark-800 border border-dark-600 rounded-lg overflow-hidden">
          <table className="w-full font-mono text-xs">
            <thead className="bg-dark-700 border-b border-dark-600">
              <tr>
                <th className="px-3 py-3 text-left text-muted">PLATFORM</th>
                {DAYS.map(day => (
                  <th key={day} className="px-2 py-3 text-center text-muted">{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {PLATFORMS.map(platform => (
                <tr key={platform} className="border-t border-dark-700">
                  <td className="px-3 py-3 capitalize text-white">{platform}</td>
                  {DAYS.map((day, idx) => {
                    const slots = getSlots(platform, idx);
                    return (
                      <td key={day} className="px-2 py-3 text-center">
                        <div className="flex flex-wrap gap-1 justify-center">
                          {slots.map(s => (
                            <div
                              key={s.id}
                              className={`px-2 py-0.5 rounded text-xs flex items-center gap-1 ${
                                s.active ? 'bg-accent-muted text-accent' : 'bg-dark-600 text-muted'
                              }`}
                            >
                              <span>{formatTime(s)}</span>
                              <button onClick={() => handleToggle(s.id)} className="hover:text-warn">
                                <Power size={9} />
                              </button>
                              <button onClick={() => handleDelete(s.id)} className="hover:text-danger">
                                <X size={9} />
                              </button>
                            </div>
                          ))}
                          {slots.length === 0 && <span className="text-muted">—</span>}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Add Time Slot">
        <div className="space-y-4 font-mono text-xs">
          <div>
            <label className="block text-muted mb-1">Platform</label>
            <select
              value={form.platform}
              onChange={(e) => setForm({ ...form, platform: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white capitalize"
            >
              {PLATFORMS.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-muted mb-1">Day</label>
            <select
              value={form.day_of_week}
              onChange={(e) => setForm({ ...form, day_of_week: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
            >
              <option value="">Every day</option>
              {DAYS.map((d, i) => <option key={d} value={i}>{d}</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-muted mb-1">Hour (0-23)</label>
              <input
                type="number"
                min="0" max="23"
                value={form.hour}
                onChange={(e) => setForm({ ...form, hour: e.target.value })}
                className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              />
            </div>
            <div>
              <label className="block text-muted mb-1">Minute (0-59)</label>
              <input
                type="number"
                min="0" max="59"
                value={form.minute}
                onChange={(e) => setForm({ ...form, minute: e.target.value })}
                className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              />
            </div>
          </div>
          <div>
            <label className="block text-muted mb-1">Timezone</label>
            <input
              type="text"
              value={form.timezone}
              onChange={(e) => setForm({ ...form, timezone: e.target.value })}
              className="w-full px-3 py-2 bg-dark-700 border border-dark-500 rounded text-white"
              placeholder="UTC"
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
              onClick={handleAddSlot}
              className="px-4 py-2 bg-accent-muted text-accent border border-accent/20 rounded font-mono text-xs"
            >
              Add Slot
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
