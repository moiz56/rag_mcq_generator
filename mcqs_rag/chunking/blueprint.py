from utility import load_chunks
from argparse import ArgumentParser

def build_blueprint(chunks):
    """
    Build a hierarchical blueprint with chunk_index for numeric ordering.
    Strips '#' from chapter names.
    """
    blueprint = {}

    for chunk in chunks:
        if chunk.get("type") not in ["chapter", "header", "exercise"]:
            continue

        chap_id = chunk.get("chapter_id", "")
        chap_name = chunk.get("chapter_name", "").lstrip("#").strip()
        chap_index = chunk.get("chunk_index", None)

        sec_id = chunk.get("section_id", "")
        sec_name = chunk.get("section_name", "")
        sec_index = chunk.get("chunk_index", None)

        sub_id = chunk.get("subsection_id", "")
        sub_name = chunk.get("subsection_name", "")
        sub_index = chunk.get("chunk_index", None)

        # Initialize chapter
        if chap_id and chap_id not in blueprint:
            blueprint[chap_id] = {
                "chapter_name": chap_name,
                "chunk_index": chap_index,
                "sections": {}
            }

        chapter = blueprint[chap_id]

        # Initialize section
        if sec_id:
            if sec_id not in chapter["sections"]:
                chapter["sections"][sec_id] = {
                    "section_name": sec_name or "",
                    "chunk_index": sec_index,
                    "subsections": {}
                }

            section = chapter["sections"][sec_id]

            # Initialize subsection
            if sub_id:
                if sub_id not in section["subsections"]:
                    section["subsections"][sub_id] = {
                        "subsection_name": sub_name or "",
                        "chunk_index": sub_index
                    }

        blueprint[chap_id] = chapter

    return blueprint


def print_blueprint(blueprint):
    """
    Print blueprint sorted by chunk_index instead of IDs.
    """
    # Sort chapters by chunk_index
    sorted_chaps = sorted(blueprint.items(), key=lambda x: x[1].get("chunk_index", 0))

    for chap_id, chap_data in sorted_chaps:
        chunk_info = f" (Chunk {chap_data['chunk_index']})" if chap_data.get('chunk_index') else ""
        print(f"Chapter {chap_id}: {chap_data.get('chapter_name', '')}{chunk_info}")

        # Sort sections by chunk_index
        sorted_secs = sorted(chap_data.get("sections", {}).items(), key=lambda x: x[1].get("chunk_index", 0))
        for sec_id, sec_data in sorted_secs:
            chunk_info = f" (Chunk {sec_data['chunk_index']})" if sec_data.get('chunk_index') else ""
            print(f"  Section {sec_id}: {sec_data.get('section_name', '')}{chunk_info}")

            # Sort subsections by chunk_index
            sorted_subs = sorted(sec_data.get("subsections", {}).items(), key=lambda x: x[1].get("chunk_index", 0))
            for sub_id, sub_data in sorted_subs:
                chunk_info = f" (Chunk {sub_data['chunk_index']})" if sub_data.get('chunk_index') else ""
                print(f"    Subsection {sub_id}: {sub_data.get('subsection_name', '')}{chunk_info}")

        print("-" * 50)
        
        
if __name__ == "__main__":
    parser = ArgumentParser(description="Build and print blueprint from chunks.")
    parser.add_argument("--chunks_file", type=str, required=True, help="Path to the chunks JSON file.")
    args = parser.parse_args()

    chunks = load_chunks(args.chunks_file)
    blueprint = build_blueprint(chunks)
    print_blueprint(blueprint)
