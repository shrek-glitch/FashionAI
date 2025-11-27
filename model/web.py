import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import time
import json
from PIL import Image
from io import BytesIO
import torch

# --- Page Config ---
st.set_page_config(
    page_title="FashionAI - Style Assistant",
    page_icon="👗",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    .main-header {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>👗 FashionAI Style Advisor</h1>", unsafe_allow_html=True)
st.caption("AI-powered fashion advice & visualization based on Qwen3 & Flux")

# --- Load API Key from Secrets ---
try:
    API_KEY = st.secrets["modelscope_api_key"]
except FileNotFoundError:
    st.error("Error: secrets.toml not found. Please configure your API key.")
    st.stop()
except KeyError:
    st.error("Error: 'modelscope_api_key' not found in secrets.toml.")
    st.stop()

# --- Core Logic ---

# 1. Load Model (Cached)
@st.cache_resource
def load_model():
    model_name = "Qwen/Qwen3-1.7B"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        return tokenizer, model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None, None

tokenizer, model = load_model()

# 2. Image Generation Configuration
BASE_URL = 'https://api-inference.modelscope.cn/'
COMMON_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def generate_fashion_image(prompt):
    full_prompt = (
        f"Fashion outfit: {prompt}. High resolution, realistic fabric texture, "
        "professional lighting, fashion magazine style, full-body front view, "
        "perfect body proportion, harmonious color matching, minimal background"
    )
    
    try:
        response = requests.post(
            f"{BASE_URL}v1/images/generations",
            headers={**COMMON_HEADERS, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps({
                "model": "MusePublic/489_ckpt_FLUX_1",
                "prompt": full_prompt
            }, ensure_ascii=False).encode('utf-8')
        )
        response.raise_for_status()
        task_id = response.json()["task_id"]
        
        # Poll for result
        start_time = time.time()
        while True:
            if time.time() - start_time > 60: # Timeout after 60s
                return None, "Generation timed out"
                
            result = requests.get(
                f"{BASE_URL}v1/tasks/{task_id}",
                headers={**COMMON_HEADERS, "X-ModelScope-Task-Type": "image_generation"},
            )
            result.raise_for_status()
            data = result.json()

            if data["task_status"] == "SUCCEED":
                image_url = data["output_images"][0]
                image = Image.open(BytesIO(requests.get(image_url).content))
                return image, "Success"
            elif data["task_status"] == "FAILED":
                return None, "Generation failed"
            
            time.sleep(2)
            
    except Exception as e:
        return None, str(e)

def get_text_advice(user_input):
    prompt = f"Provide detailed fashion advice for {user_input}, including clothing styles, color matching, accessories, and suitable occasions"
    messages = [{"role": "user", "content": prompt}]
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True 
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=4096
        )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    
    # Logic to strip thinking process
    try:
        # 151668 is the Qwen thought process separator token
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0
    
    # We only decode the final answer, ignoring the thinking part
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    
    return content

# --- Chat Interface ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "content" in message:
            st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], caption="Generated Outfit Visualization", use_container_width=True)

# User Input
if user_input := st.chat_input("Ask for fashion advice (e.g., Summer outfit for a beach date)..."):
    
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Generate Response
    with st.chat_message("assistant"):
        if not model or not tokenizer:
            st.error("Model not loaded. Please checks logs.")
        else:
            # Step A: Text Advice
            status_placeholder = st.empty()
            status_placeholder.markdown("🤔 Analyzing fashion trends...")
            
            advice = get_text_advice(user_input)
            
            # Replace loading text with actual advice
            status_placeholder.markdown(advice)
            
            # Step B: Image Generation
            with st.spinner("🎨 Creating outfit visualization..."):
                img, status = generate_fashion_image(user_input)
                
            if img:
                st.image(img, caption="Generated Outfit Visualization", use_container_width=True)
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": advice, 
                    "image": img
                })
            else:
                st.warning(f"Could not generate image: {status}")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": advice
                })