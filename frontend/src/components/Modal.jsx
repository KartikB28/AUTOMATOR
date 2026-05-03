import React from 'react';
import { X } from 'lucide-react';

export default function Modal({ open, onClose, title, children, maxWidth = 'max-w-2xl' }) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className={`bg-dark-800 border border-dark-500 rounded-lg w-full ${maxWidth} max-h-[90vh] overflow-hidden flex flex-col`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-4 border-b border-dark-600 flex items-center justify-between">
          <h2 className="font-mono text-sm font-medium">{title}</h2>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-dark-600 transition-colors"
          >
            <X size={16} className="text-muted" />
          </button>
        </div>
        <div className="overflow-y-auto p-4 flex-1">
          {children}
        </div>
      </div>
    </div>
  );
}
