# import spacy
# import pandas as pd
# import time
# import psutil
# from docx import Document
#
# nlp = spacy.load("en_core_web_sm")
#
# # read email file
# with open("input.txt", "r", encoding="utf-8") as f:
#     email_text = f.read()
#
# # ⏱️ performance tracking
# start_time = time.time()
# start_cpu = psutil.cpu_percent(interval=None)
#
# doc = nlp(email_text)
#
# end_time = time.time()
# end_cpu = psutil.cpu_percent(interval=None)
#
# print("\n--- EMAIL NER RESULTS ---\n")
#
# data = []
#
# for ent in doc.ents:
#     print(ent.text, "→", ent.label_)
#     data.append([ent.text, ent.label_])
#
# # 📊 Excel output
# df = pd.DataFrame(data, columns=["Entity", "Type"])
# df.to_excel("email_output.xlsx", index=False)
#
# # 📄 Word output
# doc_out = Document()
# doc_out.add_heading("Email NER Results", 0)
#
# for ent, label in data:
#     doc_out.add_paragraph(f"{ent} → {label}")
#
# doc_out.save("email_output.docx")
#
# # ⚡ performance report
# print("\n--- PERFORMANCE ---")
# print("Time:", round(end_time - start_time, 4), "seconds")
# print("CPU:", end_cpu, "%")
#
# print("\n✔ Email processed successfully")

# import spacy
# import pandas as pd
# import time
# import psutil
# from docx import Document
#
# # ======================
# # LOAD MODEL
# # ======================
# nlp = spacy.load("en_core_web_sm")
#
#
# with open("input.txt", "r", encoding="utf-8") as f:
#     text = f.read()
#
#
# start_time = time.time()
# start_cpu = psutil.cpu_percent(interval=None)
#
#
# doc = nlp(text)
#
#
# end_time = time.time()
# end_cpu = psutil.cpu_percent(interval=None)
#
#
# data = []
#
# print("\n--- ENTITIES FOUND ---\n")
#
# for ent in doc.ents:
#     print(ent.text, "→", ent.label_)
#     data.append([ent.text, ent.label_])
#
#
# df = pd.DataFrame(data, columns=["Entity", "Type"])
# df.to_excel("output.xlsx", index=False)
#
# doc_out = Document()
# doc_out.add_heading("NER Results", 0)
#
# for ent, label in data:
#     doc_out.add_paragraph(f"{ent} → {label}")
#
# doc_out.save("output.docx")
#
# print("\n--- PERFORMANCE METRICS ---")
# print("Time taken:", round(end_time - start_time, 4), "seconds")
# print("CPU usage:", end_cpu, "%")
#
# print("\n✔ Files created: output.xlsx, output.docx")


# import spacy
# import re
# import time
# from collections import defaultdict
#
# # lightweight + fast model
# nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])
#
# # -----------------------------
# # KNOWLEDGE BASE
# # -----------------------------
# ORG_SET = {
#     "Google","Microsoft","Amazon","TCS","Infosys","Wipro","IBM",
#     "Accenture","Deloitte","HCL Technologies","HSBC",
#     "Apple Inc.","Reliance Industries","Tata Consultancy Services",
#     "Tesla Technologies"
# }
#
# LOCATION_SET = {
#     "India","USA","London","Bangalore","Mumbai","Delhi","Pune",
#     "Hyderabad","Chennai","Gurgaon","Noida","California","Cupertino",
#     "New York","Newyork"
# }
#
# BLACKLIST = {
#     "Meta","HR","Interview","Date","Offer","Selected",
#     "HR Team","Recruitment","Congratulations","Software",
#     "Bollywood","Capgemini","---"
# }
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean_text(text):
#     text = re.sub(r"(?i)subject:.*", "", text)
#     text = re.sub(r"(?i)dear\s+\w+", "", text)
#     text = re.sub(r"(?i)regards.*", "", text)
#     text = re.sub(r"-{2,}", " ", text)
#     return re.sub(r"\s+", " ", text).strip()
#
# # -----------------------------
# # NORMALIZATION
# # -----------------------------
# def normalize(text):
#     text = text.strip()
#     text = re.sub(r"\s+in\s+\w+$", "", text)
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()
#
# # -----------------------------
# # ENTITY SCORING SYSTEM (MAIN FIX)
# # -----------------------------
# def entity_score(text, label):
#
#     score = 0
#
#     # whitelist boost
#     if text in ORG_SET or text in LOCATION_SET:
#         score += 4
#
#     # proper noun boost
#     if text.istitle():
#         score += 1
#
#     # label consistency
#     if label in ["ORG", "PERSON", "GPE"]:
#         score += 1
#
#     # penalty: long junk phrases
#     if len(text.split()) > 3:
#         score -= 2
#
#     # junk penalty
#     junk_words = ["HR", "Interview", "Date", "Congratulations", "---"]
#     if any(j in text for j in junk_words):
#         score -= 3
#
#     return score
#
# # -----------------------------
# # THRESHOLD
# # -----------------------------
# MIN_SCORE = 2
#
# # -----------------------------
# # VALIDATORS
# # -----------------------------
# def is_person(text):
#     return (
#         text.istitle()
#         and text not in ORG_SET
#         and text not in LOCATION_SET
#         and text not in BLACKLIST
#     )
#
# def is_org(text):
#     return text in ORG_SET or (text not in LOCATION_SET and text not in BLACKLIST)
#
# def is_location(text):
#     return text in LOCATION_SET
#
# # -----------------------------
# # CLASSIFIER
# # -----------------------------
# def classify(ent_text, label):
#
#     text = normalize(ent_text)
#
#     if text in BLACKLIST:
#         return None
#
#     # score filter (MAIN FIX)
#     score = entity_score(text, label)
#     if score < MIN_SCORE:
#         return None
#
#     # LOCATION FIRST
#     if is_location(text):
#         return ("LOCATION", text)
#
#     # ORG
#     if label == "ORG" and is_org(text):
#         return ("ORG", text)
#
#     # PERSON
#     if label == "PERSON" and is_person(text):
#         return ("PERSON", text)
#
#     return None
#
# # -----------------------------
# # PIPELINE
# # -----------------------------
# def process(text):
#
#     text = clean_text(text)
#     doc = nlp(text)
#
#     result = defaultdict(set)
#     seen = set()
#
#     for ent in doc.ents:
#
#         res = classify(ent.text, ent.label_)
#
#         if res:
#             cat, val = res
#
#             if val not in seen:
#                 result[cat].add(val)
#                 seen.add(val)
#
#     return {
#         "PERSON": sorted(result["PERSON"]),
#         "ORG": sorted(result["ORG"]),
#         "LOCATION": sorted(result["LOCATION"])
#     }
#
# # -----------------------------
# # RUN
# # -----------------------------
# if __name__ == "__main__":
#
#     start = time.time()
#
#     with open("input.txt", "r", encoding="utf-8") as f:
#         text = f.read()
#
#     print("\n📄 INPUT LOADED")
#
#     output = process(text)
#
#     print("\n🔍 FINAL OUTPUT:")
#     print(output)
#
#     print("\n⏱ Time:", round(time.time() - start, 2), "sec")


# import spacy
# import re
# import time
# import pandas as pd
# from docx import Document
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm", disable=["tagger", "lemmatizer"])
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean_text(text):
#     text = re.sub(r"(?i)subject:.*", "", text)
#     text = re.sub(r"(?i)dear\s+\w+", "", text)
#     text = re.sub(r"-{2,}", " ", text)
#     return re.sub(r"\s+", " ", text).strip()
#
# # -----------------------------
# # NORMALIZE ENTITY
# # -----------------------------
# def normalize(text):
#     text = text.strip()
#     text = re.sub(r"\s+in\s+\w+$", "", text)
#     return text.strip()
#
# # -----------------------------
# # VALIDATION (NO WHITELIST DEPENDENCY)
# # -----------------------------
# def is_valid(text):
#
#     if not text:
#         return False
#
#     junk = [
#         "HR", "Interview", "Date", "Congratulations",
#         "---", "Software", "Hiring", "Recruitment"
#     ]
#
#     if any(j in text for j in junk):
#         return False
#
#     if len(text) < 2:
#         return False
#
#     if len(text.split()) > 5:
#         return False
#
#     if not text[0].isupper():
#         return False
#
#     return True
#
# # -----------------------------
# # FINAL FIX + CORRECTION LAYER
# # -----------------------------
# CITY_FIX = {
#     "Hyderabad","Bangalore","Delhi","Mumbai","Pune","Noida",
#     "Gurgaon","London","California","Cupertino","Lucknow",
#     "Newyork","USA","India"
# }
#
# ORG_FIX = {
#     "Meta","Google","Microsoft","Amazon","TCS","Infosys","Wipro",
#     "IBM","Accenture","Deloitte","HSBC","Apple Inc.","Tesla Technologies",
#     "Reliance Industries","HCL Technologies"
# }
#
# # -----------------------------
# # CLASSIFIER (CORE LOGIC)
# # -----------------------------
# def classify(text, label):
#
#     text = normalize(text)
#
#     if not is_valid(text):
#         return None
#
#     # ---------------- FIX CITY MISTAKES ----------------
#     if text in CITY_FIX:
#         return ("LOCATION", text)
#
#     # ---------------- FIX ORG ----------------
#     if text in ORG_FIX:
#         return ("ORG", text)
#
#     # ---------------- RULE BASED ----------------
#     if label in ["GPE", "LOC"]:
#         return ("LOCATION", text)
#
#     if label == "ORG":
#         return ("ORG", text)
#
#     if label == "PERSON":
#         return ("PERSON", text)
#
#     return None
#
# # -----------------------------
# # PIPELINE
# # -----------------------------
# def process(text):
#
#     text = clean_text(text)
#     doc = nlp(text)
#
#     result = []
#     seen = set()
#
#     for ent in doc.ents:
#
#         res = classify(ent.text, ent.label_)
#
#         if res:
#             label, value = res
#
#             key = (label, value)
#
#             if key not in seen:
#                 result.append((value, label))
#                 seen.add(key)
#
#     return result
#
# # -----------------------------
# # MAIN
# # -----------------------------
# if __name__ == "__main__":
#
#     with open("input.txt", "r", encoding="utf-8") as f:
#         text = f.read()
#
#     start = time.time()
#
#     results = process(text)
#
#     # -----------------------------
#     # OUTPUT
#     # -----------------------------
#     print("\n--- FINAL CLEAN NER OUTPUT ---\n")
#
#     for entity, label in results:
#         print(f"{entity} → {label}")
#
#     # -----------------------------
#     # EXCEL EXPORT
#     # -----------------------------
#     df = pd.DataFrame(results, columns=["Entity", "Type"])
#     df.to_excel("output.xlsx", index=False)
#
#     # -----------------------------
#     # WORD EXPORT
#     # -----------------------------
#     doc = Document()
#     doc.add_heading("NER Results", 0)
#
#     for entity, label in results:
#         doc.add_paragraph(f"{entity} → {label}")
#
#     doc.save("output.docx")
#
#     # -----------------------------
#     # PERFORMANCE
#     # -----------------------------
#     print("\n--- PERFORMANCE ---")
#     print("Time:", round(time.time() - start, 4), "sec")
#
#     print("\n✔ Pipeline completed successfully")

# import spacy
# import json
# import os
# import re
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm")
#
# # -----------------------------
# # MEMORY FILE (SELF-LEARNING STORAGE)
# # -----------------------------
# MEMORY_FILE = "entity_memory.json"
#
# # load memory if exists
# if os.path.exists(MEMORY_FILE):
#     with open(MEMORY_FILE, "r") as f:
#         MEMORY = json.load(f)
# else:
#     MEMORY = {
#         "ORG": set(),
#         "PERSON": set(),
#         "LOCATION": set()
#     }
#
# # convert lists back to sets
# for k in MEMORY:
#     MEMORY[k] = set(MEMORY[k])
#
# # -----------------------------
# # SAVE MEMORY
# # -----------------------------
# def save_memory():
#     with open(MEMORY_FILE, "w") as f:
#         json.dump({k: list(v) for k, v in MEMORY.items()}, f, indent=2)
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean_text(text):
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"Newyork", "New York", text, flags=re.IGNORECASE)
#     return text.strip()
#
# # -----------------------------
# # CLASSIFY ENTITY
# # -----------------------------
# def classify(ent_text, label):
#     text = ent_text.strip()
#
#     if label in ["ORG", "GPE", "LOC", "PERSON"]:
#         if label == "GPE":
#             label = "LOCATION"
#
#         if label == "PER":
#             label = "PERSON"
#
#     return text, label
#
# # -----------------------------
# # SELF-LEARNING FUNCTION
# # -----------------------------
# def update_memory(text, label):
#     if text not in MEMORY[label]:
#         MEMORY[label].add(text)
#
# # -----------------------------
# # MAIN NER ENGINE
# # -----------------------------
# def extract_entities(text):
#     text = clean_text(text)
#     doc = nlp(text)
#
#     results = {}
#
#     # spaCy extraction
#     for ent in doc.ents:
#         name, label = classify(ent.text, ent.label_)
#
#         # check memory first (self-learning boost)
#         for key in MEMORY:
#             if name in MEMORY[key]:
#                 label = key
#
#         results[name] = label
#
#         # learn new entity
#         update_memory(name, label)
#
#     save_memory()
#     return results
#
# # -----------------------------
# # TEST RUN
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Zorvax Nexilon works at Google.
#     Elon Musk leads Tesla.
#     New company TruvionX is based in Bangalore.
#     """
#
#     output = extract_entities(text)
#
#     print("\n--- SELF LEARNING NER OUTPUT ---\n")
#     for k, v in output.items():
#         print(f"{k} → {v}")
#
#     print("\nMemory updated and saved!")

# import spacy
# import json
# import os
# import re
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm")
#
# # -----------------------------
# # MEMORY FILE
# # -----------------------------
# MEMORY_FILE = "entity_memory.json"
#
# if os.path.exists(MEMORY_FILE):
#     with open(MEMORY_FILE, "r") as f:
#         MEMORY = json.load(f)
# else:
#     MEMORY = {
#         "ORG": [],
#         "PERSON": [],
#         "LOCATION": []
#     }
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean_text(text):
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"Newyork", "New York", text, flags=re.IGNORECASE)
#     return text.strip()
#
# # -----------------------------
# # CONTEXT RULES (IMPORTANT UPGRADE)
# # -----------------------------
# ORG_CONTEXT = ["works at", "company", "CEO of", "joined", "at"]
# LOC_CONTEXT = ["in", "located in", "from", "based in", "city"]
# PERSON_CONTEXT = ["is", "called", "named"]
#
# # -----------------------------
# # CONTEXT DETECTOR
# # -----------------------------
# def get_context(text, entity):
#     lower = text.lower()
#
#     for phrase in ORG_CONTEXT:
#         if phrase in lower:
#             return "ORG"
#
#     for phrase in LOC_CONTEXT:
#         if phrase in lower:
#             return "LOCATION"
#
#     return None
#
# # -----------------------------
# # MEMORY LEARNER
# # -----------------------------
# def learn(entity, label):
#     if entity not in MEMORY[label]:
#         MEMORY[label].append(entity)
#
# # -----------------------------
# # SAVE MEMORY
# # -----------------------------
# def save_memory():
#     with open(MEMORY_FILE, "w") as f:
#         json.dump(MEMORY, f, indent=2)
#
# # -----------------------------
# # MAIN ENGINE
# # -----------------------------
# def extract_entities(text):
#     text = clean_text(text)
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#         name = ent.text.strip()
#         label = ent.label_
#
#         # spaCy normalization
#         if label == "GPE":
#             label = "LOCATION"
#         if label == "PER":
#             label = "PERSON"
#
#         # -----------------------------
#         # CONTEXT OVERRIDE (KEY UPGRADE)
#         # -----------------------------
#         context_label = get_context(text, name)
#         if context_label:
#             label = context_label
#
#         # -----------------------------
#         # MEMORY CHECK (SELF LEARNING)
#         # -----------------------------
#         for key in MEMORY:
#             if name in MEMORY[key]:
#                 label = key
#
#         results[name] = label
#
#         # learn new entity
#         learn(name, label)
#
#     save_memory()
#     return results
#
# # -----------------------------
# # TEST
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Zorvax Nexilon works at Google.
#     Elon Musk is CEO of Tesla.
#     Sundar Pichai works at Google in California.
#     TruvionX is based in Bangalore.
#     """
#
#     output = extract_entities(text)
#
#     print("\n--- LEVEL 2 SMART NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(f"{k} → {v}")
#
#     print("\nMemory updated successfully.")

# import spacy
# import json
# import os
# import re
#
# # -----------------------------
# # LOAD SPACY MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm")
#
# # -----------------------------
# # MEMORY FILE (SELF-LEARNING)
# # -----------------------------
# MEMORY_FILE = "entity_memory.json"
#
# if os.path.exists(MEMORY_FILE):
#     with open(MEMORY_FILE, "r") as f:
#         MEMORY = json.load(f)
# else:
#     MEMORY = {
#         "ORG": [],
#         "PERSON": [],
#         "LOCATION": []
#     }
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean_text(text):
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"Newyork", "New York", text, flags=re.IGNORECASE)
#     return text.strip()
#
# # -----------------------------
# # CONTEXT DETECTION (FIXED VERSION)
# # -----------------------------
# def get_context(text, entity):
#     lower = text.lower()
#     entity_lower = entity.lower()
#
#     idx = lower.find(entity_lower)
#     if idx == -1:
#         return None
#
#     # small window around entity (important fix)
#     window = lower[max(0, idx - 40): idx + len(entity_lower) + 40]
#
#     # ORG context (only if very close)
#     org_signals = ["works at", "company", "ceo of", "joined", "employed at"]
#     if any(word in window for word in org_signals):
#         return "ORG"
#
#     # LOCATION context
#     loc_signals = ["in", "located in", "based in", "from"]
#     if any(word in window for word in loc_signals):
#         return "LOCATION"
#
#     return None
#
# # -----------------------------
# # MEMORY UPDATE
# # -----------------------------
# def learn(entity, label):
#     if entity not in MEMORY[label]:
#         MEMORY[label].append(entity)
#
# # -----------------------------
# # SAVE MEMORY
# # -----------------------------
# def save_memory():
#     with open(MEMORY_FILE, "w") as f:
#         json.dump(MEMORY, f, indent=2)
#
# # -----------------------------
# # MAIN NER ENGINE
# # -----------------------------
# def extract_entities(text):
#     text = clean_text(text)
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#         name = ent.text.strip()
#         label = ent.label_
#
#         # spaCy normalization
#         if label == "GPE":
#             label = "LOCATION"
#         if label == "PER":
#             label = "PERSON"
#
#         # -----------------------------
#         # CONTEXT OVERRIDE (SAFE FIX)
#         # -----------------------------
#         context = get_context(text, name)
#
#         # IMPORTANT FIX: only override if spaCy is unsure OR context is strong
#         if context:
#             # avoid wrong override like Sundar Pichai → ORG
#             if not (name in MEMORY["PERSON"] and context == "ORG"):
#                 label = context
#
#         # -----------------------------
#         # MEMORY CHECK
#         # -----------------------------
#         for key in MEMORY:
#             if name in MEMORY[key]:
#                 label = key
#
#         results[name] = label
#
#         # learn new entity
#         learn(name, label)
#
#     save_memory()
#     return results
#
# # -----------------------------
# # TEST INPUT
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Zorvax Nexilon works at Google.
#     Elon Musk is CEO of Tesla.
#     Sundar Pichai works at Google in California.
#     Bangalore is a big tech hub in India.
#     """
#
#     output = extract_entities(text)
#
#     print("\n--- FINAL LEVEL 2 SMART NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(f"{k} → {v}")
#
#     print("\nMemory updated successfully.")

# import spacy
# import json
# import os
# from collections import defaultdict
#
# # -----------------------------
# # LOAD SPACY MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm")
#
# # -----------------------------
# # MEMORY FILE
# # -----------------------------
# MEMORY_FILE = "entity_memory.json"
#
# if os.path.exists(MEMORY_FILE):
#     with open(MEMORY_FILE, "r") as f:
#         MEMORY = json.load(f)
# else:
#     MEMORY = {"ORG": [], "PERSON": [], "LOCATION": []}
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean_text(text):
#     return " ".join(text.split())
#
# # -----------------------------
# # HARD KNOWLEDGE BASE (IMPORTANT FIX)
# # -----------------------------
# ORG_FORCE = {"Google", "Amazon", "Meta", "Tesla", "Microsoft", "Apple", "Infosys", "TCS"}
# LOC_FORCE = {"California", "India", "Bangalore", "Mumbai", "USA", "London"}
# PERSON_FORCE = {"Elon Musk", "Sundar Pichai", "Narendra Modi", "Mukesh Ambani"}
#
# # -----------------------------
# # MEMORY COUNTER (SAFE LEARNING)
# # -----------------------------
# COUNT = defaultdict(int)
#
# def learn(entity, label):
#     COUNT[entity] += 1
#
#     # only learn after repetition (prevents wrong learning)
#     if COUNT[entity] >= 2:
#         if entity not in MEMORY[label]:
#             MEMORY[label].append(entity)
#
# def save_memory():
#     with open(MEMORY_FILE, "w") as f:
#         json.dump(MEMORY, f, indent=2)
#
# # -----------------------------
# # NORMALIZE LABELS
# # -----------------------------
# def normalize(label):
#     if label == "GPE":
#         return "LOCATION"
#     if label == "PER":
#         return "PERSON"
#     return label
#
# # -----------------------------
# # FINAL DECISION ENGINE
# # -----------------------------
# def decide(name, label):
#
#     # 1. STRONG PERSON FIX (MOST IMPORTANT)
#     if name in PERSON_FORCE:
#         return "PERSON"
#
#     # 2. ORG FIX
#     if name in ORG_FORCE:
#         return "ORG"
#
#     # 3. LOCATION FIX
#     if name in LOC_FORCE:
#         return "LOCATION"
#
#     # 4. MEMORY BOOST (SAFE ONLY)
#     for key in MEMORY:
#         if name in MEMORY[key]:
#             return key
#
#     # 5. DEFAULT spaCy OUTPUT
#     return label
#
# # -----------------------------
# # MAIN FUNCTION
# # -----------------------------
# def extract_entities(text):
#     text = clean_text(text)
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#         name = ent.text.strip()
#         label = normalize(ent.label_)
#
#         final_label = decide(name, label)
#
#         results[name] = final_label
#
#         learn(name, final_label)
#
#     save_memory()
#     return results
#
# # -----------------------------
# # TEST RUN
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Zorvax Nexilon works at Google.
#     Elon Musk is CEO of Tesla.
#     Sundar Pichai works at Google in California.
#     Meta and Amazon are big companies.
#     Bangalore is in India.
#     """
#
#     output = extract_entities(text)
#
#     print("\n--- FINAL STABLE NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(f"{k} → {v}")
#
#     print("\nMemory updated safely.")


# import spacy
# import json
# import os
# from collections import defaultdict
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm")
#
# # -----------------------------
# # MEMORY
# # -----------------------------
# MEMORY_FILE = "entity_memory.json"
#
# if os.path.exists(MEMORY_FILE):
#     with open(MEMORY_FILE, "r") as f:
#         MEMORY = json.load(f)
# else:
#     MEMORY = {"ORG": [], "PERSON": [], "LOCATION": []}
#
# COUNT = defaultdict(int)
#
# # -----------------------------
# def clean_text(text):
#     return " ".join(text.split())
#
# # -----------------------------
# def normalize(label):
#     if label == "GPE":
#         return "LOCATION"
#     if label == "PER":
#         return "PERSON"
#     return label
#
# # -----------------------------
# # STRONGER CONTEXT ENGINE (FIXED)
# # -----------------------------
# def context_score(text, entity):
#     lower = text.lower()
#     ent = entity.lower()
#
#     idx = lower.find(ent)
#     if idx == -1:
#         return {"ORG": 0, "PERSON": 0, "LOCATION": 0}
#
#     window = lower[max(0, idx - 60): idx + len(ent) + 60]
#
#     scores = {"ORG": 0, "PERSON": 0, "LOCATION": 0}
#
#     # ORG signals (strong + specific)
#     org_signals = ["company", "ceo", "founded", "inc", "corp", "tech", "works at"]
#
#     # LOCATION signals (more strict now)
#     loc_signals = ["city", "state", "country", "located", "based in", "in "]
#
#     # PERSON signals (VERY IMPORTANT FIX)
#     person_signals = ["mr", "ms", "dr", "ceo", "founder", "sir"]
#
#     if any(w in window for w in org_signals):
#         scores["ORG"] += 3
#
#     if any(w in window for w in loc_signals):
#         scores["LOCATION"] += 3
#
#     if any(w in window for w in person_signals):
#         scores["PERSON"] += 3
#
#     return scores
#
# # -----------------------------
# def learn(entity, label):
#     COUNT[entity] += 1
#
#     if COUNT[entity] >= 2:
#         if entity not in MEMORY[label]:
#             MEMORY[label].append(entity)
#
# def save_memory():
#     with open(MEMORY_FILE, "w") as f:
#         json.dump(MEMORY, f, indent=2)
#
# # -----------------------------
# # FINAL DECISION ENGINE (FIXED LOGIC)
# # -----------------------------
# def decide(entity, spacy_label, text):
#
#     # 1. MEMORY (only boost, not force corruption)
#     for k in MEMORY:
#         if entity in MEMORY[k]:
#             return k
#
#     # 2. CONTEXT SCORING
#     scores = context_score(text, entity)
#
#     best_label = max(scores, key=scores.get)
#
#     # only accept strong confidence (IMPORTANT FIX)
#     if scores[best_label] >= 3:
#         return best_label
#
#     # 3. spaCy fallback
#     return normalize(spacy_label)
#
# # -----------------------------
# def extract_entities(text):
#     text = clean_text(text)
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#         name = ent.text.strip()
#         label = ent.label_
#
#         final_label = decide(name, label, text)
#
#         results[name] = final_label
#
#         learn(name, final_label)
#
#     save_memory()
#     return results
#
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Zorvax Nexilon works at Google.
#     Elon Musk is CEO of Tesla.
#     Sundar Pichai works at Google in California.
#     Meta and Amazon are big companies.
#     Bangalore is in India.
#     """
#
#     output = extract_entities(text)
#
#     print("\n--- IMPROVED LEVEL 3 NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(f"{k} → {v}")
#
#     print("\nMemory updated safely.")
# ================================best wrking==========
# import spacy
# import re
#
# nlp = spacy.load("en_core_web_lg")
#
# def clean_text(text):
#     return re.sub(r"\s+", " ", text).strip()
#
# def normalize(label):
#     if label == "GPE":
#         return "LOCATION"
#     if label == "PER":
#         return "PERSON"
#     return label
#
# def extract_entities(text):
#     text = clean_text(text)
#     doc = nlp(text)
#
#     output = {}
#
#     for ent in doc.ents:
#         name = ent.text.strip()
#         label = normalize(ent.label_)
#
#         output[name] = label
#
#     return output
#
#
# if __name__ == "__main__":
#
#     text = """
# Elon Musk is the CEO of Tesla and SpaceX. He was born in South Africa and later moved to the United States.
#
# Sundar Pichai leads Google and previously worked at Twitter and Microsoft. He studied in India before moving to California.
#
# Mark Zuckerberg founded Facebook (now Meta) in the United States. Meta is headquartered in Menlo Park.
#
# Jeff Bezos founded Amazon and built it into one of the largest e-commerce companies in the world. Amazon operates heavily in India and Europe.
#
# Bill Gates co-founded Microsoft with Paul Allen in Seattle.
#
# Apple Inc. is based in Cupertino, California and is led by Tim Cook.
#
# Bangalore is known as the Silicon Valley of India and hosts companies like Infosys, Wipro, and Flipkart.
#
# Narendra Modi is the Prime Minister of India. He frequently visits countries like the USA, France, and Japan.
#
# The United Nations is headquartered in New York City.
#
# London is a global financial hub with banks like HSBC and Barclays.
#
# Google acquired YouTube in 2006.
#
# Tesla is expanding its operations in Germany and China.
#
# Amazon Web Services (AWS) competes with Microsoft Azure and Google Cloud.
#
# The Eiffel Tower is located in Paris, France.
#
# The Great Wall of China is one of the wonders of the world.
# """
#
#     result = extract_entities(text)
#
#     print("\n--- TEXT TO TEXT NER OUTPUT ---\n")
#
#     for k, v in result.items():
#         print(f"{k} → {v}")

# ==================working better====
# import spacy
# from collections import defaultdict
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# nlp = spacy.load("en_core_web_sm")
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean(text):
#     return " ".join(text.split())
#
# # -----------------------------
# # LABEL NORMALIZATION (IMPORTANT FIX)
# # -----------------------------
# def normalize_label(label):
#     if label == "GPE":
#         return "LOCATION"
#     if label == "LOC":
#         return "LOCATION"
#     if label == "PER":
#         return "PERSON"
#     return label
#
# # -----------------------------
# # CONTEXT ANALYSIS ENGINE
# # -----------------------------
# def analyze_context(ent):
#
#     scores = {"PERSON": 0, "ORG": 0, "LOCATION": 0}
#
#     text = ent.text.lower()
#     head = ent.root.head.text.lower()
#
#     # ---------------- ORG signals (strong but controlled)
#     org_words = ["company", "founded", "ceo", "works at", "built", "launched"]
#     if head in org_words:
#         scores["ORG"] += 3
#
#     # ---------------- LOCATION signals (STRICT NOW)
#     loc_words = ["city", "country", "state", "located"]
#     if head in loc_words:
#         scores["LOCATION"] += 3
#
#     # IMPORTANT: avoid over-triggering "in / at"
#     if head in ["in", "at", "from"] and ent.label_ == "GPE":
#         scores["LOCATION"] += 1
#
#     # ---------------- PERSON signals (STRONG PRIORITY FIX)
#     person_words = ["mr", "ms", "dr", "ceo", "founder", "president"]
#
#     if any(w in text for w in person_words):
#         scores["PERSON"] += 4   # higher priority than others
#
#     # If spaCy already says PERSON → boost it
#     if ent.label_ == "PERSON":
#         scores["PERSON"] += 2
#
#     return scores
# # -----------------------------
# # SAFE LABEL RESOLVER (FIXED GPE ERROR)
# # -----------------------------
# def resolve_label(spacy_label, context_scores):
#
#     # normalize spaCy output
#     spacy_label = normalize_label(spacy_label)
#
#     # ensure key exists (prevents crash)
#     if spacy_label not in context_scores:
#         context_scores[spacy_label] = 0
#
#     # boost spaCy confidence
#     context_scores[spacy_label] += 1
#
#     return max(context_scores, key=context_scores.get)
#
# # -----------------------------
# # MAIN EXTRACTION FUNCTION
# # -----------------------------
# def extract_entities(text):
#
#     doc = nlp(clean(text))
#     output = {}
#
#     for ent in doc.ents:
#
#         context_scores = analyze_context(ent)
#         final_label = resolve_label(ent.label_, context_scores)
#
#         output[ent.text] = final_label
#
#     return output
#
# # -----------------------------
# # TEST DATA
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Elon Musk is CEO of Tesla.
#     Sundar Pichai works at Google in California.
#     Amazon is expanding in India.
#     Apple is hiring engineers in Cupertino.
#     The Amazon river flows through South America.
#     """
#
#     result = extract_entities(text)
#
#     print("\n--- FINAL STABLE NER OUTPUT ---\n")
#
#     for k, v in result.items():
#         print(f"{k} → {v}")


# =====================
# import spacy
# from collections import defaultdict
#
# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "attribute_ruler"]
# )
#
# # -----------------------------
# # CLEAN TEXT
# # -----------------------------
# def clean(text):
#     return " ".join(text.split())
#
# # -----------------------------
# # LABEL NORMALIZATION (IMPORTANT FIX)
# # -----------------------------
# def normalize_label(label):
#     if label == "GPE":
#         return "LOCATION"
#     if label == "LOC":
#         return "LOCATION"
#     if label == "PER":
#         return "PERSON"
#     return label
#
# # -----------------------------
# # CONTEXT ANALYSIS ENGINE
# # -----------------------------
# def analyze_context(ent):
#
#     scores = {"PERSON": 0, "ORG": 0, "LOCATION": 0}
#
#     text = ent.text.lower()
#     head = ent.root.head.text.lower()
#
#     # ---------------- ORG signals (strong but controlled)
#     org_words = ["company", "founded", "ceo", "works at", "built", "launched"]
#     if head in org_words:
#         scores["ORG"] += 3
#
#     # ---------------- LOCATION signals (STRICT NOW)
#     loc_words = ["city", "country", "state", "located"]
#     if head in loc_words:
#         scores["LOCATION"] += 3
#
#     # IMPORTANT: avoid over-triggering "in / at"
#     if head in ["in", "at", "from"] and ent.label_ == "GPE":
#         scores["LOCATION"] += 1
#
#     # ---------------- PERSON signals (STRONG PRIORITY FIX)
#     person_words = ["mr", "ms", "dr", "ceo", "founder", "president"]
#
#     if any(w in text for w in person_words):
#         scores["PERSON"] += 4   # higher priority than others
#
#     # If spaCy already says PERSON → boost it
#     if ent.label_ == "PERSON":
#         scores["PERSON"] += 2
#
#     return scores
# # -----------------------------
# # SAFE LABEL RESOLVER (FIXED GPE ERROR)
# # -----------------------------
# def resolve_label(spacy_label, context_scores):
#
#     # normalize spaCy output
#     spacy_label = normalize_label(spacy_label)
#
#     # ensure key exists (prevents crash)
#     if spacy_label not in context_scores:
#         context_scores[spacy_label] = 0
#
#     # boost spaCy confidence
#     context_scores[spacy_label] += 1
#
#     return max(context_scores, key=context_scores.get)
#
# # -----------------------------
# # MAIN EXTRACTION FUNCTION
# # -----------------------------
# def extract_entities(text):
#
#     doc = nlp(clean(text))
#     output = {}
#
#     for ent in doc.ents:
#
#         context_scores = analyze_context(ent)
#         final_label = resolve_label(ent.label_, context_scores)
#
#         output[ent.text] = final_label
#
#     return output
#
# # -----------------------------
# # TEST DATA
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Elon Musk is CEO of Tesla.
#     Sundar Pichai works at Google in California.
#     Amazon is expanding in India.
#     Apple is hiring engineers in Cupertino.
#     The Amazon river flows through South America.
#     """
#
#     result = extract_entities(text)
#
#     print("\n--- FINAL STABLE NER OUTPUT ---\n")
#
#     for k, v in result.items():
#         print(f"{k} → {v}")
# ========================================
# import spacy
#
# # FAST MODE LOAD
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "attribute_ruler"]
# )
#
# def extract_entities(text):
#
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#
#         label = ent.label_
#
#         # ultra-fast normalization (no function call)
#         if label == "GPE":
#             label = "LOCATION"
#
#         results[ent.text] = label
#
#     return results
#
#
# if __name__ == "__main__":
#
#     text = """
#     Elon Musk works at Tesla in California.
#     Sundar Pichai leads Google in India.
#     Amazon is expanding globally.
#     """
#
#     output = extract_entities(text)
#
#     for k, v in output.items():
#         print(k, "→", v)

# ======================================================
# import spacy
#
# # ULTRA LIGHT MODE
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# nlp.max_length = 2000000
#
#
# def chunk_text(text, size=300):
#     words = text.split()
#     for i in range(0, len(words), size):
#         yield " ".join(words[i:i+size])
#
#
# def extract_entities(text):
#
#     results = {}
#
#     for chunk in chunk_text(text):
#
#         doc = nlp(chunk)
#
#         for ent in doc.ents:
#
#             label = ent.label_
#
#             if label == "GPE":
#                 label = "LOCATION"
#
#             results[ent.text] = label
#
#     return results
#
#
# if __name__ == "__main__":
#
#     text = """
#     Elon Musk works at Tesla in California.
#     Sundar Pichai leads Google in India.
#     Amazon is expanding globally across many countries.
#     """
#
#     output = extract_entities(text)
#
#     for k, v in output.items():
#         print(k, "→", v)

# import spacy
#
# # -----------------------------
# # ULTRA LIGHT SPA CY SETUP
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# nlp.max_length = 2000000  # safety for long text
#
# # -----------------------------
# # SIMPLE NORMALIZATION
# # -----------------------------
# def normalize(label):
#     if label == "GPE":
#         return "LOCATION"
#     if label == "LOC":
#         return "LOCATION"
#     return label
#
# # -----------------------------
# # OPTIONAL: FAST CHUNKING (prevents CPU spikes on big text)
# # -----------------------------
# def chunk_text(text, size=300):
#     words = text.split()
#     for i in range(0, len(words), size):
#         yield " ".join(words[i:i+size])
#
# # -----------------------------
# # MAIN NER FUNCTION
# # -----------------------------
# def extract_entities(text, use_chunking=False):
#
#     results = {}
#
#     # choose mode
#     if use_chunking:
#         inputs = chunk_text(text)
#     else:
#         inputs = [text]
#
#     for chunk in inputs:
#
#         doc = nlp(chunk)
#
#         for ent in doc.ents:
#
#             label = normalize(ent.label_)
#
#             # keep first occurrence only (saves CPU + avoids duplicates)
#             if ent.text not in results:
#                 results[ent.text] = label
#
#     return results
#
# # -----------------------------
# # TEST RUN
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Elon Musk works at Tesla in California.
#     Sundar Pichai leads Google in India.
#     Amazon is expanding globally.
#     Apple is based in Cupertino.
#     South America is a continent.
#     """
#
#     output = extract_entities(text, use_chunking=True)
#
#     print("\n--- FINAL STABLE NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(k, "→", v)
# =======================================================30
# import spacy
#
# # -----------------------------
# # LOAD LIGHT MODEL
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# # 🔥 FIX: sentence splitter (VERY LIGHT, NO CPU HIT)
# nlp.add_pipe("sentencizer")
#
# # -----------------------------
# def trim_text(text, max_words=200):
#     return " ".join(text.split()[:max_words])
#
# # -----------------------------
# def extract_entities(text):
#
#     text = trim_text(text)
#
#     results = {}
#
#     doc = nlp(text)
#
#     for sent in doc.sents:
#
#         sent_doc = nlp(sent.text)
#
#         for ent in sent_doc.ents:
#
#             if ent.text not in results:
#
#                 label = ent.label_
#
#                 if label == "GPE":
#                     label = "LOCATION"
#
#                 results[ent.text] = label
#
#     return results
#
# # -----------------------------
# if __name__ == "__main__":
#
#     text = """
#     Elon Musk works at Tesla in California.
#     Sundar Pichai leads Google in India.
#     Amazon is expanding globally.
#     Apple is based in Cupertino.
#     """
#
#     output = extract_entities(text)
#
#     print("\n--- FINAL STABLE NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(k, "→", v)

# ==========================
# import spacy
#
# # -----------------------------
# # LIGHTWEIGHT MODEL
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# nlp.add_pipe("sentencizer")
#
# # -----------------------------
# def extract_entities(text):
#
#     doc = nlp(text)
#
#     results = {}
#
#     for ent in doc.ents:
#
#         label = ent.label_
#
#         if label == "GPE":
#             label = "LOCATION"
#
#         results[ent.text] = label
#
#     return results
#
# # -----------------------------
# # ON-DEMAND RUN FUNCTION
# # -----------------------------
# def run_ner_once():
#
#     text = input("\nEnter text for NER (or type 'exit'): ")
#
#     if text.lower() == "exit":
#         return False
#
#     output = extract_entities(text)
#
#     print("\n--- NER OUTPUT ---\n")
#
#     for k, v in output.items():
#         print(k, "→", v)
#
#     return True
#
# # -----------------------------
# if __name__ == "__main__":
#
#     print("NER SYSTEM READY (ON-DEMAND MODE)")
#
#     while True:
#         if not run_ner_once():
#             break


# ==========================================
# import spacy
# import pandas as pd
#
# # -----------------------------
# # LOAD LIGHT MODEL
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# nlp.add_pipe("sentencizer")
#
# # -----------------------------
# def extract_entities(text):
#
#     doc = nlp(text)
#
#     results = []
#
#     for ent in doc.ents:
#
#         label = ent.label_
#
#         if label == "GPE":
#             label = "LOCATION"
#
#         results.append((ent.text, label))
#
#     return results
#
# # -----------------------------
# def read_file(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()
#
# # -----------------------------
# def save_as_txt(data, output_path):
#
#     with open(output_path, "w", encoding="utf-8") as f:
#         for entity, label in data:
#             f.write(f"{entity} → {label}\n")
#
# # -----------------------------
# def save_as_excel(data, output_path):
#
#     df = pd.DataFrame(data, columns=["Entity", "Label"])
#     df.to_excel(output_path, index=False)
#
# # -----------------------------
# def run_pipeline():
#
#     file_path = input("\nEnter TXT file path: ").strip()
#
#     text = read_file(file_path)
#
#     results = extract_entities(text)
#
#     print("\nChoose output format:")
#     print("1. TXT")
#     print("2. Excel")
#
#     choice = input("Enter choice (1/2): ")
#
#     if choice == "1":
#         out_path = "ner_output.txt"
#         save_as_txt(results, out_path)
#         print("\nSaved as TXT:", out_path)
#
#     elif choice == "2":
#         out_path = "ner_output.xlsx"
#         save_as_excel(results, out_path)
#         print("\nSaved as Excel:", out_path)
#
#     else:
#         print("Invalid choice")
#
# # -----------------------------
# if __name__ == "__main__":
#
#     print("NER FILE PROCESSOR READY")
#
#     run_pipeline()


# ====================
# import spacy
#
# # -----------------------------
# # ULTRA LIGHT SPA CY SETUP
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# # sentence splitter (very cheap)
# nlp.add_pipe("sentencizer")
#
# # -----------------------------
# # FAST NORMALIZATION
# # -----------------------------
# def normalize(label):
#     if label in ("GPE", "LOC"):
#         return "LOCATION"
#     return label
#
# # -----------------------------
# # MAIN FUNCTION (OPTIMIZED)
# # -----------------------------
# def extract_entities(text):
#
#     # LIMIT INPUT SIZE (VERY IMPORTANT FOR CPU)
#     text = " ".join(text.split()[:250])
#
#     doc = nlp(text)
#
#     results = {}
#
#     # IMPORTANT: no nested NLP calls anymore
#     for ent in doc.ents:
#
#         label = normalize(ent.label_)
#
#         # filter noise
#         if ent.text.lower().startswith("dear"):
#             continue
#
#         if ent.text not in results:
#             results[ent.text] = label
#
#     return results
#
# # -----------------------------
# # ON-DEMAND RUN
# # -----------------------------
# if __name__ == "__main__":
#
#     print("\nNER READY (LOW CPU MODE)\n")
#
#     while True:
#
#         text = input("Enter text (or type exit): ")
#
#         if text.lower() == "exit":
#             break
#
#         output = extract_entities(text)
#
#         print("\n--- OUTPUT ---\n")
#
#         for k, v in output.items():
#             print(k, "→", v)
#
#         print("\n-------------------\n")

# import spacy
#
# # -----------------------------
# # LIGHT SPA CY MODEL (ONLY FALLBACK)
# # -----------------------------
# nlp = spacy.load(
#     "en_core_web_sm",
#     disable=["parser", "lemmatizer", "tagger", "attribute_ruler"]
# )
#
# nlp.add_pipe("sentencizer")
#
# # -----------------------------
# # FAST RULE BASE (NO CPU COST)
# # -----------------------------
# ORG = {
#     "Google", "Amazon", "Tesla", "Microsoft", "Apple",
#     "Infosys", "TCS", "Wipro", "Meta", "IBM"
# }
#
# LOC = {
#     "India", "USA", "London", "Bangalore", "Mumbai",
#     "Delhi", "California", "Hyderabad", "Cupertino"
# }
#
# PERSON = {
#     "Elon Musk", "Sundar Pichai", "Narendra Modi",
#     "Mukesh Ambani", "Bill Gates"
# }
#
# # -----------------------------
# def rule_match(word):
#
#     if word in ORG:
#         return "ORG"
#
#     if word in LOC:
#         return "LOCATION"
#
#     if word in PERSON:
#         return "PERSON"
#
#     return None
#
# # -----------------------------
# def extract_entities(text):
#
#     results = {}
#
#     # LIMIT TEXT (IMPORTANT CPU CONTROL)
#     text = " ".join(text.split()[:300])
#
#     doc = nlp(text)
#
#     for ent in doc.ents:
#
#         name = ent.text.strip()
#
#         # -------------------------
#         # STEP 1: RULE ENGINE (FAST)
#         # -------------------------
#         label = rule_match(name)
#
#         # -------------------------
#         # STEP 2: SPA CY FALLBACK ONLY IF NEEDED
#         # -------------------------
#         if label is None:
#
#             spacy_label = ent.label_
#
#             if spacy_label == "GPE":
#                 label = "LOCATION"
#             elif spacy_label == "NORP":
#                 label = "ORG"
#             else:
#                 label = spacy_label
#
#         # -------------------------
#         # CLEAN OUTPUT
#         # -------------------------
#         if name.lower().startswith("dear"):
#             continue
#
#         if name not in results:
#             results[name] = label
#
#     return results
#
# # -----------------------------
# # ON-DEMAND RUN
# # -----------------------------
# if __name__ == "__main__":
#
#     print("\n--- HYBRID LOW CPU NER SYSTEM ---\n")
#
#     while True:
#
#         text = input("Enter text (or exit): ")
#
#         if text.lower() == "exit":
#             break
#
#         output = extract_entities(text)
#
#         print("\n--- OUTPUT ---\n")
#
#         for k, v in output.items():
#             print(k, "→", v)
#
#         print("\n------------------\n")


# import spacy
# import re
# import time
# import os
#
# # -----------------------------
# # LOAD MODEL (ONLY NER ENABLED)
# # -----------------------------
# print("Loading model...")
# nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "lemmatizer"])
# print("Model loaded.\n")
#
# # -----------------------------
# # REGEX PATTERNS (FAST)
# # -----------------------------
# EMAIL_PATTERN = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
# PHONE_PATTERN = r"\b\d{10}\b"
#
# # -----------------------------
# # READ TEXT FILE
# # -----------------------------
# def read_file(file_path):
#     if not os.path.exists(file_path):
#         print("File not found!")
#         return None
#
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()
#
# # -----------------------------
# # EXTRACT ENTITIES
# # -----------------------------
# def extract_entities(text):
#     entities = []
#
#     # ---- REGEX ENTITIES ----
#     for email in re.findall(EMAIL_PATTERN, text):
#         entities.append((email, "EMAIL"))
#
#     for phone in re.findall(PHONE_PATTERN, text):
#         entities.append((phone, "PHONE"))
#
#     # ---- LIMIT TEXT (CPU CONTROL) ----
#     text = text[:5000]
#
#     # ---- NER ----
#     doc = nlp(text)
#
#     for ent in doc.ents:
#         entities.append((ent.text, ent.label_))
#
#     return entities
#
# # -----------------------------
# # MAIN FUNCTION
# # -----------------------------
# def process_file(file_path):
#     start_time = time.time()
#
#     text = read_file(file_path)
#     if text is None:
#         return
#
#     entities = extract_entities(text)
#
#     # Remove duplicates
#     entities = list(set(entities))
#
#     print("\n🔹 Extracted Entities:\n")
#     for ent, label in entities:
#         print(f"{ent}  -->  {label}")
#
#     print("\n-----------------------------")
#     print(f"Total Entities: {len(entities)}")
#     print(f"Time Taken: {round(time.time() - start_time, 2)} sec")
#     print("-----------------------------")
#
#
# # -----------------------------
# # RUN
# # -----------------------------
# if __name__ == "__main__":
#     file_path = input("Enter path of .txt file: ").strip()
#     process_file(file_path)

import random
import json

# -----------------------------
# DATA POOLS
# -----------------------------
persons = [
    "Rahul Sharma", "Amit Patel", "Priya Singh", "Anjali Mehta",
    "Rohit Verma", "Neha Kapoor", "Arjun Reddy", "Sneha Joshi",
    "Vikram Malhotra", "Karan Shah", "Pooja Desai", "Manish Gupta"
]

orgs = [
    "Google", "Microsoft", "Amazon", "Infosys", "TCS",
    "Wipro", "Accenture", "IBM", "Capgemini", "Deloitte",
    "TechNova", "Zyntrix Labs", "DataCore", "NextGen Solutions"
]

locations = [
    "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune",
    "Ahmedabad", "Chennai", "Gurgaon", "Noida", "London",
    "New York", "California", "Texas"
]

# -----------------------------
# SENTENCE TEMPLATES
# -----------------------------
templates = [
    "{person} works at {org} in {loc}",
    "{org} hired {person} in {loc}",
    "{person} joined {org}",
    "{org} is located in {loc}",
    "{person} moved to {loc}",
    "{person} is working at {org}",
    "{org} appointed {person} as manager",
    "{person} visited {loc} for work at {org}",
    "{org} has an office in {loc}",
    "{person} relocated to {loc} and joined {org}"
]

# -----------------------------
# GENERATE DATA
# -----------------------------
def generate_data(n=400):
    data = []

    for _ in range(n):
        person = random.choice(persons)
        org = random.choice(orgs)
        loc = random.choice(locations)
        template = random.choice(templates)

        text = template.format(person=person, org=org, loc=loc)

        entities = []

        # Find positions dynamically (NO ERROR GUARANTEED)
        if person in text:
            start = text.index(person)
            end = start + len(person)
            entities.append((start, end, "PERSON"))

        if org in text:
            start = text.index(org)
            end = start + len(org)
            entities.append((start, end, "ORG"))

        if loc in text:
            start = text.index(loc)
            end = start + len(loc)
            entities.append((start, end, "GPE"))

        data.append((text, {"entities": entities}))

    return data

# -----------------------------
# SAVE DATA
# -----------------------------
dataset = generate_data(400)

with open("train_data.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2)

print("✅ Generated 400 training samples (clean & aligned)")