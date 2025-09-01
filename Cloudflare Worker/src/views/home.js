/**
 * Home page view - CSV upload interface
 */

export function renderHomePage(error = null) {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Ingredient Tracker</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="navbar-brand">
                <i class="fas fa-utensils"></i> Restaurant Ingredient Tracker
            </a>
        </div>
    </nav>

    <div class="container">
        ${error ? `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i> ${error}
        </div>
        ` : ''}

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h2><i class="fas fa-upload"></i> Upload CSV Files</h2>
                    </div>
                    <div class="card-body">
                        <p>Upload your restaurant ingredient data to analyze usage, waste, and costs. This tool helps identify shrinkage, track expenses, and optimize inventory management.</p>
                        
                        <form action="/upload" method="post" enctype="multipart/form-data">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="ingredient_info">
                                            <i class="fas fa-info-circle"></i> Ingredient Information CSV
                                        </label>
                                        <small>Required columns: Ingredient, Unit Cost</small>
                                        <input type="file" name="ingredient_info" id="ingredient_info" accept=".csv" class="form-control" required>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="input_stock">
                                            <i class="fas fa-box"></i> Input Stock CSV
                                        </label>
                                        <small>Required columns: Ingredient, Received Qty</small>
                                        <input type="file" name="input_stock" id="input_stock" accept=".csv" class="form-control" required>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="usage">
                                            <i class="fas fa-chart-line"></i> Usage CSV
                                        </label>
                                        <small>Required columns: Ingredient, Used Qty</small>
                                        <input type="file" name="usage" id="usage" accept=".csv" class="form-control" required>
                                    </div>
                                </div>
                                
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="waste">
                                            <i class="fas fa-trash"></i> Waste CSV
                                        </label>
                                        <small>Required columns: Ingredient, Wasted Qty</small>
                                        <input type="file" name="waste" id="waste" accept=".csv" class="form-control" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="text-center">
                                <button type="submit" class="btn btn-success">
                                    <i class="fas fa-upload"></i> Process Files
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-eye"></i> Try Sample Data</h3>
                    </div>
                    <div class="card-body">
                        <p>Don't have data ready? Try our sample dataset to see how the system works with restaurant ingredient data.</p>
                        <a href="/sample-data" class="btn btn-secondary">
                            <i class="fas fa-database"></i> Load Sample Data
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-chart-bar"></i> Features</h4>
                    </div>
                    <div class="card-body">
                        <ul>
                            <li><strong>Cost Analysis:</strong> Track ingredient costs and identify expensive items</li>
                            <li><strong>Waste Tracking:</strong> Monitor food waste percentages and costs</li>
                            <li><strong>Shrinkage Detection:</strong> Identify missing inventory (theft/spoilage)</li>
                            <li><strong>Interactive Analytics:</strong> Filter and sort data by various metrics</li>
                            <li><strong>Export Reports:</strong> Generate PDF and Excel reports</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-file-csv"></i> CSV Format Guide</h4>
                    </div>
                    <div class="card-body">
                        <p><strong>Ingredient Info:</strong> Ingredient, Unit Cost</p>
                        <p><strong>Input Stock:</strong> Ingredient, Received Qty</p>
                        <p><strong>Usage:</strong> Ingredient, Used Qty</p>
                        <p><strong>Waste:</strong> Ingredient, Wasted Qty</p>
                        
                        <small class="text-muted">
                            All files must use comma-separated values with headers in the first row.
                            Ingredient names must match exactly across all files.
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
  `
}