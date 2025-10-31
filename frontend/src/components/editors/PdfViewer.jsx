import React, { useState, useRef } from 'react';
import { useDocument } from '../../contexts/DocumentContext';
import './PdfViewer.css';

const PdfViewer = () => {
  const { currentDocument } = useDocument();
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(5);
  const [zoom, setZoom] = useState(100);
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawingColor, setDrawingColor] = useState('#ff0000');
  const canvasRef = useRef(null);

  // Mock PDF pages - in real app, this would come from PDF.js or similar
  const mockPages = Array.from({ length: totalPages }, (_, i) => ({
    number: i + 1,
    content: `This is page ${i + 1} of the PDF document. 
    
You can view, annotate, and interact with PDF files in WPS Office.

Features include:
• Text highlighting
• Drawing and annotations
• Comments and notes
• Form filling
• Digital signatures`
  }));

  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 25, 200));
  };

  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 25, 50));
  };

  const handleFitToWidth = () => {
    setZoom(100);
  };

  const goToPreviousPage = () => {
    setCurrentPage(prev => Math.max(1, prev - 1));
  };

  const goToNextPage = () => {
    setCurrentPage(prev => Math.min(totalPages, prev + 1));
  };

  const handlePageInput = (e) => {
    const page = parseInt(e.target.value);
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const toggleDrawing = () => {
    setIsDrawing(!isDrawing);
  };

  const downloadPdf = () => {
    // Mock download functionality
    console.log('Downloading PDF...');
    alert('PDF download functionality would be implemented here.');
  };

  const printPdf = () => {
    // Mock print functionality
    console.log('Printing PDF...');
    window.print();
  };

  return (
    <div className="pdf-viewer">
      <div className="pdf-toolbar">
        <div className="toolbar-group">
          <button className="tool-button" onClick={() => setCurrentPage(1)}>
            ⏮️ First
          </button>
          <button className="tool-button" onClick={goToPreviousPage} disabled={currentPage === 1}>
            ◀️ Previous
          </button>
          
          <div className="page-controls">
            <input
              type="number"
              value={currentPage}
              onChange={handlePageInput}
              className="page-input"
              min="1"
              max={totalPages}
            />
            <span className="page-count">of {totalPages}</span>
          </div>
          
          <button className="tool-button" onClick={goToNextPage} disabled={currentPage === totalPages}>
            Next ▶️
          </button>
          <button className="tool-button" onClick={() => setCurrentPage(totalPages)}>
            Last ⏭️
          </button>
        </div>

        <div className="toolbar-group">
          <button className="tool-button" onClick={handleZoomOut}>
            🔍-
          </button>
          <span className="zoom-level">{zoom}%</span>
          <button className="tool-button" onClick={handleZoomIn}>
            🔍+
          </button>
          <button className="tool-button" onClick={handleFitToWidth}>
            📏 Fit
          </button>
        </div>

        <div className="toolbar-group">
          <button 
            className={`tool-button ${isDrawing ? 'active' : ''}`}
            onClick={toggleDrawing}
          >
            🖊️ Draw
          </button>
          <input
            type="color"
            value={drawingColor}
            onChange={(e) => setDrawingColor(e.target.value)}
            className="color-picker"
            title="Drawing Color"
          />
          <button className="tool-button">
            🟡 Highlight
          </button>
          <button className="tool-button">
            💬 Comment
          </button>
        </div>

        <div className="toolbar-group">
          <button className="tool-button" onClick={downloadPdf}>
            ⬇️ Download
          </button>
          <button className="tool-button" onClick={printPdf}>
            🖨️ Print
          </button>
          <button className="tool-button">
            🔒 Protect
          </button>
        </div>
      </div>

      <div className="pdf-content">
        <div 
          className="pdf-page-container"
          style={{ transform: `scale(${zoom / 100})`, transformOrigin: 'top center' }}
        >
          <div className="pdf-page">
            <div className="page-content">
              <h2>PDF Document - Page {currentPage}</h2>
              <div className="page-text">
                {mockPages[currentPage - 1]?.content}
              </div>
              
              {/* Mock form fields for demonstration */}
              {currentPage === 1 && (
                <div className="pdf-form">
                  <h3>Sample Form</h3>
                  <div className="form-field">
                    <label>Name:</label>
                    <input type="text" className="form-input" placeholder="Enter your name" />
                  </div>
                  <div className="form-field">
                    <label>Email:</label>
                    <input type="email" className="form-input" placeholder="Enter your email" />
                  </div>
                  <div className="form-field">
                    <label>Date:</label>
                    <input type="date" className="form-input" />
                  </div>
                </div>
              )}
            </div>
            
            {/* Drawing canvas */}
            <canvas
              ref={canvasRef}
              className="drawing-canvas"
              style={{ cursor: isDrawing ? 'crosshair' : 'default' }}
            />
          </div>
        </div>
      </div>

      <div className="pdf-sidebar">
        <div className="sidebar-section">
          <h4>Thumbnails</h4>
          <div className="thumbnails-list">
            {mockPages.map(page => (
              <div
                key={page.number}
                className={`thumbnail ${currentPage === page.number ? 'active' : ''}`}
                onClick={() => setCurrentPage(page.number)}
              >
                <div className="thumbnail-number">{page.number}</div>
                <div className="thumbnail-content">
                  Page {page.number}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="sidebar-section">
          <h4>Annotations</h4>
          <div className="annotations-list">
            <div className="annotation-item">
              <span className="annotation-icon">💬</span>
              <div className="annotation-content">
                <div className="annotation-text">Sample comment on page 1</div>
                <div className="annotation-meta">Added just now</div>
              </div>
            </div>
            <div className="annotation-item">
              <span className="annotation-icon">🟡</span>
              <div className="annotation-content">
                <div className="annotation-text">Important section</div>
                <div className="annotation-meta">Page 2</div>
              </div>
            </div>
          </div>
        </div>

        <div className="sidebar-section">
          <h4>Properties</h4>
          <div className="properties-list">
            <div className="property">
              <span className="property-label">File Size:</span>
              <span className="property-value">2.4 MB</span>
            </div>
            <div className="property">
              <span className="property-label">Pages:</span>
              <span className="property-value">{totalPages}</span>
            </div>
            <div className="property">
              <span className="property-label">Security:</span>
              <span className="property-value">None</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PdfViewer;