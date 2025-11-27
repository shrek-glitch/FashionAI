# FashionAI - AI-Powered Fashion Style Advisor

<div align="center">

![FashionAI Logo](https://img.shields.io/badge/FashionAI-Style%20Advisor-blue?style=for-the-badge&logo=python)

An intelligent fashion advice system that combines **Qwen3-1.7B** for text generation and **Flux** for realistic fashion image generation.

[![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

## 🌟 Features

- **🤖 AI Fashion Advice**: Get personalized fashion recommendations using Qwen2.5 language model
- **🎨 Visual Outfits**: Generate realistic outfit images with Flux image generation
- **💬 Interactive Chat**: Natural conversation interface for fashion queries
- **⚡ Local Processing**: Private and secure - no data leaves your device (except image generation)
- **🎯 Style Customization**: Advice tailored to specific occasions, preferences, and body types

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for optimal performance)
- ModelScope API key (for image generation)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/FashionAI.git
cd FashionAI
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Configuration

1. **Get ModelScope API Key**
   - Visit [ModelScope](https://modelscope.cn)
   - Create an account and obtain your API key
   - This is required for Flux image generation

2. **Set up Streamlit secrets**
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

   Edit `.streamlit/secrets.toml` and replace the placeholder:
   ```toml
   # Replace with your actual ModelScope API key
   # Get your API key from: https://modelscope.cn
   modelscope_api_key = "your-api-key-here"
   ```

### Running the Application

```bash
streamlit run model/web.py
```

The application will open in your web browser at `http://localhost:8501`

## 📋 User Guide

### How to Use FashionAI

1. **Start the Application**
   - Run the command: `streamlit run model/web.py`
   - Open the displayed URL in your browser

2. **Ask for Fashion Advice**
   - Type your fashion query in the chat input
   - Examples:
     - "Summer outfit for a beach date"
     - "Professional business casual for a tech startup"
     - "Formal evening gown for a wedding"
     - "Casual weekend outfit that's comfortable yet stylish"

3. **Get Recommendations**
   - FashionAI will provide detailed text advice including:
     - Clothing suggestions
     - Color combinations
     - Accessory recommendations
     - Occasion-appropriate styling

4. **View Visual Outfit**
   - After text advice, FashionAI generates a visual representation
   - Images show realistic outfit examples with proper styling

### Sample Queries

```
• "What should I wear for a job interview in finance?"
• "Help me create a capsule wardrobe for spring"
• "Outfit suggestion for a first date at a café"
• "Business casual presentation attire"
• "Weekend brunch with friends outfit"
```

### Tips for Best Results

- **Be Specific**: Include occasion, weather, personal style preferences
- **Mention Constraints**: Budget, body type, colors you prefer/avoid
- **Ask Follow-ups**: Refine suggestions with additional questions
- **Save Your Favorites**: Take screenshots of generated outfits for reference

## 🔧 Technical Details

### Architecture

```
FashionAI Stack:
├── Frontend: Streamlit Web Interface
├── Language Model: Qwen2.5-1.7B (Local)
├── Image Generation: Flux API (ModelScope)
├── Processing: PyTorch, Transformers
└── Dependencies: requests, PIL, streamlit
```

### Model Information

- **Qwen3-1.7B**: Lightweight language model optimized for conversational AI
- **Flux**: Advanced text-to-image generation model for fashion visualization
- **Local Processing**: All text generation happens locally on your machine
- **API Integration**: Only image generation requires external API calls

### Performance

- **Startup Time**: ~30 seconds (model loading)
- **Response Time**: ~2-5 seconds for text, ~10-30 seconds for images
- **Memory Usage**: ~4-8GB RAM (varies by model and GPU)
- **GPU Support**: Automatic CUDA detection and usage

## 📁 Project Structure

```
FashionAI/
├── model/
│   └── web.py              # Main Streamlit application
├── .streamlit/
│   ├── secrets.toml        # API configuration (create from example)
│   └── secrets.toml.example # Configuration template
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Development

### Customizing the Application

1. **Modify Prompts**: Edit the `full_prompt` in `generate_fashion_image()` to change image style
2. **Adjust Models**: Change `model_name` in `load_model()` to use different language models
3. **Update UI**: Modify Streamlit components in the chat interface section

### Adding New Features

- **Multiple Image Generation**: Generate outfit variations
- **Style History**: Save and retrieve past recommendations
- **User Profiles**: Store preferences and measurements
- **Brand Integration**: Link to specific clothing items

## 🔒 Security & Privacy

- **Local Processing**: Fashion queries and text generation happen locally
- **API Security**: Only image descriptions are sent to ModelScope API
- **No Data Storage**: Conversations are not stored after session ends
- **Secure Configuration**: API keys stored in Streamlit secrets

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Write clean, commented code
- Follow Python PEP 8 standards
- Test your changes thoroughly
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

**Model Loading Errors**
```bash
# Solution: Ensure transformers is up to date
pip install --upgrade transformers
```

**CUDA Out of Memory**
```bash
# Solution: Use CPU-only mode or smaller model
# Edit model loading to remove device_map="auto"
```

**API Key Issues**
```bash
# Solution: Verify your ModelScope API key is correct
# Check .streamlit/secrets.toml for proper formatting
```

**Slow Performance**
```bash
# Solution: Ensure GPU is available
# Check torch.cuda.is_available() in Python
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Qwen Team**: For the excellent Qwen3 language model
- **ModelScope**: For providing the Flux image generation API
- **Streamlit**: For the amazing web framework
- **OpenAI**: For inspiration in conversational AI interfaces

## 📞 Contact

- **Project Maintainer**: [Chen Yiming](1345227885@qq.com)
- **School Email**: [@CHEN Yiming](yiming0011.chen@connect.polyu.hk)

---

<div align="center">

**Made with ❤️ for fashion enthusiasts and AI developers**

[⭐ Star this repo](https://github.com/yourusername/FashionAI) | [🍴 Fork this repo](https://github.com/yourusername/FashionAI/fork)

</div>