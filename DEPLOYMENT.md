# TacticalLink Deployment Guide

This guide covers deploying TacticalLink to Vercel (frontend) and Railway (backend).

## 🚀 Deployment Overview

- **Frontend**: Vercel (React app)
- **Backend**: Railway (Flask API)
- **Database**: Railway MongoDB

## 📋 Prerequisites

1. GitHub repository with TacticalLink code
2. Vercel account
3. Railway account
4. MongoDB Atlas account (optional)

## 🎯 Backend Deployment (Railway)

### Step 1: Connect Repository

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your TacticalLink repository
5. Select the `backend` folder

### Step 2: Configure Environment Variables

In Railway dashboard, add these environment variables:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tactical_link
JWT_SECRET_KEY=your-super-secret-jwt-key-here
PORT=5000
FLASK_ENV=production
```

### Step 3: Deploy

1. Railway will automatically detect the Python app
2. It will install dependencies from `requirements.txt`
3. The app will be deployed and accessible via Railway URL

### Step 4: Configure Database

1. In Railway, add MongoDB service
2. Copy the connection string
3. Update `MONGODB_URL` environment variable

## 🎨 Frontend Deployment (Vercel)

### Step 1: Connect Repository

1. Go to [Vercel](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select the `frontend` folder

### Step 2: Configure Build Settings

- **Framework Preset**: Create React App
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### Step 3: Environment Variables

Add these environment variables in Vercel:

```env
REACT_APP_BACKEND_URL=https://your-railway-backend-url.railway.app
```

### Step 4: Deploy

1. Click "Deploy"
2. Vercel will build and deploy your React app
3. You'll get a Vercel URL for your frontend

## 🔧 Configuration

### Backend Configuration

Update your backend to handle CORS for production:

```python
# In app.py
CORS(app, origins=[
    "https://your-vercel-frontend.vercel.app",
    "http://localhost:3000"  # For development
])
```

### Frontend Configuration

Update API calls to use environment variable:

```javascript
// In your API calls
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
```

## 🗄️ Database Setup

### Option 1: Railway MongoDB

1. Add MongoDB service in Railway
2. Use the provided connection string
3. No additional setup required

### Option 2: MongoDB Atlas

1. Create cluster at [MongoDB Atlas](https://cloud.mongodb.com)
2. Create database user
3. Whitelist Railway IP addresses
4. Use Atlas connection string

## 🔒 Security Configuration

### Environment Variables

Ensure these are set in production:

```env
# Backend
JWT_SECRET_KEY=very-long-random-secret-key
MONGODB_URL=secure-connection-string
FLASK_ENV=production

# Frontend
REACT_APP_BACKEND_URL=https://your-backend-url
```

### SSL/HTTPS

- Vercel provides HTTPS by default
- Railway provides HTTPS by default
- Ensure all API calls use HTTPS

## 📊 Monitoring

### Railway Monitoring

1. View logs in Railway dashboard
2. Monitor resource usage
3. Set up alerts for errors

### Vercel Monitoring

1. View deployment logs
2. Monitor performance
3. Set up error tracking

## 🔄 CI/CD Pipeline

### Automatic Deployments

Both Vercel and Railway support automatic deployments:

1. Push to main branch
2. Automatic build and deployment
3. Environment variables preserved

### Manual Deployments

For manual deployments:

```bash
# Backend
railway up

# Frontend
vercel --prod
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Update CORS origins in backend
   - Check environment variables

2. **Database Connection**
   - Verify MongoDB URL
   - Check network access

3. **Build Failures**
   - Check dependencies
   - Review build logs

### Debugging

1. Check Railway logs for backend issues
2. Check Vercel logs for frontend issues
3. Use browser dev tools for client-side debugging

## 📈 Performance Optimization

### Backend Optimization

1. Enable gunicorn workers
2. Use Redis for caching
3. Optimize database queries

### Frontend Optimization

1. Enable code splitting
2. Optimize bundle size
3. Use CDN for static assets

## 🔐 Security Checklist

- [ ] Strong JWT secret key
- [ ] Secure MongoDB connection
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Environment variables secured
- [ ] Rate limiting enabled
- [ ] Input validation
- [ ] Error handling

## 📞 Support

For deployment issues:

1. Check Railway documentation
2. Check Vercel documentation
3. Review application logs
4. Create GitHub issue

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] Database connected
- [ ] SSL certificates active
- [ ] Monitoring set up
- [ ] Error tracking configured
- [ ] Performance monitoring
- [ ] Backup strategy
- [ ] Security audit completed

---

**Note**: This deployment guide assumes you have the TacticalLink codebase ready. Make sure to test locally before deploying to production.
