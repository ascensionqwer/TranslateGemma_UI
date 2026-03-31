#!/usr/bin/env python3
"""
TranslateGemma Translator Backend
A Flask server that provides translation services using Ollama's translategemma:27b model.
"""

import json
import time
import os
import signal
import threading
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "translategemma:27b"

# All supported languages from TranslateGemma documentation
LANGUAGES = {
    "aa": "Afar",
    "aa-DJ": "Afar",
    "aa-ER": "Afar",
    "ab": "Abkhazian",
    "af": "Afrikaans",
    "af-NA": "Afrikaans",
    "ak": "Akan",
    "am": "Amharic",
    "an": "Aragonese",
    "ar": "Arabic",
    "ar-AE": "Arabic",
    "ar-BH": "Arabic",
    "ar-DJ": "Arabic",
    "ar-DZ": "Arabic",
    "ar-EG": "Arabic",
    "ar-EH": "Arabic",
    "ar-ER": "Arabic",
    "ar-IL": "Arabic",
    "ar-IQ": "Arabic",
    "ar-JO": "Arabic",
    "ar-KM": "Arabic",
    "ar-KW": "Arabic",
    "ar-LB": "Arabic",
    "ar-LY": "Arabic",
    "ar-MA": "Arabic",
    "ar-MR": "Arabic",
    "ar-OM": "Arabic",
    "ar-PS": "Arabic",
    "ar-QA": "Arabic",
    "ar-SA": "Arabic",
    "ar-SD": "Arabic",
    "ar-SO": "Arabic",
    "ar-SS": "Arabic",
    "ar-SY": "Arabic",
    "ar-TD": "Arabic",
    "ar-TN": "Arabic",
    "ar-YE": "Arabic",
    "as": "Assamese",
    "az": "Azerbaijani",
    "az-Arab": "Azerbaijani",
    "az-Arab-IQ": "Azerbaijani",
    "az-Arab-TR": "Azerbaijani",
    "az-Cyrl": "Azerbaijani",
    "az-Latn": "Azerbaijani",
    "ba": "Bashkir",
    "be": "Belarusian",
    "be-tarask": "Belarusian",
    "bg": "Bulgarian",
    "bg-BG": "Bulgarian",
    "bm": "Bambara",
    "bm-Nkoo": "Bambara",
    "bn": "Bengali",
    "bn-IN": "Bengali",
    "bo": "Tibetan",
    "bo-IN": "Tibetan",
    "br": "Breton",
    "bs": "Bosnian",
    "bs-Cyrl": "Bosnian",
    "bs-Latn": "Bosnian",
    "ca": "Catalan",
    "ca-AD": "Catalan",
    "ca-ES": "Catalan",
    "ca-FR": "Catalan",
    "ca-IT": "Catalan",
    "ce": "Chechen",
    "co": "Corsican",
    "cs": "Czech",
    "cs-CZ": "Czech",
    "cv": "Chuvash",
    "cy": "Welsh",
    "da": "Danish",
    "da-DK": "Danish",
    "da-GL": "Danish",
    "de": "German",
    "de-AT": "German",
    "de-BE": "German",
    "de-CH": "German",
    "de-DE": "German",
    "de-IT": "German",
    "de-LI": "German",
    "de-LU": "German",
    "dv": "Divehi",
    "dz": "Dzongkha",
    "ee": "Ewe",
    "ee-TG": "Ewe",
    "el": "Greek",
    "el-CY": "Greek",
    "el-GR": "Greek",
    "el-polyton": "Greek",
    "en": "English",
    "en-AE": "English",
    "en-AG": "English",
    "en-AI": "English",
    "en-AS": "English",
    "en-AT": "English",
    "en-AU": "English",
    "en-BB": "English",
    "en-BE": "English",
    "en-BI": "English",
    "en-BM": "English",
    "en-BS": "English",
    "en-BW": "English",
    "en-BZ": "English",
    "en-CA": "English",
    "en-CC": "English",
    "en-CH": "English",
    "en-CK": "English",
    "en-CM": "English",
    "en-CX": "English",
    "en-CY": "English",
    "en-CZ": "English",
    "en-DE": "English",
    "en-DG": "English",
    "en-DK": "English",
    "en-DM": "English",
    "en-ER": "English",
    "en-ES": "English",
    "en-FI": "English",
    "en-FJ": "English",
    "en-FK": "English",
    "en-FM": "English",
    "en-FR": "English",
    "en-GB": "English",
    "en-GD": "English",
    "en-GG": "English",
    "en-GH": "English",
    "en-GI": "English",
    "en-GM": "English",
    "en-GS": "English",
    "en-GU": "English",
    "en-GY": "English",
    "en-HK": "English",
    "en-HU": "English",
    "en-ID": "English",
    "en-IE": "English",
    "en-IL": "English",
    "en-IM": "English",
    "en-IN": "English",
    "en-IO": "English",
    "en-IT": "English",
    "en-JE": "English",
    "en-JM": "English",
    "en-KE": "English",
    "en-KI": "English",
    "en-KN": "English",
    "en-KY": "English",
    "en-LC": "English",
    "en-LR": "English",
    "en-LS": "English",
    "en-MG": "English",
    "en-MH": "English",
    "en-MO": "English",
    "en-MP": "English",
    "en-MS": "English",
    "en-MT": "English",
    "en-MU": "English",
    "en-MV": "English",
    "en-MW": "English",
    "en-MY": "English",
    "en-NA": "English",
    "en-NF": "English",
    "en-NG": "English",
    "en-NL": "English",
    "en-NO": "English",
    "en-NR": "English",
    "en-NU": "English",
    "en-NZ": "English",
    "en-PG": "English",
    "en-PH": "English",
    "en-PK": "English",
    "en-PL": "English",
    "en-PN": "English",
    "en-PR": "English",
    "en-PT": "English",
    "en-PW": "English",
    "en-RO": "English",
    "en-RW": "English",
    "en-SB": "English",
    "en-SC": "English",
    "en-SD": "English",
    "en-SE": "English",
    "en-SG": "English",
    "en-SH": "English",
    "en-SI": "English",
    "en-SK": "English",
    "en-SL": "English",
    "en-SS": "English",
    "en-SX": "English",
    "en-SZ": "English",
    "en-TC": "English",
    "en-TK": "English",
    "en-TO": "English",
    "en-TT": "English",
    "en-TV": "English",
    "en-TZ": "English",
    "en-UG": "English",
    "en-UM": "English",
    "en-VC": "English",
    "en-VG": "English",
    "en-VI": "English",
    "en-VU": "English",
    "en-WS": "English",
    "en-ZA": "English",
    "en-ZM": "English",
    "en-ZW": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "es-AR": "Spanish",
    "es-BO": "Spanish",
    "es-BR": "Spanish",
    "es-BZ": "Spanish",
    "es-CL": "Spanish",
    "es-CO": "Spanish",
    "es-CR": "Spanish",
    "es-CU": "Spanish",
    "es-DO": "Spanish",
    "es-EA": "Spanish",
    "es-EC": "Spanish",
    "es-ES": "Spanish",
    "es-GQ": "Spanish",
    "es-GT": "Spanish",
    "es-HN": "Spanish",
    "es-IC": "Spanish",
    "es-MX": "Spanish",
    "es-NI": "Spanish",
    "es-PA": "Spanish",
    "es-PE": "Spanish",
    "es-PH": "Spanish",
    "es-PR": "Spanish",
    "es-PY": "Spanish",
    "es-SV": "Spanish",
    "es-US": "Spanish",
    "es-UY": "Spanish",
    "es-VE": "Spanish",
    "et": "Estonian",
    "et-EE": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fa-AF": "Persian",
    "fa-IR": "Persian",
    "ff": "Fulah",
    "ff-Adlm": "Fulah",
    "ff-Adlm-BF": "Fulah",
    "ff-Adlm-CM": "Fulah",
    "ff-Adlm-GH": "Fulah",
    "ff-Adlm-GM": "Fulah",
    "ff-Adlm-GW": "Fulah",
    "ff-Adlm-LR": "Fulah",
    "ff-Adlm-MR": "Fulah",
    "ff-Adlm-NE": "Fulah",
    "ff-Adlm-NG": "Fulah",
    "ff-Adlm-SL": "Fulah",
    "ff-Adlm-SN": "Fulah",
    "ff-Latn": "Fulah",
    "ff-Latn-BF": "Fulah",
    "ff-Latn-CM": "Fulah",
    "ff-Latn-GH": "Fulah",
    "ff-Latn-GM": "Fulah",
    "ff-Latn-GN": "Fulah",
    "ff-Latn-GW": "Fulah",
    "ff-Latn-LR": "Fulah",
    "ff-Latn-MR": "Fulah",
    "ff-Latn-NE": "Fulah",
    "ff-Latn-NG": "Fulah",
    "ff-Latn-SL": "Fulah",
    "fi": "Finnish",
    "fi-FI": "Finnish",
    "fil-PH": "Filipino",
    "fo": "Faroese",
    "fo-DK": "Faroese",
    "fr": "French",
    "fr-BE": "French",
    "fr-BF": "French",
    "fr-BI": "French",
    "fr-BJ": "French",
    "fr-BL": "French",
    "fr-CA": "French",
    "fr-CD": "French",
    "fr-CF": "French",
    "fr-CG": "French",
    "fr-CH": "French",
    "fr-CI": "French",
    "fr-CM": "French",
    "fr-DJ": "French",
    "fr-DZ": "French",
    "fr-FR": "French",
    "fr-GA": "French",
    "fr-GF": "French",
    "fr-GN": "French",
    "fr-GP": "French",
    "fr-GQ": "French",
    "fr-HT": "French",
    "fr-KM": "French",
    "fr-LU": "French",
    "fr-MA": "French",
    "fr-MC": "French",
    "fr-MF": "French",
    "fr-MG": "French",
    "fr-ML": "French",
    "fr-MQ": "French",
    "fr-MR": "French",
    "fr-MU": "French",
    "fr-NC": "French",
    "fr-NE": "French",
    "fr-PF": "French",
    "fr-PM": "French",
    "fr-RE": "French",
    "fr-RW": "French",
    "fr-SC": "French",
    "fr-SN": "French",
    "fr-SY": "French",
    "fr-TD": "French",
    "fr-TG": "French",
    "fr-TN": "French",
    "fr-VU": "French",
    "fr-WF": "French",
    "fr-YT": "French",
    "fy": "Western Frisian",
    "ga": "Irish",
    "ga-GB": "Irish",
    "gd": "Scottish Gaelic",
    "gl": "Galician",
    "gn": "Guarani",
    "gu": "Gujarati",
    "gu-IN": "Gujarati",
    "gv": "Manx",
    "ha": "Hausa",
    "ha-Arab": "Hausa",
    "ha-Arab-SD": "Hausa",
    "ha-GH": "Hausa",
    "ha-NE": "Hausa",
    "he": "Hebrew",
    "he-IL": "Hebrew",
    "hi": "Hindi",
    "hi-IN": "Hindi",
    "hi-Latn": "Hindi",
    "hr": "Croatian",
    "hr-BA": "Croatian",
    "hr-HR": "Croatian",
    "ht": "Haitian",
    "hu": "Hungarian",
    "hu-HU": "Hungarian",
    "hy": "Armenian",
    "ia": "Interlingua",
    "id": "Indonesian",
    "id-ID": "Indonesian",
    "ie": "Interlingue",
    "ig": "Igbo",
    "ii": "Sichuan Yi",
    "ik": "Inupiaq",
    "io": "Ido",
    "is": "Icelandic",
    "it": "Italian",
    "it-CH": "Italian",
    "it-IT": "Italian",
    "it-SM": "Italian",
    "it-VA": "Italian",
    "iu": "Inuktitut",
    "iu-Latn": "Inuktitut",
    "ja": "Japanese",
    "ja-JP": "Japanese",
    "jv": "Javanese",
    "ka": "Georgian",
    "ki": "Kikuyu",
    "kk": "Kazakh",
    "kk-Arab": "Kazakh",
    "kk-Cyrl": "Kazakh",
    "kk-KZ": "Kazakh",
    "kl": "Kalaallisut",
    "km": "Central Khmer",
    "kn": "Kannada",
    "kn-IN": "Kannada",
    "ko": "Korean",
    "ko-CN": "Korean",
    "ko-KP": "Korean",
    "ko-KR": "Korean",
    "ks": "Kashmiri",
    "ks-Arab": "Kashmiri",
    "ks-Deva": "Kashmiri",
    "ku": "Kurdish",
    "kw": "Cornish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lb": "Luxembourgish",
    "lg": "Ganda",
    "ln": "Lingala",
    "ln-AO": "Lingala",
    "ln-CF": "Lingala",
    "ln-CG": "Lingala",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lt-LT": "Lithuanian",
    "lu": "Luba-Katanga",
    "lv": "Latvian",
    "lv-LV": "Latvian",
    "mg": "Malagasy",
    "mi": "Maori",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "ml-IN": "Malayalam",
    "mn": "Mongolian",
    "mn-Mong": "Mongolian",
    "mn-Mong-MN": "Mongolian",
    "mr": "Marathi",
    "mr-IN": "Marathi",
    "ms": "Malay",
    "ms-Arab": "Malay",
    "ms-Arab-BN": "Malay",
    "ms-BN": "Malay",
    "ms-ID": "Malay",
    "ms-SG": "Malay",
    "mt": "Maltese",
    "my": "Burmese",
    "nb": "Norwegian Bokmål",
    "nb-SJ": "Norwegian Bokmål",
    "nd": "North Ndebele",
    "ne": "Nepali",
    "ne-IN": "Nepali",
    "nl": "Dutch",
    "nl-AW": "Dutch",
    "nl-BE": "Dutch",
    "nl-BQ": "Dutch",
    "nl-CW": "Dutch",
    "nl-NL": "Dutch",
    "nl-SR": "Dutch",
    "nl-SX": "Dutch",
    "nn": "Norwegian Nynorsk",
    "no": "Norwegian",
    "no-NO": "Norwegian",
    "nr": "South Ndebele",
    "nv": "Navajo",
    "ny": "Chichewa",
    "oc": "Occitan",
    "oc-ES": "Occitan",
    "om": "Oromo",
    "om-KE": "Oromo",
    "or": "Oriya",
    "os": "Ossetian",
    "os-RU": "Ossetian",
    "pa": "Punjabi",
    "pa-IN": "Punjabi",
    "pa-Arab": "Punjabi",
    "pa-Guru": "Punjabi",
    "pl": "Polish",
    "pl-PL": "Polish",
    "ps": "Pashto",
    "ps-PK": "Pashto",
    "pt": "Portuguese",
    "pt-AO": "Portuguese",
    "pt-BR": "Portuguese",
    "pt-CH": "Portuguese",
    "pt-CV": "Portuguese",
    "pt-GQ": "Portuguese",
    "pt-GW": "Portuguese",
    "pt-LU": "Portuguese",
    "pt-MO": "Portuguese",
    "pt-MZ": "Portuguese",
    "pt-PT": "Portuguese",
    "pt-ST": "Portuguese",
    "pt-TL": "Portuguese",
    "qu": "Quechua",
    "qu-BO": "Quechua",
    "qu-EC": "Quechua",
    "rm": "Romansh",
    "rn": "Rundi",
    "ro": "Romanian",
    "ro-MD": "Romanian",
    "ro-RO": "Romanian",
    "ru": "Russian",
    "ru-BY": "Russian",
    "ru-KG": "Russian",
    "ru-KZ": "Russian",
    "ru-MD": "Russian",
    "ru-RU": "Russian",
    "ru-UA": "Russian",
    "rw": "Kinyarwanda",
    "sa": "Sanskrit",
    "sc": "Sardinian",
    "sd": "Sindhi",
    "sd-Arab": "Sindhi",
    "sd-Deva": "Sindhi",
    "se": "Northern Sami",
    "se-FI": "Northern Sami",
    "se-SE": "Northern Sami",
    "sg": "Sango",
    "si": "Sinhala",
    "sk": "Slovak",
    "sk-SK": "Slovak",
    "sl": "Slovenian",
    "sl-SI": "Slovenian",
    "sn": "Shona",
    "so": "Somali",
    "so-DJ": "Somali",
    "so-ET": "Somali",
    "so-KE": "Somali",
    "sq": "Albanian",
    "sq-MK": "Albanian",
    "sq-XK": "Albanian",
    "sr": "Serbian",
    "sr-RS": "Serbian",
    "sr-Cyrl": "Serbian",
    "sr-Cyrl-BA": "Serbian",
    "sr-Cyrl-ME": "Serbian",
    "sr-Cyrl-XK": "Serbian",
    "sr-Latn": "Serbian",
    "sr-Latn-BA": "Serbian",
    "sr-Latn-ME": "Serbian",
    "sr-Latn-XK": "Serbian",
    "ss": "Swati",
    "ss-SZ": "Swati",
    "st": "Southern Sotho",
    "st-LS": "Southern Sotho",
    "su": "Sundanese",
    "su-Latn": "Sundanese",
    "sv": "Swedish",
    "sv-AX": "Swedish",
    "sv-FI": "Swedish",
    "sv-SE": "Swedish",
    "sw": "Swahili",
    "sw-CD": "Swahili",
    "sw-KE": "Swahili",
    "sw-TZ": "Swahili",
    "sw-UG": "Swahili",
    "ta": "Tamil",
    "ta-IN": "Tamil",
    "ta-LK": "Tamil",
    "ta-MY": "Tamil",
    "ta-SG": "Tamil",
    "te": "Telugu",
    "te-IN": "Telugu",
    "tg": "Tajik",
    "th": "Thai",
    "th-TH": "Thai",
    "ti": "Tigrinya",
    "ti-ER": "Tigrinya",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tn": "Tswana",
    "tn-BW": "Tswana",
    "to": "Tonga",
    "tr": "Turkish",
    "tr-CY": "Turkish",
    "tr-TR": "Turkish",
    "ts": "Tsonga",
    "tt": "Tatar",
    "ug": "Uyghur",
    "uk": "Ukrainian",
    "uk-UA": "Ukrainian",
    "ur": "Urdu",
    "ur-IN": "Urdu",
    "ur-PK": "Urdu",
    "uz": "Uzbek",
    "uz-Arab": "Uzbek",
    "uz-Cyrl": "Uzbek",
    "uz-Latn": "Uzbek",
    "ve": "Venda",
    "vi": "Vietnamese",
    "vi-VN": "Vietnamese",
    "vo": "Volapük",
    "wa": "Walloon",
    "wo": "Wolof",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "yo-BJ": "Yoruba",
    "za": "Zhuang",
    "zh": "Chinese",
    "zh-CH": "Chinese",
    "zh-TW": "Chinese",
    "zh-Hans": "Chinese",
    "zh-Hans-HK": "Chinese",
    "zh-Hans-MO": "Chinese",
    "zh-Hans-MY": "Chinese",
    "zh-Hans-SG": "Chinese",
    "zh-Hant": "Chinese",
    "zh-Hant-HK": "Chinese",
    "zh-Hant-MO": "Chinese",
    "zh-Hant-MY": "Chinese",
    "zh-Latn": "Chinese",
    "zu": "Zulu",
    "zu-ZA": "Zulu",
}


def get_language_name(code):
    """Get the display name for a language code."""
    return LANGUAGES.get(code, code)


def build_translation_prompt(source_lang, target_lang, text):
    """
    Build the translation prompt following TranslateGemma's exact format.
    
    Format:
    You are a professional {SOURCE_LANG} ({SOURCE_CODE}) to {TARGET_LANG} ({TARGET_CODE}) translator...
    Produce only the {TARGET_LANG} translation...
    Please translate the following {SOURCE_LANG} text into {TARGET_LANG}:
    
    
    {TEXT}
    """
    source_name = get_language_name(source_lang)
    target_name = get_language_name(target_lang)
    
    prompt = f"""You are a professional {source_name} ({source_lang}) to {target_name} ({target_lang}) translator. Your goal is to accurately convey the meaning and nuances of the original {source_name} text while adhering to {target_name} grammar, vocabulary, and cultural sensitivities.
Produce only the {target_name} translation, without any additional explanations or commentary. Please translate the following {source_name} text into {target_name}:


{text}"""
    
    return prompt


def call_ollama(prompt):
    """Call the Ollama API to get translation."""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        else:
            raise ValueError("No translation content received from Ollama")
            
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
    except requests.exceptions.Timeout:
        raise TimeoutError("Translation request timed out")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Model '{MODEL}' not found. Run: ollama pull {MODEL}")
        raise


@app.route('/')
def index():
    """Serve the main translation page."""
    return render_template('index.html', languages=LANGUAGES)


@app.route('/api/languages')
def get_languages():
    """Return the list of supported languages."""
    # Return unique language codes with their names
    unique_languages = {}
    for code, name in LANGUAGES.items():
        # Use base code if it doesn't have a variant
        if '-' not in code or code in ['zh-Hans', 'zh-Hant']:
            unique_languages[code] = name
    
    return jsonify(unique_languages)


@app.route('/api/translate', methods=['POST'])
def translate():
    """Handle translation requests."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    text = data.get('text')
    
    if not source_lang or not target_lang or not text:
        return jsonify({"error": "Missing required fields: source_lang, target_lang, or text"}), 400
    
    if source_lang == target_lang:
        return jsonify({"error": "Source and target languages must be different"}), 400
    
    if not text.strip():
        return jsonify({"error": "Text cannot be empty"}), 400
    
    try:
        prompt = build_translation_prompt(source_lang, target_lang, text.strip())
        translation = call_ollama(prompt)
        
        return jsonify({
            "success": True,
            "translation": translation,
            "source_lang": source_lang,
            "target_lang": target_lang
        })
        
    except ConnectionError as e:
        return jsonify({"error": str(e)}), 503
    except TimeoutError as e:
        return jsonify({"error": str(e)}), 504
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500


import os
import signal
import threading

@app.route('/api/health')
def health():
    """Health check endpoint."""
    try:
        # Check if Ollama is reachable
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "connected" if response.ok else "error"
    except:
        ollama_status = "not_connected"
    
    return jsonify({
        "status": "healthy",
        "ollama": ollama_status,
        "model": MODEL
    })


@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the Flask server."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # Not running with werkzeug server, use SIGTERM
        os.kill(os.getpid(), signal.SIGTERM)
    else:
        func()
    return jsonify({"status": "shutting down"})


if __name__ == '__main__':
    print("=" * 60)
    print("TranslateGemma Translator Server")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"Ollama API: {OLLAMA_API_URL}")
    print(f"Supported Languages: {len(LANGUAGES)} language codes")
    print("=" * 60)
    print("Starting server on http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)