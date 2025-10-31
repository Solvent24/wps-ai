import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './AuthCallback.css';

const AuthCallback = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [status, setStatus] = useState('processing');

  useEffect(() => {
    const handleAuthCallback = async () => {
      const urlParams = new URLSearchParams(location.search);
      const token = urlParams.get('token');
      const error = urlParams.get('message');
      const user_id = urlParams.get('user_id');

      if (token) {
        try {
          // Store token in localStorage
          localStorage.setItem('auth_token', token);
          localStorage.setItem('user_id', user_id);
          
          setStatus('success');
          
          // Wait a moment to show success message
          setTimeout(() => {
            navigate('/dashboard', { replace: true });
          }, 2000);
          
        } catch (err) {
          console.error('Token storage error:', err);
          setStatus('error');
        }
      } else if (error) {
        console.error('Authentication error:', error);
        setStatus('error');
        // Show error for 3 seconds then redirect to login
        setTimeout(() => {
          navigate('/login', { replace: true, state: { error } });
        }, 3000);
      } else {
        // No token or error - redirect to login
        navigate('/login', { replace: true });
      }
    };

    handleAuthCallback();
  }, [location, navigate]);

  const renderContent = () => {
    switch (status) {
      case 'success':
        return (
          <div className="auth-status success">
            <div className="status-icon">✅</div>
            <h2>Authentication Successful!</h2>
            <p>Redirecting to your dashboard...</p>
          </div>
        );
      case 'error':
        const errorMessage = new URLSearchParams(location.search).get('message') || 'Authentication failed';
        return (
          <div className="auth-status error">
            <div className="status-icon">❌</div>
            <h2>Authentication Failed</h2>
            <p>{errorMessage}</p>
            <p>Redirecting to login page...</p>
          </div>
        );
      default:
        return (
          <div className="auth-status processing">
            <div className="loading-spinner"></div>
            <h2>Completing Authentication</h2>
            <p>Please wait while we log you in...</p>
          </div>
        );
    }
  };

  return (
    <div className="auth-callback-page">
      <div className="auth-callback-container">
        {renderContent()}
      </div>
    </div>
  );
};

export default AuthCallback;