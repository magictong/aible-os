"use client";

import { useState, useEffect, useCallback } from "react";
import { InstalledApp, fetchInstalled, waitForBackend } from "@/lib/api";
import AppCard from "@/components/AppCard";
import AppWindow from "@/components/AppWindow";
import AppStore from "@/components/AppStore";

export default function Home() {
  const [installedApps, setInstalledApps] = useState<InstalledApp[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(true);
  const [showStore, setShowStore] = useState(false);
  const [activeApp, setActiveApp] = useState<InstalledApp | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadInstalled = useCallback(async () => {
    try {
      // Wait for backend to be ready (up to 15 seconds)
      setStarting(true);
      const ready = await waitForBackend(15000);
      if (!ready) {
        console.warn("Backend not ready, trying anyway...");
      }
      setStarting(false);

      const apps = await fetchInstalled();
      setInstalledApps(apps);
      setError(null);
    } catch (e) {
      // If backend is not running, use empty state gracefully
      setInstalledApps([]);
      setError(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadInstalled();
  }, [loadInstalled]);

  const handleInstallSuccess = useCallback(() => {
    loadInstalled();
  }, [loadInstalled]);

  const handleUninstallSuccess = useCallback(() => {
    loadInstalled();
  }, [loadInstalled]);

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Top bar */}
      <header className="flex items-center justify-between px-8 py-5 border-b border-gray-100">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-md bg-gray-900 flex items-center justify-center">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <rect x="1" y="1" width="5" height="5" rx="1" fill="white" />
              <rect x="8" y="1" width="5" height="5" rx="1" fill="white" />
              <rect x="1" y="8" width="5" height="5" rx="1" fill="white" />
              <rect x="8" y="8" width="5" height="5" rx="1" fill="white" />
            </svg>
          </div>
          <span className="text-sm font-semibold text-gray-900 tracking-tight">
            Aible OS
          </span>
        </div>
        <div className="text-xs text-gray-400">
          {new Date().toLocaleDateString("zh-CN", {
            weekday: "short",
            month: "short",
            day: "numeric",
          })}
        </div>
      </header>

      {/* Desktop area */}
      <main className="flex-1 flex flex-col items-center justify-start px-8 py-12">
        {loading ? (
          <div className="flex flex-col items-center justify-center h-48 gap-3">
            <div className="w-5 h-5 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin" />
            {starting && <p className="text-xs text-gray-400">正在启动服务...</p>}
          </div>
        ) : installedApps.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-center animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-gray-50 border border-gray-200 flex items-center justify-center text-3xl mb-4">
              📦
            </div>
            <h2 className="text-lg font-semibold text-gray-900">桌面还是空的</h2>
            <p className="text-sm text-gray-400 mt-1">
              从应用商店安装你的第一个 App
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 animate-fade-in">
            {installedApps.map((app) => (
              <AppCard
                key={app.app_id}
                app={app}
                onClick={() => setActiveApp(app)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Store button */}
      <div className="fixed bottom-6 right-6 z-30">
        <button
          onClick={() => setShowStore(true)}
          className="flex items-center gap-2 px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-xl shadow-lg hover:bg-gray-800 hover:shadow-xl transition-all duration-200"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1V13M1 7H13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
          应用商店
        </button>
      </div>

      {/* App window */}
      {activeApp && (
        <AppWindow app={activeApp} onClose={() => setActiveApp(null)} />
      )}

      {/* Store panel */}
      {showStore && (
        <AppStore
          installedApps={installedApps}
          onClose={() => setShowStore(false)}
          onInstallSuccess={handleInstallSuccess}
          onUninstallSuccess={handleUninstallSuccess}
        />
      )}
    </div>
  );
}