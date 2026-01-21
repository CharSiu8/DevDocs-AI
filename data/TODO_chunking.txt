# =============================================================================
# TODO LIST - CHUNKING.PY
# =============================================================================

# ✅ COMPLETED (Jan 20):
# - chunk_text(): Split text into fixed-size chunks with overlap
# - chunk_document(): Chunk a single doc, preserve metadata (url, title, chunk_index)
# - chunk_all_docs(): Load JSON, chunk all 145 docs, save results (6148 chunks)
# - Sentence boundaries: Don't split mid-sentence. went from 6,148 to 14,285 in output because now we have smaller, complete sentances.



# 🔧 ADD LATER (if needed to improve quality):
# - Sentance boundaries are slowing down chunking significantly, consider optimizing by comniniing the searches or using regex
# - Token counting: Use tiktoken instead of character count (more accurate for LLMs)
# - Code block handling: Don't split in the middle of code examples
# - Chunk quality scoring: Flag chunks that are too short or incomplete

# 🚀 V2 FEATURES (smarter chunking):
# - SemanticChunker: Split on headings/paragraphs instead of fixed size
# - HierarchicalChunker: Parent chunks (sections) + child chunks (paragraphs)
# - Metadata enrichment: Add section headers, has_code flag

# =============================================================================
