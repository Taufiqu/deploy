# 🔒 SECURITY & CREDENTIALS MANAGEMENT

## ⚠️ IMPORTANT SECURITY NOTICE

This repository contains **template files only**. Actual credentials are **NOT** committed to version control.

## 📋 CREDENTIAL FILES STRUCTURE

### ✅ Safe to Commit (Templates):
```
📄 credentials_template.txt        → Template with placeholders
📄 .env.example                   → Environment template
📄 README_SECURITY.md             → This security guide
```

### 🚫 NEVER Commit (Actual Credentials):
```
📄 supabase_credentials_actual.txt → Real credentials (gitignored)
📄 .env                           → Local environment (gitignored)
📄 railway_env_*.txt              → Production configs (gitignored)
📄 *_real*.py                     → Test files with credentials (gitignored)
```

## 🛡️ SECURITY PRACTICES

### 1. Local Development:
1. Copy `credentials_template.txt` 
2. Fill with your actual Supabase credentials
3. Save as `.env` in service directories
4. **Never commit** .env files

### 2. Railway Deployment:
1. Use `supabase_credentials_actual.txt` as reference
2. Copy environment variables to Railway dashboard
3. Set variables in Railway project settings
4. **Never commit** production credentials

### 3. Team Collaboration:
1. Share `credentials_template.txt` with placeholders
2. Each developer gets their own credentials
3. Production credentials shared via secure channels
4. **Never commit** actual values

## 🔧 DEPLOYMENT WORKFLOW

### Step 1: Setup Local Development
```bash
# Copy template
cp credentials_template.txt .env

# Fill actual credentials in .env
# This file is gitignored and won't be committed
```

### Step 2: Deploy to Railway
```bash
# Use supabase_credentials_actual.txt as reference
# Copy environment variables to Railway dashboard
# Don't commit this file - it's gitignored
```

### Step 3: Verify Security
```bash
# Check what will be committed
git status

# Ensure no .env or *_actual.txt files are staged
git add .
git commit -m "Add templates only"
```

## ✅ GITIGNORE PROTECTION

The following patterns protect your credentials:

```gitignore
# Environment files
.env
.env.*
*.env

# Actual credentials
*_actual.*
*_real*.py
railway_env_*.txt
supabase_credentials.txt
```

## 🆘 IF CREDENTIALS ARE ACCIDENTALLY COMMITTED

1. **Immediately rotate credentials** in Supabase
2. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch filename' \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. Force push: `git push --force --all`
4. Update all deployment environments

## 📞 SUPPORT

If you have questions about credential management:
1. Check this security guide
2. Review `.gitignore` file
3. Ensure templates are used for sharing
4. Keep actual credentials secure and private

---

**Remember: Security is everyone's responsibility! 🔒**
