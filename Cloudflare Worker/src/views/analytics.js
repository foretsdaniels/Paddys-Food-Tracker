/**
 * Analytics page view - data analysis and filtering
 */

import { calculateSummaryStats, getInsights, filterResults, sortResults } from '../utils/dataProcessor'

export function renderAnalyticsPage(results, sessionId, filterType = 'all', sortBy = 'shrinkage_cost', sortOrder = 'desc') {
  const summaryStats = calculateSummaryStats(results)
  const insights = getInsights(results)
  
  // Apply filters and sorting
  const filteredResults = filterResults(results, filterType)
  const sortedResults = sortResults(filteredResults, sortBy, sortOrder)
  
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - Restaurant Ingredient Tracker</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="navbar-brand">
                <i class="fas fa-utensils"></i> Restaurant Ingredient Tracker
            </a>
            <div class="float-end">
                <a href="/reports?session=${sessionId}" class="btn btn-secondary">
                    <i class="fas fa-file-alt"></i> Reports
                </a>
                <a href="/" class="btn btn-secondary">
                    <i class="fas fa-upload"></i> New Upload
                </a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1><i class="fas fa-chart-line"></i> Analytics Dashboard</h1>
        </div>

        <!-- Summary Statistics -->
        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h3 class="text-success">$${summaryStats.totalCost.toFixed(2)}</h3>
                        <p>Total Cost</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h3 class="text-danger">$${summaryStats.totalShrinkageCost.toFixed(2)}</h3>
                        <p>Shrinkage Cost</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <h3 class="text-warning">$${summaryStats.totalWasteCost.toFixed(2)}</h3>
                        <p>Waste Cost</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Key Insights -->
        ${insights.length > 0 ? `
        <div class="alert alert-warning">
            <h5><i class="fas fa-exclamation-triangle"></i> Key Insights</h5>
            <ul>
                ${insights.map(insight => `<li>${insight}</li>`).join('')}
            </ul>
        </div>
        ` : ''}

        <!-- Filters and Controls -->
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-filter"></i> Filters & Sorting</h5>
            </div>
            <div class="card-body">
                <form method="get" class="row">
                    <input type="hidden" name="session" value="${sessionId}">
                    
                    <div class="col-md-4">
                        <label>Filter by Issue Type:</label>
                        <select name="filter" class="form-control" onchange="this.form.submit()">
                            <option value="all" ${filterType === 'all' ? 'selected' : ''}>All Items</option>
                            <option value="high_shrinkage" ${filterType === 'high_shrinkage' ? 'selected' : ''}>High Shrinkage (>$10)</option>
                            <option value="high_waste" ${filterType === 'high_waste' ? 'selected' : ''}>High Waste (>10%)</option>
                            <option value="missing_stock" ${filterType === 'missing_stock' ? 'selected' : ''}>Missing Stock</option>
                            <option value="profitable" ${filterType === 'profitable' ? 'selected' : ''}>Well Managed</option>
                        </select>
                    </div>
                    
                    <div class="col-md-4">
                        <label>Sort by:</label>
                        <select name="sort" class="form-control" onchange="this.form.submit()">
                            <option value="shrinkage_cost" ${sortBy === 'shrinkage_cost' ? 'selected' : ''}>Shrinkage Cost</option>
                            <option value="total_cost" ${sortBy === 'total_cost' ? 'selected' : ''}>Total Cost</option>
                            <option value="waste_percentage" ${sortBy === 'waste_percentage' ? 'selected' : ''}>Waste Percentage</option>
                            <option value="ingredient" ${sortBy === 'ingredient' ? 'selected' : ''}>Ingredient Name</option>
                        </select>
                    </div>
                    
                    <div class="col-md-4">
                        <label>Sort Order:</label>
                        <select name="order" class="form-control" onchange="this.form.submit()">
                            <option value="desc" ${sortOrder === 'desc' ? 'selected' : ''}>High to Low</option>
                            <option value="asc" ${sortOrder === 'asc' ? 'selected' : ''}>Low to High</option>
                        </select>
                    </div>
                </form>
            </div>
        </div>

        <!-- Results Table -->
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-table"></i> Ingredient Analysis (${sortedResults.length} items)</h5>
            </div>
            <div class="card-body">
                <div style="overflow-x: auto;">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Ingredient</th>
                                <th>Unit Cost</th>
                                <th>Received</th>
                                <th>Used</th>
                                <th>Wasted</th>
                                <th>Shrinkage</th>
                                <th>Waste %</th>
                                <th>Shrinkage Cost</th>
                                <th>Total Cost</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${sortedResults.map(item => {
                              const shrinkageCost = item['Shrinkage Cost'] || 0
                              const wastePercent = item['Waste %'] || 0
                              const receivedQty = item['Received Qty'] || 0
                              
                              let rowClass = ''
                              if (shrinkageCost > 10) rowClass = 'bg-danger'
                              else if (receivedQty === 0) rowClass = 'bg-warning'
                              
                              return `
                                <tr class="${rowClass}">
                                    <td><strong>${item.Ingredient || ''}</strong></td>
                                    <td>$${(item['Unit Cost'] || 0).toFixed(2)}</td>
                                    <td>${receivedQty}</td>
                                    <td>${item['Used Qty'] || 0}</td>
                                    <td>${item['Wasted Qty'] || 0}</td>
                                    <td>${(item['Shrinkage'] || 0).toFixed(1)}</td>
                                    <td>${wastePercent.toFixed(1)}%</td>
                                    <td class="${shrinkageCost > 10 ? 'text-danger' : ''}">
                                        $${shrinkageCost.toFixed(2)}
                                    </td>
                                    <td>$${(item['Total Cost'] || 0).toFixed(2)}</td>
                                </tr>
                              `
                            }).join('')}
                        </tbody>
                    </table>
                </div>
                
                ${sortedResults.length === 0 ? `
                <div class="text-center">
                    <p>No items match the current filter criteria.</p>
                </div>
                ` : ''}
            </div>
        </div>

        <!-- Legend -->
        <div class="card">
            <div class="card-body">
                <h6>Legend:</h6>
                <div class="row">
                    <div class="col-md-6">
                        <span class="bg-danger" style="padding: 2px 8px; color: white;">High Shrinkage</span> - Shrinkage cost > $10
                    </div>
                    <div class="col-md-6">
                        <span class="bg-warning" style="padding: 2px 8px;">Missing Stock</span> - No stock received
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
  `
}