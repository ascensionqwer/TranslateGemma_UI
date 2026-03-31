# TranslateGemma Translator

A beautiful web-based translation UI powered by Ollama's **translategemma:27b** model, supporting 55+ languages.

![TranslateGemma](https://ollama.com/public/og.png)

## Features

- 🌐 **55+ Languages Supported** - Full support for all TranslateGemma language codes
- 🎨 **Beautiful UI** - Modern, responsive design with gradient styling
- ⚡ **Fast Translation** - Direct integration with Ollama API
- 🔄 **Language Swap** - One-click swap between source and target languages
- 📋 **Copy to Clipboard** - Easy copy of translated text
- 🖥️ **One-Click Launch** - Desktop shortcut for instant startup

## Prerequisites

1. **Ollama** - Install from [ollama.com](https://ollama.com)
2. **Python 3** - Install from [python.org](https://www.python.org/downloads/)
3. **TranslateGemma Model** - Pull with: `ollama pull translategemma:27b`

## Quick Start

### Option 1: Desktop Shortcut (macOS)

Double-click the **TranslateGemma.command** file on your Desktop to launch the translator.

### Option 2: Terminal Launch

```bash
# Navigate to the project directory
cd /Users/wesleygwn/Documents/Work/Codes/Translator

# Run the start script
./start.sh
```

### Option 3: Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python3 app.py

# Open in browser
open http://localhost:5001
```

> **Note:** The server uses port 5001 to avoid conflicts with macOS AirPlay Receiver which uses port 5000.

## Project Structure

```
Translator/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── start.sh               # Launch script
├── templates/
│   └── index.html         # Web UI
└── Translator.app/        # macOS app bundle
    └── Contents/
        ├── Info.plist     # App metadata
        └── MacOS/
            └── start      # App executable
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main translation UI |
| `/api/languages` | GET | List supported languages |
| `/api/translate` | POST | Translate text |
| `/api/health` | GET | Health check |

### Translation API Example

```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "source_lang": "en",
    "target_lang": "es",
    "text": "Hello, how are you?"
  }'
```

## Supported Languages

TranslateGemma supports over 200 language codes across 55 languages. Here are the most common:

| Code | Language | Code | Language |
|------|----------|------|----------|
| en | English | es | Spanish |
| fr | French | de | German |
| it | Italian | pt | Portuguese |
| ru | Russian | ja | Japanese |
| ko | Korean | zh-Hans | Chinese (Simplified) |
| zh-Hant | Chinese (Traditional) | ar | Arabic |
| hi | Hindi | bn | Bengali |
| tr | Turkish | vi | Vietnamese |
| th | Thai | nl | Dutch |
| pl | Polish | sv | Swedish |
| da | Danish | fi | Finnish |
| no | Norwegian | el | Greek |
| he | Hebrew | id | Indonesian |
| ms | Malay | uk | Ukrainian |
| cs | Czech | sk | Slovak |
| hu | Hungarian | ro | Romanian |
| bg | Bulgarian | sr | Serbian |
| hr | Croatian | sl | Slovenian |
| fa | Persian | ur | Urdu |
| ta | Tamil | te | Telugu |
| ml | Malayalam | kn | Kannada |
| mr | Marathi | gu | Gujarati |
| pa | Punjabi | sw | Swahili |

For the full list of 200+ language codes, see the [TranslateGemma documentation](https://ollama.com/library/translategemma).

## Prompt Format

The translator uses TranslateGemma's recommended prompt format:

```
You are a professional {SOURCE_LANG} ({SOURCE_CODE}) to {TARGET_LANG} ({TARGET_CODE}) translator. Your goal is to accurately convey the meaning and nuances of the original {SOURCE_LANG} text while adhering to {TARGET_LANG} grammar, vocabulary, and cultural sensitivities.
Produce only the {TARGET_LANG} translation, without any additional explanations or commentary. Please translate the following {SOURCE_LANG} text into {TARGET_LANG}:


{TEXT}
```

## Troubleshooting

### Ollama Not Running

```bash
# Start Ollama
ollama serve
```

### Model Not Found

```bash
# Pull the model
ollama pull translategemma:27b
```

### Python Dependencies Issues

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Check what's using port 5000
lsof -i :5000

# Kill the process if needed
kill -9 <PID>
```

## License

This project uses the TranslateGemma model from Ollama. See [Ollama's license](https://ollama.com) for model usage terms.

## Credits

- **TranslateGemma** - Open translation models built on Gemma 3
- **Ollama** - Local LLM runtime
- **Flask** - Python web framework