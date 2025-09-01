import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { html } from 'hono/html'
import { processCSVData } from './utils/dataProcessor'
import { generatePDF } from './utils/pdfGenerator'
import { generateExcel } from './utils/excelGenerator'
import { renderHomePage } from './views/home'
import { renderAnalyticsPage } from './views/analytics'
import { renderReportsPage } from './views/reports'

const app = new Hono()

// CORS middleware for cross-origin requests
app.use('*', cors({
  origin: '*',
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
}))

// Static file serving for CSS and assets
app.get('/static/*', async (c) => {
  const path = c.req.path.replace('/static/', '')
  
  // Basic CSS for the application
  if (path === 'style.css') {
    return c.text(`
/* Bootstrap-inspired CSS for Restaurant Ingredient Tracker */
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f8f9fa; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.navbar { background-color: #343a40; color: white; padding: 1rem 0; margin-bottom: 2rem; }
.navbar-brand { font-size: 1.5rem; font-weight: bold; color: white; text-decoration: none; }
.card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem; }
.card-header { background-color: #f8f9fa; border-bottom: 1px solid #dee2e6; padding: 1rem; font-weight: bold; }
.card-body { padding: 1.5rem; }
.btn { display: inline-block; padding: 0.5rem 1rem; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; margin: 0.5rem 0.5rem 0.5rem 0; }
.btn:hover { background-color: #0056b3; }
.btn-success { background-color: #28a745; }
.btn-success:hover { background-color: #1e7e34; }
.btn-danger { background-color: #dc3545; }
.btn-danger:hover { background-color: #c82333; }
.btn-secondary { background-color: #6c757d; }
.btn-secondary:hover { background-color: #545b62; }
.alert { padding: 1rem; margin-bottom: 1rem; border-radius: 4px; }
.alert-success { background-color: #d4edda; border-color: #c3e6cb; color: #155724; }
.alert-danger { background-color: #f8d7da; border-color: #f5c6cb; color: #721c24; }
.alert-warning { background-color: #fff3cd; border-color: #ffeaa7; color: #856404; }
.form-group { margin-bottom: 1rem; }
.form-control { width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; }
.table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
.table th, .table td { padding: 0.75rem; border-bottom: 1px solid #dee2e6; text-align: left; }
.table th { background-color: #f8f9fa; font-weight: bold; }
.table-striped tbody tr:nth-child(odd) { background-color: #f8f9fa; }
.row { display: flex; flex-wrap: wrap; margin: -15px; }
.col-md-6 { flex: 0 0 50%; max-width: 50%; padding: 15px; }
.col-md-4 { flex: 0 0 33.333333%; max-width: 33.333333%; padding: 15px; }
.col-12 { flex: 0 0 100%; max-width: 100%; padding: 15px; }
.text-center { text-align: center; }
.text-danger { color: #dc3545; }
.text-success { color: #28a745; }
.bg-warning { background-color: #fff3cd; }
.bg-danger { background-color: #f8d7da; }
.float-end { float: right; }
@media (max-width: 768px) { .col-md-6, .col-md-4 { flex: 0 0 100%; max-width: 100%; } }
    `, {
      headers: { 'Content-Type': 'text/css' }
    })
  }
  
  return c.text('Not Found', 404)
})

// Home page - upload interface
app.get('/', (c) => {
  return c.html(renderHomePage())
})

// Process CSV upload
app.post('/upload', async (c) => {
  try {
    const formData = await c.req.formData()
    
    // Extract CSV files from form data
    const files = {
      ingredient_info: formData.get('ingredient_info'),
      input_stock: formData.get('input_stock'),
      usage: formData.get('usage'),
      waste: formData.get('waste')
    }
    
    // Validate that all files are present
    for (const [key, file] of Object.entries(files)) {
      if (!file || file.size === 0) {
        return c.html(renderHomePage(`Missing required file: ${key.replace('_', ' ')}`))
      }
    }
    
    // Process the CSV data
    const csvData = {}
    for (const [key, file] of Object.entries(files)) {
      csvData[key] = await file.text()
    }
    
    const results = await processCSVData(csvData)
    
    // Store results in KV for later retrieval
    const sessionId = crypto.randomUUID()
    await c.env.DATA_STORE.put(`session:${sessionId}`, JSON.stringify({
      results,
      timestamp: Date.now(),
      expires: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
    }))
    
    // Redirect to analytics with session ID
    return c.redirect(`/analytics?session=${sessionId}`)
    
  } catch (error) {
    console.error('Upload error:', error)
    return c.html(renderHomePage(`Error processing files: ${error.message}`))
  }
})

// Load sample data
app.get('/sample-data', async (c) => {
  try {
    // Sample CSV data embedded in the worker
    const sampleData = getSampleCSVData()
    const results = await processCSVData(sampleData)
    
    // Store results in KV
    const sessionId = crypto.randomUUID()
    await c.env.DATA_STORE.put(`session:${sessionId}`, JSON.stringify({
      results,
      timestamp: Date.now(),
      expires: Date.now() + (24 * 60 * 60 * 1000)
    }))
    
    return c.redirect(`/analytics?session=${sessionId}`)
    
  } catch (error) {
    console.error('Sample data error:', error)
    return c.html(renderHomePage(`Error loading sample data: ${error.message}`))
  }
})

// Analytics page
app.get('/analytics', async (c) => {
  const sessionId = c.req.query('session')
  
  if (!sessionId) {
    return c.redirect('/')
  }
  
  try {
    const sessionData = await c.env.DATA_STORE.get(`session:${sessionId}`)
    if (!sessionData) {
      return c.html(renderHomePage('Session expired. Please upload files again.'))
    }
    
    const { results } = JSON.parse(sessionData)
    
    // Apply filters and sorting
    const filterType = c.req.query('filter') || 'all'
    const sortBy = c.req.query('sort') || 'shrinkage_cost'
    const sortOrder = c.req.query('order') || 'desc'
    
    return c.html(renderAnalyticsPage(results, sessionId, filterType, sortBy, sortOrder))
    
  } catch (error) {
    console.error('Analytics error:', error)
    return c.html(renderHomePage(`Error loading analytics: ${error.message}`))
  }
})

// Reports page
app.get('/reports', async (c) => {
  const sessionId = c.req.query('session')
  
  if (!sessionId) {
    return c.redirect('/')
  }
  
  try {
    const sessionData = await c.env.DATA_STORE.get(`session:${sessionId}`)
    if (!sessionData) {
      return c.html(renderHomePage('Session expired. Please upload files again.'))
    }
    
    return c.html(renderReportsPage(sessionId))
    
  } catch (error) {
    console.error('Reports error:', error)
    return c.html(renderHomePage(`Error loading reports: ${error.message}`))
  }
})

// PDF Export
app.get('/export/pdf', async (c) => {
  const sessionId = c.req.query('session')
  
  if (!sessionId) {
    return c.redirect('/')
  }
  
  try {
    const sessionData = await c.env.DATA_STORE.get(`session:${sessionId}`)
    if (!sessionData) {
      return c.text('Session expired', 404)
    }
    
    const { results } = JSON.parse(sessionData)
    const pdfBuffer = await generatePDF(results)
    
    return c.body(pdfBuffer, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': \`attachment; filename=ingredient_tracker_report_\${new Date().toISOString().slice(0,10)}.pdf\`
      }
    })
    
  } catch (error) {
    console.error('PDF export error:', error)
    return c.text('Error generating PDF', 500)
  }
})

// Excel Export
app.get('/export/excel', async (c) => {
  const sessionId = c.req.query('session')
  
  if (!sessionId) {
    return c.redirect('/')
  }
  
  try {
    const sessionData = await c.env.DATA_STORE.get(`session:${sessionId}`)
    if (!sessionData) {
      return c.text('Session expired', 404)
    }
    
    const { results } = JSON.parse(sessionData)
    const excelBuffer = await generateExcel(results)
    
    return c.body(excelBuffer, {
      headers: {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'Content-Disposition': \`attachment; filename=ingredient_tracker_report_\${new Date().toISOString().slice(0,10)}.xlsx\`
      }
    })
    
  } catch (error) {
    console.error('Excel export error:', error)
    return c.text('Error generating Excel', 500)
  }
})

// API endpoint for getting data as JSON
app.get('/api/data', async (c) => {
  const sessionId = c.req.query('session')
  
  if (!sessionId) {
    return c.json({ error: 'No session ID provided' }, 400)
  }
  
  try {
    const sessionData = await c.env.DATA_STORE.get(`session:${sessionId}`)
    if (!sessionData) {
      return c.json({ error: 'Session not found' }, 404)
    }
    
    const { results } = JSON.parse(sessionData)
    return c.json(results)
    
  } catch (error) {
    console.error('API data error:', error)
    return c.json({ error: 'Error retrieving data' }, 500)
  }
})

// Health check
app.get('/health', (c) => {
  return c.json({ status: 'ok', timestamp: Date.now() })
})

// Function to provide sample CSV data
function getSampleCSVData() {
  return {
    ingredient_info: \`Ingredient,Unit Cost
Tomatoes,2.50
Onions,1.20
Carrots,1.80
Potatoes,1.00
Chicken Breast,8.50
Ground Beef,6.00
Salmon Fillet,15.00
Rice,1.50
Pasta,2.00
Olive Oil,12.00\`,
    input_stock: \`Ingredient,Received Qty
Tomatoes,50
Onions,30
Carrots,25
Potatoes,40
Chicken Breast,20
Ground Beef,25
Salmon Fillet,10
Rice,100
Pasta,50
Olive Oil,5\`,
    usage: \`Ingredient,Used Qty
Tomatoes,35
Onions,22
Carrots,18
Potatoes,32
Chicken Breast,15
Ground Beef,20
Salmon Fillet,7
Rice,80
Pasta,35
Olive Oil,3\`,
    waste: \`Ingredient,Wasted Qty
Tomatoes,5
Onions,2
Carrots,3
Potatoes,4
Chicken Breast,1
Ground Beef,2
Salmon Fillet,1
Rice,5
Pasta,8
Olive Oil,0\`
  }
}

export default app