import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './NotFound.css';

const NotFound = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const quickActions = [
    { 
      id: 'writer', 
      name: 'Create Document', 
      icon: '📝', 
      description: 'Start a new text document',
      action: () => navigate('/?module=writer')
    },
    { 
      id: 'spreadsheet', 
      name: 'Create Spreadsheet', 
      icon: '📊', 
      description: 'Start a new spreadsheet',
      action: () => navigate('/?module=spreadsheet')
    },
    { 
      id: 'presentation', 
      name: 'Create Presentation', 
      icon: '🎞️', 
      description: 'Start a new presentation',
      action: () => navigate('/?module=presentation')
    },
    { 
      id: 'home', 
      name: 'Go Home', 
      icon: '🏠', 
      description: 'Return to homepage',
      action: () => navigate('/')
    }
  ];

  const handleGoBack = () => {
    if (window.history.length > 1) {
      navigate(-1);
    } else {
      navigate('/');
    }
  };

  return (
    <div className="not-found-container">
      <div className="not-found-content">
        {/* Animated 404 Graphic */}
        <div className="not-found-graphic">
          <div className="error-code">404</div>
          <div className="error-icon">🔍</div>
        </div>

        {/* Main Message */}
        <div className="not-found-message">
          <h1>Page Not Found</h1>
          <p className="path-message">
            The page <code>{location.pathname}</code> doesn't exist or has been moved.
          </p>
          <p className="suggestion">
            Don't worry! Let's get you back on track with WPS Office.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions">
          <h3>Quick Actions</h3>
          <div className="action-grid">
            {quickActions.map(action => (
              <button
                key={action.id}
                className="action-card"
                onClick={action.action}
              >
                <div className="action-icon">{action.icon}</div>
                <div className="action-content">
                  <h4>{action.name}</h4>
                  <p>{action.description}</p>
                </div>
                <div className="action-arrow">→</div>
              </button>
            ))}
          </div>
        </div>

        {/* Help Section */}
        <div className="help-section">
          <div className="help-options">
            <button className="help-button" onClick={handleGoBack}>
              ← Go Back
            </button>
            <button 
              className="help-button primary" 
              onClick={() => navigate('/')}
            >
              🏠 Home Dashboard
            </button>
            <button 
              className="help-button secondary"
              onClick={() => window.location.reload()}
            >
              🔄 Refresh Page
            </button>
          </div>

          {/* AI Assistance Offer */}
          <div className="ai-assistance">
            <div className="ai-icon">🤖</div>
            <div className="ai-message">
              <strong>Need help finding something?</strong>
              <p>Our AI assistant can help you navigate or create what you need.</p>
              <button 
                className="ai-help-button"
                onClick={() => navigate('/?module=ai')}
              >
                Ask AI Assistant
              </button>
            </div>
          </div>
        </div>

        {/* Search Suggestion */}
        <div className="search-suggestion">
          <p>Or try searching for what you're looking for:</p>
          <div className="search-box">
            <input 
              type="text" 
              placeholder="Search documents, features, or help..."
              className="search-input"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  // Implement search functionality
                  console.log('Search:', e.target.value);
                }
              }}
            />
            <button className="search-button">🔍</button>
          </div>
        </div>
      </div>

      {/* Footer Links */}
      <div className="not-found-footer">
        <div className="footer-links">
          <a href="/help">Help Center</a>
          <a href="/contact">Contact Support</a>
          <a href="/feedback">Give Feedback</a>
          <a href="/status">System Status</a>
        </div>
        <div className="copyright">
          © 2024 WPS Office Clone. All rights reserved.
        </div>
      </div>
    </div>
  );
};

export default NotFound;