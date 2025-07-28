# Connecting the Dots — Round 1A

## Challenge Objective

Reimagine how machines read PDFs by extracting structured outlines from raw documents. This includes identifying the **title**, and **headings** (H1, H2, H3) in a hierarchical format to enable intelligent downstream applications like semantic search, document navigation, and summarization.

---

## Solution Overview

Our solution reads PDFs, extracts their structural elements, and outputs them as a clean JSON outline.

### Key Components

- **Text Extraction**: Leveraged `PyMuPDF` (`fitz`) to extract text, font size, font style, and positioning.
- **Title Detection**: Title is defined as the first large-font text (H1) on the first page.
- **Heading Detection**:
  - Top 3 font sizes dynamically mapped to `H1`, `H2`, `H3`
  - Font + layout-based heuristics used instead of hardcoding sizes
- **Line Merging**:
  - Spans with similar font, same page, and close vertical proximity are merged
  - Merging is skipped when the next line looks like a new section (e.g., starts with a capital/number or ends with a period)
- **Noise Filtering**:
  - Filters out fragments like "fare", "bus", "rs.", etc.
  - Ignores overly short or repeated utility words

---

## 📦 File Structure

connecting-dots-round1a/

├── extract_headings.py # Main script

├── requirements.txt # Python dependency list

├── Dockerfile # Build file for containerized environment

├── README.md # You’re reading it

├── input/ # Input PDFs

└── output/ # JSON output files

---

## 📁 Input / Output Format

### 🧾 Input:
- Any `.pdf` file placed in the `input/` folder

### 📤 Output:
- A `.json` file with the same base name in the `output/` folder  
- Format:

{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}

---

## Docker Instructions

### Build the Docker Image

docker build --platform linux/amd64 -t mysolution:abc123 .

### Run the Container

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolution:abc123
On Windows CMD use:
docker run --rm -v %cd%/input:/app/input -v %cd%/output:/app/output --network none mysolution:abc123

---

## Constraints Met

## ✅ Constraints Met

| Constraint                     | Status   |
|-------------------------------|----------|
| CPU-only, no GPU              | ✅       |
| Offline mode (no network)     | ✅       |
| Execution time ≤ 10s (50 pgs) | ✅       |
| Model size < 200MB            | ✅ (no model used) |
| Output format valid JSON      | ✅       |

---

## Sample Output

{
  "title": "Application form for grant of LTC advance",
  "outline": [
    {
      "level": "H1",
      "text": "Application form for grant of LTC advance",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Name of the Government Servant",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Designation",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Date of entering the Central Government",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Service",
      "page": 1
    },
    {
      "level": "H2",
      "text": "PAY + SI + NPA",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Whether permanent or temporary",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Home Town as recorded in the Service Book",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Whether wife / husband is employed and if so whether entitled to LTC",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Whether the concession is to be availed for visiting home town and if so block for which",
      "page": 1
    },
    {
      "level": "H2",
      "text": "LTC is to be availed.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "(a) If the concession is to visit anywhere in",
      "page": 1
    },
    {
      "level": "H2",
      "text": "India, the place to be visited.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "(b) Block for which to be availed.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "fare/bus headquarters to home town/place of visit by",
      "page": 1
    },
    {
      "level": "H2",
      "text": "shortest route.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Persons in respect of whom LTC is proposed to be availed.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Relationship",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Amount of advance required.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "I declare that the particulars furnished above are true and correct to the best of my knowledge.  I",
      "page": 1
    },
    {
      "level": "H2",
      "text": "undertake to produce the tickets for the outward journey within ten days of receipt of the advance.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "In the event of cancellation of the journey or if I fail to produce the tickets within ten days of receipt of",
      "page": 1
    },
    {
      "level": "H2",
      "text": "advance, I undertake to refund the entire advance in one lump sum.",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Signature of Government Servant.",
      "page": 1
    }
  ]
}
