/**
 * PDF generation utilities using jsPDF
 */
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import { calculateSummaryStats } from './dataProcessor'

export async function generatePDF(results) {
  try {
    const doc = new jsPDF()
    const summaryStats = calculateSummaryStats(results)
    
    // Title
    doc.setFontSize(20)
    doc.text('Restaurant Ingredient Tracker Report', 20, 20)
    
    // Date
    doc.setFontSize(12)
    doc.text(`Generated: ${new Date().toLocaleDateString()}`, 20, 30)
    
    // Summary Statistics
    doc.setFontSize(16)
    doc.text('Summary Statistics', 20, 45)
    
    doc.setFontSize(12)
    let yPos = 55
    
    const summaryData = [
      ['Total Ingredients', summaryStats.totalIngredients.toString()],
      ['Total Cost', `$${summaryStats.totalCost.toFixed(2)}`],
      ['Total Waste Cost', `$${summaryStats.totalWasteCost.toFixed(2)}`],
      ['Total Shrinkage Cost', `$${summaryStats.totalShrinkageCost.toFixed(2)}`],
      ['Average Waste %', `${summaryStats.averageWastePercentage.toFixed(1)}%`],
      ['Average Shrinkage %', `${summaryStats.averageShrinkagePercentage.toFixed(1)}%`]
    ]
    
    summaryData.forEach(([label, value]) => {
      doc.text(`${label}: ${value}`, 20, yPos)
      yPos += 8
    })
    
    // Top Issues
    yPos += 10
    doc.setFontSize(16)
    doc.text('Top Issues', 20, yPos)
    yPos += 10
    
    doc.setFontSize(12)
    
    // High shrinkage items
    const highShrinkageItems = results
      .filter(item => (item['Shrinkage Cost'] || 0) > 10)
      .sort((a, b) => (b['Shrinkage Cost'] || 0) - (a['Shrinkage Cost'] || 0))
      .slice(0, 5)
    
    if (highShrinkageItems.length > 0) {
      doc.text('Highest Shrinkage Items:', 20, yPos)
      yPos += 8
      
      highShrinkageItems.forEach(item => {
        doc.text(`- ${item.Ingredient}: $${(item['Shrinkage Cost'] || 0).toFixed(2)}`, 25, yPos)
        yPos += 6
      })
      yPos += 5
    }
    
    // High waste items
    const highWasteItems = results
      .filter(item => (item['Waste %'] || 0) > 15)
      .sort((a, b) => (b['Waste %'] || 0) - (a['Waste %'] || 0))
      .slice(0, 5)
    
    if (highWasteItems.length > 0) {
      doc.text('Highest Waste Items:', 20, yPos)
      yPos += 8
      
      highWasteItems.forEach(item => {
        doc.text(`- ${item.Ingredient}: ${(item['Waste %'] || 0).toFixed(1)}%`, 25, yPos)
        yPos += 6
      })
    }
    
    // New page for detailed data
    doc.addPage()
    
    // Detailed Table
    doc.setFontSize(16)
    doc.text('Detailed Breakdown', 20, 20)
    
    // Prepare table data
    const tableHeaders = [
      'Ingredient',
      'Unit Cost',
      'Received',
      'Used',
      'Wasted',
      'Shrinkage',
      'Waste %',
      'Shrinkage Cost'
    ]
    
    const tableData = results.map(item => [
      item.Ingredient || '',
      `$${(item['Unit Cost'] || 0).toFixed(2)}`,
      (item['Received Qty'] || 0).toString(),
      (item['Used Qty'] || 0).toString(),
      (item['Wasted Qty'] || 0).toString(),
      (item['Shrinkage'] || 0).toFixed(1),
      `${(item['Waste %'] || 0).toFixed(1)}%`,
      `$${(item['Shrinkage Cost'] || 0).toFixed(2)}`
    ])
    
    // Generate table
    doc.autoTable({
      head: [tableHeaders],
      body: tableData,
      startY: 30,
      styles: {
        fontSize: 9,
        cellPadding: 3
      },
      headStyles: {
        fillColor: [66, 139, 202],
        textColor: [255, 255, 255]
      },
      alternateRowStyles: {
        fillColor: [245, 245, 245]
      },
      columnStyles: {
        1: { halign: 'right' }, // Unit Cost
        2: { halign: 'center' }, // Received
        3: { halign: 'center' }, // Used
        4: { halign: 'center' }, // Wasted
        5: { halign: 'center' }, // Shrinkage
        6: { halign: 'right' }, // Waste %
        7: { halign: 'right' }  // Shrinkage Cost
      }
    })
    
    // Footer
    const pageCount = doc.internal.getNumberOfPages()
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      doc.setFontSize(10)
      doc.text(`Page ${i} of ${pageCount}`, 20, doc.internal.pageSize.height - 10)
      doc.text('Restaurant Ingredient Tracker', doc.internal.pageSize.width - 60, doc.internal.pageSize.height - 10)
    }
    
    return doc.output('arraybuffer')
    
  } catch (error) {
    console.error('PDF generation error:', error)
    throw new Error(`Failed to generate PDF: ${error.message}`)
  }
}