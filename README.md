# TAPPaaS Documentation

Documentation site for TAPPaaS - Trusted Automated Private Platform as a (selfhosted) Service.

**Live site:** https://tappaas.github.io/Documentation/

## Making Changes

Edit the markdown files in the `docs/` folder.

## Deploying Changes

After editing content, commit and push to deploy:

```bash
# Stage your changes
git add .

# Commit
git commit -m "Your commit message"

# Push to deploy
git push origin main
```

The GitHub Actions workflow will automatically build and deploy the site. Changes typically appear within 1-2 minutes.

## Local Development

### Preview locally

```bash
mkdocs serve
```

Then open http://127.0.0.1:8000

### Verify build before pushing

```bash
mkdocs build --strict
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```
