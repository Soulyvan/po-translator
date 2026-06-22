import os

import polib
import requests
import time
import re
import argparse
import json
from dotenv import load_dotenv

load_dotenv()

# =========================
# CONFIG
# =========================
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

DEEPL_URL = "https://api-free.deepl.com/v2/translate"

cache = {}

VAR_PATTERN = re.compile(r"(%\([a-zA-Z0-9_]+\)s|%s)")


# =========================
# VARIABLES PROTECTION
# =========================
def protect_variables(text):
    variables = VAR_PATTERN.findall(text)

    mapping = {}
    protected = text

    for i, var in enumerate(variables):
        token = f"__VAR_{i}__"
        protected = protected.replace(var, token, 1)
        mapping[token] = var

    return protected, mapping


def restore_variables(text, mapping):
    for token, var in mapping.items():
        text = text.replace(token, var)
    return text


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# DEEPL CALL (FIXED)
# =========================
def translate(text, target_lang):
    key = (text, target_lang)

    if key in cache:
        return cache[key]

    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": [text],
        "target_lang": target_lang
    }

    response = requests.post(
        DEEPL_URL,
        headers=headers,
        data=json.dumps(payload)
    )

    result = response.json()

    # 🔥 SAFE CHECK
    if "translations" not in result:
        print("❌ DeepL ERROR RESPONSE:")
        print(result)
        raise Exception("DeepL API error")

    translation = result["translations"][0]["text"]

    cache[key] = translation

    time.sleep(0.2)

    return translation


# =========================
# TRANSLATION CORE
# =========================
def translate_entry(text, lang):
    if not text.strip():
        return text

    protected, mapping = protect_variables(text)
    cleaned = clean_text(protected)

    translated = translate(cleaned, lang)

    return restore_variables(translated, mapping)


# =========================
# IN-PLACE PO PROCESS
# =========================
def process_po_inplace(file_path, lang):
    po = polib.pofile(file_path)

    changed = False

    for entry in po:

        # skip déjà traduit
        if entry.msgstr.strip():
            continue

        try:
            print(f"Traduction: {entry.msgid[:60]}")

            entry.msgstr = translate_entry(entry.msgid, lang)
            changed = True

        except Exception as e:
            print(f"❌ Erreur: {entry.msgid} -> {e}")

    if changed:
        po.save(file_path)
        print(f"\n✔ Fichier mis à jour : {file_path}")
    else:
        print("\n✔ Rien à modifier")


# =========================
# CLI
# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--lang", required=True, choices=["es", "pt"])
    parser.add_argument("--file", default="django.po")

    args = parser.parse_args()

    lang_map = {
        "es": "ES",        # Espagnol
        "pt": "PT-PT",     # Portugais (Portugal)
        "en": "EN-US",     # Anglais (États-Unis)
        # les autres si vous voulez
    }

    process_po_inplace(args.file, lang_map[args.lang])
