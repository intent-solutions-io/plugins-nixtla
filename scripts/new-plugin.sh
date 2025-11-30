#!/bin/bash
# ============================================================
# new-plugin.sh - Scaffold new plugin with documentation
#
# Usage: ./scripts/new-plugin.sh <slug> "<Name>" <category>
# Example: ./scripts/new-plugin.sh cost-optimizer "Cost Optimizer" efficiency
# ============================================================

set -e

PLUGIN_SLUG=$1
PLUGIN_NAME=$2
CATEGORY=$3  # efficiency or growth

if [ -z "$PLUGIN_SLUG" ] || [ -z "$PLUGIN_NAME" ]; then
  echo "❌ Usage: ./scripts/new-plugin.sh <slug> \"<Name>\" [category]"
  echo "   Example: ./scripts/new-plugin.sh cost-optimizer \"Cost Optimizer\" efficiency"
  exit 1
fi

CATEGORY=${CATEGORY:-efficiency}
CATEGORY_DISPLAY=$(echo "$CATEGORY" | sed 's/^./\U&/')
TODAY=$(date +%Y-%m-%d)
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

echo "🔧 Creating plugin: $PLUGIN_NAME ($PLUGIN_SLUG)"
echo "   Category: $CATEGORY"
echo "   Date: $TODAY"
echo ""

# Create plugin directory structure
echo "📁 Creating plugin directory..."
mkdir -p "$REPO_ROOT/plugins/$PLUGIN_SLUG"/{.claude-plugin,commands,skills/skill-adapter,scripts,tests}

# Create plugin.json
cat > "$REPO_ROOT/plugins/$PLUGIN_SLUG/.claude-plugin/plugin.json" << EOF
{
  "name": "$PLUGIN_SLUG",
  "version": "0.1.0",
  "description": "$PLUGIN_NAME - [Add description]",
  "author": "Intent Solutions",
  "license": "MIT",
  "category": "$CATEGORY",
  "keywords": ["$PLUGIN_SLUG", "$CATEGORY"]
}
EOF

# Create plugin README
cat > "$REPO_ROOT/plugins/$PLUGIN_SLUG/README.md" << EOF
# $PLUGIN_NAME

> [One-line description]

## Quick Start

\`\`\`bash
# Setup
./scripts/setup.sh

# In Claude Code
/[command-name] [params]
\`\`\`

## Documentation

- [Business Case](../../000-docs/plugins/$PLUGIN_SLUG/01-BUSINESS-CASE.md)
- [PRD](../../000-docs/plugins/$PLUGIN_SLUG/02-PRD.md)
- [Architecture](../../000-docs/plugins/$PLUGIN_SLUG/03-ARCHITECTURE.md)
- [User Journey](../../000-docs/plugins/$PLUGIN_SLUG/04-USER-JOURNEY.md)
- [Technical Spec](../../000-docs/plugins/$PLUGIN_SLUG/05-TECHNICAL-SPEC.md)
- [Status](../../000-docs/plugins/$PLUGIN_SLUG/06-STATUS.md)
EOF

# Create docs directory
echo "📄 Creating documentation..."
mkdir -p "$REPO_ROOT/000-docs/plugins/$PLUGIN_SLUG"

# Copy and customize templates
for template in 01-BUSINESS-CASE 02-PRD 03-ARCHITECTURE 04-USER-JOURNEY 05-TECHNICAL-SPEC 06-STATUS; do
  if [ -f "$REPO_ROOT/templates/$template-TEMPLATE.md" ]; then
    sed -e "s/\[Plugin Name\]/$PLUGIN_NAME/g" \
        -e "s/\[plugin-slug\]/$PLUGIN_SLUG/g" \
        -e "s/\[TODAY\]/$TODAY/g" \
        -e "s/\[Efficiency | Growth\]/$CATEGORY_DISPLAY/g" \
        "$REPO_ROOT/templates/$template-TEMPLATE.md" > "$REPO_ROOT/000-docs/plugins/$PLUGIN_SLUG/$template.md"
    echo "   ✅ Created $template.md"
  else
    echo "   ⚠️  Template not found: $template-TEMPLATE.md"
  fi
done

echo ""
echo "✅ Plugin scaffolded successfully!"
echo ""
echo "📁 Code:  plugins/$PLUGIN_SLUG/"
echo "📄 Docs:  000-docs/plugins/$PLUGIN_SLUG/"
echo ""
echo "Next steps:"
echo "  1. Fill in the 6 documentation files"
echo "  2. Implement plugin code"
echo "  3. Update README.md plugin catalog"
echo "  4. Run ./scripts/validate-docs.sh to verify"
