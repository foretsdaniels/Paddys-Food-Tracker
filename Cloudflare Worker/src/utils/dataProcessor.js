/**
 * Data processing utilities for CSV analysis
 */

export async function processCSVData(csvData) {
  try {
    // Parse CSV data into objects
    const ingredientInfo = parseCSV(csvData.ingredient_info)
    const inputStock = parseCSV(csvData.input_stock)
    const usage = parseCSV(csvData.usage)
    const waste = parseCSV(csvData.waste)
    
    // Validate data structure
    validateCSVStructure(ingredientInfo, 'ingredient_info', ['Ingredient', 'Unit Cost'])
    validateCSVStructure(inputStock, 'input_stock', ['Ingredient', 'Received Qty'])
    validateCSVStructure(usage, 'usage', ['Ingredient', 'Used Qty'])
    validateCSVStructure(waste, 'waste', ['Ingredient', 'Wasted Qty'])
    
    // Create lookup maps for faster processing
    const stockMap = createLookupMap(inputStock, 'Ingredient', 'Received Qty')
    const usageMap = createLookupMap(usage, 'Ingredient', 'Used Qty')
    const wasteMap = createLookupMap(waste, 'Ingredient', 'Wasted Qty')
    
    // Process each ingredient
    const results = ingredientInfo.map(ingredient => {
      const name = ingredient.Ingredient
      const unitCost = parseFloat(ingredient['Unit Cost']) || 0
      const receivedQty = parseFloat(stockMap[name]) || 0
      const usedQty = parseFloat(usageMap[name]) || 0
      const wastedQty = parseFloat(wasteMap[name]) || 0
      
      // Calculate metrics
      const expectedUse = usedQty + wastedQty
      const shrinkage = receivedQty - expectedUse
      
      // Calculate costs
      const usedCost = usedQty * unitCost
      const wasteCost = wastedQty * unitCost
      const shrinkageCost = shrinkage * unitCost
      const totalCost = receivedQty * unitCost
      
      // Calculate percentages
      const wastePercentage = receivedQty > 0 ? (wastedQty / receivedQty) * 100 : 0
      const shrinkagePercentage = receivedQty > 0 ? (shrinkage / receivedQty) * 100 : 0
      
      return {
        Ingredient: name,
        'Unit Cost': unitCost,
        'Received Qty': receivedQty,
        'Used Qty': usedQty,
        'Wasted Qty': wastedQty,
        'Expected Use': expectedUse,
        Shrinkage: shrinkage,
        'Used Cost': usedCost,
        'Waste Cost': wasteCost,
        'Shrinkage Cost': shrinkageCost,
        'Total Cost': totalCost,
        'Waste %': wastePercentage,
        'Shrinkage %': shrinkagePercentage
      }
    })
    
    return results
    
  } catch (error) {
    console.error('Data processing error:', error)
    throw new Error(`Failed to process CSV data: ${error.message}`)
  }
}

function parseCSV(csvText) {
  const lines = csvText.trim().split('\n')
  if (lines.length < 2) {
    throw new Error('CSV must have at least a header and one data row')
  }
  
  const headers = lines[0].split(',').map(h => h.trim())
  const data = []
  
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim())
    if (values.length !== headers.length) {
      console.warn(`Row ${i + 1} has ${values.length} values but expected ${headers.length}`)
      continue
    }
    
    const row = {}
    headers.forEach((header, index) => {
      row[header] = values[index]
    })
    data.push(row)
  }
  
  return data
}

function validateCSVStructure(data, fileName, requiredColumns) {
  if (!data || data.length === 0) {
    throw new Error(`${fileName} is empty or invalid`)
  }
  
  const actualColumns = Object.keys(data[0])
  const missingColumns = requiredColumns.filter(col => !actualColumns.includes(col))
  
  if (missingColumns.length > 0) {
    throw new Error(`${fileName} is missing required columns: ${missingColumns.join(', ')}`)
  }
}

function createLookupMap(data, keyColumn, valueColumn) {
  const map = {}
  data.forEach(row => {
    map[row[keyColumn]] = row[valueColumn]
  })
  return map
}

export function calculateSummaryStats(results) {
  if (!results || results.length === 0) {
    return {
      totalIngredients: 0,
      totalCost: 0,
      totalWasteCost: 0,
      totalShrinkageCost: 0,
      averageWastePercentage: 0,
      averageShrinkagePercentage: 0
    }
  }
  
  const totalIngredients = results.length
  const totalCost = results.reduce((sum, item) => sum + (item['Total Cost'] || 0), 0)
  const totalWasteCost = results.reduce((sum, item) => sum + (item['Waste Cost'] || 0), 0)
  const totalShrinkageCost = results.reduce((sum, item) => sum + (item['Shrinkage Cost'] || 0), 0)
  
  const averageWastePercentage = results.reduce((sum, item) => sum + (item['Waste %'] || 0), 0) / totalIngredients
  const averageShrinkagePercentage = results.reduce((sum, item) => sum + (item['Shrinkage %'] || 0), 0) / totalIngredients
  
  return {
    totalIngredients,
    totalCost: Math.round(totalCost * 100) / 100,
    totalWasteCost: Math.round(totalWasteCost * 100) / 100,
    totalShrinkageCost: Math.round(totalShrinkageCost * 100) / 100,
    averageWastePercentage: Math.round(averageWastePercentage * 100) / 100,
    averageShrinkagePercentage: Math.round(averageShrinkagePercentage * 100) / 100
  }
}

export function getInsights(results) {
  if (!results || results.length === 0) {
    return []
  }
  
  const insights = []
  
  // High waste items
  const highWasteItems = results.filter(item => (item['Waste %'] || 0) > 15)
  if (highWasteItems.length > 0) {
    insights.push(`High waste detected: ${highWasteItems.length} items have >15% waste`)
  }
  
  // High shrinkage items
  const highShrinkageItems = results.filter(item => (item['Shrinkage Cost'] || 0) > 10)
  if (highShrinkageItems.length > 0) {
    insights.push(`Significant shrinkage: ${highShrinkageItems.length} items have >$10 shrinkage cost`)
  }
  
  // Missing stock items
  const missingStockItems = results.filter(item => (item['Received Qty'] || 0) === 0)
  if (missingStockItems.length > 0) {
    insights.push(`Missing stock: ${missingStockItems.length} items not received`)
  }
  
  return insights
}

export function filterResults(results, filterType) {
  if (!results || filterType === 'all') {
    return results
  }
  
  switch (filterType) {
    case 'high_waste':
      return results.filter(item => (item['Waste %'] || 0) > 10)
    case 'high_shrinkage':
      return results.filter(item => (item['Shrinkage Cost'] || 0) > 10)
    case 'missing_stock':
      return results.filter(item => (item['Received Qty'] || 0) === 0)
    case 'profitable':
      return results.filter(item => (item['Shrinkage Cost'] || 0) <= 0 && (item['Waste %'] || 0) <= 5)
    default:
      return results
  }
}

export function sortResults(results, sortBy, sortOrder = 'desc') {
  if (!results || results.length === 0) {
    return results
  }
  
  const columnMapping = {
    'shrinkage_cost': 'Shrinkage Cost',
    'total_cost': 'Total Cost',
    'waste_cost': 'Waste Cost',
    'used_cost': 'Used Cost',
    'waste_percentage': 'Waste %',
    'shrinkage_percentage': 'Shrinkage %',
    'received_qty': 'Received Qty',
    'used_qty': 'Used Qty',
    'wasted_qty': 'Wasted Qty',
    'ingredient': 'Ingredient',
    'unit_cost': 'Unit Cost'
  }
  
  const columnName = columnMapping[sortBy] || sortBy
  
  return results.sort((a, b) => {
    let aVal = a[columnName]
    let bVal = b[columnName]
    
    // Handle string vs number comparison
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      aVal = aVal.toLowerCase()
      bVal = bVal.toLowerCase()
    } else {
      aVal = parseFloat(aVal) || 0
      bVal = parseFloat(bVal) || 0
    }
    
    if (sortOrder === 'asc') {
      return aVal > bVal ? 1 : (aVal < bVal ? -1 : 0)
    } else {
      return aVal < bVal ? 1 : (aVal > bVal ? -1 : 0)
    }
  })
}