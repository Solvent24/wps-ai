import React, { useState, useEffect } from 'react';
import { useDocument } from '../../contexts/DocumentContext';
import './PresentationEditor.css';

const PresentationEditor = () => {
  const { currentDocument, updateDocument } = useDocument();
  const [slides, setSlides] = useState([]);
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    if (currentDocument?.content?.slides) {
      setSlides(currentDocument.content.slides);
    } else {
      // Initialize with a blank slide
      const initialSlides = [{
        id: 1,
        title: 'Title Slide',
        content: 'Subtitle',
        layout: 'title',
        background: '#ffffff'
      }];
      setSlides(initialSlides);
    }
  }, [currentDocument]);

  const addSlide = () => {
    const newSlide = {
      id: slides.length + 1,
      title: `Slide ${slides.length + 1}`,
      content: 'Content goes here...',
      layout: 'content',
      background: '#ffffff'
    };
    const newSlides = [...slides, newSlide];
    setSlides(newSlides);
    updateDocumentContent(newSlides);
    setCurrentSlide(newSlides.length - 1);
  };

  const updateSlide = (slideIndex, updates) => {
    const newSlides = slides.map((slide, index) =>
      index === slideIndex ? { ...slide, ...updates } : slide
    );
    setSlides(newSlides);
    updateDocumentContent(newSlides);
  };

  const updateDocumentContent = (newSlides) => {
    if (currentDocument) {
      updateDocument(currentDocument.id, {
        content: { slides: newSlides }
      });
    }
  };

  const deleteSlide = (slideIndex) => {
    if (slides.length <= 1) return;
    const newSlides = slides.filter((_, index) => index !== slideIndex);
    setSlides(newSlides);
    updateDocumentContent(newSlides);
    setCurrentSlide(Math.min(currentSlide, newSlides.length - 1));
  };

  const duplicateSlide = (slideIndex) => {
    const slideToDuplicate = slides[slideIndex];
    const newSlide = {
      ...slideToDuplicate,
      id: Math.max(...slides.map(s => s.id)) + 1,
      title: `${slideToDuplicate.title} (Copy)`
    };
    const newSlides = [...slides];
    newSlides.splice(slideIndex + 1, 0, newSlide);
    setSlides(newSlides);
    updateDocumentContent(newSlides);
    setCurrentSlide(slideIndex + 1);
  };

  return (
    <div className="presentation-editor">
      <div className="slides-panel">
        <div className="slides-header">
          <h3>Slides</h3>
          <button className="add-slide-button" onClick={addSlide}>
            + Add Slide
          </button>
        </div>
        <div className="slides-list">
          {slides.map((slide, index) => (
            <div
              key={slide.id}
              className={`slide-thumbnail ${currentSlide === index ? 'active' : ''}`}
              onClick={() => setCurrentSlide(index)}
            >
              <div className="slide-number">{index + 1}</div>
              <div className="slide-preview">
                <div className="slide-title">{slide.title}</div>
                <div className="slide-content-preview">{slide.content}</div>
              </div>
              <div className="slide-actions">
                <button 
                  className="slide-action"
                  onClick={(e) => {
                    e.stopPropagation();
                    duplicateSlide(index);
                  }}
                  title="Duplicate"
                >
                  📄
                </button>
                <button 
                  className="slide-action"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteSlide(index);
                  }}
                  title="Delete"
                  disabled={slides.length <= 1}
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="slide-editor">
        {slides[currentSlide] && (
          <div 
            className="slide-container"
            style={{ backgroundColor: slides[currentSlide].background }}
          >
            <input
              type="text"
              className="slide-title-input"
              value={slides[currentSlide].title}
              onChange={(e) => updateSlide(currentSlide, { title: e.target.value })}
              placeholder="Slide Title"
            />
            <textarea
              className="slide-content-input"
              value={slides[currentSlide].content}
              onChange={(e) => updateSlide(currentSlide, { content: e.target.value })}
              placeholder="Slide content..."
              rows="6"
            />
          </div>
        )}
        
        <div className="slide-controls">
          <button 
            className="control-button"
            onClick={() => setCurrentSlide(Math.max(0, currentSlide - 1))}
            disabled={currentSlide === 0}
          >
            ← Previous
          </button>
          <span className="slide-counter">
            Slide {currentSlide + 1} of {slides.length}
          </span>
          <button 
            className="control-button"
            onClick={() => setCurrentSlide(Math.min(slides.length - 1, currentSlide + 1))}
            disabled={currentSlide === slides.length - 1}
          >
            Next →
          </button>
        </div>
      </div>

      <div className="properties-panel">
        <h4>Slide Properties</h4>
        {slides[currentSlide] && (
          <div className="property-group">
            <label>Background Color</label>
            <input
              type="color"
              value={slides[currentSlide].background}
              onChange={(e) => updateSlide(currentSlide, { background: e.target.value })}
            />
            
            <label>Layout</label>
            <select
              value={slides[currentSlide].layout}
              onChange={(e) => updateSlide(currentSlide, { layout: e.target.value })}
            >
              <option value="title">Title Slide</option>
              <option value="content">Content</option>
              <option value="two-column">Two Column</option>
              <option value="image">Image with Caption</option>
            </select>
            
            <label>Transition</label>
            <select>
              <option value="none">None</option>
              <option value="fade">Fade</option>
              <option value="slide">Slide</option>
              <option value="zoom">Zoom</option>
            </select>
          </div>
        )}
      </div>
    </div>
  );
};

export default PresentationEditor;