/**
 * Reports page view - export functionality
 */

export function renderReportsPage(sessionId) {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reports - Restaurant Ingredient Tracker</title>
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
                <a href="/analytics?session=${sessionId}" class="btn btn-secondary">
                    <i class="fas fa-chart-line"></i> Analytics
                </a>
                <a href="/" class="btn btn-secondary">
                    <i class="fas fa-upload"></i> New Upload
                </a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1><i class="fas fa-file-alt"></i> Export Reports</h1>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-file-pdf text-danger"></i> PDF Report</h5>
                    </div>
                    <div class="card-body">
                        <p>Generate a comprehensive PDF report with:</p>
                        <ul>
                            <li>Executive summary with key metrics</li>
                            <li>Top problematic items highlighting</li>
                            <li>Detailed breakdown table with all data</li>
                            <li>Professional formatting for presentations</li>
                        </ul>
                        <a href="/export/pdf?session=${sessionId}" class="btn btn-danger" target="_blank">
                            <i class="fas fa-download"></i> Download PDF Report
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-file-excel text-success"></i> Excel Report</h5>
                    </div>
                    <div class="card-body">
                        <p>Generate a detailed Excel workbook with:</p>
                        <ul>
                            <li>Multiple worksheets for different analyses</li>
                            <li>Summary statistics and cost breakdowns</li>
                            <li>High-risk items with recommendations</li>
                            <li>Detailed data for further analysis</li>
                        </ul>
                        <a href="/export/excel?session=${sessionId}" class="btn btn-success" target="_blank">
                            <i class="fas fa-download"></i> Download Excel Report
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Report Contents</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>📊 Summary Statistics</h6>
                                <ul>
                                    <li>Total ingredients analyzed</li>
                                    <li>Complete cost breakdown analysis</li>
                                    <li>Average waste and shrinkage percentages</li>
                                    <li>Cost impact assessments</li>
                                </ul>
                                
                                <h6>🔍 Detailed Analysis</h6>
                                <ul>
                                    <li>Individual ingredient performance</li>
                                    <li>Usage vs. waste ratios</li>
                                    <li>Shrinkage cost calculations</li>
                                    <li>Efficiency metrics</li>
                                </ul>
                            </div>
                            
                            <div class="col-md-6">
                                <h6>⚠️ Risk Assessment</h6>
                                <ul>
                                    <li>High-cost shrinkage items</li>
                                    <li>Excessive waste identification</li>
                                    <li>Missing inventory alerts</li>
                                    <li>Actionable recommendations</li>
                                </ul>
                                
                                <h6>💡 Insights & Recommendations</h6>
                                <ul>
                                    <li>Cost optimization opportunities</li>
                                    <li>Inventory management improvements</li>
                                    <li>Waste reduction strategies</li>
                                    <li>Portion control suggestions</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-question-circle"></i> How to Use Reports</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                <h6>For Management</h6>
                                <p>Use the <strong>PDF report</strong> for executive presentations and stakeholder meetings. It provides a clear overview of costs and key issues.</p>
                            </div>
                            
                            <div class="col-md-4">
                                <h6>For Kitchen Staff</h6>
                                <p>Focus on the <strong>high-risk items</strong> section to identify which ingredients need improved handling and portion control.</p>
                            </div>
                            
                            <div class="col-md-4">
                                <h6>For Accounting</h6>
                                <p>Use the <strong>Excel report</strong> for detailed financial analysis and integration with existing accounting systems.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
  `
}