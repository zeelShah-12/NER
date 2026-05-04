import spacy
import os
import re

nlp = spacy.load("en_core_web_md")
nlp.max_length = 2000000

# -----------------------------
# CLEAN
# -----------------------------
def clean(t):
    return t.strip()

def normalize(t):
    return re.sub(r"\s+", " ", t.strip().lower())

# -----------------------------
# ❌ REMOVE NON-ENTITIES (CRITICAL FIX)
# -----------------------------
NON_ENTITIES = {
    "software engineer", "recruitment team", "hr team",
    "cinema", "movie", "film", "engineering", "department",
    "manager", "engineer", "team"
}

def is_non_entity(t):
    return t in NON_ENTITIES

# -----------------------------
# ORG DETECTION
# -----------------------------
def is_org(t):
    org_keywords = [
        "inc", "ltd", "technologies", "systems",
        "services", "solutions", "industries"
    ]

    known_orgs = {
        "google", "microsoft", "amazon", "facebook",
        "apple inc.", "tesla", "infosys", "tcs",
        "wipro", "accenture", "ibm", "capgemini",
        "deloitte", "hsbc", "meta", "reliance industries",
        "hcl technologies", "spacex"
    }

    return t in known_orgs or any(k in t for k in org_keywords)

# -----------------------------
# GPE DETECTION
# -----------------------------
def is_gpe(t):
    gpes = {
        "india", "usa", "united states", "california",
        "london", "mumbai", "delhi", "bangalore",
        "hyderabad", "chennai", "pune", "noida",
        "gurgaon", "cupertino", "lucknow", "mysore",
        "new york"
    }

    return t in gpes

# -----------------------------
# PERSON DETECTION (STRICT)
# -----------------------------
def is_person(ent):
    words = ent.text.split()

    return (
        ent.label_ == "PERSON" and
        1 <= len(words) <= 3 and
        ent.text[0].isupper()
    )

# -----------------------------
# PROCESS
# -----------------------------
def process_file(path):

    if not os.path.exists(path):
        print("File not found")
        return

    text = open(path, encoding="utf-8").read()
    doc = nlp(text)

    results = set()

    for ent in doc.ents:

        t = normalize(ent.text)

        # -----------------------------
        # STEP 0: REMOVE NON-ENTITIES
        # -----------------------------
        if is_non_entity(t):
            continue

        # -----------------------------
        # STEP 1: ORG
        # -----------------------------
        if is_org(t):
            results.add((ent.text, "ORG"))

        # -----------------------------
        # STEP 2: GPE
        # -----------------------------
        elif is_gpe(t):
            results.add((ent.text, "GPE"))

        # -----------------------------
        # STEP 3: PERSON (ONLY REAL PEOPLE)
        # -----------------------------
        elif is_person(ent):
            results.add((ent.text, "PERSON"))

    print("\nFINAL CLEAN OUTPUT:\n")

    for r in sorted(results):
        print(r[0], "-->", r[1])


file_path = input("Enter txt file path: ").strip()
process_file(file_path)