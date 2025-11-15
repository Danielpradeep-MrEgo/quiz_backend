# Quick Railway Deployment Guide

## Deploy in 5 Minutes

### Prerequisites
- GitHub account
- Railway account (free tier works)
- MongoDB Atlas account (free tier works)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app/new](https://railway.app/new)
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and start building

### Step 3: Set Environment Variables

In Railway Dashboard → Your Project → Variables:

| Variable | Value |
|----------|-------|
| `MONGO_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `DB_NAME` | `quiz_management` (optional) |
| `FLASK_DEBUG` | `False` |
| `FLASK_HOST` | `0.0.0.0` |

**Note:** Railway automatically sets `PORT` - you don't need to set it!

### Step 4: Configure MongoDB Atlas

1. Go to MongoDB Atlas → Network Access
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (or add `0.0.0.0/0`)
4. Save

### Step 5: Test Your API

Railway will provide a URL like: `https://your-project.up.railway.app`

```bash
# Test health endpoint
curl https://your-project.up.railway.app/health

# Should return: {"status": "healthy"}
```

## What's Different from Vercel?

- ✅ No serverless function wrapper needed
- ✅ Uses your existing `app.py` directly
- ✅ Simpler configuration (just `Procfile`)
- ✅ Better for long-running connections (MongoDB)
- ✅ Automatic port management

## Troubleshooting

**Build fails:**
- Check Railway build logs
- Verify `requirements.txt` is correct
- Ensure `Procfile` exists

**App crashes:**
- Check Railway logs: Click on your service → Logs
- Verify `MONGO_URI` is set
- Make sure `FLASK_HOST=0.0.0.0`

**502 Bad Gateway:**
- Check that app is listening on correct port
- Verify `Procfile` is correct: `web: python app.py`

## Next Steps

- See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed guide
- See [README.md](README.md) for API documentation

