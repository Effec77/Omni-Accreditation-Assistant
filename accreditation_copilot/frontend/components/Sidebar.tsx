"use client";

import { LayoutDashboard, FileCheck, FolderOpen, BarChart3, History, Settings, Bot } from "lucide-react";
import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();

  const menuItems = [
    { icon: LayoutDashboard, label: "DASHBOARD", path: "/" },
    { icon: FileCheck, label: "MY AUDITS", path: "/audits" },
    { icon: FolderOpen, label: "EVIDENCE HUB", path: "/evidence" },
    { icon: BarChart3, label: "INSTITUTIONAL METRICS", path: "/metrics" },
    { icon: History, label: "HISTORY", path: "/history" },
    { icon: Settings, label: "SETTINGS", path: "/settings" },
    { icon: Bot, label: "AI HELP", path: "/help" },
  ];

  const isActive = (path: string) => pathname === path;

  return (
    <aside className="fixed left-0 h-screen w-72 bg-indigo-950/60 backdrop-blur-xl shadow-[20px_0_40px_rgba(0,0,0,0.12)] flex flex-col py-8 px-4 z-50">
      {/* Logo */}
      <div className="mb-10 px-4">
        <h1 className="text-xl font-bold tracking-tighter text-cyan-200">Omni Copilot</h1>
        <p className="text-[11px] uppercase tracking-wider text-indigo-300/70 mt-1">Accreditation Intel</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          
          return (
            <button
              key={item.path}
              onClick={() => router.push(item.path)}
              className={`flex items-center gap-4 px-4 py-3 rounded-lg w-full text-left transition-all duration-200 group ${
                active
                  ? 'text-white border-l-2 border-pink-500 bg-white/5 font-bold'
                  : 'text-indigo-300/70 hover:text-white hover:bg-indigo-800/40'
              }`}
            >
              <Icon 
                size={20} 
                className={active ? 'text-cyan-200' : 'text-current'} 
              />
              <span className="text-[11px] uppercase tracking-wider font-medium">
                {item.label}
              </span>
            </button>
          );
        })}
      </nav>

      {/* Run New Audit Button */}
      <div className="mt-auto px-4">
        <button 
          onClick={() => router.push('/')}
          className="w-full py-4 bg-gradient-to-br from-primary to-cyan-400 text-background font-bold rounded-xl shadow-lg shadow-cyan-900/20 hover:shadow-cyan-900/40 active:scale-95 transition-all"
        >
          Run New Audit
        </button>
      </div>
    </aside>
  );
}
