"use client";

import { CatalogApp } from "@/lib/api";

interface StoreAppCardProps {
  app: CatalogApp;
  installed: boolean;
  onInstall: () => void;
  onUninstall: () => void;
}

export default function StoreAppCard({
  app,
  installed,
  onInstall,
  onUninstall,
}: StoreAppCardProps) {
  const icon = app.icon || "📦";

  return (
    <div className="flex items-start gap-4 p-4 rounded-xl bg-white border border-gray-100 hover:border-gray-200 transition-colors">
      <div className="w-12 h-12 shrink-0 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center text-xl">
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <h4 className="text-sm font-medium text-gray-900">{app.name}</h4>
          <span className="text-[10px] font-medium text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
            {app.category}
          </span>
        </div>
        <p className="text-xs text-gray-500 mt-1 leading-relaxed">
          {app.description}
        </p>
      </div>
      <button
        onClick={installed ? onUninstall : onInstall}
        className={`shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
          installed
            ? "bg-red-50 text-red-600 hover:bg-red-100 border border-red-200"
            : "bg-gray-900 text-white hover:bg-gray-800"
        }`}
      >
        {installed ? "卸载" : "安装"}
      </button>
    </div>
  );
}