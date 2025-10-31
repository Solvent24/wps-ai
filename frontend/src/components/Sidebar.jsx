import React from 'react'

const Sidebar = ({ activeModule, setActiveModule }) => {
  const modules = [
    { id: 'writer', name: 'Writer', icon: '📝' },
    { id: 'spreadsheet', name: 'Spreadsheet', icon: '📊' },
    { id: 'presentation', name: 'Presentation', icon: '🎞️' },
    { id: 'pdf', name: 'PDF', icon: '📚' },
    { id: 'cloud', name: 'Cloud', icon: '☁️' },
    { id: 'ai', name: 'AI Assistant', icon: '🤖' }
  ]

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>WPS Office</h2>
        <p>AI-Powered Productivity</p>
      </div>
      <div className="sidebar-nav">
        {modules.map(module => (
          <div
            key={module.id}
            className={`nav-item ${activeModule === module.id ? 'active' : ''}`}
            onClick={() => setActiveModule(module.id)}
          >
            <span>{module.icon}</span>
            <span>{module.name}</span>
          </div>
        ))}
      </div>
      <div className="sidebar-footer">
        <div className="nav-item">
          <span>⚙️</span>
          <span>Settings</span>
        </div>
      </div>
    </div>
  )
}

export default Sidebar