import React from 'react';

export default function MetricCard({ label, value, color = 'text-white', icon: Icon, subtext }) {
  return (
    <div className="bg-dark-700 border border-dark-500 rounded-lg p-4">
      <div className="flex items-center justify-between mb-1">
        <div className="text-xs font-mono text-muted">{label}</div>
        {Icon && <Icon size={14} className="text-muted" />}
      </div>
      <div className={`text-3xl font-mono font-medium ${color}`}>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </div>
      {subtext && <div className="text-xs text-muted font-mono mt-1">{subtext}</div>}
    </div>
  );
}
