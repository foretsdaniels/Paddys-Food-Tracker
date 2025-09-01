# Cloudflare Worker Deployment Guide

Complete guide for deploying the Restaurant Ingredient Tracker on Cloudflare Workers.

## Prerequisites

### 1. Cloudflare Account Setup
- Create a free Cloudflare account at [cloudflare.com](https://www.cloudflare.com)
- Upgrade to Workers Paid plan ($5/month) for production use
- Note your Account ID from the Workers dashboard

### 2. Install Wrangler CLI
```bash
# Install globally
npm install -g wrangler

# Or use npx (recommended)
npx wrangler --version
```

### 3. Authentication
```bash
# Login to Cloudflare
wrangler login

# Verify authentication
wrangler whoami
```

## Initial Setup

### 1. Clone and Install Dependencies
```bash
git clone <repository-url>
cd "Cloudflare Worker"
npm install
```

### 2. Create KV Namespace
```bash
# Create production namespace
wrangler kv:namespace create "DATA_STORE"

# Create preview namespace for development
wrangler kv:namespace create "DATA_STORE" --preview
```

**Important**: Copy the namespace IDs from the output and update `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "DATA_STORE"
id = "your_production_namespace_id_here"
preview_id = "your_preview_namespace_id_here"
```

### 3. Configure wrangler.toml
Update the following fields in `wrangler.toml`:

```toml
name = "restaurant-tracker-your-name"  # Make this unique
account_id = "your_account_id_here"    # From Cloudflare dashboard

# Update KV namespace IDs from step 2
[[kv_namespaces]]
binding = "DATA_STORE"
id = "your_production_kv_id"
preview_id = "your_preview_kv_id"
```

## Development and Testing

### 1. Local Development
```bash
# Start local development server
npm run dev

# Or use wrangler directly
wrangler dev --local
```

Access the application at `http://localhost:8787`

### 2. Preview Deployment
```bash
# Deploy to preview environment
wrangler deploy --env dev
```

### 3. Test Core Functionality
1. Upload CSV files or use sample data
2. Verify analytics page loads correctly
3. Test PDF and Excel export downloads
4. Check session persistence across pages

## Production Deployment

### 1. Build and Deploy
```bash
# Build production bundle
npm run build

# Deploy to production
npm run deploy

# Or use wrangler directly
wrangler deploy
```

### 2. Verify Deployment
```bash
# Check deployment status
wrangler status

# View recent deployments
wrangler deployments list
```

### 3. Test Production Environment
- Visit your Worker URL (shown after deployment)
- Test full upload workflow
- Verify report generation
- Check global performance from different locations

## Custom Domain Setup

### 1. Add Domain to Cloudflare
1. Add your domain to Cloudflare (free)
2. Update nameservers as instructed
3. Wait for DNS propagation

### 2. Configure Worker Route
```bash
# Add route for your domain
wrangler route add "your-domain.com/*" --name restaurant-tracker

# Or subdomain
wrangler route add "tracker.your-domain.com/*" --name restaurant-tracker
```

### 3. SSL Configuration
- SSL is automatically provided by Cloudflare
- HTTPS is enforced by default
- Custom certificates can be uploaded if needed

## Environment Configuration

### 1. Environment Variables
```bash
# Set production environment variables
wrangler secret put NODE_ENV
# Enter: production

# Set development variables
wrangler secret put NODE_ENV --env dev
# Enter: development
```

### 2. Multiple Environments
Update `wrangler.toml` for staging environment:

```toml
[env.staging]
name = "restaurant-tracker-staging"
vars = { NODE_ENV = "staging" }

[[env.staging.kv_namespaces]]
binding = "DATA_STORE"
id = "staging_kv_namespace_id"
```

Deploy to staging:
```bash
wrangler deploy --env staging
```

## Monitoring and Analytics

### 1. Cloudflare Analytics
- Access through Cloudflare dashboard
- Monitor request volume, response times
- Track error rates and geographic distribution

### 2. Custom Logging
```bash
# View real-time logs
wrangler tail

# View logs for specific environment
wrangler tail --env production
```

### 3. Health Monitoring
The application includes a health endpoint at `/health`:
```bash
curl https://your-worker.your-subdomain.workers.dev/health
```

## Performance Optimization

### 1. Bundle Size Optimization
```bash
# Analyze bundle size
npm run build
ls -la dist/

# Bundle should be under 1MB
```

### 2. KV Operations Optimization
- Sessions automatically expire after 24 hours
- Data is compressed before storage
- Efficient key naming for fast lookups

### 3. Caching Configuration
```javascript
// In your Worker code
return new Response(content, {
  headers: {
    'Cache-Control': 'public, max-age=3600',
    'Content-Type': 'text/html'
  }
})
```

## Security Configuration

### 1. CORS Settings
Update CORS configuration in `src/index.js`:
```javascript
app.use('*', cors({
  origin: ['https://your-domain.com'],
  allowMethods: ['GET', 'POST'],
  allowHeaders: ['Content-Type']
}))
```

### 2. Rate Limiting
```javascript
// Add rate limiting middleware
app.use('*', async (c, next) => {
  const key = c.req.header('CF-Connecting-IP')
  // Implement rate limiting logic
  await next()
})
```

### 3. Data Protection
- Session data expires automatically
- No persistent user data storage
- CSV files are processed in memory only

## Troubleshooting

### Common Issues

1. **KV Namespace Errors**
   ```bash
   # Verify namespace exists
   wrangler kv:namespace list
   
   # Check binding in wrangler.toml
   ```

2. **Bundle Size Too Large**
   ```bash
   # Check what's included in bundle
   npm run build
   
   # Optimize dependencies
   npm audit
   ```

3. **Memory Limit Exceeded**
   - Reduce CSV file size limits
   - Optimize data processing algorithms
   - Use streaming for large files

4. **Deployment Failures**
   ```bash
   # Check Wrangler version
   wrangler --version
   
   # Update if needed
   npm install -g wrangler@latest
   ```

### Debug Mode
```bash
# Enable debug logging
wrangler dev --local --debug

# Check Worker logs
wrangler tail --debug
```

## Maintenance

### 1. Updates and Upgrades
```bash
# Update dependencies
npm update

# Check for security vulnerabilities
npm audit

# Update Wrangler
npm install -g wrangler@latest
```

### 2. KV Storage Management
```bash
# List all keys in namespace
wrangler kv:key list --binding DATA_STORE

# Clean up expired sessions
wrangler kv:key delete "session:old-session-id" --binding DATA_STORE
```

### 3. Performance Monitoring
- Monitor request patterns in Cloudflare Analytics
- Track error rates and response times
- Optimize based on usage patterns

### 4. Backup and Recovery
- KV data is automatically replicated globally
- Configuration is version controlled in Git
- Workers are stateless (no data loss risk)

## Cost Management

### 1. Usage Monitoring
- Monitor request volume in Cloudflare dashboard
- Track KV operations and storage usage
- Set up billing alerts

### 2. Optimization Strategies
- Implement client-side caching
- Optimize session data size
- Use efficient data structures

### 3. Scaling Considerations
- Workers scale automatically
- KV storage scales to petabytes
- No infrastructure management needed

## Support

### Resources
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/)
- [Cloudflare Community](https://community.cloudflare.com/)

### Getting Help
1. Check the troubleshooting section above
2. Review Cloudflare Workers documentation
3. Open an issue in the project repository
4. Contact Cloudflare support for platform issues

## Production Checklist

Before going live:

- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] KV namespaces properly configured
- [ ] Environment variables set
- [ ] Rate limiting implemented
- [ ] Monitoring and logging enabled
- [ ] Error handling tested
- [ ] Performance optimization complete
- [ ] Security review completed
- [ ] Backup strategy documented