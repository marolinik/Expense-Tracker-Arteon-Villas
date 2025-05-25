# Render Deployment Checklist

## Pre-Deployment
- [ ] All code is committed to Git
- [ ] `requirements.txt` includes all dependencies + gunicorn
- [ ] `render.yaml` is present
- [ ] `build.sh` is present and executable
- [ ] `runtime.txt` specifies Python version
- [ ] No sensitive data in code (passwords, keys)

## GitHub Setup
- [ ] Create GitHub repository
- [ ] Push code to GitHub:
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

## Render Deployment
- [ ] Sign up/login at https://render.com
- [ ] Click "New +" → "Blueprint"
- [ ] Connect GitHub account
- [ ] Select your repository
- [ ] Click "Apply" to deploy

## Post-Deployment
- [ ] Wait for build to complete (5-10 mins)
- [ ] Access your app URL
- [ ] Test login with initial users
- [ ] Have all users change passwords
- [ ] Test expense creation
- [ ] Test admin functions (Jovan only)

## Important URLs
- Your App: `https://arteon-villas-expense-tracker.onrender.com`
- Render Dashboard: `https://dashboard.render.com`
- Logs: Dashboard → Your Service → Logs

## If Issues Occur
1. Check build logs in Render dashboard
2. Make `build.sh` executable:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   git push
   ```
3. Check environment variables are set
4. Verify database is created and running

## Initial Users
| Email | Initial Password | Role |
|-------|-----------------|------|
| hookloop1@yahoo.com | password1 | Admin |
| marolinik@gmail.com | password2 | User |
| fonmarko@gmail.com | password3 | User |
| zoran.radisavljevic@egzakta.com | password4 | User |

**Remember**: All users must change password on first login! 