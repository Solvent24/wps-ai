import React, { useState } from 'react';
import './TopBar.css';

const TopBar = ({ onAIClick }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    if (e.key === 'Enter') {
      console.log('Searching for:', searchQuery);
      // Implement search functionality
    }
  };

  return (
    <div className="top-bar">
      <div className="top-bar-left">
        <button 
          className="menu-button"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          ☰
        </button>
        
        <div className="document-info">
          <span className="document-title">Untitled Document</span>
          <span className="document-status">• Saved</span>
        </div>
      </div>

      <div className="top-bar-center">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search commands, features, or help..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleSearch}
            className="search-input"
          />
          <span className="search-icon">🔍</span>
        </div>
      </div>

      <div className="top-bar-right">
        <button className="ai-button" onClick={onAIClick}>
          <span className="ai-icon">🤖</span>
          AI Assistant
        </button>
        
        <button className="collaboration-button">
          <span className="collab-icon">👥</span>
          Share
        </button>
        
        <div className="user-menu">
          <div className="user-avatar">U</div>
          <div className="user-dropdown">
            <span>User</span>
            <div className="dropdown-arrow">▼</div>
          </div>
        </div>
      </div>

      {isMenuOpen && (
        <div className="quick-menu">
          <div className="menu-item">New Document</div>
          <div className="menu-item">Open</div>
          <div className="menu-item">Save</div>
          <div className="menu-item">Save As</div>
          <div className="menu-divider"></div>
          <div className="menu-item">Print</div>
          <div className="menu-item">Export</div>
          <div className="menu-divider"></div>
          <div className="menu-item">Settings</div>
          <div className="menu-item">Help</div>
        </div>
      )}
    </div>
  );
};

export default TopBar;