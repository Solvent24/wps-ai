import React from 'react';
import './Toolbar.css';

const Toolbar = ({ activeModule }) => {
  const writerTools = [
    { icon: '📄', name: 'New', action: 'new' },
    { icon: '💾', name: 'Save', action: 'save' },
    { icon: '📂', name: 'Open', action: 'open' },
    { icon: '🖨️', name: 'Print', action: 'print' },
    { separator: true },
    { icon: 'B', name: 'Bold', action: 'bold' },
    { icon: 'I', name: 'Italic', action: 'italic' },
    { icon: 'U', name: 'Underline', action: 'underline' },
    { icon: '🎨', name: 'Color', action: 'color' },
    { separator: true },
    { icon: '⫞', name: 'Align Left', action: 'align-left' },
    { icon: '⫟', name: 'Align Center', action: 'align-center' },
    { icon: '⫠', name: 'Align Right', action: 'align-right' },
    { icon: '⫡', name: 'Justify', action: 'justify' },
    { separator: true },
    { icon: '📊', name: 'Insert Table', action: 'insert-table' },
    { icon: '🖼️', name: 'Insert Image', action: 'insert-image' },
    { icon: '📈', name: 'Insert Chart', action: 'insert-chart' }
  ];

  const spreadsheetTools = [
    { icon: '📄', name: 'New', action: 'new' },
    { icon: '💾', name: 'Save', action: 'save' },
    { icon: '📂', name: 'Open', action: 'open' },
    { separator: true },
    { icon: '∑', name: 'AutoSum', action: 'autosum' },
    { icon: 'ƒ', name: 'Insert Function', action: 'insert-function' },
    { icon: '📊', name: 'Insert Chart', action: 'insert-chart' },
    { icon: '🔍', name: 'Find', action: 'find' },
    { separator: true },
    { icon: '💵', name: 'Currency', action: 'currency' },
    { icon: '%', name: 'Percentage', action: 'percentage' },
    { icon: '#', name: 'Number', action: 'number' },
    { separator: true },
    { icon: '🎨', name: 'Conditional Formatting', action: 'conditional-formatting' },
    { icon: '📋', name: 'Paste Special', action: 'paste-special' },
    { icon: '🔢', name: 'Sort & Filter', action: 'sort-filter' }
  ];

  const presentationTools = [
    { icon: '📄', name: 'New Slide', action: 'new-slide' },
    { icon: '💾', name: 'Save', action: 'save' },
    { icon: '📂', name: 'Open', action: 'open' },
    { separator: true },
    { icon: '🎨', name: 'Design', action: 'design' },
    { icon: '📐', name: 'Layout', action: 'layout' },
    { icon: '✨', name: 'Transitions', action: 'transitions' },
    { icon: '🌟', name: 'Animations', action: 'animations' },
    { separator: true },
    { icon: '🖼️', name: 'Insert Image', action: 'insert-image' },
    { icon: '📊', name: 'Insert Chart', action: 'insert-chart' },
    { icon: '🎬', name: 'Insert Video', action: 'insert-video' },
    { separator: true },
    { icon: '👁️', name: 'Slide Show', action: 'slideshow' },
    { icon: '📝', name: 'Presenter View', action: 'presenter-view' }
  ];

  const pdfTools = [
    { icon: '📄', name: 'Open', action: 'open' },
    { icon: '💾', name: 'Save', action: 'save' },
    { icon: '🖨️', name: 'Print', action: 'print' },
    { separator: true },
    { icon: '🔍', name: 'Zoom', action: 'zoom' },
    { icon: '📝', name: 'Annotate', action: 'annotate' },
    { icon: '🖊️', name: 'Draw', action: 'draw' },
    { icon: '📌', name: 'Comment', action: 'comment' },
    { separator: true },
    { icon: '🧩', name: 'Merge', action: 'merge' },
    { icon: '✂️', name: 'Split', action: 'split' },
    { icon: '📄', name: 'Extract', action: 'extract' },
    { separator: true },
    { icon: '🔒', name: 'Protect', action: 'protect' },
    { icon: '✍️', name: 'Sign', action: 'sign' }
  ];

  const getTools = () => {
    switch (activeModule) {
      case 'writer': return writerTools;
      case 'spreadsheet': return spreadsheetTools;
      case 'presentation': return presentationTools;
      case 'pdf': return pdfTools;
      default: return writerTools;
    }
  };

  const handleToolClick = (action) => {
    console.log(`Tool action: ${action}`);
    // Implement tool functionality
  };

  return (
    <div className="toolbar">
      <div className="toolbar-group">
        {getTools().map((tool, index) => 
          tool.separator ? (
            <div key={index} className="tool-separator"></div>
          ) : (
            <button
              key={index}
              className="tool-button"
              onClick={() => handleToolClick(tool.action)}
              title={tool.name}
            >
              <span className="tool-icon">{tool.icon}</span>
              <span className="tool-name">{tool.name}</span>
            </button>
          )
        )}
      </div>
      
      <div className="toolbar-actions">
        <button className="action-button undo" title="Undo">
          ↩️
        </button>
        <button className="action-button redo" title="Redo">
          ↪️
        </button>
        <button className="action-button help" title="Help">
          ❓
        </button>
      </div>
    </div>
  );
};

export default Toolbar;