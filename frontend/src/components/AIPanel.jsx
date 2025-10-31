import React, { useState } from 'react'
import { useDocument } from '../contexts/DocumentContext'

const AIPanel = ({ isOpen, onClose }) => {
  const { currentDocument } = useDocument()
  const [aiAction, setAiAction] = useState('')

  const aiFeatures = [
    { id: 'summarize', name: 'Summarize Document', icon: '📋' },
    { id: 'grammar', name: 'Fix Grammar', icon: '✏️' },
    { id: 'translate', name: 'Translate', icon: '🌐' },
    { id: 'analyze', name: 'Data Analysis', icon: '📊' },
    { id: 'format', name: 'Auto Format', icon: '🎨' },
    { id: 'generate', name: 'Generate Content', icon: '✨' }
  ]

  const handleAIAction = async (action) => {
    setAiAction(action)
    // Implement AI functionality here
    console.log(`Executing AI action: ${action} for document:`, currentDocument)
  }

  if (!isOpen) return null

  return (
    <div className="ai-panel open">
      <div className="ai-panel-header">
        <h3>AI Assistant</h3>
        <button onClick={onClose} className="close-button">×</button>
      </div>
      <div className="ai-panel-content">
        <h4>AI Features</h4>
        {aiFeatures.map(feature => (
          <button
            key={feature.id}
            className="ai-feature-button"
            onClick={() => handleAIAction(feature.id)}
          >
            <span>{feature.icon}</span>
            <span>{feature.name}</span>
          </button>
        ))}
        
        {aiAction && (
          <div className="ai-result">
            <h5>AI Result for {aiAction}</h5>
            <div className="ai-output">
              {/* AI output will be displayed here */}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AIPanel