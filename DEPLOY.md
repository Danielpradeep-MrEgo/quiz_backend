# Quick Deployment Guide

## Deploy to Vercel in 5 Minutes

### Prerequisites
- GitHub account
- Vercel account (free tier works)
- MongoDB Atlas account (free tier works)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Ready for Vercel deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Vercel will auto-detect Python settings
4. **Add Environment Variables:**
   - `MONGO_URI` = Your MongoDB connection string
   - `DB_NAME` = `quiz_management` (or your choice)
5. Click **Deploy**

### Step 3: Configure MongoDB Atlas

1. Go to MongoDB Atlas → Network Access
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (or add `0.0.0.0/0`)
4. Save

### Step 4: Test Your API

Your API will be live at: `https://your-project.vercel.app`

```bash
# Test health endpoint
curl https://your-project.vercel.app/health

# Should return: {"status": "healthy"}
```

## Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Value | Required |
|----------|-------|----------|
| `MONGO_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/` | ✅ Yes |
| `DB_NAME` | `quiz_management` | ❌ No (has default) |

## Troubleshooting

**"Module not found" error:**
- Check that `requirements.txt` is in the root directory

**MongoDB connection error:**
- Verify `MONGO_URI` is set correctly
- Check MongoDB Atlas Network Access settings

**Function timeout:**
- Vercel Hobby plan has 10s timeout
- Optimize queries or upgrade plan

## Next Steps

- See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for detailed deployment guide
- See [README.md](README.md) for API documentation

