#!/bin/bash

# Create the index.md file with front matter
cat > index.md << 'FRONTMATTER'
---
layout: default
title: Job Application Resources
---

## Available Documents
FRONTMATTER

# Loop through markdown files and create links
for file in public/*.md; do
  name=$(basename "$file" .md)
  display_name=$(echo "$name" | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++)sub(/./,toupper(substr($i,1,1)),$i)}1')
  pdf_file="public/${name}.pdf"
  if [ -f "$pdf_file" ]; then
    echo "- $display_name ([View Online]($file) | [Download PDF]($pdf_file))" >> index.md
  else
    echo "- [$display_name]($file)" >> index.md
  fi
done

# Add contact information
cat >> index.md << 'CONTACT'

Reach me at [jobs@teetow.com](mailto:jobs@teetow.com)!
CONTACT

echo "Index file generated successfully."
