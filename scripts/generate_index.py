# This script generates an index.md file for job application resources.
# It was mostly written by a word guessing robot named Claude.

import os
import datetime
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)  # Parent directory

public_dir = os.path.join(repo_root, "public")
index_output_dir = repo_root
excluded_files = ["README.md"]

index_content = """---
layout: default
title: Job Application Resources
---

## Available Documents

"""

presets = {
    "cv.md": "Curriculum Vitae",
    "cv_long.md": "Detailed Experience (Long CV)",
    "linkedin_profile.md": "LinkedIn Profile Dump",
}

files_by_basename = {}

if not os.path.exists(public_dir):
    print(f"Error: public directory not found at {public_dir}")
    print(f"Script directory: {script_dir}")
    print(f"Repository root: {repo_root}")
    exit(1)

# Debug info for GitHub Actions
if "GITHUB_ACTIONS" in os.environ:
    print(f"Running in GitHub Actions")
    print(f"Working directory: {os.getcwd()}")
    print(f"Script directory: {script_dir}")
    print(f"Repository root: {repo_root}")
    print(f"Public directory: {public_dir}")

for filename in os.listdir(public_dir):
    if (
        os.path.isfile(os.path.join(public_dir, filename))
        and filename not in excluded_files
    ):
        base_filename = os.path.splitext(filename)[0]

        if base_filename not in files_by_basename:
            files_by_basename[base_filename] = []

        files_by_basename[base_filename].append(filename)

# Create index entries
for base_filename, file_versions in files_by_basename.items():
    display_name = ""

    for filename in file_versions:
        if filename in presets:
            display_name = presets[filename]
            break

    if not display_name:
        display_name = base_filename.replace("_", " ")
        display_name = display_name[0].upper() + display_name[1:]

    if len(file_versions) == 1:
        filename = file_versions[0]
        file_ext = os.path.splitext(filename)[1].lower()
        format_indicator = ""
        if file_ext == ".pdf":
            format_indicator = " (PDF)"
        elif file_ext and file_ext != ".md":
            format_indicator = f" ({file_ext[1:].upper()})"

        index_content += f"- [{display_name}{format_indicator}]({filename})\n"
    else:
        index_content += f"- {display_name} ("
        links = []

        md_file = next((f for f in file_versions if f.endswith(".md")), None)
        if md_file:
            links.append(f"[View Online]({md_file})")

        pdf_file = next((f for f in file_versions if f.endswith(".pdf")), None)
        if pdf_file:
            links.append(f"[Download PDF]({pdf_file})")

        for filename in file_versions:
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in [".md", ".pdf"]:
                format_name = file_ext[1:].upper()
                links.append(f"[{format_name}]({filename})")

        index_content += " | ".join(links) + ")\n"

index_content += "\nReach me at [jobs@teetow.com](mailto:jobs@teetow.com)!\n\n"

current_date = datetime.datetime.now().strftime("%B %Y")
index_content += f"## Last Updated\n\n{current_date}\n"

# Write the index.md file
index_file_path = os.path.join(index_output_dir, "index.md")
with open(index_file_path, "w") as f:
    f.write(index_content)

print(f"index.md generated successfully at: {index_file_path}")
