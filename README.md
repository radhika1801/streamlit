# Create README.md file
cat > README.md << 'EOF'
# Vision Studio

An AI-powered image analysis platform combining multiple state-of-the-art computer vision models.

## Features

- **Image Classification** using Vision Transformer (ViT)
- **Caption Generation** using BLIP
- **Style Analysis** using CLIP

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Technologies

- Streamlit
- Hugging Face Transformers
- PyTorch
- Plotly

## Models

- Vision Transformer (google/vit-base-patch16-224)
- BLIP (Salesforce/blip-image-captioning-base)
- CLIP (openai/clip-vit-base-patch32)
EOF

# Add it to git
git add README.md

# Commit
git commit -m "Add README"

# Push
git push origin main