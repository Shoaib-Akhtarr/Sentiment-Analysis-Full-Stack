import React, { useState } from 'react';
import './App.css';

const ThreatAnalyzer = () => {
  const [message, setMessage] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [recentScans, setRecentScans] = useState([]);
  const [systemLogs, setSystemLogs] = useState([]);
  const [charCount, setCharCount] = useState(0);

  const API_URL = 'http://127.0.0.1:8000/api';

  // Handle message input
  const handleMessageChange = (e) => {
    const text = e.target.value;
    if (text.length <= 5000) {
      setMessage(text);
      setCharCount(text.length);
    }
  };

  // Add log entry
  const addLog = (text, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
    setSystemLogs(prev => [...prev, { timestamp, text, type }]);
  };

  // Analyze message
  const analyzeThreat = async () => {
    if (!message.trim()) {
      addLog('Error: No message provided', 'error');
      return;
    }

    setIsAnalyzing(true);
    setResult(null);
    addLog('Analyzing keyword density...');
    
    setTimeout(() => {
      addLog('Cross-referencing threat database...');
    }, 500);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      if (!response.ok) throw new Error('API request failed');

      const data = await response.json();
      
      // Calculate dynamic score based on probability
      const calculateScore = (prediction, probability) => {
        if (prediction === 'SPAM') {
          // SPAM: probability 0.5-1.0 → score 5-10
          return Math.floor(probability * 10);
        } else {
          // HAM: probability 0.5-1.0 → score 0-5 (inverted)
          return Math.floor((1 - probability) * 10);
        }
      };

      const scanResult = {
        prediction: data.prediction,
        probability: data.probability,
        score: calculateScore(data.prediction, data.probability),
        message: message.substring(0, 50) + (message.length > 50 ? '...' : ''),
        timestamp: new Date().toLocaleTimeString('en-US', { 
          hour12: false, 
          hour: '2-digit', 
          minute: '2-digit' 
        }),
        threatLevel: data.prediction === 'SPAM' 
          ? Math.floor(data.probability * 10) 
          : Math.floor((1 - data.probability) * 10)
      };

      setResult(scanResult);
      setRecentScans(prev => [scanResult, ...prev.slice(0, 9)]);
      
      addLog(
        `SCAN ${data.prediction === 'SPAM' ? 'THREAT DETECTED' : 'CLEAN'}: Score ${scanResult.score}`, 
        data.prediction === 'SPAM' ? 'error' : 'success'
      );

    } catch (error) {
      addLog(`Error: ${error.message}`, 'error');
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Clear input
  const handleClear = () => {
    setMessage('');
    setCharCount(0);
    setResult(null);
  };

  // Paste from clipboard
  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setMessage(text.substring(0, 5000));
      setCharCount(text.length > 5000 ? 5000 : text.length);
    } catch (err) {
      addLog('Failed to paste from clipboard', 'error');
    }
  };

  // Icons as SVG
  const ShieldIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  );

  const UploadIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
      <polyline points="17 8 12 3 7 8"/>
      <line x1="12" y1="3" x2="12" y2="15"/>
    </svg>
  );

  const TrashIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <polyline points="3 6 5 6 21 6"/>
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
    </svg>
  );

  const CopyIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
  );

  const SettingsIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="3"/>
      <path d="M12 1v6m0 6v6m6-12l-3 3m-6 6l-3 3m12-12l-3 3m-6 6l-3 3"/>
    </svg>
  );

  const ClockIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12 6 12 12 16 14"/>
    </svg>
  );

  return (
    <div className="app-container">
      <div className="main-grid">
        
        {/* Left Sidebar */}
        <div className="sidebar left-sidebar">
          {/* Logo */}
          <div className="card logo-card">
            <div className="logo-content">
              <div className="logo-icon">
                <ShieldIcon />
              </div>
              <h1 className="logo-text">NEXUS</h1>
            </div>
          </div>

          {/* Recent Scans */}
          <div className="card">
            <div className="card-header">
              <ClockIcon />
              <h2 className="card-title">RECENT SCANS</h2>
            </div>
            
            <div className="recent-scans">
              {recentScans.length === 0 ? (
                <p className="no-data">No logs found.</p>
              ) : (
                recentScans.map((scan, idx) => (
                  <div key={idx} className="scan-item">
                    <div className={`status-dot ${scan.prediction === 'SPAM' ? 'threat' : 'safe'}`} />
                    <div className="scan-content">
                      <div className="scan-header">
                        <span className={`scan-score ${scan.prediction === 'SPAM' ? 'threat' : 'safe'}`}>
                          {scan.score}%
                        </span>
                        <span className="scan-time">{scan.timestamp}</span>
                      </div>
                      <p className="scan-message">{scan.message}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Batch Upload */}
          <div className="card upload-card">
            <div className="upload-content">
              <div className="upload-icon">
                <UploadIcon />
              </div>
              <h3 className="upload-title">Batch Upload</h3>
              <p className="upload-subtitle">Drop .CSV or Click</p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="main-content">
          {/* Header */}
          <div className="card header-card">
            <div className="header-content">
              <div>
                <h2 className="header-title">Threat Analyzer</h2>
                <p className="header-subtitle">v4.0.0 Enterprise Edition</p>
              </div>
              <button className="settings-btn">
                <SettingsIcon />
              </button>
            </div>
          </div>

          {/* Input Area */}
          <div className="card input-card">
            <textarea
              value={message}
              onChange={handleMessageChange}
              placeholder="// Initialize scan by entering message payload..."
              className="message-input"
              disabled={isAnalyzing}
            />
            
            <div className="input-footer">
              <div className="input-actions">
                <button onClick={handleClear} className="action-btn">
                  <TrashIcon />
                  Clear
                </button>
                <button onClick={handlePaste} className="action-btn">
                  <CopyIcon />
                  Paste
                </button>
              </div>
              <div className="char-count">
                {charCount} / 5000 chars
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-row">
            <div className="status-badge">
              <div className="status-indicator" />
              <span className="status-text">SYSTEM READY</span>
            </div>
            
            <button
              onClick={analyzeThreat}
              disabled={isAnalyzing || !message.trim()}
              className={`scan-btn ${(isAnalyzing || !message.trim()) ? 'disabled' : ''}`}
            >
              <ShieldIcon />
              {isAnalyzing ? 'ANALYZING...' : 'INITIATE SCAN'}
            </button>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="sidebar right-sidebar">
          {/* System Log */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">SYSTEM LOG</h3>
              <div className="status-indicator active" />
            </div>
            
            <div className="system-logs">
              {systemLogs.length === 0 ? (
                <p className="no-data">Awaiting analysis...</p>
              ) : (
                systemLogs.slice(-5).reverse().map((log, idx) => (
                  <div key={idx} className="log-entry">
                    <span className="log-time">{log.timestamp}</span>
                    <span className={`log-text ${log.type}`}>{log.text}</span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Result Display */}
          <div className="card result-card">
            {!result ? (
              <div className="empty-result">
                <div className="empty-icon">
                  <ShieldIcon />
                </div>
                <p className="empty-text">Awaiting Analysis Data</p>
              </div>
            ) : (
              <div className="result-content">
                {/* Score Circle */}
                <div className="score-circle-container">
                  <div className={`score-circle ${result.prediction === 'SPAM' ? 'threat' : 'safe'}`}>
                    <span className="score-number">{result.score}</span>
                  </div>
                  <div className="result-info">
                    <h3 className={`result-status ${result.prediction === 'SPAM' ? 'threat' : 'safe'}`}>
                      {result.prediction === 'SPAM' ? 'THREAT DETECTED' : 'SAFE CONTENT'}
                    </h3>
                    <p className="result-description">
                      Content appears {result.prediction === 'SPAM' ? 'malicious' : 'legitimate'} 
                      ({Math.round(result.probability * 100)}% trust score)
                    </p>
                  </div>
                </div>

                {/* Details */}
                <div className="result-details">
                  <div className="detail-row">
                    <span className="detail-label">Threat Level</span>
                    <span className={`detail-value ${result.prediction === 'SPAM' ? 'threat' : 'safe'}`}>
                      {result.threatLevel}/10
                    </span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Confidence</span>
                    <span className="detail-value">{Math.round(result.probability * 100)}%</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Scan Time</span>
                    <span className="detail-value">{result.timestamp}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreatAnalyzer;