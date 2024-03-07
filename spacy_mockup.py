from pathlib import Path

from IPython.core.display import HTML
import spacy
import fitz  # PyMuPDF
from spacy import displacy
#import en_core_web_sm

# Load the language model
nlp = spacy.load("en_core_web_sm")
# nlp = en_core_web_sm.load()

# Read the content of the PDF document
pdf_document = "/home/ermaro/know-sdgs/external/policy-mapping_2/data/52019DC0640/EN/PDF/52019DC0640_EN_DOC_1.pdf"
text = ""
with fitz.open(pdf_document) as doc:
    for page_num in range(len(doc)):
        page = doc[page_num]
        text += page.get_text("text")

# Tokenize the text using spaCy
doc = nlp(text)

# Identify keywords or entities and count their occurrences
keywords = {"climate change" : "SDG-13", "biodiversity" : "SDG-15", "sustainable food" : "SDG-12"}  # Replace with your actual keywords
#keywords = ["climate change" , "biodiversity", "sustainable food"]
keyword_counts = {keyword: 0 for keyword in keywords}
for token in doc:
    if token.text in keywords.keys():
        keyword_counts[token.text] += 1

# Create a list of colors for each keyword
colors = {"climate change" : "#ff5733", "biodiversity" : "#33ff57", "sustainable food" : "#3366ff"}  # Replace with colors of your choice

# Highlight each keyword with a different color and label using spaCy's visualizer
options = {"ents": keywords.keys(), "colors": colors, "labels": keywords}
html = displacy.render(doc, style="ent", page=True, minify=True, options=options) #jupyter=True
output_path = Path(__file__).parent.joinpath("sentences.html")
output_path.open("w", encoding="utf-8").write(html)

# Display the keyword counts
for keyword, count in keyword_counts.items():
    print(f"The keyword '{keyword}' appears {count} times in the document.")