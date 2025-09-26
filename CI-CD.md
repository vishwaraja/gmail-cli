# CI/CD Pipeline Setup

This document explains how to set up the CI/CD pipeline for the Gmail CLI project.

## 🚀 Overview

The project includes three GitHub Actions workflows:

1. **CI Pipeline** (`.github/workflows/ci.yml`) - Runs on PRs and pushes to main/develop
2. **Docker Deploy** (`.github/workflows/docker-deploy.yml`) - Deploys to Docker Hub on main branch pushes
3. **Docker Build & Push** (`.github/workflows/docker-build-push.yml`) - Comprehensive build and test pipeline

## 🔧 Setup Instructions

### 1. Configure Docker Hub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

   - **Name**: `DOCKERHUB_USERNAME`
   - **Value**: `vishwa86`

   - **Name**: `DOCKERHUB_TOKEN`
   - **Value**: `your_docker_hub_personal_access_token`

### 2. Enable GitHub Actions

GitHub Actions should be enabled by default. If not:

1. Go to your repository **Settings**
2. Click on **Actions** → **General**
3. Ensure **Allow all actions and reusable workflows** is selected

## 📋 Workflow Details

### CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
- **Test**: Runs on Python 3.8, 3.9, 3.10, 3.11
  - Installs dependencies
  - Runs linting with flake8
  - Tests CLI help command
- **Docker Test**: Builds and tests Docker image (PRs only)
- **Security Scan**: Runs Trivy vulnerability scanner (PRs only)

### Docker Deploy (`docker-deploy.yml`)

**Triggers:**
- Push to `main` branch
- Tag pushes (e.g., `v1.0.0`)

**Jobs:**
- **Deploy**: Builds and pushes multi-architecture Docker image to Docker Hub
  - Supports `linux/amd64` and `linux/arm64`
  - Tags with `latest` for main branch
  - Tags with version for releases

### Docker Build & Push (`docker-build-push.yml`)

**Triggers:**
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches

**Jobs:**
- **Build and Push**: Builds and pushes Docker image (main branch only)
- **Test**: Tests Docker image (PRs only)

## 🏷️ Tagging Strategy

The workflows automatically create tags based on:

- **Main branch**: `latest`
- **Version tags**: `v1.0.0`, `1.0.0`, `1.0`
- **Branches**: `main`, `develop`

## 🔍 Monitoring

### View Workflow Runs

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select the workflow you want to view
4. Click on a specific run to see detailed logs

### Docker Hub

Your images will be available at:
- `docker.io/vishwa86/gmail-cli:latest`
- `docker.io/vishwa86/gmail-cli:1.0.0` (for versioned releases)

## 🚨 Troubleshooting

### Common Issues

1. **Docker Hub Authentication Failed**
   - Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set correctly
   - Ensure the token has the correct permissions

2. **Build Failures**
   - Check the Actions logs for specific error messages
   - Ensure all dependencies are properly specified in `requirements.txt`

3. **Permission Denied**
   - Verify the GitHub repository has Actions enabled
   - Check that the workflow files are in the correct location (`.github/workflows/`)

### Debug Commands

```bash
# Test Docker build locally
docker build -t gmail-cli:test .

# Test the built image
docker run --rm gmail-cli:test --help

# Check Docker Hub login
docker login
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Docker Buildx Documentation](https://docs.docker.com/buildx/)

## 🔄 Workflow Customization

You can customize the workflows by:

1. **Adding more test steps** in the CI pipeline
2. **Modifying the Docker build context** or build arguments
3. **Adding deployment to other registries** (e.g., GitHub Container Registry)
4. **Implementing automated versioning** based on git tags

## 📝 Example Usage

Once the pipeline is set up:

1. **Make changes** to your code
2. **Create a pull request** - CI pipeline will run tests
3. **Merge to main** - Docker image will be built and pushed automatically
4. **Create a release tag** - Versioned image will be pushed

```bash
# Create and push a release tag
git tag v1.0.0
git push origin v1.0.0
```

This will trigger the deployment workflow and create a versioned Docker image.
