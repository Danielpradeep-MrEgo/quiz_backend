# Deploying to Vercel

This guide will help you deploy your Quiz Management System backend to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. MongoDB Atlas account with a cluster (or MongoDB connection string)
3. Vercel CLI installed (optional, for CLI deployment)

## Step 1: Prepare Your Project

The project is already configured for Vercel with:
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `.vercelignore` - Files to exclude from deployment

## Step 2: Set Up Environment Variables

Before deploying, you need to set up environment variables in Vercel:

### Required Environment Variables:
- `MONGO_URI` - Your MongoDB connection string
- `DB_NAME` - Your database name (default: `quiz_management`)

### Optional Environment Variables:
- `SECRET_KEY` - Secret key for Flask (optional)
- `FLASK_DEBUG` - Set to `False` for production

## Step 3: Deploy via Vercel Dashboard

### Option A: Deploy via GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import Project in Vercel:**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the settings

3. **Configure Environment Variables:**
   - In the project settings, go to "Environment Variables"
   - Add the following:
     - `MONGO_URI` = `your-mongodb-connection-string`
     - `DB_NAME` = `quiz_management` (or your preferred name)
   - Click "Save"

4. **Deploy:**
   - Click "Deploy"
   - Wait for the build to complete

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set Environment Variables:**
   ```bash
   vercel env add MONGO_URI
   vercel env add DB_NAME
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

## Step 4: Verify Deployment

After deployment, Vercel will provide you with a URL like:
```
https://your-project-name.vercel.app
```

Test the API:
```bash
curl https://your-project-name.vercel.app/health
```

Expected response:
```json
{"status": "healthy"}
```

## Step 5: Update MongoDB Atlas Network Access

Make sure your MongoDB Atlas cluster allows connections from Vercel:

1. Go to MongoDB Atlas Dashboard
2. Navigate to "Network Access"
3. Click "Add IP Address"
4. Click "Allow Access from Anywhere" (or add Vercel's IP ranges)
5. Save changes

## API Endpoints After Deployment

Your API will be available at:
- Base URL: `https://your-project-name.vercel.app`
- Health Check: `https://your-project-name.vercel.app/health`
- Admin API: `https://your-project-name.vercel.app/admin/*`
- Public API: `https://your-project-name.vercel.app/quizzes/*`

## Example: Test Your Deployed API

```bash
# Health check
curl https://your-project-name.vercel.app/health

# Get published quizzes
curl https://your-project-name.vercel.app/quizzes

# Create a quiz (Admin)
curl -X POST https://your-project-name.vercel.app/admin/quizzes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Quiz",
    "description": "A test quiz",
    "published": true
  }'
```

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Make sure all dependencies are in `requirements.txt` and properly formatted.

### Issue: MongoDB connection errors
**Solution:** 
- Verify `MONGO_URI` is set correctly in Vercel environment variables
- Check MongoDB Atlas network access settings
- Ensure the connection string includes authentication credentials

### Issue: Function timeout
**Solution:** 
- Vercel has a 10-second timeout for Hobby plan
- Consider optimizing database queries
- Upgrade to Pro plan for longer timeouts

### Issue: CORS errors
**Solution:** 
- `flask-cors` is already configured
- If issues persist, check your frontend's CORS configuration

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGO_URI` | Yes | - | MongoDB connection string |
| `DB_NAME` | No | `quiz_management` | Database name |
| `SECRET_KEY` | No | `dev-secret-key...` | Flask secret key |
| `FLASK_DEBUG` | No | `True` | Debug mode (set to `False` in production) |

## Production Checklist

- [ ] Set `FLASK_DEBUG=False` in environment variables
- [ ] Use a strong `SECRET_KEY`
- [ ] MongoDB Atlas network access configured
- [ ] All environment variables set in Vercel
- [ ] Test all API endpoints
- [ ] Monitor Vercel logs for errors
- [ ] Set up custom domain (optional)

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes/python)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test MongoDB connection locally
4. Review Vercel function logs in dashboard

