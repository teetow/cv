# This script generates an index.md file for job application resources.
# It was mostly written by a word guessing robot named Claude.

import os
import datetime

current_dir = os.getcwd()
excluded_files = ["README.md", "generate_index.py", "index.md"]
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
    "_config.yml": "Jekyll Configuration"
}

files_by_basename = {}

for filename in os.listdir(current_dir):
    if (
        os.path.isfile(os.path.join(current_dir, filename))
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

# Add last updated date
current_date = datetime.datetime.now().strftime("%B %Y")
index_content += f"## Last Updated\n\n{current_date}\n"

with open(os.path.join(current_dir, "index.md"), "w") as f:
    f.write(index_content)

print("index.md generated successfully.")
