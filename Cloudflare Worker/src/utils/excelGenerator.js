/**
 * Excel generation utilities using XLSX
 */
import * as XLSX from 'xlsx'
import { calculateSummaryStats, getInsights } from './dataProcessor'

export async function generateExcel(results) {
  try {
    const workbook = XLSX.utils.book_new()
    const summaryStats = calculateSummaryStats(results)
    const insights = getInsights(results)
    
    // Summary Sheet
    const summaryData = [
      ['Restaurant Ingredient Tracker Report'],
      ['Generated:', new Date().toLocaleDateString()],
      [''],
      ['Summary Statistics'],
      ['Total Ingredients', summaryStats.totalIngredients],
      ['Total Cost', summaryStats.totalCost],
      ['Total Waste Cost', summaryStats.totalWasteCost],
      ['Total Shrinkage Cost', summaryStats.totalShrinkageCost],
      ['Average Waste %', summaryStats.averageWastePercentage],
      ['Average Shrinkage %', summaryStats.averageShrinkagePercentage],
      [''],
      ['Key Insights'],
      ...insights.map(insight => [insight])
    ]
    
    const summarySheet = XLSX.utils.aoa_to_sheet(summaryData)
    
    // Style the summary sheet
    summarySheet['!cols'] = [{ width: 30 }, { width: 20 }]
    
    XLSX.utils.book_append_sheet(workbook, summarySheet, 'Summary')
    
    // Detailed Data Sheet
    const detailedData = results.map(item => ({
      'Ingredient': item.Ingredient || '',
      'Unit Cost': item['Unit Cost'] || 0,
      'Received Qty': item['Received Qty'] || 0,
      'Used Qty': item['Used Qty'] || 0,
      'Wasted Qty': item['Wasted Qty'] || 0,
      'Expected Use': item['Expected Use'] || 0,
      'Shrinkage': item['Shrinkage'] || 0,
      'Used Cost': item['Used Cost'] || 0,
      'Waste Cost': item['Waste Cost'] || 0,
      'Shrinkage Cost': item['Shrinkage Cost'] || 0,
      'Total Cost': item['Total Cost'] || 0,
      'Waste %': item['Waste %'] || 0,
      'Shrinkage %': item['Shrinkage %'] || 0
    }))
    
    const detailedSheet = XLSX.utils.json_to_sheet(detailedData)
    
    // Set column widths
    detailedSheet['!cols'] = [
      { width: 20 }, // Ingredient
      { width: 12 }, // Unit Cost
      { width: 12 }, // Received Qty
      { width: 12 }, // Used Qty
      { width: 12 }, // Wasted Qty
      { width: 12 }, // Expected Use
      { width: 12 }, // Shrinkage
      { width: 12 }, // Used Cost
      { width: 12 }, // Waste Cost
      { width: 15 }, // Shrinkage Cost
      { width: 12 }, // Total Cost
      { width: 10 }, // Waste %
      { width: 12 }  // Shrinkage %
    ]
    
    XLSX.utils.book_append_sheet(workbook, detailedSheet, 'Detailed Data')
    
    // High Risk Items Sheet
    const highRiskItems = results.filter(item => 
      (item['Shrinkage Cost'] || 0) > 10 || (item['Waste %'] || 0) > 15
    ).sort((a, b) => {
      const aShrinkage = a['Shrinkage Cost'] || 0
      const bShrinkage = b['Shrinkage Cost'] || 0
      return bShrinkage - aShrinkage
    })
    
    if (highRiskItems.length > 0) {
      const highRiskData = highRiskItems.map(item => ({
        'Ingredient': item.Ingredient || '',
        'Issue Type': getIssueType(item),
        'Shrinkage Cost': item['Shrinkage Cost'] || 0,
        'Waste %': item['Waste %'] || 0,
        'Total Cost Impact': (item['Shrinkage Cost'] || 0) + (item['Waste Cost'] || 0),
        'Recommendation': getRecommendation(item)
      }))
      
      const highRiskSheet = XLSX.utils.json_to_sheet(highRiskData)
      highRiskSheet['!cols'] = [
        { width: 20 }, // Ingredient
        { width: 15 }, // Issue Type
        { width: 15 }, // Shrinkage Cost
        { width: 10 }, // Waste %
        { width: 15 }, // Total Cost Impact
        { width: 40 }  // Recommendation
      ]
      
      XLSX.utils.book_append_sheet(workbook, highRiskSheet, 'High Risk Items')
    }
    
    // Cost Analysis Sheet
    const costAnalysisData = [
      ['Cost Breakdown Analysis'],
      [''],
      ['Category', 'Amount', 'Percentage of Total'],
      ['Used Cost', summaryStats.totalCost - summaryStats.totalWasteCost - summaryStats.totalShrinkageCost, ((summaryStats.totalCost - summaryStats.totalWasteCost - summaryStats.totalShrinkageCost) / summaryStats.totalCost * 100).toFixed(1) + '%'],
      ['Waste Cost', summaryStats.totalWasteCost, (summaryStats.totalWasteCost / summaryStats.totalCost * 100).toFixed(1) + '%'],
      ['Shrinkage Cost', summaryStats.totalShrinkageCost, (summaryStats.totalShrinkageCost / summaryStats.totalCost * 100).toFixed(1) + '%'],
      ['Total Cost', summaryStats.totalCost, '100.0%'],
      [''],
      ['Top Cost Drivers'],
      ['Ingredient', 'Total Cost', 'Impact'],
      ...results
        .sort((a, b) => (b['Total Cost'] || 0) - (a['Total Cost'] || 0))
        .slice(0, 10)
        .map(item => [
          item.Ingredient || '',
          item['Total Cost'] || 0,
          ((item['Total Cost'] || 0) / summaryStats.totalCost * 100).toFixed(1) + '%'
        ])
    ]
    
    const costAnalysisSheet = XLSX.utils.aoa_to_sheet(costAnalysisData)
    costAnalysisSheet['!cols'] = [{ width: 20 }, { width: 15 }, { width: 15 }]
    
    XLSX.utils.book_append_sheet(workbook, costAnalysisSheet, 'Cost Analysis')
    
    // Generate buffer
    const buffer = XLSX.write(workbook, { 
      type: 'array',
      bookType: 'xlsx'
    })
    
    return buffer
    
  } catch (error) {
    console.error('Excel generation error:', error)
    throw new Error(`Failed to generate Excel: ${error.message}`)
  }
}

function getIssueType(item) {
  const shrinkageCost = item['Shrinkage Cost'] || 0
  const wastePercent = item['Waste %'] || 0
  
  if (shrinkageCost > 10 && wastePercent > 15) {
    return 'High Shrinkage & Waste'
  } else if (shrinkageCost > 10) {
    return 'High Shrinkage'
  } else if (wastePercent > 15) {
    return 'High Waste'
  } else {
    return 'At Risk'
  }
}

function getRecommendation(item) {
  const shrinkageCost = item['Shrinkage Cost'] || 0
  const wastePercent = item['Waste %'] || 0
  const receivedQty = item['Received Qty'] || 0
  
  if (receivedQty === 0) {
    return 'Check inventory management - no stock received'
  } else if (shrinkageCost > 20) {
    return 'Critical: Investigate theft/spoilage, improve security measures'
  } else if (shrinkageCost > 10) {
    return 'Review portion control and inventory tracking procedures'
  } else if (wastePercent > 25) {
    return 'High waste: Review preparation methods and order quantities'
  } else if (wastePercent > 15) {
    return 'Monitor expiration dates and optimize menu planning'
  } else {
    return 'Continue monitoring for trends'
  }
}