import re
import os
import json
import argparse
from chunking.constants import MATH_11_CHAPTERS
from data_loading.data_ingestion import read_file, MATH_11_PATH



def chunk_markdown(text, chapters ,source_name=None):
    """
    Chunk markdown text exercise-wise and add metadata including parent chapter and section.
    All metadata fields default to empty string if missing.
    """
    # Detect numbered headers
    header_pattern = re.compile(r"^(#+)\s+(\d+(\.\d+)*)\s+(.*)", re.MULTILINE)



    # Detect chapter headers
    chapter_pattern = re.compile(
        r"^#\s+(" + "|".join(re.escape(ch) for ch in chapters) + r")\s*$",
        re.MULTILINE
    )

    # Detect exercise headers
    exercise_pattern = re.compile(r"^(#{1,2})\s+EXERCISE", re.MULTILINE)

    # Collect all matches
    header_matches = [{"type": "header", "match": m} for m in header_pattern.finditer(text)]
    chapter_matches = [{"type": "chapter", "match": m} for m in chapter_pattern.finditer(text)]
    exercise_matches = [{"type": "exercise", "match": m} for m in exercise_pattern.finditer(text)]

    all_matches = header_matches + chapter_matches + exercise_matches
    all_matches.sort(key=lambda x: x["match"].start())

    if not all_matches:
        return [{"title": "full_document", "content": text, "type": "full_document", "chunk_index": 0}]

    chunks = []

    for i, item in enumerate(all_matches):
        match = item["match"]
        start = match.start()
        end = all_matches[i + 1]["match"].start() if i + 1 < len(all_matches) else len(text)
        chunk_text = text[start:end].strip()
        chunk_type = item["type"]

        header_level = len(match.group(1)) if chunk_type in ["header", "exercise"] else 1
        section_number = match.group(2) if chunk_type == "header" else ""
        title = match.group(4) if chunk_type == "header" else match.group(0).strip()
        subsection_title = match.group(4).strip() if chunk_type == "header" and match.group(4) else ""

        # Parent chapter lookup
        parent_chapter_name = ""
        for prev in reversed(chunks):
            if prev.get("type") == "chapter":
                parent_chapter_name = prev.get("title", "")
                break

        # Initialize metadata fields
        chapter_id = ""
        section_id = ""
        subsection_id = ""
        chapter_name = parent_chapter_name
        section_name = ""
        subsection_name = ""

        if chunk_type == "chapter":
            chapter_id = section_number or title or ""
            chapter_name = title or ""
        elif chunk_type == "header":
            parts = section_number.split(".") if section_number else []
            if len(parts) == 1:
                chapter_id = parts[0] or ""
                chapter_name = title or ""
            elif len(parts) == 2:
                chapter_id = parts[0] or ""
                section_id = section_number or ""
                section_name = title or ""
            elif len(parts) >= 3:
                chapter_id = parts[0] or ""
                section_id = ".".join(parts[:2]) or ""
                subsection_id = section_number or ""
                subsection_name = subsection_title or ""
                # Also set section_name from the parent section
                for prev in reversed(chunks):
                    if prev.get("section") == section_id:
                        section_name = prev.get("title", "")
                        break
        elif chunk_type == "exercise":
            chapter_id = parent_chapter_name or ""
            chapter_name = parent_chapter_name or ""

        # Parent section
        parent_section = ""
        if section_number and len(parts) > 1:
            parent_section = ".".join(parts[:-1]) or ""

        chunk = {
            "type": chunk_type or "",
            "header_level": header_level or 0,
            "section": section_number or "",
            "chapter_id": chapter_id or "",
            "section_id": section_id or "",
            "subsection_id": subsection_id or "",
            "chapter_name": chapter_name or "",
            "section_name": section_name or "",
            "subsection_name": subsection_name or "",
            "subsection_title": subsection_title or "",
            "parent_chapter": parent_chapter_name or "",
            "title": title or "",
            "chunk_index": i,
            "char_count": len(chunk_text),
            "word_count": len(chunk_text.split()),
            "start_pos": start,
            "end_pos": end,
            "source": source_name or "",
            "content": chunk_text or "",
            "embedding": None
        }

        chunks.append(chunk)

    return chunks

def view_chunks(chunks):
    """
    Nicely print chunks with metadata.
    """
    for c in chunks:
        print("="*80)
        print(f"Chunk {c.get('chunk_index', '')}: {c.get('title', '')}")
        print(f"Type: {c.get('type', '')} | Header Level: {c.get('header_level', '')} | Section: {c.get('section', '')}")
        print(f"Chapter ID: {c.get('chapter_id', '')} | Section ID: {c.get('section_id', '')} | Subsection ID: {c.get('subsection_id', '')}")
        print(f"Chapter Name: {c.get('chapter_name', '')} | Section Name: {c.get('section_name', '')} | Subsection Name: {c.get('subsection_name', '')}")
        print(f"Parent Chapter: {c.get('parent_chapter', '')}")
        print(f"Words: {c.get('word_count', 0)} | Characters: {c.get('char_count', 0)}")
        print(f"Source: {c.get('source', '')}")
        print(f"Embedding: {c.get('embedding', None)}")
        print("-"*80)
        print(c.get('content', ''))
        print("="*80 + "\n")

def split_exercises_in_chunks(chunks,chapters):
    """
    Split existing chunks on '# Exercise' or '## Exercise' (case-insensitive),
    stopping at the next chapter, section, or exercise.
    """
    new_chunks = []

    # Regex patterns
    exercise_pattern = r'(?i)(?=^#{1,2}\s*EXERCISE)'  # # or ## Exercise
    section_pattern = r'(?=^## |^### )'  # section or subsection
    chapter_pattern = r'(?=^# (?:' + "|".join(re.escape(ch) for ch in chapters) + r'))'  # chapters

    # Combine patterns
    split_pattern = re.compile('|'.join([exercise_pattern, section_pattern, chapter_pattern]), re.MULTILINE)

    for chunk in chunks:
        content = chunk['content']

        # Only split if content has 'Exercise'
        if re.search(r'(?i)^\s*#{1,2}\s*EXERCISE', content, re.MULTILINE):
            parts = [p.strip() for p in split_pattern.split(content) if p.strip()]
            for idx, part in enumerate(parts):
                subchunk = {
                    **chunk,  # inherit metadata
                    'chunk_index': f"{chunk['chunk_index']}-{idx+1}",
                    'title': part.splitlines()[0].replace('#', '').strip(),
                    'content': part,
                    'char_count': len(part),
                    'word_count': len(part.split())
                }
                new_chunks.append(subchunk)
        else:
            new_chunks.append(chunk)

    return new_chunks

def basic_chunk_preprocessing(chunk):
    """
    Minimal preprocessing for a single chunk's content.
    Does not modify metadata.
    """
    content = chunk['content']

    # 1. Remove empty image placeholders
    content = re.sub(r'\[Image removed\]', '', content)

    # 2. Normalize LaTeX backslashes from OCR errors
    content = content.replace(r'\backslash[', r'\[').replace(r'\backslash]', r'\]')

    # 3. Strip leading/trailing whitespace from each line
    content = "\n".join(line.strip() for line in content.splitlines())

    # 4. Remove extra blank lines (more than 1 in a row)
    content = re.sub(r'\n{2,}', '\n\n', content)

    # 5. Strip overall leading/trailing whitespace
    content = content.strip()

    # Return a new chunk dictionary, keeping metadata unchanged
    new_chunk = chunk.copy()
    new_chunk['content'] = content
    new_chunk['char_count'] = len(content)
    new_chunk['word_count'] = len(content.split())

    return new_chunk

def chunk_pipeline(chapters,input_path):
    text = read_file(input_path)

    chunks = chunk_markdown(text, chapters ,source_name=input_path)
    chunks = split_exercises_in_chunks(chunks,chapters)
    chunks = [basic_chunk_preprocessing(c) for c in chunks]
    chunks = [c for c in chunks if c.get('type') != 'exercise']

    folder_path = "chunks"

    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder '{folder_path}' created (or already exists).")

    base_name = os.path.basename(input_path)              # "MATH 11.md"
    name_without_ext = os.path.splitext(base_name)[0]     # "MATH 11"
    safe_name = name_without_ext.replace(" ", "_").lower()  # "math_11"

    output_path = os.path.join(folder_path, f"{safe_name}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"\nSaved chunks to: {output_path}\n")

    # view_chunks(chunks)
    
    return chunks



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Chunk a markdown file and save JSON output.")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input markdown file. Example: 'markdown DS (NON IMG)/MATH 11.md'"
    )

    args = parser.parse_args()

    input_path = args.input

    chunk_pipeline(MATH_11_CHAPTERS,input_path)

    