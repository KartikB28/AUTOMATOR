import React from 'react';
import { Instagram, Music2, Youtube, Twitter, Linkedin, Facebook, Image as ImageIcon } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { getMediaUrl } from '../api.js';

const PLATFORM_ICONS = {
  instagram: Instagram,
  tiktok: Music2,
  youtube: Youtube,
  twitter: Twitter,
  linkedin: Linkedin,
  facebook: Facebook,
};

const STATUS_COLORS = {
  pending: 'text-muted bg-dark-600',
  building: 'text-info bg-info/10',
  media_pending: 'text-info bg-info/10',
  media_ready: 'text-warn bg-warn/10',
  scheduled: 'text-warn bg-warn/10',
  posting: 'text-info bg-info/10',
  posted: 'text-accent bg-accent/10',
  failed: 'text-danger bg-danger/10',
  skipped: 'text-muted bg-dark-600',
};

export default function ContentCard({ item, onClick }) {
  const Icon = PLATFORM_ICONS[item.platform] || ImageIcon;
  const statusClass = STATUS_COLORS[item.status] || STATUS_COLORS.pending;

  return (
    <div
      onClick={() => onClick && onClick(item)}
      className="bg-dark-700 border border-dark-500 rounded-lg overflow-hidden cursor-pointer hover:border-dark-400 transition-colors"
    >
      <div className="aspect-square bg-dark-600 relative">
        {item.thumbnail_path ? (
          <img
            src={getMediaUrl(item.thumbnail_path)}
            alt={item.topic}
            className="w-full h-full object-cover"
            onError={(e) => { e.target.style.display = 'none'; }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <ImageIcon size={32} className="text-muted" />
          </div>
        )}
        <div className="absolute top-2 left-2">
          <Icon size={16} className="text-white drop-shadow" />
        </div>
        <div className={`absolute top-2 right-2 px-2 py-0.5 rounded text-xs font-mono uppercase ${statusClass}`}>
          {item.status}
        </div>
      </div>
      <div className="p-3">
        <div className="font-mono text-xs text-white truncate" title={item.topic}>
          {item.topic}
        </div>
        {item.hook && (
          <div className="text-xs text-muted font-mono mt-1 line-clamp-2">
            {item.hook}
          </div>
        )}
        <div className="text-xs text-muted font-mono mt-2">
          {item.created_at ? formatDistanceToNow(new Date(item.created_at)) + ' ago' : ''}
        </div>
      </div>
    </div>
  );
}
