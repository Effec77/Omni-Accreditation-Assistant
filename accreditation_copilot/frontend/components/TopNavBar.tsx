"use client";

import { Search, Bell, User } from "lucide-react";
import { useState, useEffect } from "react";
import ThemeSwitcher from "./ThemeSwitcher";

export default function TopNavBar() {
  const [user, setUser] = useState<any>(null);
  const [institution, setInstitution] = useState("National Institute of Excellence");

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      setUser(userData);
      if (userData.institution) {
        setInstitution(userData.institution);
      }
    }
  }, []);

  return (
    <header className="sticky top-0 z-40 px-8 py-3 bg-indigo-950/40 backdrop-blur-md rounded-full mt-4 mx-6 flex justify-between items-center shadow-lg shadow-indigo-950/20">
      {/* Left: Institution Name & Theme Switcher */}
      <div className="flex items-center gap-6">
        <span className="text-lg font-semibold text-white/90">{institution}</span>
        <div className="h-6 w-px bg-white/10"></div>
        <ThemeSwitcher />
      </div>

      {/* Right: Search, Notifications, Profile */}
      <div className="flex items-center gap-4">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
          <input
            type="text"
            placeholder="Search criteria..."
            className="bg-surface-container-lowest/50 border-none rounded-full pl-10 pr-4 py-1.5 text-sm w-64 focus:ring-1 focus:ring-primary transition-all text-foreground placeholder:text-muted-foreground"
          />
        </div>

        {/* Notifications */}
        <button className="p-2 text-indigo-200/60 hover:text-white transition-all rounded-full hover:bg-white/10">
          <Bell size={20} />
        </button>

        {/* Profile */}
        <div className="w-8 h-8 rounded-full overflow-hidden border border-primary/30 bg-gradient-to-br from-cyan-400 to-pink-400 flex items-center justify-center text-white font-bold text-sm">
          {user?.name?.charAt(0).toUpperCase() || 'U'}
        </div>
      </div>
    </header>
  );
}
