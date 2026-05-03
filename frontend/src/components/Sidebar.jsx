import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Bot, FileText, Layers,
  CalendarDays, BarChart3, Settings, Zap
} from 'lucide-react';
import { useStore } from '../store.js';

const NAV_ITEMS = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/bots', icon: Bot, label: 'Bots' },
  { to: '/content', icon: FileText, label: 'Content' },
  { to: '/niches', icon: Layers, label: 'Niches' },
  { to: '/schedule', icon: CalendarDays, label: 'Schedule' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  const stats = useStore(s => s.systemStats);

  return (
    <aside className="w-56 bg-dark-800 border-r border-dark-600 flex flex-col flex-shrink-0">
      <div className="p-4 border-b border-dark-600">
        <div className="flex items-center gap-2">
          <Zap size={18} className="text-accent" />
          <span className="font-mono font-medium text-sm tracking-wider">THE AUTOMATOR</span>
        </div>
        {stats && (
          <div className="mt-2 text-xs text-muted font-mono">
            {stats.posted_content} posted - {stats.pending_content} pending
          </div>
        )}
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-mono transition-all
               ${isActive
                 ? 'bg-accent-muted text-accent border border-accent/20'
                 : 'text-muted hover:text-white hover:bg-dark-700'}`
            }
          >
            <Icon size={15} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-dark-600">
        <div className="text-xs text-muted font-mono text-center">v1.0.0</div>
      </div>
    </aside>
  );
}
