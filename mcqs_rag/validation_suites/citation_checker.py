import re

def parse_citation(citation_text):
    """
    Extract chapter, optional section and subsection from citation string.
    Returns tuple: (chapter_id, section_id, subsection_id)
    """
    chapter = section = subsection = None

    m = re.search(r"Chapter\s*(\d+)", citation_text)
    if m:
        chapter = m.group(1)

    m = re.search(r"Section\s*([\d\.]+)", citation_text)
    if m:
        section = m.group(1)

    m = re.search(r"Subsection\s*([\d\.]+)", citation_text)
    if m:
        subsection = m.group(1)

    return chapter, section, subsection


def check_citation(mcq, blueprint):
    """
    Check if an MCQ's citation exists in the hierarchical blueprint.

    Returns a dict:
        valid: True/False
        issues: list of problems
    """
    citation = mcq.get("citation", "").strip()
    if not citation:
        return {"valid": False, "issues": ["No citation provided"]}

    chapter_id, section_id, subsection_id = parse_citation(citation)
    issues = []

    # Check chapter
    chapter = blueprint.get(chapter_id)
    if not chapter:
        issues.append(f"Chapter {chapter_id} not found")
        return {"valid": False, "issues": issues}

    # Check section
    section = chapter.get("sections", {}).get(section_id) if section_id else None
    if section_id and not section:
        issues.append(f"Section {section_id} not found in Chapter {chapter_id}")

    # Check subsection
    subsection = section.get("subsections", {}).get(subsection_id) if section and subsection_id else None
    if subsection_id and not subsection:
        issues.append(f"Subsection {subsection_id} not found in Section {section_id}")

    valid = len(issues) == 0
    return {"valid": valid, "issues": issues}
