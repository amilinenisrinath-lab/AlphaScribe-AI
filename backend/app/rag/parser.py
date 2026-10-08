from pathlib import Path
from typing import List, Dict, Any
import fitz  # PyMuPDF

class FinancialDocumentParser:
    """Parses complex financial documents (10-K, 10-Q) preserving table structure."""

    @staticmethod
    def extract_text_and_tables(file_path: Path) -> List[Dict[str, Any]]:
        """Extracts structured text page by page with basic table formatting."""
        doc = fitz.open(file_path)
        pages_content = []

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            
            # Extract plain text
            text = page.get_text("text").strip()
            
            # Extract tables if PyMuPDF table detection is available
            tables_data = []
            try:
                tables = page.find_tables()
                for table in tables:
                    df = table.extract()
                    if df:
                        # Convert table rows into clean markdown table representation
                        header = " | ".join(str(cell or "").strip() for cell in df[0])
                        separator = " | ".join(["---"] * len(df[0]))
                        rows = [" | ".join(str(cell or "").strip() for cell in row) for row in df[1:]]
                        md_table = f"{header}\n{separator}\n" + "\n".join(rows)
                        tables_data.append(md_table)
            except Exception:
                pass  # Fallback to pure text extraction

            pages_content.append({
                "page_number": page_idx + 1,
                "text": text,
                "tables": tables_data
            })

        doc.close()
        return pages_content

    @classmethod
    def chunk_document(
        cls, 
        pages_content: List[Dict[str, Any]], 
        chunk_size: int = 1000, 
        overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """Splits page content into semantic chunks preserving financial tables."""
        chunks = []
        chunk_id = 0

        for page in pages_content:
            page_num = page["page_number"]
            page_text = page["text"]
            
            # First, treat each extracted table as a standalone high-priority chunk
            for table_idx, table_str in enumerate(page["tables"]):
                chunk_id += 1
                chunks.append({
                    "chunk_id": f"p{page_num}_tbl{table_idx+1}_{chunk_id}",
                    "page_number": page_num,
                    "content": f"[FINANCIAL TABLE - Page {page_num}]\n{table_str}",
                    "is_table": True
                })

            # Chunk narrative text with sliding window
            if len(page_text) <= chunk_size:
                if page_text:
                    chunk_id += 1
                    chunks.append({
                        "chunk_id": f"p{page_num}_narrative_{chunk_id}",
                        "page_number": page_num,
                        "content": page_text,
                        "is_table": False
                    })
            else:
                start = 0
                while start < len(page_text):
                    end = start + chunk_size
                    chunk_text = page_text[start:end]
                    chunk_id += 1
                    chunks.append({
                        "chunk_id": f"p{page_num}_narrative_{chunk_id}",
                        "page_number": page_num,
                        "content": chunk_text,
                        "is_table": False
                    })
                    start += (chunk_size - overlap)

        return chunks
