"use client";

import { useState, useRef, useEffect } from "react";
import { Check, ChevronDown, Search, X } from "lucide-react";

interface Criterion {
  criterion: string;
  description: string;
  query_template: string;
}

interface CriteriaSelectorProps {
  availableCriteria: Criterion[];
  selectedCriteria: string[];
  onChange: (selected: string[]) => void;
  disabled?: boolean;
  loading?: boolean;
}

export default function CriteriaSelector({
  availableCriteria,
  selectedCriteria,
  onChange,
  disabled = false,
  loading = false
}: CriteriaSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredCriteria = availableCriteria.filter(crit =>
    crit.criterion.toLowerCase().includes(searchTerm.toLowerCase()) ||
    crit.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleCriterion = (criterion: string) => {
    if (selectedCriteria.includes(criterion)) {
      onChange(selectedCriteria.filter(c => c !== criterion));
    } else {
      onChange([...selectedCriteria, criterion]);
    }
  };

  const selectAll = () => {
    onChange(availableCriteria.map(c => c.criterion));
  };

  const clearAll = () => {
    onChange([]);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <label className="block text-sm font-medium mb-2 text-cyan-400">
        Criteria {loading && <span className="text-xs">(Loading...)</span>}
        {selectedCriteria.length > 0 && (
          <span className="text-xs ml-2">({selectedCriteria.length} selected)</span>
        )}
      </label>

      {/* Dropdown Button */}
      <button
        type="button"
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled || loading}
        className="w-full px-4 py-3 glass-card rounded-xl focus:outline-none focus:ring-2 focus:ring-primary transition-all hover-glow flex items-center justify-between text-left"
      >
        <span className="text-cyan-400">
          {selectedCriteria.length === 0
            ? "Select criteria..."
            : selectedCriteria.length === 1
            ? selectedCriteria[0]
            : `${selectedCriteria.length} criteria selected`}
        </span>
        <ChevronDown
          size={20}
          className={`transition-transform ${isOpen ? "rotate-180" : ""}`}
        />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute z-50 w-full mt-2 glass-card rounded-xl shadow-lg max-h-96 overflow-hidden">
          {/* Search Bar */}
          <div className="p-3 border-b border-cyan-400/20">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-cyan-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search criteria..."
                className="w-full pl-10 pr-3 py-2 bg-transparent border border-cyan-400/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2 p-3 border-b border-cyan-400/20">
            <button
              onClick={selectAll}
              className="flex-1 px-3 py-1 text-xs bg-cyan-400/10 text-cyan-400 rounded-lg hover:bg-cyan-400/20 transition-all"
            >
              Select All
            </button>
            <button
              onClick={clearAll}
              className="flex-1 px-3 py-1 text-xs bg-pink-400/10 text-pink-400 rounded-lg hover:bg-pink-400/20 transition-all"
            >
              Clear All
            </button>
          </div>

          {/* Criteria List */}
          <div className="max-h-64 overflow-y-auto">
            {filteredCriteria.length === 0 ? (
              <div className="p-4 text-center text-muted-foreground text-sm">
                No criteria found
              </div>
            ) : (
              filteredCriteria.map((crit) => {
                const isSelected = selectedCriteria.includes(crit.criterion);
                return (
                  <button
                    key={crit.criterion}
                    onClick={() => toggleCriterion(crit.criterion)}
                    className="w-full px-4 py-3 flex items-start gap-3 hover:bg-cyan-400/10 transition-all text-left"
                  >
                    {/* Checkbox */}
                    <div
                      className={`flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
                        isSelected
                          ? "bg-cyan-400 border-cyan-400"
                          : "border-cyan-400/50"
                      }`}
                    >
                      {isSelected && <Check size={14} className="text-black" />}
                    </div>

                    {/* Criterion Info */}
                    <div className="flex-1 min-w-0">
                      <div className="text-cyan-400 font-medium text-sm">
                        {crit.criterion}
                      </div>
                      <div className="text-muted-foreground text-xs mt-1 line-clamp-2">
                        {crit.description}
                      </div>
                    </div>
                  </button>
                );
              })
            )}
          </div>

          {/* Apply Button */}
          <div className="p-3 border-t border-cyan-400/20">
            <button
              onClick={() => setIsOpen(false)}
              className="w-full px-4 py-2 gradient-bg text-white rounded-lg hover:opacity-90 transition-all text-sm font-medium"
            >
              Apply
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
