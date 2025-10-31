import React, { useState, useEffect } from 'react'
import { useDocument } from '../../contexts/DocumentContext'

const DocumentEditor = () => {
  const { currentDocument, updateDocument } = useDocument()
  const [content, setContent] = useState('')

  useEffect(() => {
    if (currentDocument?.content?.text) {
      setContent(currentDocument.content.text)
    }
  }, [currentDocument])

  const handleContentChange = (e) => {
    const newContent = e.target.value
    setContent(newContent)
    if (currentDocument) {
      updateDocument(currentDocument.id, {
        content: { ...currentDocument.content, text: newContent }
      })
    }
  }

  return (
    <div className="document-editor-container">
      <textarea
        className="document-editor"
        value={content}
        onChange={handleContentChange}
        placeholder="Start typing your document..."
      />
    </div>
  )
}

export default DocumentEditor