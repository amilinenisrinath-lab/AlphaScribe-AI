import fitz

doc = fitz.open(r"C:\Users\amili\Downloads\Srinath Chowdary Amilineni - Resume (Goldman Sachs).pdf")
for i, page in enumerate(doc):
    print(f"=== PAGE {i+1} ===")
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                line_text = "".join(s["text"] for s in l["spans"]).strip()
                if line_text:
                    sample_span = l["spans"][0]
                    print(f"[{sample_span['size']:.1f}pt | {sample_span['font']}] {line_text}")
