"""Generates the code reference pages.

Source: https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
"""
# Standard library
import re
from pathlib import Path

# Third party
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()
migration_file_pattern = r"\d+_.+$"

for path in sorted(Path("src").rglob("*.py")):
    module_path = path.relative_to("src").with_suffix("")
    doc_path = path.relative_to("src").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = list(module_path.parts)

    # Skip test packages and modules
    if "tests" in parts or "conftest" in parts or any((part.startswith("test") for part in parts)):
        continue
    # Skip Django migrations
    # N.B.: this will leave the "migrations" package page, since its "__init__" is not excluded. This is done on
    #       purpose, in case someone creates a regular non-Django "migrations" package that should be documented.
    if (
        len(parts) > 1 and re.match(migration_file_pattern, parts[-1]) is not None and parts[-2] == "migrations"
    ) or parts[-1] == "migrations":
        continue
    # Use __init__ module as package index
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    # Skip __main__
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, Path("../..") / path)

# Create a global reference summary
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
