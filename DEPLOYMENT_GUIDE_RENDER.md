# Deployment Guide: Arteon Villas Expense Tracker on Render

This guide will walk you through deploying the Arteon Villas Expense Tracker on Render, a cloud platform that makes it easy to deploy web applications with free PostgreSQL databases.

## Prerequisites

1. A GitHub account (to host your code)
2. A Render account (free tier available at https://render.com)
3. Your application code ready to deploy

## Step 1: Prepare Your Code for Deployment

### 1.1 Update Your Code

The application is already configured for Render deployment. Make sure you have these files:
- `render.yaml` - Render blueprint configuration
- `requirements.txt` - Python dependencies (including gunicorn)
- `build.sh` - Build script for initialization

### 1.2 Push Code to GitHub

1. Create a new repository on GitHub
2. Initialize git in your project folder (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Arteon Villas Expense Tracker"
   ```
3. Add your GitHub repository as remote:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy on Render

### Method 1: Using Render Blueprint (Recommended)

1. **Log in to Render** at https://dashboard.render.com

2. **Click "New +" → "Blueprint"**

3. **Connect your GitHub repository**:
   - Click "Connect account" to link your GitHub
   - Select the repository containing your code
   - Grant Render access to the repository

4. **Render will automatically detect `render.yaml`** and show:
   - 1 PostgreSQL database (arteon-villas-db)
   - 1 Web Service (arteon-villas-expense-tracker)

5. **Click "Apply"** to create all resources

6. **Wait for deployment** (5-10 minutes):
   - Render will create the PostgreSQL database
   - Build your application
   - Run the initialization script
   - Start the web service

### Method 2: Manual Setup

If you prefer manual setup or need more control:

#### 2.1 Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: arteon-villas-db
   - **Database**: arteon_villas_expenses
   - **User**: arteon_user
   - **Region**: Choose nearest to your users
   - **Plan**: Free
3. Click "Create Database"
4. Wait for database to be ready (few minutes)
5. Copy the "Internal Database URL" for later

#### 2.2 Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: arteon-villas-expense-tracker
   - **Region**: Same as your database
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. Add Environment Variables:
   - Click "Advanced" → "Add Environment Variable"
   - Add:
     - `DATABASE_URL`: Paste the Internal Database URL from step 2.1
     - `SECRET_KEY`: Click "Generate" for a random value
     - `PYTHON_VERSION`: 3.11.0

5. Click "Create Web Service"

## Step 3: Make build.sh Executable

If deployment fails with permission error:

1. Make build.sh executable locally:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   git push
   ```

2. Render will automatically redeploy

## Step 4: Access Your Application

1. Once deployment is complete, you'll see "Your service is live 🎉"
2. Click the URL provided (format: `https://arteon-villas-expense-tracker.onrender.com`)
3. You should see the login page

## Step 5: Verify Initial Users

The build script automatically creates the initial users:

1. **Admin User**:
   - Email: hookloop1@yahoo.com
   - Password: password1

2. **Regular Users**:
   - marolinik@gmail.com / password2
   - fonmarko@gmail.com / password3
   - zoran.radisavljevic@egzakta.com / password4

**Important**: All users must change their password on first login!

## Troubleshooting

### Build Fails

1. **Check Build Logs**: Click on the failed deploy → "Logs"
2. **Common Issues**:
   - Permission denied on build.sh: Make it executable (see Step 3)
   - Module not found: Ensure all dependencies are in requirements.txt
   - Database connection: Check DATABASE_URL is set correctly

### Application Errors

1. **500 Internal Server Error**:
   - Check the web service logs
   - Verify database is running
   - Ensure SECRET_KEY is set

2. **Database Not Initialized**:
   - Go to "Settings" → "Build & Deploy"
   - Change Build Command to: `pip install -r requirements.txt && python init_db.py`
   - Trigger manual deploy

### Performance Issues

- Render free tier services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- Consider upgrading to paid tier for always-on service

## Custom Domain (Optional)

1. Go to your web service settings
2. Click "Add Custom Domain"
3. Enter your domain (e.g., expenses.arteonvillas.com)
4. Update your DNS records as instructed
5. Render provides free SSL certificates

## Monitoring & Maintenance

### View Logs
- Web Service → "Logs" tab shows application logs
- Database → "Logs" tab shows PostgreSQL logs

### Database Backups
- Render free tier: No automatic backups
- Manual backup:
  ```bash
  pg_dump DATABASE_URL > backup.sql
  ```

### Updates
1. Make changes locally
2. Test thoroughly
3. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
4. Render auto-deploys on push to main branch

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes (auto-set) |
| SECRET_KEY | Flask secret key for sessions | Yes |
| PYTHON_VERSION | Python runtime version | Yes |
| FLASK_ENV | Flask environment (production) | Optional |

## Security Recommendations

1. **Change default passwords immediately** after deployment
2. **Update SECRET_KEY** regularly
3. **Use strong passwords** for all accounts
4. **Enable 2FA** on your Render account
5. **Monitor logs** for suspicious activity

## Cost Considerations

### Free Tier Limits
- **Database**: 256MB storage, 1GB RAM
- **Web Service**: 512MB RAM, sleeps after inactivity
- **Bandwidth**: 100GB/month
- **Build Minutes**: 500/month

### When to Upgrade
- More than 10 active users
- Need 24/7 availability
- Database approaching 256MB
- Want automatic backups

## Support Resources

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Application Issues**: Check this guide first
- **Database Issues**: Check PostgreSQL logs in Render dashboard

## Next Steps

1. **Test all functionality** after deployment
2. **Change all default passwords**
3. **Set up monitoring** (e.g., UptimeRobot for free)
4. **Document any customizations** for your team
5. **Plan for backups** if using free tier

---

Congratulations! Your Arteon Villas Expense Tracker is now live on Render. Remember to have all users change their passwords on first login for security. 