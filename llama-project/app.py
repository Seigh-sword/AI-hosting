from flask import Flask, render_template, request, jsonify
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import os

app = Flask(__name__)

# --- Model Loading ---
MODEL_NAME = "TheBloke/Llama-2-7B-Chat-GGUF"
MODEL_FILE = "llama-2-7b-chat.Q2_K.gguf"
MODEL_PATH = None
LLM = None

def load_model():
    global MODEL_PATH, LLM
    if LLM is None:
        try:
            print("Downloading model...")
            MODEL_PATH = hf_hub_download(repo_id=MODEL_NAME, filename=MODEL_FILE)
            print(f"Model downloaded to: {MODEL_PATH}")

            print("Loading model...")
            LLM = Llama(model_path=MODEL_PATH, n_ctx=2048)
            print("Model loaded successfully.")

        except Exception as e:
            print(f"Error loading model: {e}")
            # Handle model loading failure gracefully
            LLM = None

# Load the model when the app starts
load_model()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    global LLM
    if LLM is None:
        return jsonify({'error': 'Model is not loaded. Please check the server logs.'}), 500

    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400

    try:
        output = LLM(f"Q: {prompt} A: ", max_tokens=256, stop=["Q:", "\n"], echo=True)
        response = output['choices'][0]['text']
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
