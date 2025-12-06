#!/usr/bin/env bash
#
# Nixtla Playground - GCP Setup Script
#
# This script sets up a complete GCP project for the Nixtla BigQuery Forecaster plugin
# with GitHub Actions deployment via Workload Identity Federation (keyless auth).
#
# What this does:
# 1. Creates "Nixtla Playground" GCP project
# 2. Enables all required APIs (BigQuery, Cloud Functions, Cloud Run)
# 3. Creates service accounts
# 4. Sets up Workload Identity Federation for GitHub Actions
# 5. Configures IAM permissions
# 6. Outputs GitHub secrets to configure
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Nixtla Playground - GCP Setup"
echo "=========================================="
echo ""

# Step 1: Check gcloud is installed and authenticated
echo -e "${YELLOW}Step 1: Checking gcloud CLI...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}ERROR: gcloud CLI not found. Please install: https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Check authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}Not authenticated. Running gcloud auth login...${NC}"
    gcloud auth login
fi

echo -e "${GREEN}✓ gcloud CLI ready${NC}"
echo ""

# Step 2: Create GCP project
echo -e "${YELLOW}Step 2: Creating GCP project 'Nixtla Playground'...${NC}"

# Generate unique project ID
TIMESTAMP=$(date +%s)
PROJECT_ID="nixtla-playground-${TIMESTAMP}"
PROJECT_NAME="Nixtla Playground"

echo "Project ID will be: ${PROJECT_ID}"
echo "Project Name: ${PROJECT_NAME}"
echo ""

# Check if user wants to continue
read -p "Continue with project creation? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create project
echo "Creating project..."
gcloud projects create "${PROJECT_ID}" \
    --name="${PROJECT_NAME}" \
    --set-as-default

echo -e "${GREEN}✓ Project created: ${PROJECT_ID}${NC}"
echo ""

# Step 3: Link billing account
echo -e "${YELLOW}Step 3: Linking billing account...${NC}"
echo "Available billing accounts:"
gcloud billing accounts list

echo ""
echo "Please enter the billing account ID from above:"
read -r BILLING_ACCOUNT_ID

gcloud billing projects link "${PROJECT_ID}" \
    --billing-account="${BILLING_ACCOUNT_ID}"

echo -e "${GREEN}✓ Billing linked${NC}"
echo ""

# Step 4: Enable required APIs
echo -e "${YELLOW}Step 4: Enabling required APIs...${NC}"

APIS=(
    "bigquery.googleapis.com"
    "cloudfunctions.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "artifactregistry.googleapis.com"
    "iamcredentials.googleapis.com"
    "cloudresourcemanager.googleapis.com"
    "iam.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo "Enabling ${api}..."
    gcloud services enable "${api}" --project="${PROJECT_ID}"
done

echo -e "${GREEN}✓ All APIs enabled${NC}"
echo ""

# Step 5: Create service account for GitHub Actions
echo -e "${YELLOW}Step 5: Creating service account for GitHub Actions...${NC}"

SA_NAME="nixtla-github-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts create "${SA_NAME}" \
    --display-name="Nixtla GitHub Actions Deployer" \
    --project="${PROJECT_ID}"

echo -e "${GREEN}✓ Service account created: ${SA_EMAIL}${NC}"
echo ""

# Step 6: Grant IAM permissions to service account
echo -e "${YELLOW}Step 6: Granting IAM permissions...${NC}"

ROLES=(
    "roles/cloudfunctions.admin"
    "roles/run.admin"
    "roles/bigquery.admin"
    "roles/iam.serviceAccountUser"
    "roles/artifactregistry.admin"
    "roles/storage.admin"
)

for role in "${ROLES[@]}"; do
    echo "Granting ${role}..."
    gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="${role}" \
        --quiet
done

echo -e "${GREEN}✓ IAM permissions granted${NC}"
echo ""

# Step 7: Set up Workload Identity Federation
echo -e "${YELLOW}Step 7: Setting up Workload Identity Federation (keyless auth)...${NC}"

# Get project number
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")

# Create workload identity pool
POOL_NAME="github-pool"
echo "Creating workload identity pool: ${POOL_NAME}..."

gcloud iam workload-identity-pools create "${POOL_NAME}" \
    --location=global \
    --display-name="GitHub Actions Pool" \
    --project="${PROJECT_ID}"

# Create workload identity provider
PROVIDER_NAME="github-provider"
GITHUB_REPO="intent-solutions-io/plugins-nixtla"

echo "Creating workload identity provider: ${PROVIDER_NAME}..."

gcloud iam workload-identity-pools providers create-oidc "${PROVIDER_NAME}" \
    --location=global \
    --workload-identity-pool="${POOL_NAME}" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository=='${GITHUB_REPO}'" \
    --project="${PROJECT_ID}"

# Allow GitHub Actions to impersonate service account
echo "Allowing GitHub Actions to impersonate service account..."

gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}" \
    --project="${PROJECT_ID}"

echo -e "${GREEN}✓ Workload Identity Federation configured${NC}"
echo ""

# Step 8: Output configuration for GitHub Secrets
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "GCP Project: ${PROJECT_ID}"
echo "Service Account: ${SA_EMAIL}"
echo ""
echo "=========================================="
echo -e "${YELLOW}NEXT STEPS: Configure GitHub Secrets${NC}"
echo "=========================================="
echo ""
echo "Go to: https://github.com/${GITHUB_REPO}/settings/secrets/actions"
echo ""
echo "Add the following repository secrets:"
echo ""
echo "1. GCP_PROJECT_ID"
echo "   Value: ${PROJECT_ID}"
echo ""
echo "2. GCP_SA_EMAIL"
echo "   Value: ${SA_EMAIL}"
echo ""
echo "3. GCP_WORKLOAD_IDENTITY_PROVIDER"
echo "   Value: projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}"
echo ""
echo "4. NIXTLA_TIMEGPT_API_KEY (from Max)"
echo "   Value: nixak-JNfT4z4JQb9uK3gdAyiWYWSBELdt6iW0PmE0Sy3k8ETAInJkFSPp4gOfyAZrENcGOsKyTqfDmuLghVq9"
echo ""
echo "=========================================="
echo ""
echo "Once GitHub secrets are configured, push to main branch to trigger deployment."
echo ""

# Save configuration to file
CONFIG_FILE="/home/jeremy/000-projects/nixtla/nixtla-playground-config.env"
cat > "${CONFIG_FILE}" <<EOF
# Nixtla Playground GCP Configuration
# Generated: $(date)

export GCP_PROJECT_ID="${PROJECT_ID}"
export GCP_SA_EMAIL="${SA_EMAIL}"
export GCP_WORKLOAD_IDENTITY_PROVIDER="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}"
export NIXTLA_TIMEGPT_API_KEY="nixak-JNfT4z4JQb9uK3gdAyiWYWSBELdt6iW0PmE0Sy3k8ETAInJkFSPp4gOfyAZrENcGOsKyTqfDmuLghVq9"

# For local development
gcloud config set project "${PROJECT_ID}"
EOF

echo "Configuration saved to: ${CONFIG_FILE}"
echo "Source this file for local development: source ${CONFIG_FILE}"
echo ""
echo -e "${GREEN}Setup complete!${NC}"
