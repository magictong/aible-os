"use client";

import { useState, useEffect } from "react";
import {
  CatalogApp,
  InstalledApp,
  fetchCatalog,
  fetchInstalled,
  installApp,
  uninstallApp,
} from "@/lib/api";
import StoreAppCard from "./StoreAppCard";

interface AppStoreProps {
  installedApps: InstalledApp[];
  onClose: () => void;
  onInstallSuccess: () => void;
  onUninstallSuccess: () => void;
}

export default function AppStore({
  installedApps,
  onClose,
  onInstallSuccess,
  onUninstallSuccess,
}: AppStoreProps) {
  const [catalog, setCatalog] = useState<CatalogApp[]>([]);
  const [loading, setLoading] = useState(true);
  const [installing, setInstalling] = useState<string | null>(null);

  useEffect(() => {
    fetchCatalog()
      .then(setCatalog)
      .catch(() => setCatalog([]))
      .finally(() => setLoading(false));
  }, []);

  const installedIds = new Set(installedApps.map((a) => a.app_id));

  const handleInstall = async (appId: string) => {
    setInstalling(appId);
    try {
      await installApp(appId);
      onInstallSuccess();
    } catch {
      // silent
    } finally {
      setInstalling(null);
    }
  };

  const handleUninstall = async (appId: string) => {
    setInstalling(appId);
    try {
      await uninstallApp(appId);
      onUninstallSuccess();
    } catch {
      // silent
    } finally {
      setInstalling(null);
    }
  };

  return (
    <div className="fixed inset-0 z-40 flex">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/10 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative ml-auto w-full max-w-sm h-full bg-white shadow-xl border-l border-gray-100 animate-slide-in-right flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-gray-100">
          <div>
            <h2 className="text-base font-semibold text-gray-900">应用商店</h2>
            <p className="text-xs text-gray-400 mt-0.5">浏览并安装 App</p>
          </div>
          <button
            onClick={onClose}
            className="w-7 h-7 flex items-center justify-center rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M1 1L13 13M13 1L1 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-6 py-5">
          {loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="w-5 h-5 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin" />
            </div>
          ) : catalog.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-32 text-center">
              <p className="text-sm text-gray-500">暂无可用 App</p>
            </div>
          ) : (
            <div className="space-y-3">
              {catalog.map((app) => (
                <StoreAppCard
                  key={app.app_id}
                  app={app}
                  installed={installedIds.has(app.app_id)}
                  onInstall={() => handleInstall(app.app_id)}
                  onUninstall={() => handleUninstall(app.app_id)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}