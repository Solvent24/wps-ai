import React, { useState, useEffect } from 'react'
import { useDocument } from '../../contexts/DocumentContext'

const SpreadsheetEditor = () => {
  const { currentDocument, updateDocument } = useDocument()
  const [sheetData, setSheetData] = useState([])
  const [selectedCell, setSelectedCell] = useState({ row: 0, col: 0 })

  useEffect(() => {
    if (currentDocument?.content?.sheets?.[0]?.data) {
      setSheetData(currentDocument.content.sheets[0].data)
    } else {
      // Initialize empty spreadsheet
      const initialData = Array(20).fill().map(() => Array(10).fill(''))
      setSheetData(initialData)
    }
  }, [currentDocument])

  const handleCellChange = (row, col, value) => {
    const newData = [...sheetData]
    newData[row][col] = value
    setSheetData(newData)
    
    if (currentDocument) {
      updateDocument(currentDocument.id, {
        content: { 
          sheets: [{ 
            name: 'Sheet1', 
            data: newData 
          }] 
        }
      })
    }
  }

  return (
    <div className="spreadsheet-editor">
      <table className="spreadsheet-table">
        <tbody>
          {sheetData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, colIndex) => (
                <td 
                  key={colIndex}
                  className={`spreadsheet-cell ${
                    selectedCell.row === rowIndex && selectedCell.col === colIndex ? 'selected' : ''
                  }`}
                  onClick={() => setSelectedCell({ row: rowIndex, col: colIndex })}
                >
                  <input
                    type="text"
                    className="cell-input"
                    value={cell}
                    onChange={(e) => handleCellChange(rowIndex, colIndex, e.target.value)}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default SpreadsheetEditor