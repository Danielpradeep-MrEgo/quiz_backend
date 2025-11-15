# Deploying to Railway

This guide will help you deploy your Quiz Management System backend to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. GitHub account (for connecting your repository)
3. MongoDB Atlas account (or use Railway's MongoDB service)

## Step 1: Prepare Your Project

Your project is already configured for Railway with:
- `Procfile` - Tells Railway how to run your app
- `railway.json` - Railway configuration (optional)
- `requirements.txt` - Python dependencies
- `app.py` - Main application entry point

## Step 2: Deploy via Railway Dashboard

### Option A: Deploy from GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Create a new project in Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python and start building

3. **Configure Environment Variables:**
   - In your Railway project, go to "Variables" tab
   - Add the following environment variables:
     - `MONGO_URI` = Your MongoDB connection string
     - `DB_NAME` = `quiz_management` (optional, has default)
     - `FLASK_DEBUG` = `False` (for production)
     - `FLASK_HOST` = `0.0.0.0` (required for Railway)
     - `FLASK_PORT` = `$PORT` (Railway provides this automatically)

4. **Deploy:**
   - Railway will automatically deploy when you push to GitHub
   - Or click "Deploy" in the dashboard

### Option B: Deploy via Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize Railway in your project:**
   ```bash
   railway init
   ```

4. **Set Environment Variables:**
   ```bash
   railway variables set MONGO_URI="your-mongodb-connection-string"
   railway variables set DB_NAME="quiz_management"
   railway variables set FLASK_DEBUG="False"
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

## Step 3: Set Up MongoDB

### Option A: Use MongoDB Atlas (Recommended)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster (free tier available)
3. Get your connection string
4. Add it to Railway environment variables as `MONGO_URI`
5. Configure Network Access:
   - Go to Network Access
   - Add IP Address: `0.0.0.0/0` (allows all IPs)
   - Or add Railway's IP ranges

### Option B: Use Railway's MongoDB Service

1. In Railway dashboard, click "New" → "Database" → "Add MongoDB"
2. Railway will automatically create a MongoDB instance
3. The connection string will be available as `MONGO_URI` environment variable
4. You can reference it in your app

## Step 4: Configure Your App

Railway automatically sets the `PORT` environment variable. Make sure your `app.py` uses it:

```python
# In app.py or config.py
PORT = int(os.environ.get("PORT", 5000))
```

Your `app.py` should already be configured correctly.

## Step 5: Verify Deployment

After deployment, Railway will provide you with a URL like:
```
https://your-project-name.up.railway.app
```

Test the API:
```bash
curl https://your-project-name.up.railway.app/health
```

Expected response:
```json
{"status": "healthy", "mongodb_connected": true}
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGO_URI` | Yes | - | MongoDB connection string |
| `DB_NAME` | No | `quiz_management` | Database name |
| `PORT` | Auto | - | Railway sets this automatically |
| `FLASK_DEBUG` | No | `True` | Set to `False` in production |
| `FLASK_HOST` | No | `0.0.0.0` | Host to bind to (use `0.0.0.0` for Railway) |
| `SECRET_KEY` | No | `dev-secret-key...` | Flask secret key |

## API Endpoints After Deployment

Your API will be available at:
- Base URL: `https://your-project-name.up.railway.app`
- Health Check: `https://your-project-name.up.railway.app/health`
- Admin API: `https://your-project-name.up.railway.app/admin/*`
- Public API: `https://your-project-name.up.railway.app/quizzes/*`

## Example: Test Your Deployed API

```bash
# Health check
curl https://your-project-name.up.railway.app/health

# Get published quizzes
curl https://your-project-name.up.railway.app/quizzes

# Create a quiz (Admin)
curl -X POST https://your-project-name.up.railway.app/admin/quizzes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Quiz",
    "description": "A test quiz",
    "published": true
  }'
```

## Troubleshooting

### Issue: "Port already in use" or binding errors
**Solution:** 
- Make sure `FLASK_HOST=0.0.0.0` is set
- Use `PORT` environment variable: `PORT = int(os.environ.get("PORT", 5000))`

### Issue: MongoDB connection errors
**Solution:**
- Verify `MONGO_URI` is set correctly in Railway environment variables
- Check MongoDB Atlas network access settings
- Ensure connection string includes authentication

### Issue: Build fails
**Solution:**
- Check Railway build logs
- Verify `requirements.txt` has all dependencies
- Ensure `Procfile` exists and is correct

### Issue: App crashes on startup
**Solution:**
- Check Railway logs: `railway logs`
- Verify all environment variables are set
- Test locally first: `python app.py`

### Issue: 502 Bad Gateway
**Solution:**
- Check that your app is listening on `0.0.0.0` and the correct port
- Verify the app starts successfully (check logs)
- Ensure `Procfile` is correct

## Railway CLI Commands

```bash
# View logs
railway logs

# Open project in browser
railway open

# View environment variables
railway variables

# Set environment variable
railway variables set KEY=value

# Connect to project shell
railway shell

# Deploy
railway up
```

## Production Checklist

- [ ] Set `FLASK_DEBUG=False` in environment variables
- [ ] Use a strong `SECRET_KEY`
- [ ] MongoDB Atlas network access configured (if using Atlas)
- [ ] All environment variables set in Railway
- [ ] Test all API endpoints
- [ ] Monitor Railway logs for errors
- [ ] Set up custom domain (optional)
- [ ] Enable automatic deployments from GitHub

## Custom Domain

1. Go to Railway project → Settings → Domains
2. Click "Generate Domain" or "Add Custom Domain"
3. Follow the DNS configuration instructions
4. Your API will be available at your custom domain

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Python Guide](https://docs.railway.app/guides/python)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)

## Support

If you encounter issues:
1. Check Railway deployment logs
2. Check Railway application logs: `railway logs`
3. Verify environment variables
4. Test MongoDB connection locally
5. Review Railway status page

