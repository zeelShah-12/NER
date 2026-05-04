# import spacy
# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# import os
#
# # -----------------------------
# # 1. LOAD SPACY (FAST LAYER)
# # -----------------------------
# nlp = spacy.load("en_core_web_md")
#
# # -----------------------------
# # 2. LOAD TRANSFORMER (FALLBACK ONLY)
# # -----------------------------
# MODEL_NAME = "dslim/bert-base-NER"
#
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
#
# ner_model = pipeline(
#     "ner",
#     model=model,
#     tokenizer=tokenizer,
#     aggregation_strategy="simple",
#     device=-1
# )
#
# # -----------------------------
# # 3. KNOWLEDGE BASE (FINAL LAYER)
# # -----------------------------
# PERSON_LIST = {
#     "Elon Musk", "Deepika Padukone", "Sundar Pichai",
#     "Narendra Modi", "Rahul Sharma", "Priya", "Vipul",
#     "Karan", "Rohit", "Sneha"
# }
#
# ORG_LIST = {
#     "Google", "Microsoft", "Amazon", "Apple Inc",
#     "TCS", "Infosys", "Meta", "IBM", "Capgemini",
#     "Deloitte", "Netflix", "SpaceX", "Tesla", "Accenture",
#     "Amazon Web Services", "IIT Delhi"
# }
#
# GPE_LIST = {
#     "India", "USA", "Germany", "London", "Mumbai",
#     "Delhi", "Bangalore", "Hyderabad", "Pune",
#     "New York", "Los Angeles", "San Francisco",
#     "California", "New Delhi"
# }
#
# # -----------------------------
# # 4. CLEAN FUNCTION
# # -----------------------------
# def clean(text):
#     return text.strip()
#
# # -----------------------------
# # 5. ENTITY ENFORCEMENT (IMPORTANT FIX)
# # -----------------------------
# def enforce_entity_type(word, label):
#
#     if word in PERSON_LIST:
#         return "PERSON"
#
#     if word in ORG_LIST:
#         return "ORG"
#
#     if word in GPE_LIST:
#         return "GPE"
#
#     return label
#
# # -----------------------------
# # 6. VALIDATION ENGINE
# # -----------------------------
# def is_valid(word):
#
#     if len(word) < 3:
#         return False
#
#     bad = {"deep", "sun", "riya", "ika", "noi", "fosys", "liance"}
#
#     if word.lower() in bad:
#         return False
#
#     if not any(c.isalpha() for c in word):
#         return False
#
#     return True
#
# # -----------------------------
# # 7. TRANSFORMER FALLBACK
# # -----------------------------
# def transformer_fallback(text):
#
#     results = []
#
#     ents = ner_model(text)
#
#     for e in ents:
#
#         label = e["entity_group"]
#         word = e["word"].strip()
#
#         if label == "PER":
#             label = "PERSON"
#         elif label in ["LOC", "GPE"]:
#             label = "GPE"
#         elif label == "ORG":
#             label = "ORG"
#
#         results.append((word, label))
#
#     return results
#
# # -----------------------------
# # 8. MAIN PIPELINE
# # -----------------------------
# def process(text):
#
#     doc = nlp(text)
#
#     results = set()
#
#     # STEP 1: SPACY EXTRACTION
#     for ent in doc.ents:
#
#         word = clean(ent.text)
#         label = ent.label_
#
#         if not is_valid(word):
#             continue
#
#         label = enforce_entity_type(word, label)
#
#         results.add((word, label))
#
#     # STEP 2: FALLBACK IF WEAK OUTPUT
#     if len(results) < 5:
#         fallback = transformer_fallback(text)
#
#         for w, l in fallback:
#             if is_valid(w):
#                 l = enforce_entity_type(w, l)
#                 results.add((w, l))
#
#     return results
#
# # -----------------------------
# # 9. FILE RUNNER
# # -----------------------------
# def run_file(path):
#
#     if not os.path.exists(path):
#         print("❌ File not found")
#         return
#
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     output = process(text)
#
#     print("\n🔥 FINAL HYBRID NER OUTPUT:\n")
#
#     for w, l in sorted(output):
#         print(f"{w} --> {l}")
#
# # -----------------------------
# # 10. RUN PROGRAM
# # -----------------------------
# if __name__ == "__main__":
#     file_path = input("Enter txt file path: ").strip()
#     run_file(file_path)

# import spacy
# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# import os
#
# # =============================
# # 1. SPACY FAST MODEL
# # =============================
# nlp = spacy.load("en_core_web_md")
#
# # =============================
# # 2. TRANSFORMER FALLBACK
# # =============================
# MODEL_NAME = "dslim/bert-base-NER"
#
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
#
# ner_model = pipeline(
#     "ner",
#     model=model,
#     tokenizer=tokenizer,
#     aggregation_strategy="simple",
#     device=-1
# )
#
# # =============================
# # 3. KNOWLEDGE BASE
# # =============================
# PERSONS = {
#     "Elon Musk", "Deepika Padukone", "Sundar Pichai",
#     "Narendra Modi", "Rahul Sharma", "Priya", "Vipul",
#     "Karan", "Rohit", "Sneha"
# }
#
# ORG = {
#     "Google", "Microsoft", "Amazon", "Apple Inc",
#     "TCS", "Infosys", "Meta", "IBM", "Capgemini",
#     "Deloitte", "Netflix", "SpaceX", "Tesla",
#     "Neuralink", "Amazon Web Services",
#     "Google DeepMind", "Accenture", "IIT Delhi"
# }
#
# GPE = {
#     "India", "USA", "Germany", "London", "Mumbai",
#     "Delhi", "Bangalore", "Hyderabad", "Pune",
#     "New York", "Los Angeles", "San Francisco",
#     "California", "New Delhi", "Gurgaon",
#     "Florida", "Texas", "Seattle"
# }
#
# PRODUCTS = {"iPhone", "Samsung", "iPad"}
#
# # =============================
# # 4. IGNORE NON-ENTITIES
# # =============================
# IGNORE = {
#     "quantum",
#     "machine learning",
#     "artificial intelligence",
#     "deep learning",
#     "computer science"
# }
#
# # =============================
# # 5. CLEAN
# # =============================
# def clean(text):
#     return text.strip()
#
# # =============================
# # 6. VALIDATION
# # =============================
# def valid(word):
#     if len(word) < 3:
#         return False
#     if not any(c.isalpha() for c in word):
#         return False
#     return True
#
# # =============================
# # 7. FINAL CONTEXT ENGINE (MOST IMPORTANT)
# # =============================
# def context_fix(word, label):
#
#     if word in IGNORE:
#         return None
#
#     if word in PRODUCTS:
#         return "PRODUCT"
#
#     if word in ORG:
#         return "ORG"
#
#     if word in PERSONS:
#         return "PERSON"
#
#     if word in GPE:
#         return "GPE"
#
#     return label
#
# # =============================
# # 8. TRANSFORMER FALLBACK
# # =============================
# def fallback(text):
#
#     results = []
#
#     ents = ner_model(text)
#
#     for e in ents:
#
#         word = e["word"].strip()
#         label = e["entity_group"]
#
#         if label == "PER":
#             label = "PERSON"
#         elif label in ["LOC", "GPE"]:
#             label = "GPE"
#         elif label == "ORG":
#             label = "ORG"
#
#         results.append((word, label))
#
#     return results
#
# # =============================
# # 9. MAIN PIPELINE
# # =============================
# def process(text):
#
#     doc = nlp(text)
#
#     results = set()
#
#     # STEP 1: SPACY
#     for ent in doc.ents:
#
#         word = clean(ent.text)
#         label = ent.label_
#
#         if not valid(word):
#             continue
#
#         label = context_fix(word, label)
#
#         if label:
#             results.add((word, label))
#
#     # STEP 2: FALLBACK IF LOW OUTPUT
#     if len(results) < 5:
#
#         fb = fallback(text)
#
#         for w, l in fb:
#
#             if valid(w):
#                 l = context_fix(w, l)
#                 if l:
#                     results.add((w, l))
#
#     return results
#
# # =============================
# # 10. FILE RUNNER
# # =============================
# def run_file(path):
#
#     if not os.path.exists(path):
#         print("File not found")
#         return
#
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     output = process(text)
#
#     print("\n FINAL CLEAN HYBRID NER OUTPUT:\n")
#
#     for w, l in sorted(output):
#         print(f"{w} --> {l}")
#
# # =============================
# # 11. RUN
# # =============================
# if __name__ == "__main__":
#     file_path = input("Enter txt file path: ").strip()
#     run_file(file_path)

# import spacy
# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# import os
#
# # =============================
# # 1. LOAD SPACY (FAST LAYER)
# # =============================
# nlp = spacy.load("en_core_web_md")
#
# # =============================
# # 2. TRANSFORMER (FALLBACK)
# # =============================
# MODEL_NAME = "dslim/bert-base-NER"
#
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
#
# ner_model = pipeline(
#     "ner",
#     model=model,
#     tokenizer=tokenizer,
#     aggregation_strategy="simple",
#     device=-1
# )
#
# # =============================
# # 3. KNOWLEDGE BASE (TRUTH MAP)
# # =============================
# PERSON = {
#     "Elon Musk", "Deepika Padukone", "Sundar Pichai",
#     "Narendra Modi", "Rahul Sharma", "Priya", "Vipul",
#     "Karan", "Rohit", "Sneha"
# }
#
# ORG = {
#     "Google", "Microsoft", "Amazon", "Apple Inc",
#     "TCS", "Infosys", "Meta", "IBM",
#     "Capgemini", "Deloitte", "Netflix",
#     "SpaceX", "Tesla", "Neuralink",
#     "Amazon Web Services", "Google DeepMind"
# }
#
# GPE = {
#     "India", "USA", "Germany", "London", "Mumbai",
#     "Delhi", "Bangalore", "Hyderabad", "Pune",
#     "New York", "Los Angeles", "San Francisco",
#     "California", "New Delhi", "Gurgaon",
#     "Florida", "Texas", "Seattle"
# }
#
# PRODUCT = {"iPhone", "Samsung", "iPad"}
#
# # =============================
# # 4. IGNORE NON-ENTITIES
# # =============================
# IGNORE = {
#     "quantum",
#     "machine learning",
#     "artificial intelligence",
#     "computer science",
#     "software engineering"
# }
#
# # =============================
# # 5. VALIDATION
# # =============================
# def valid(word):
#     return len(word) > 2 and any(c.isalpha() for c in word)
#
# # =============================
# # 6. CONTEXT FIX ENGINE
# # =============================
# def fix_entity(word, label):
#
#     if word in IGNORE:
#         return None
#
#     if word in PRODUCT:
#         return "PRODUCT"
#
#     if word in ORG:
#         return "ORG"
#
#     if word in PERSON:
#         return "PERSON"
#
#     if word in GPE:
#         return "GPE"
#
#     return label
#
# # =============================
# # 7. FALLBACK MODEL
# # =============================
# def transformer_fallback(text):
#
#     results = []
#
#     ents = ner_model(text)
#
#     for e in ents:
#
#         word = e["word"].strip()
#         label = e["entity_group"]
#
#         if label == "PER":
#             label = "PERSON"
#         elif label in ["LOC", "GPE"]:
#             label = "GPE"
#         elif label == "ORG":
#             label = "ORG"
#
#         results.append((word, label))
#
#     return results
#
# # =============================
# # 8. MAIN PIPELINE
# # =============================
# def process(text):
#
#     doc = nlp(text)
#
#     results = set()
#
#     # STEP 1: spaCy extraction
#     for ent in doc.ents:
#
#         word = ent.text.strip()
#         label = ent.label_
#
#         if not valid(word):
#             continue
#
#         label = fix_entity(word, label)
#
#         if label:
#             results.add((word, label))
#
#     # STEP 2: fallback if low results
#     if len(results) < 5:
#
#         fb = transformer_fallback(text)
#
#         for w, l in fb:
#
#             if valid(w):
#                 l = fix_entity(w, l)
#                 if l:
#                     results.add((w, l))
#
#     return results
#
# # =============================
# # 9. FILE RUNNER
# # =============================
# def run_file(path):
#
#     if not os.path.exists(path):
#         print("File not found")
#         return
#
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     output = process(text)
#
#     print("\n🔥 FINAL CLEAN HYBRID NER OUTPUT:\n")
#
#     for w, l in sorted(output):
#         print(f"{w} --> {l}")
#
# # =============================
# # 10. RUN
# # =============================
# if __name__ == "__main__":
#     file_path = input("Enter txt file path: ").strip()
#     run_file(file_path)

# import spacy
# import os
#
# # ✔ LIGHT + STABLE MODEL
# nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer"])
#
# # =========================
# # KNOWLEDGE BASE (TRUTH FIX)
# # =========================
# PERSON = {
#     "Elon Musk", "Narendra Modi", "Sundar Pichai",
#     "Deepika Padukone", "Rahul Sharma", "Priya",
#     "Vipul", "Rohit", "Karan"
# }
#
# ORG = {
#     "Google", "Microsoft", "Amazon", "Apple", "Apple Inc",
#     "TCS", "Infosys", "Meta", "IBM",
#     "Capgemini", "Deloitte", "Netflix",
#     "SpaceX", "Tesla", "Neuralink",
#     "Amazon Web Services"
# }
#
# GPE = {
#     "India", "USA", "Germany", "London",
#     "Mumbai", "Delhi", "Bangalore", "Hyderabad",
#     "Pune", "New York", "Los Angeles",
#     "San Francisco", "California", "Texas"
# }
#
# # =========================
# # INVALID ENTITY FILTER
# # =========================
# IGNORE = {
#     "computer science",
#     "machine learning",
#     "artificial intelligence",
#     "quantum",
#     "software engineering",
#     "AI"
# }
#
# cache = {}
#
# # =========================
# # CLEANING FUNCTION
# # =========================
# def normalize(word):
#     return word.strip()
#
# def fix_entity(word, label):
#
#     word = normalize(word)
#
#     if word.lower() in IGNORE:
#         return None
#
#     # FORCE CORRECT LABELS
#     if word in PERSON:
#         return "PERSON"
#
#     if word in ORG:
#         return "ORG"
#
#     if word in GPE:
#         return "GPE"
#
#     # REMOVE WRONG spaCy LABELS
#     if label in ["WORK_OF_ART", "FAC", "LOC"]:
#         if word in GPE:
#             return "GPE"
#         if word in ORG:
#             return "ORG"
#
#     return label
#
# # =========================
# # MAIN PROCESS
# # =========================
# def process(text):
#
#     if text in cache:
#         return cache[text]
#
#     results = set()
#
#     # chunk for stability
#     chunks = [text[i:i+800] for i in range(0, len(text), 800)]
#
#     for chunk in chunks:
#
#         doc = nlp(chunk)
#
#         for ent in doc.ents:
#
#             word = ent.text.strip()
#             label = ent.label_
#
#             label = fix_entity(word, label)
#
#             if label:
#                 results.add((word, label))
#
#     cache[text] = results
#     return results
#
# # =========================
# # FILE RUNNER
# # =========================
# def run_file(path):
#
#     if not os.path.exists(path):
#         print("File not found")
#         return
#
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     output = process(text)
#
#     print("\n🔥 FINAL FIXED LOW CPU NER OUTPUT:\n")
#
#     for w, l in sorted(output):
#         print(f"{w} --> {l}")
#
# # =========================
# # RUN
# # =========================
# if __name__ == "__main__":
#     file_path = input("Enter txt file path: ").strip()
#     run_file(file_path)

# low cpu
# import re
# import os
#
# # =========================
# # KNOWLEDGE BASE
# # =========================
# PERSON = {
#     "Elon Musk", "Narendra Modi", "Sundar Pichai",
#     "Deepika Padukone", "Rahul Sharma", "Priya",
#     "Vipul", "Rohit", "Karan"
# }
#
# ORG = {
#     "Google", "Microsoft", "Amazon", "Apple", "Apple Inc",
#     "TCS", "Infosys", "Meta", "IBM",
#     "Capgemini", "Deloitte", "Netflix",
#     "SpaceX", "Tesla", "Reliance Industries"
# }
#
# GPE = {
#     "India", "USA", "Germany", "London",
#     "Mumbai", "Delhi", "Bangalore", "Hyderabad",
#     "Pune", "California", "Texas"
# }
#
# # =========================
# # PATTERNS
# # =========================
# DATE_PATTERN = r"\b(\d{1,2}(st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b"
#
# ORDINAL_PATTERN = r"\b\d{1,2}(st|nd|rd|th)\b"
#
# # =========================
# # CLEAN CHECK
# # =========================
# def valid_word(w):
#     return len(w) > 1 and w.isalpha() or " " in w
#
# def classify(word):
#
#     word = word.strip()
#
#     if word in PERSON:
#         return "PERSON"
#
#     if word in ORG:
#         return "ORG"
#
#     if word in GPE:
#         return "GPE"
#
#     return None
#
# # =========================
# # MAIN PROCESS
# # =========================
# def process(text):
#
#     results = set()
#
#     # DATE
#     for m in re.findall(DATE_PATTERN, text):
#         results.add((m[0], "DATE"))
#
#     # ORDINAL (SAFE FILTER)
#     for m in re.findall(ORDINAL_PATTERN, text):
#         if len(m[0]) > 2:
#             results.add((m[0], "ORDINAL"))
#
#     # CLEAN WORD SPLIT
#     words = text.split()
#
#     i = 0
#     while i < len(words):
#
#         found = False
#
#         for size in range(5, 0, -1):
#
#             chunk = " ".join(words[i:i+size]).strip(".,()")
#
#             if not valid_word(chunk):
#                 continue
#
#             label = classify(chunk)
#
#             if label:
#                 results.add((chunk, label))
#                 i += size
#                 found = True
#                 break
#
#         if not found:
#             i += 1
#
#     return results
#
# # =========================
# # RUN FILE
# # =========================
# def run_file(path):
#
#     if not os.path.exists(path):
#         print("File not found")
#         return
#
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#
#     output = process(text)
#
#     print("\n FINAL CLEAN ULTRA LOW CPU OUTPUT:\n")
#
#     for w, l in sorted(output):
#         print(f"{w} --> {l}")
#
# # =========================
# # RUN
# # =========================
# if __name__ == "__main__":
#     file_path = input("Enter txt file path: ").strip()
#     run_file(file_path)


# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForTokenClassification
#
# torch.set_num_threads(2)
#
# model_name = "dslim/bert-base-NER"
#
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForTokenClassification.from_pretrained(model_name)
#
# id2label = model.config.id2label
#
# # =============================
# # BIO MERGING (FIX CORE ISSUE)
# # =============================
# def merge_bio(tokens, labels):
#     entities = []
#     current_word = ""
#     current_label = None
#
#     for token, label in zip(tokens, labels):
#
#         if token in ["[CLS]", "[SEP]"]:
#             continue
#
#         if token.startswith("##"):
#             current_word += token[2:]
#             continue
#
#         if label.startswith("B-"):
#             if current_word:
#                 entities.append((current_word, current_label))
#
#             current_word = token
#             current_label = label[2:]
#
#         elif label.startswith("I-") and current_label == label[2:]:
#             current_word += " " + token
#
#         else:
#             if current_word:
#                 entities.append((current_word, current_label))
#             current_word = token
#             current_label = label[2:] if label != "O" else None
#
#     if current_word:
#         entities.append((current_word, current_label))
#
#     return entities
#
# # =============================
# # PREDICT
# # =============================
# def predict(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True)
#
#     with torch.no_grad():
#         outputs = model(**inputs)
#
#     preds = torch.argmax(outputs.logits, dim=2)[0].tolist()
#     tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
#
#     labels = [id2label[p] for p in preds]
#
#     merged = merge_bio(tokens, labels)
#
#     result = {}
#
#     for word, label in merged:
#         if not label:
#             continue
#         if len(word.strip()) < 2:
#             continue
#         result[word.strip()] = label
#
#     return result
#
# # =============================
# # RUN FILE
# # =============================
# def process_file(path):
#     text = open(path, encoding="utf-8").read()
#
#     print("\n🔥 FINAL CLEAN NER OUTPUT:\n")
#
#     result = predict(text)
#
#     for k, v in sorted(result.items()):
#         print(k, "-->", v)
#
# file_path = input("Enter txt file path: ").strip()
# process_file(file_path)

# import spacy
#
# print("Loading spaCy NER model (fast + stable)...")
#
# nlp = spacy.load("en_core_web_trf")  # lightweight CPU model
#
# # -----------------------------
# # CLEAN LABEL MAP
# # -----------------------------
# def map_label(label):
#     if label == "PERSON":
#         return "PERSON"
#     elif label == "ORG":
#         return "ORGANIZATION"
#     elif label in ["GPE", "LOC"]:
#         return "LOCATION"
#     return None
#
#
# file_path = input("Enter txt file path: ")
#
# with open(file_path, "r", encoding="utf-8") as f:
#     text = f.read()
#
# print("\nProcessing...\n")
#
# doc = nlp(text)
#
# seen = set()
#
# print("\n🔥 FINAL UPGRADED NER OUTPUT:\n")
#
# for ent in doc.ents:
#     label = map_label(ent.label_)
#     entity = ent.text.strip()
#
#     # clean noise
#     if not entity or len(entity) <= 1:
#         continue
#
#     # remove junk tokens
#     junk = {"In", "It", "He", "She", "A", "I"}
#     if entity in junk:
#         continue
#
#     key = (entity, label)
#
#     if label and key not in seen:
#         print(f"{entity} --> {label}")
#         seen.add(key)
#
# print("\nDone ✔")

# ========good accuracy but 32
# import spacy
# import re
# import time
#
# print("Running ULTRA LOW CPU NER (spaCy ONLY)...")
#
# # Load ONLY small model (fastest option)
# nlp = spacy.load("en_core_web_sm")
#
# # Simple cleanup rules (VERY LIGHT)
# def clean_entity(text):
#     text = text.strip()
#     text = re.sub(r"[^a-zA-Z0-9 .]", "", text)
#     return text
#
# def map_label(label):
#     if label in ["PERSON"]:
#         return "PERSON"
#     elif label in ["ORG"]:
#         return "ORGANIZATION"
#     elif label in ["GPE", "LOC"]:
#         return "LOCATION"
#     return None
#
# def run_ner(text):
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#         label = map_label(ent.label_)
#         if label:
#             entity = clean_entity(ent.text)
#
#             # ignore very small garbage tokens
#             if len(entity) < 2:
#                 continue
#
#             results[entity] = label
#
#     return results
#
#
# # ---------------- MAIN ----------------
# file_path = input("Enter txt file path: ")
#
# start = time.time()
#
# with open(file_path, "r", encoding="utf-8") as f:
#     text = f.read()
#
# print("\nProcessing...\n")
#
# output = run_ner(text)
#
# print("\n🔥 FINAL ULTRA LOW CPU OUTPUT:\n")
#
# for k, v in output.items():
#     print(f"{k} --> {v}")
#
# end = time.time()
#
# print("\nDone ✔")
# print(f"CPU TIME: {round(end - start, 2)} sec")
# ===30 good
import spacy
import re

print("Running SMART LOW CPU NER (spaCy + Fix Layer)...")

nlp = spacy.load("en_core_web_sm")

# ---------- SMART FIX RULES ----------
ORG_HINTS = {"inc", "llc", "ltd", "technologies", "systems", "google", "microsoft", "apple", "amazon", "tcs", "infosys"}
LOC_HINTS = {"city", "state", "usa", "india", "california", "texas", "new york"}

def clean(text):
    return re.sub(r"\s+", " ", text.strip())

def smart_fix(entity, label):
    e_low = entity.lower()

    # Fix ORGANIZATION
    if any(word in e_low for word in ORG_HINTS):
        return "ORGANIZATION"

    # Fix LOCATION
    if any(word in e_low for word in LOC_HINTS):
        return "LOCATION"

    # Fix known PERSON patterns (simple heuristic)
    if len(entity.split()) <= 3 and entity[0].isupper():
        if label == "PERSON":
            return "PERSON"

    return label


def map_label(label):
    if label == "PERSON":
        return "PERSON"
    elif label in ["ORG"]:
        return "ORGANIZATION"
    elif label in ["GPE", "LOC"]:
        return "LOCATION"
    return None


def run_ner(text):
    doc = nlp(text)
    results = {}

    for ent in doc.ents:
        label = map_label(ent.label_)
        if not label:
            continue

        entity = clean(ent.text)

        if len(entity) < 2:
            continue

        label = smart_fix(entity, label)

        results[entity] = label

    return results


# ---------- MAIN ----------
file_path = input("Enter txt file path: ")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

print("\nProcessing...\n")

output = run_ner(text)

print("\n FINAL SMART OUTPUT:\n")

for k, v in output.items():
    print(f"{k} --> {v}")

print("\nDone ✔")