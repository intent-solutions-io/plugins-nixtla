#!/bin/bash
# ============================================================
# validate-docs.sh - Validate documentation completeness
# ============================================================

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
ERRORS=0
WARNINGS=0

echo "🔍 Validating Enterprise Plugin Showcase documentation..."
echo ""

# Check for required global docs
echo "📋 Checking global documentation..."
for doc in "000-EXECUTIVE-SUMMARY.md" "001-ENGAGEMENT-OPTIONS.md"; do
  if [ -f "$REPO_ROOT/000-docs/global/$doc" ]; then
    echo "   ✅ $doc"
  else
    echo "   ❌ Missing: 000-docs/global/$doc"
    ((ERRORS++))
  fi
done

# Check each plugin has all 6 docs
echo ""
echo "📋 Checking per-plugin documentation..."

for plugin_dir in "$REPO_ROOT/plugins"/*/; do
  if [ -d "$plugin_dir" ]; then
    plugin_slug=$(basename "$plugin_dir")
    doc_dir="$REPO_ROOT/000-docs/plugins/$plugin_slug"

    echo ""
    echo "   Plugin: $plugin_slug"

    if [ ! -d "$doc_dir" ]; then
      echo "      ❌ No docs directory: 000-docs/plugins/$plugin_slug/"
      ((ERRORS++))
      continue
    fi

    for doc in "01-BUSINESS-CASE.md" "02-PRD.md" "03-ARCHITECTURE.md" "04-USER-JOURNEY.md" "05-TECHNICAL-SPEC.md" "06-STATUS.md"; do
      if [ -f "$doc_dir/$doc" ]; then
        # Check if file has content beyond template placeholders
        if grep -q "\[Plugin Name\]\|\[plugin-slug\]\|\[TODAY\]" "$doc_dir/$doc" 2>/dev/null; then
          echo "      ⚠️  $doc (contains unfilled placeholders)"
          ((WARNINGS++))
        else
          echo "      ✅ $doc"
        fi
      else
        echo "      ❌ Missing: $doc"
        ((ERRORS++))
      fi
    done
  fi
done

# Check README has required sections
echo ""
echo "📋 Checking README.md sections..."
readme="$REPO_ROOT/README.md"

if [ -f "$readme" ]; then
  required_sections=("Quick Navigation" "Portfolio Overview" "Ideas & Backlog" "Demo" "Documentation Index" "Engagement Options" "Contact")

  for section in "${required_sections[@]}"; do
    if grep -q "## $section\|# $section" "$readme" 2>/dev/null; then
      echo "   ✅ $section"
    else
      echo "   ⚠️  Missing section: $section"
      ((WARNINGS++))
    fi
  done
else
  echo "   ❌ README.md not found!"
  ((ERRORS++))
fi

# Summary
echo ""
echo "═══════════════════════════════════════"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo "✅ All checks passed!"
elif [ $ERRORS -eq 0 ]; then
  echo "⚠️  Passed with $WARNINGS warning(s)"
else
  echo "❌ Failed: $ERRORS error(s), $WARNINGS warning(s)"
fi
echo "═══════════════════════════════════════"

exit $ERRORS
