"use client";

import { InstalledApp } from "@/lib/api";

interface AppCardProps {
  app: InstalledApp;
  onClick: () => void;
}

export default function AppCard({ app, onClick }: AppCardProps) {
  const icon = app.icon || "⚡";

  return (
    <button
      onClick={onClick}
      className="group flex flex-col items-center gap-3 p-6 rounded-xl bg-white border border-gray-200/70 shadow-sm hover:shadow-md hover:border-gray-300/80 transition-all duration-200 cursor-pointer w-36"
    >
      <div className="w-14 h-14 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center text-2xl group-hover:bg-gray-100 transition-colors duration-200">
        {icon}
      </div>
      <div className="text-center">
        <p className="text-sm font-medium text-gray-800 group-hover:text-gray-900 transition-colors">
          {app.display_name}
        </p>
        <p className="text-xs text-gray-400 mt-0.5 line-clamp-1">
          {app.category}
        </p>
      </div>
    </button>
  );
}