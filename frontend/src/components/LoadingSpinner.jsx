import React from 'react';

export default function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-slate-700"></div>
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-cyan-500 border-r-cyan-500 animate-spin"></div>
      </div>
    </div>
  );
}
