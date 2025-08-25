import os
def iter_files(root, exts=(".pdf",".docx",".txt")):
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith(exts):
                yield os.path.join(dirpath, f)

def chunk_text(text, chunk_size=800, chunk_overlap=200):
    words, chunks, i = text.split(), [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+chunk_size]))
        i += max(1, chunk_size - chunk_overlap)
    return chunks
