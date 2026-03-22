"use client";

import { useState, useRef, useEffect } from "react";
import { Mic, Upload, Send, X, Loader2, ChevronDown, Check } from "lucide-react";

interface QueryPanelProps {
  onAuditStart: () => void;
  onAuditComplete: (result: any) => void;
}

interface Criterion {
  criterion: string;
  description: string;
  query_template: string;
}

export default function QueryPanel({ onAuditStart, onAuditComplete }: QueryPanelProps) {
  const [query, setQuery] = useState("");
  const [framework, setFramework] = useState("NAAC");
  const [selectedCriteria, setSelectedCriteria] = useState<string[]>([]);
  const [availableCriteria, setAvailableCriteria] = useState<Criterion[]>([]);
  const [loadingCriteria, setLoadingCriteria] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [isIngested, setIsIngested] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Fetch available criteria when framework changes
  useEffect(() => {
    const fetchCriteria = async () => {
      setLoadingCriteria(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/audit/criteria/${framework}`);
        if (response.ok) {
          const data = await response.json();
          setAvailableCriteria(data.criteria || []);
          // Auto-select first criterion if none selected
          if (selectedCriteria.length === 0 && data.criteria.length > 0) {
            setSelectedCriteria([data.criteria[0].criterion]);
          }
        } else {
          console.error('Failed to fetch criteria:', response.status);
        }
      } catch (error) {
        console.error('Failed to fetch criteria:', error);
      } finally {
        setLoadingCriteria(false);
      }
    };

    fetchCriteria();
  }, [framework]);

  // Toggle criterion selection
  const toggleCriterion = (criterionId: string) => {
    setSelectedCriteria(prev => 
      prev.includes(criterionId)
        ? prev.filter(id => id !== criterionId)
        : [...prev, criterionId]
    );
  };

  // Clear all selections
  const clearAll = () => {
    setSelectedCriteria([]);
  };

  // Apply and close dropdown
  const applySelection = () => {
    setIsDropdownOpen(false);
  };

  // Filter criteria based on search
  const filteredCriteria = availableCriteria.filter(crit =>
    crit.criterion.toLowerCase().includes(searchTerm.toLowerCase()) ||
    crit.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Voice input using Web Speech API
  const startVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Voice input not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      setIsListening(false);
    };

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      if (event.error !== 'no-speech') {
        alert(`Voice input error: ${event.error}`);
      }
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    try {
      recognition.start();
    } catch (error) {
      console.error('Failed to start recognition:', error);
      setIsListening(false);
    }
  };

  // File upload handler - automatically upload to backend
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      const validFiles = files.filter(file => {
        const ext = file.name.toLowerCase();
        return ext.endsWith('.pdf') || ext.endsWith('.png') || ext.endsWith('.jpg') || ext.endsWith('.jpeg');
      });
      
      if (validFiles.length !== files.length) {
        alert('Some files were skipped. Only PDF, PNG, and JPG files are allowed.');
      }
      
      if (validFiles.length === 0) return;
      
      setUploadedFiles(prev => [...prev, ...validFiles]);
      
      // Automatically upload to backend
      setIsUploading(true);
      try {
        const formData = new FormData();
        validFiles.forEach(file => {
          formData.append('files', file);
        });

        const response = await fetch('http://127.0.0.1:8000/api/upload/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Upload failed');
        }

        const result = await response.json();
        console.log('Upload successful:', result);
        alert(`Successfully uploaded ${validFiles.length} file(s). Now click "Ingest Files" to process them.`);
      } catch (error) {
        console.error('Upload failed:', error);
        alert('File upload failed. Please try again.');
        // Remove files from UI if upload failed
        setUploadedFiles(prev => prev.filter(f => !validFiles.includes(f)));
      } finally {
        setIsUploading(false);
      }
    }
  };

  // Upload files to backend
  const uploadFilesToBackend = async () => {
    if (uploadedFiles.length === 0) return;

    setIsUploading(true);
    try {
      const formData = new FormData();
      uploadedFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch('http://127.0.0.1:8000/api/upload/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();
      console.log('Upload successful:', result);
      alert(`Successfully uploaded ${uploadedFiles.length} file(s). Click "Ingest Files" to process them.`);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('File upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  // Trigger ingestion
  const handleIngestFiles = async () => {
    setIsUploading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload/ingest', {
        method: 'POST',
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Ingestion error:', errorText);
        throw new Error(`Ingestion failed: ${response.status}`);
      }

      const result = await response.json();
      console.log('Ingestion successful:', result);
      setIsIngested(true);
      alert(`Files ingested successfully! ${result.files_processed} files, ${result.chunks_created} chunks created.\n\nYou can now test multiple criteria without re-ingesting.`);
    } catch (error) {
      console.error('Ingestion failed:', error);
      alert(`File ingestion failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsUploading(false);
    }
  };

  // Run audit for selected criteria
  const handleRunAudit = async () => {
    if (selectedCriteria.length === 0) {
      alert('Please select at least one criterion');
      return;
    }

    if (!isIngested && uploadedFiles.length === 0) {
      alert('Please upload and ingest files first');
      return;
    }

    setIsRunning(true);
    onAuditStart();

    try {
      // Run audit for each selected criterion
      const results = [];
      for (const criterion of selectedCriteria) {
        const response = await fetch('http://127.0.0.1:8000/api/audit/run', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            framework,
            criterion: criterion.trim(),
            query: query.trim() || null,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || `Audit failed for ${criterion}`);
        }

        const result = await response.json();
        results.push(result);
      }

      // If multiple criteria, show combined results
      if (results.length > 1) {
        onAuditComplete({
          multi_criterion: true,
          results: results,
          framework: framework,
          criteria: selectedCriteria
        });
      } else {
        onAuditComplete(results[0]);
      }
    } catch (error: any) {
      console.error('Audit failed:', error);
      alert(error.message || 'Audit failed. Please check if the backend is running and try again.');
      onAuditComplete(null);
    } finally {
      setIsRunning(false);
    }
  };

  // Run full NAAC audit (all criteria)
  const handleRunFullAudit = async () => {
    if (!isIngested && uploadedFiles.length === 0) {
      alert('Please upload and ingest files first');
      return;
    }

    setIsRunning(true);
    onAuditStart();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/audit/run-full-audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Full audit failed');
      }

      const result = await response.json();
      
      // Mark as full audit result
      result.is_full_audit = true;
      
      onAuditComplete(result);
    } catch (error: any) {
      console.error('Full audit failed:', error);
      alert(error.message || 'Full audit failed. Please check if the backend is running and try again.');
      onAuditComplete(null);
    } finally {
      setIsRunning(false);
    }
  };

  // Remove uploaded file
  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      {/* Framework and Criterion Selection */}
      <div className="flex gap-4">
        <div className="flex-1">
          <label className="block text-sm font-medium mb-2 text-cyan-400">Framework</label>
          <select
            value={framework}
            onChange={(e) => {
              setFramework(e.target.value);
              setSelectedCriteria([]); // Reset criteria when framework changes
            }}
            className="w-full px-4 py-3 glass-card rounded-xl focus:outline-none focus:ring-2 focus:ring-primary transition-all hover-glow"
            disabled={isRunning}
          >
            <option value="NAAC">NAAC</option>
            <option value="NBA">NBA</option>
          </select>
        </div>
        <div className="flex-1 relative" ref={dropdownRef}>
          <label className="block text-sm font-medium mb-2 text-cyan-400">
            Criteria {loadingCriteria && <span className="text-xs">(Loading...)</span>}
            {selectedCriteria.length > 0 && <span className="text-xs ml-2">({selectedCriteria.length} selected)</span>}
          </label>
          
          {/* Custom Dropdown Trigger */}
          <button
            type="button"
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            disabled={isRunning || loadingCriteria}
            className="w-full px-4 py-3 glass-card rounded-xl focus:outline-none focus:ring-2 focus:ring-primary transition-all hover-glow flex items-center justify-between text-left"
          >
            <span className="text-cyan-400">
              {selectedCriteria.length === 0 
                ? "Select criteria..." 
                : selectedCriteria.length === 1
                ? selectedCriteria[0]
                : `${selectedCriteria.length} criteria selected`
              }
            </span>
            <ChevronDown size={20} className={`transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {/* Custom Dropdown Menu */}
          {isDropdownOpen && (
            <div className="absolute z-50 w-full mt-2 glass-card rounded-xl border border-cyan-500/20 shadow-xl max-h-96 overflow-hidden flex flex-col">
              {/* Search Bar */}
              <div className="p-3 border-b border-cyan-500/20">
                <input
                  type="text"
                  placeholder="Search criteria..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-3 py-2 bg-transparent border border-cyan-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-sm"
                />
              </div>

              {/* Criteria List */}
              <div className="overflow-y-auto flex-1 p-2">
                {filteredCriteria.map((crit) => (
                  <label
                    key={crit.criterion}
                    className="flex items-start gap-3 px-3 py-2 hover:bg-cyan-500/10 rounded-lg cursor-pointer transition-colors"
                  >
                    <div className="flex items-center h-5 mt-0.5">
                      <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
                        selectedCriteria.includes(crit.criterion)
                          ? 'bg-cyan-500 border-cyan-500'
                          : 'border-cyan-500/50'
                      }`}>
                        {selectedCriteria.includes(crit.criterion) && (
                          <Check size={14} className="text-white" />
                        )}
                      </div>
                      <input
                        type="checkbox"
                        checked={selectedCriteria.includes(crit.criterion)}
                        onChange={() => toggleCriterion(crit.criterion)}
                        className="sr-only"
                      />
                    </div>
                    <div className="flex-1 text-sm">
                      <div className="font-medium text-cyan-400">{crit.criterion}</div>
                      <div className="text-muted-foreground text-xs mt-0.5">{crit.description}</div>
                    </div>
                  </label>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="p-3 border-t border-cyan-500/20 flex gap-2">
                <button
                  type="button"
                  onClick={clearAll}
                  className="flex-1 px-3 py-2 text-sm text-cyan-400 hover:bg-cyan-500/10 rounded-lg transition-colors"
                >
                  Clear All
                </button>
                <button
                  type="button"
                  onClick={applySelection}
                  className="flex-1 px-3 py-2 text-sm gradient-bg text-white rounded-lg hover:opacity-90 transition-all"
                >
                  Apply
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Query Input */}
      <div>
        <label className="block text-sm font-medium mb-2 text-cyan-400">Query (Optional)</label>
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your query or use voice input..."
            className="flex-1 px-4 py-3 glass-card rounded-xl focus:outline-none focus:ring-2 focus:ring-primary transition-all hover-glow"
            disabled={isRunning}
          />
          
          {/* Voice Input Button */}
          <button
            onClick={startVoiceInput}
            disabled={isRunning || isListening}
            className={`px-4 py-3 rounded-xl transition-all hover-glow ${
              isListening
                ? 'bg-red-500/20 text-red-400 glow-pink animate-pulse'
                : 'glass-card text-cyan-400 hover:glow-cyan'
            }`}
            title="Voice Input"
          >
            <Mic size={20} className={isListening ? 'animate-pulse' : ''} />
          </button>
          
          {/* Upload Button */}
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isRunning}
            className="px-4 py-3 glass-card text-pink-400 rounded-xl hover:glow-pink transition-all hover-glow"
            title="Upload Files"
          >
            <Upload size={20} />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileUpload}
            className="hidden"
          />
          
          {/* Run Audit Button */}
          <button
            onClick={handleRunAudit}
            disabled={isRunning || selectedCriteria.length === 0}
            className="px-6 py-3 gradient-bg text-white rounded-xl hover:opacity-90 transition-all flex items-center gap-2 font-medium disabled:opacity-50 disabled:cursor-not-allowed hover-glow"
            title={!isIngested && uploadedFiles.length === 0 ? "Please upload and ingest files first" : ""}
          >
            {isRunning ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                Running...
              </>
            ) : (
              <>
                <Send size={20} />
                Run Audit {selectedCriteria.length > 1 && `(${selectedCriteria.length})`}
              </>
            )}
          </button>

          {/* Run Full NAAC Audit Button */}
          <button
            onClick={handleRunFullAudit}
            disabled={isRunning || !isIngested}
            className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl hover:opacity-90 transition-all flex items-center gap-2 font-medium disabled:opacity-50 disabled:cursor-not-allowed hover-glow border-2 border-green-400/50"
            title={!isIngested ? "Please upload and ingest files first" : "Run comprehensive NAAC audit for all criteria"}
          >
            {isRunning ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                Running Full Audit...
              </>
            ) : (
              <>
                <Send size={20} />
                Run Full NAAC Audit
              </>
            )}
          </button>
        </div>
      </div>

      {/* Uploaded Files Preview */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-cyan-400">
              Uploaded Files ({uploadedFiles.length}) {isIngested && <span className="text-green-400">✓ Ingested</span>}
            </label>
            <div className="flex items-center gap-2">
              {isUploading && (
                <span className="text-sm text-muted-foreground flex items-center gap-2">
                  <Loader2 size={16} className="animate-spin" />
                  Processing...
                </span>
              )}
              {!isIngested && (
                <button
                  onClick={handleIngestFiles}
                  disabled={isUploading}
                  className="px-3 py-1 text-sm gradient-bg text-white rounded-lg hover:opacity-90 transition-all disabled:opacity-50"
                >
                  Ingest Files
                </button>
              )}
              {isIngested && (
                <span className="text-xs text-green-400">
                  Ready to test multiple criteria
                </span>
              )}
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {uploadedFiles.map((file, index) => (
              <div
                key={index}
                className="px-3 py-2 glass-card rounded-full text-sm flex items-center gap-2 hover-glow"
              >
                <span className="text-cyan-400">{file.name}</span>
                <span className="text-muted-foreground text-xs">
                  ({(file.size / 1024).toFixed(1)} KB)
                </span>
                <button
                  onClick={() => removeFile(index)}
                  className="hover:text-red-400 transition-colors"
                  disabled={isUploading}
                >
                  <X size={16} />
                </button>
              </div>
            ))}
          </div>
          {isIngested && (
            <p className="text-xs text-cyan-400">
              ℹ️ Files are ingested. You can now test different criteria without re-ingesting.
            </p>
          )}
        </div>
      )}

      {/* Voice Listening Indicator */}
      {isListening && (
        <div className="flex items-center gap-2 text-sm text-cyan-400 animate-pulse">
          <div className="w-2 h-2 bg-cyan-400 rounded-full animate-ping"></div>
          Listening... Speak now
        </div>
      )}
    </div>
  );
}
