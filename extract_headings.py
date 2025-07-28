from flask import Flask, request, jsonify, send_from_directory
import os
import fitz
import json
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "input"
OUTPUT_FOLDER = "output"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_text(text):
    text = text.strip()
    if not text or len(text) < 4:
        return None
    if text.lower() in {"the", "a", "an", "in", "fare", "from", "date", "age", "name", "bus", "rail", "rs."}:
        return None
    if re.match(r"^\d+$", text):
        return None
    return text

def is_likely_new_section(text):
    return bool(re.match(r"^[A-Z0-9(\[]", text.strip())) or text.strip().endswith(".") or text.strip().endswith(":")

def merge_spans(spans, max_y_gap=8):
    merged = []
    i = 0
    while i < len(spans):
        current = spans[i].copy()
        i += 1
        while i < len(spans):
            next_span = spans[i]
            same_style = current["size"] == next_span["size"] and current["font"] == next_span["font"]
            close_vertically = abs(next_span["bbox"][1] - current["bbox"][3]) < max_y_gap
            same_page = current["page"] == next_span["page"]
            merge_safe = not is_likely_new_section(next_span["text"])
            if same_style and close_vertically and same_page and merge_safe:
                current["text"] += " " + next_span["text"]
                current["bbox"] = (
                    min(current["bbox"][0], next_span["bbox"][0]),
                    current["bbox"][1],
                    max(current["bbox"][2], next_span["bbox"][2]),
                    next_span["bbox"][3],
                )
                i += 1
            else:
                break
        merged.append(current)
    return merged

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    spans = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = clean_text(s["text"])
                    if not text:
                        continue
                    spans.append({
                        "text": text,
                        "size": s["size"],
                        "font": s["font"],
                        "bbox": s["bbox"],
                        "page": page_num
                    })

    merged_spans = merge_spans(spans)
    unique_sizes = sorted({s["size"] for s in merged_spans}, reverse=True)
    size_to_level = {}
    if len(unique_sizes) > 0:
        size_to_level[unique_sizes[0]] = "H1"
    if len(unique_sizes) > 1:
        size_to_level[unique_sizes[1]] = "H2"
    if len(unique_sizes) > 2:
        size_to_level[unique_sizes[2]] = "H3"

    outline = []
    title = ""
    for span in merged_spans:
        level = size_to_level.get(span["size"])
        if level:
            if not title and level == "H1" and span["page"] == 1:
                title = span["text"]
            outline.append({
                "level": level,
                "text": span["text"],
                "page": span["page"]
            })

    return {
        "title": title or "Untitled Document",
        "outline": outline
    }

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(pdf_path)

    try:
        result = extract_outline_from_pdf(pdf_path)
        # ⚠️ Use the correct base URL if deployed
        pdf_url = f"http://127.0.0.1:5000/input/{filename}"
        result["success"] = True
        result["pdf_url"] = pdf_url
        result["filename"] = filename
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ➕ Route to serve uploaded PDF
@app.route("/input/<filename>")
def serve_pdf(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
