import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import Toolbar from './components/Toolbar'
import DocumentEditor from './components/editors/DocumentEditor'
import SpreadsheetEditor from './components/editors/SpreadsheetEditor'
import PresentationEditor from './components/editors/PresentationEditor'
import PdfViewer from './components/editors/PdfViewer'
import AIPanel from './components/AIPanel'
import NotFound from './components/NotFound'
import { DocumentProvider } from './contexts/DocumentContext'
import './App.css'

function App() {
  const [activeModule, setActiveModule] = useState('writer')
  const [isAIPanelOpen, setIsAIPanelOpen] = useState(false)

  // Parse URL parameters for module
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    const moduleParam = urlParams.get('module')
    if (moduleParam && ['writer', 'spreadsheet', 'presentation', 'pdf', 'ai'].includes(moduleParam)) {
      setActiveModule(moduleParam)
    }
  }, [])

  const renderEditor = () => {
    switch (activeModule) {
      case 'writer':
        return <DocumentEditor />
      case 'spreadsheet':
        return <SpreadsheetEditor />
      case 'presentation':
        return <PresentationEditor />
      case 'pdf':
        return <PdfViewer />
      default:
        return <DocumentEditor />
    }
  }

  return (
    <DocumentProvider>
      <Router>
        <div className="app">
          <Sidebar 
            activeModule={activeModule} 
            setActiveModule={setActiveModule}
          />
          <div className="main-content">
            <TopBar 
              onAIClick={() => setIsAIPanelOpen(!isAIPanelOpen)}
            />
            <Toolbar activeModule={activeModule} />
            <div className="editor-area">
              <Routes>
                <Route path="/" element={renderEditor()} />
                <Route path="/document/:id" element={<DocumentEditor />} />
                <Route path="/spreadsheet/:id" element={<SpreadsheetEditor />} />
                <Route path="/presentation/:id" element={<PresentationEditor />} />
                <Route path="/pdf/:id" element={<PdfViewer />} />
                {/* Catch all route for 404 */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </div>
          </div>
          <AIPanel 
            isOpen={isAIPanelOpen} 
            onClose={() => setIsAIPanelOpen(false)}
          />
        </div>
      </Router>
    </DocumentProvider>
  )
}

export default App