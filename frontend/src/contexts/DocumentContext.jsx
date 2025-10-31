import React, { createContext, useContext, useState, useCallback } from 'react'

const DocumentContext = createContext()

export const useDocument = () => {
  const context = useContext(DocumentContext)
  if (!context) {
    throw new Error('useDocument must be used within a DocumentProvider')
  }
  return context
}

export const DocumentProvider = ({ children }) => {
  const [currentDocument, setCurrentDocument] = useState(null)
  const [documents, setDocuments] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [collaborators, setCollaborators] = useState([])

  const createDocument = useCallback(async (type, title = 'Untitled Document') => {
    setIsLoading(true)
    try {
      const doc = {
        id: Date.now().toString(),
        title,
        type,
        content: getDefaultContent(type),
        createdAt: new Date(),
        updatedAt: new Date()
      }
      setDocuments(prev => [...prev, doc])
      setCurrentDocument(doc)
      return doc
    } finally {
      setIsLoading(false)
    }
  }, [])

  const updateDocument = useCallback(async (id, updates) => {
    setDocuments(prev => 
      prev.map(doc => 
        doc.id === id 
          ? { ...doc, ...updates, updatedAt: new Date() }
          : doc
      )
    )
    if (currentDocument?.id === id) {
      setCurrentDocument(prev => ({ ...prev, ...updates }))
    }
  }, [currentDocument])

  const getDefaultContent = (type) => {
    switch (type) {
      case 'writer':
        return { type: 'doc', content: [] }
      case 'spreadsheet':
        return { sheets: [{ name: 'Sheet1', data: [] }] }
      case 'presentation':
        return { slides: [] }
      case 'pdf':
        return { pages: [] }
      default:
        return {}
    }
  }

  const value = {
    currentDocument,
    documents,
    isLoading,
    collaborators,
    createDocument,
    updateDocument,
    setCurrentDocument,
    setDocuments
  }

  return (
    <DocumentContext.Provider value={value}>
      {children}
    </DocumentContext.Provider>
  )
}