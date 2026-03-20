"use client";

import { Home, FileText, BarChart3, History, Settings, Sparkles, User, LogOut, Trophy, ChevronRight, Menu } from "lucide-react";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import ThemeSwitcher from "./ThemeSwitcher";

export default function Sidebar() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    // Load user from localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
    router.push('/login');
  };

  const menuItems = [
    { icon: Home, label: "Dashboard", path: "/", color: "cyan", active: true },
    { icon: FileText, label: "Run Audit", path: "/", color: "blue" },
    { icon: BarChart3, label: "Metrics", path: "/metrics", color: "green" },
    { icon: History, label: "History", path: "/history", color: "purple" },
    { icon: Trophy, label: "Top Universities", path: "/top-universities", color: "yellow" },
    { icon: User, label: "Profile", path: "/profile", color: "pink" },
  ];

  const shouldShow = isExpanded || isHovered;

  return (
    <>
      {/* Backdrop for mobile */}
      <AnimatePresence>
        {shouldShow && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
            onClick={() => setIsExpanded(false)}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.div
        className={`fixed left-0 top-0 h-full z-50 flex flex-col bg-background/95 backdrop-blur-xl border-r border-border/50 shadow-2xl transition-all duration-300 ease-in-out ${
          shouldShow ? 'w-72' : 'w-16'
        }`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => {
          setIsHovered(false);
          setShowProfileMenu(false);
        }}
        initial={false}
        animate={{
          width: shouldShow ? 288 : 64,
        }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
      >
        {/* Toggle Button */}
        <div className="absolute -right-3 top-6 z-10">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center shadow-lg hover:scale-110 transition-transform"
          >
            <motion.div
              animate={{ rotate: shouldShow ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronRight size={14} />
            </motion.div>
          </button>
        </div>

        {/* Logo Section */}
        <div className="p-4 border-b border-border/30">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <AnimatePresence>
              {shouldShow && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2, delay: 0.1 }}
                  className="flex items-center justify-between flex-1"
                >
                  <div>
                    <h1 className="text-lg font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
                      Omni
                    </h1>
                    <p className="text-xs text-muted-foreground">Accreditation Copilot</p>
                  </div>
                  <ThemeSwitcher />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* User Profile Section */}
        {user && (
          <div className="p-4 border-b border-border/30">
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="w-full flex items-center gap-3 p-2 rounded-xl hover:bg-primary/10 transition-all group"
              >
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-400 to-pink-400 flex items-center justify-center text-white font-bold text-sm shadow-lg">
                  {user.name?.charAt(0).toUpperCase() || 'D'}
                </div>
                <AnimatePresence>
                  {shouldShow && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      transition={{ duration: 0.2, delay: 0.1 }}
                      className="flex-1 text-left"
                    >
                      <p className="text-sm font-semibold text-foreground">{user.name || 'Demo User'}</p>
                      <p className="text-xs text-muted-foreground">{user.role || 'Accreditation Coordinator'}</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </button>

              {/* Profile Dropdown */}
              <AnimatePresence>
                {showProfileMenu && shouldShow && (
                  <motion.div
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -10, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                    className="absolute top-full left-0 right-0 mt-2 p-3 bg-background/95 backdrop-blur-xl border border-border/50 rounded-xl shadow-xl z-50"
                  >
                    <div className="px-3 py-2 border-b border-border/30 mb-2">
                      <p className="text-xs text-muted-foreground">Institution</p>
                      <p className="text-sm font-medium text-foreground">{user.institution || 'Demo University'}</p>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-red-500/10 text-red-400 hover:text-red-300 transition-all"
                    >
                      <LogOut size={16} />
                      <span className="text-sm">Logout</span>
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = item.active;
            
            return (
              <motion.div
                key={item.label}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2, delay: index * 0.05 }}
              >
                <button
                  onClick={() => router.push(item.path)}
                  className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all duration-200 group relative overflow-hidden ${
                    isActive
                      ? 'bg-primary/20 text-primary shadow-lg'
                      : 'hover:bg-accent text-muted-foreground hover:text-foreground'
                  }`}
                >
                  {/* Active indicator */}
                  {isActive && (
                    <motion.div
                      layoutId="activeIndicator"
                      className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                      transition={{ duration: 0.3 }}
                    />
                  )}
                  
                  {/* Icon */}
                  <div className={`relative z-10 ${isActive ? 'scale-110' : 'group-hover:scale-110'} transition-transform duration-200`}>
                    <Icon size={20} />
                  </div>
                  
                  {/* Label */}
                  <AnimatePresence>
                    {shouldShow && (
                      <motion.span
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.2, delay: 0.1 }}
                        className="text-sm font-medium relative z-10"
                      >
                        {item.label}
                      </motion.span>
                    )}
                  </AnimatePresence>

                  {/* Hover effect */}
                  <div className="absolute inset-0 bg-accent/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-xl" />
                </button>
              </motion.div>
            );
          })}
        </nav>

        {/* Settings */}
        <div className="p-4 border-t border-border/30">
          <button
            onClick={() => router.push('/settings')}
            className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-500/10 text-muted-foreground hover:text-gray-400 transition-all group"
          >
            <Settings size={20} className="group-hover:rotate-90 transition-transform duration-300" />
            <AnimatePresence>
              {shouldShow && (
                <motion.span
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2, delay: 0.1 }}
                  className="text-sm font-medium"
                >
                  Settings
                </motion.span>
              )}
            </AnimatePresence>
          </button>
        </div>

        {/* Gradient overlay for visual depth */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background/20 pointer-events-none" />
      </motion.div>

      {/* Main content spacer */}
      <div className={`transition-all duration-300 ${shouldShow ? 'ml-72' : 'ml-16'}`} />
    </>
  );
}
