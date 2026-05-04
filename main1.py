import spacy
import os
import re

nlp = spacy.load("en_core_web_md")
nlp.max_length = 2000000

# -----------------------------
# FILTERS
# -----------------------------
REMOVE = {"thanks", "regards", "best"}

ORG_KEYWORDS = [
    "inc", "ltd", "technologies", "systems",
    "services", "solutions", "industries", "company"
]

GPE_KEYWORDS = [
    "india", "usa", "united states", "new york",
    "california", "texas", "london", "mumbai",
    "delhi", "bangalore", "chennai", "hyderabad",
    "pune", "noida", "gurgaon", "cupertino",
    "lucknow", "mysore"
]

KNOWN_ORGS = {
    "google", "microsoft", "amazon", "facebook",
    "apple inc.", "tesla", "infosys", "tcs",
    "wipro", "accenture", "ibm", "capgemini",
    "deloitte", "hsbc", "meta", "reliance industries",
    "hcl technologies", "space x"
}

# -----------------------------
# NORMALIZATION (IMPORTANT FIX)
# -----------------------------
def normalize(text):
    text = text.lower().strip()

    # fix no-space issues like "newyork"
    text = re.sub(r'newyork', 'new york', text)
    text = re.sub(r'usa', 'united states', text)

    return text

# -----------------------------
# CLEAN OUTPUT TEXT
# -----------------------------
def clean(text):
    return text.strip().replace("Dear ", "")

# -----------------------------
# FINAL CLASSIFIER
# -----------------------------
def classify(text, label):

    t = normalize(text)

    # ❌ REMOVE JUNK
    if any(x in t for x in REMOVE):
        return None

    # -----------------------------
    # 🔵 ORG FIRST (HIGHEST PRIORITY)
    # -----------------------------
    if t in KNOWN_ORGS:
        return "ORG"

    if any(x in t for x in ORG_KEYWORDS):
        return "ORG"

    # -----------------------------
    # 🔵 GPE SECOND
    # -----------------------------
    if t in GPE_KEYWORDS:
        return "GPE"

    # -----------------------------
    # 🔵 PERSON LAST (ONLY IF SAFE)
    # -----------------------------
    if label == "PERSON":
        words = text.split()

        if len(words) <= 3 and text[0].isupper():
            return "PERSON"

    return None

# -----------------------------
# PROCESS FILE
# -----------------------------
def process_file(path):

    if not os.path.exists(path):
        print("File not found")
        return

    text = open(path, encoding="utf-8").read()
    doc = nlp(text)

    results = set()

    for ent in doc.ents:

        if ent.label_ not in ["PERSON", "ORG", "GPE"]:
            continue

        label = classify(ent.text, ent.label_)

        if label:
            results.add((clean(ent.text), label))

    print("\nFINAL CLEAN OUTPUT:\n")

    for r in sorted(results):
        print(r[0], "-->", r[1])


file_path = input("Enter txt file path: ").strip()
process_file(file_path)