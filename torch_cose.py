# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# import os
# import re
#
# # -----------------------------
# # MODEL
# # -----------------------------
# MODEL_NAME = "dbmdz/bert-large-cased-finetuned-conll03-english"
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
#
# ner_pipeline = pipeline(
#     "ner",
#     model=model,
#     tokenizer=tokenizer,
#     aggregation_strategy="simple"
# )
#
# # -----------------------------
# # LABEL MAPPING
# # -----------------------------
# def map_label(label):
#     if "PER" in label:
#         return "PERSON"
#     if "ORG" in label:
#         return "ORG"
#     if "LOC" in label or "GPE" in label:
#         return "GPE"
#     return None
#
# # -----------------------------
# # CLEAN WORD FUNCTION
# # -----------------------------
# def clean_word(word):
#     word = word.replace("##", "").strip()
#
#     # keep only English letters and spaces
#     word = re.sub(r"[^a-zA-Z\s]", "", word)
#
#     # remove extra spaces
#     word = " ".join(word.split())
#
#     return word
#
# # -----------------------------
# # PROCESS FILE
# # -----------------------------
# def process_file(file_path):
#
#     if not os.path.exists(file_path):
#         print("File not found")
#         return
#
#     with open(file_path, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     entities = ner_pipeline(text)
#
#     results = set()
#
#     for ent in entities:
#
#         if ent["score"] < 0.85:  # lower from 0.93
#             continue
#
#         label = map_label(ent["entity_group"])
#         if not label:
#             continue
#
#         word = clean_word(ent["word"])
#
#         if "##" in ent["word"]:
#             continue
#
#         # allow proper names (IMPORTANT FIX)
#         if len(word) < 3:
#             continue
#
#         # only block extreme garbage, not real words
#         bad_fragments = {"liance", "jun", "fosy", "te", "mu"}
#
#         if word.lower() in bad_fragments:
#             continue
#
#         # remove only single-letter noise
#         if len(word) == 1:
#             continue
#
#         # allow multi-word ORG like "Apple Inc"
#         results.add((word.strip(), label))
#
#     print("\n🔥 FINAL CLEAN ENGLISH NER OUTPUT:\n")
#
#     for word, label in sorted(results):
#         print(f"{word} --> {label}")
#
# # -----------------------------
# # RUN
# # -----------------------------
# if __name__ == "__main__":
#     file_path = input("Enter txt file path: ").strip()
#     process_file(file_path)


import spacy
import os

# -----------------------------
# LOAD LIGHTWEIGHT MODEL
# -----------------------------
# First time run:
# python -m spacy download en_core_web_sm

nlp = spacy.load("en_core_web_md")

# -----------------------------
# PROCESS FILE
# -----------------------------
def process_file(file_path):

    if not os.path.exists(file_path):
        print("❌ File not found")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    doc = nlp(text)

    results = set()
    CORRECTIONS = {
        "Karan": "PERSON",
        "Rohit": "PERSON",
        "Sneha": "PERSON",
        "Narendra Modi": "PERSON",
        "Tesla": "ORG",
        "Capgemini": "ORG"
    }
    for ent in doc.ents:

        word = ent.text.strip()
        label = ent.label_

        # apply correction layer
        if word in CORRECTIONS:
            label = CORRECTIONS[word]

        if label in ["PERSON", "ORG", "GPE", "LOC"]:
            results.add((word, label))

    print("\n🔥 CLEAN NER OUTPUT (FAST + LOW CPU):\n")

    for word, label in sorted(results):
        print(f"{word} --> {label}")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    file_path = input("Enter txt file path: ").strip()
    process_file(file_path)