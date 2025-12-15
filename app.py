import streamlit as st
from PIL import Image
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Vision Studio",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional custom CSS - Remove ALL Streamlit branding
st.markdown("""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500;600&family=Space+Mono:wght@400;700&display=swap');
    
    /* Remove Streamlit branding completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Global styles */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem 3rem;
    }
    
    /* Typography */
    h1 {
        font-family: 'Outfit', sans-serif;
        font-weight: 200;
        font-size: 3rem;
        letter-spacing: -2px;
        color: #0a0a0a;
        margin-bottom: 0.3rem;
    }
    
    h2 {
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
        font-size: 1.8rem;
        letter-spacing: -1px;
        color: #2a2a2a;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #e8e8e8;
        padding-bottom: 0.8rem;
    }
    
    h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        letter-spacing: -0.3px;
        color: #3a3a3a;
        margin-bottom: 1rem;
    }
    
    p, div, span, label {
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
        color: #4a4a4a;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.1rem;
        color: #6a6a6a;
        font-weight: 300;
        letter-spacing: 0.3px;
        margin-bottom: 3rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e0e0;
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8a8a8a;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0a0a0a 0%, #2a2a2a 100%);
        color: #ffffff;
        height: 3.5rem;
        border-radius: 0;
        border: none;
        font-family: 'Space Mono', monospace;
        font-weight: 400;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a2a2a 0%, #4a4a4a 100%);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background: transparent;
        border: 1px solid #d0d0d0;
        color: #4a4a4a;
        height: 2.8rem;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    .stDownloadButton>button:hover {
        background: #f5f5f5;
        border-color: #a0a0a0;
        box-shadow: none;
        transform: none;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 3rem;
        border-bottom: 1px solid #e0e0e0;
        padding: 0 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1.2rem 0;
        font-family: 'Space Mono', monospace;
        font-weight: 400;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #9a9a9a;
        border: none;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0a0a0a;
        border-bottom: 2px solid #0a0a0a;
        font-weight: 700;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #d0d0d0;
        border-radius: 0;
        padding: 3rem;
        background: #fafafa;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #a0a0a0;
        background: #ffffff;
    }
    
    [data-testid="stFileUploader"] section {
        border: none;
        padding: 0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 200;
        color: #0a0a0a;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8a8a8a;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 0;
        border-left: 3px solid #0a0a0a;
        background: #f8f8f8;
        padding: 1rem 1.5rem;
        font-size: 0.95rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #4a4a4a;
        background: #fafafa;
        border: 1px solid #e8e8e8;
        border-radius: 0;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f0f0f0;
    }
    
    /* Divider */
    hr {
        margin: 3rem 0;
        border: none;
        border-top: 1px solid #e8e8e8;
    }
    
    /* Images */
    img {
        border: 1px solid #e8e8e8;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
    }
    
    /* Column gaps */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* Remove padding from main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f0f0f0;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c0c0c0;
        border-radius: 0;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a0a0a0;
    }
    
    /* Demo badge */
    .demo-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: #fff3cd;
        border-left: 3px solid #ffc107;
        margin: 1rem 0;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Sidebar
with st.sidebar:
    st.markdown("# Vision Studio")
    st.markdown("---")
    
    st.markdown('<div class="demo-badge">DEMO VERSION</div>', unsafe_allow_html=True)
    
    st.markdown("### About")
    st.write("""
    This is a lightweight demonstration of Vision Studio. The full version with AI models runs locally.
    """)
    
    st.markdown("---")
    
    st.markdown("### Full Version Features")
    st.write("""
    - Vision Transformer (ViT) Classification
    - BLIP Caption Generation  
    - CLIP Style Analysis
    - Multi-model Predictions
    - Export Results
    """)
    
    st.markdown("---")
    
    st.markdown("### Run Locally")
    st.code("""
git clone https://github.com/
radhika1801/streamlit.git
cd streamlit
pip install transformers torch
streamlit run app_full.py
    """)

# Main content
st.markdown("# Vision Studio")
st.markdown('<p class="subtitle">AI-powered image analysis platform</p>', unsafe_allow_html=True)

st.info("🚀 **Demo Version** - This lightweight version showcases the interface design. The full version with Vision Transformer, BLIP, and CLIP models requires GPU resources and runs locally.")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Upload", "Demo Results", "About"])

with tab1:
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("### Upload Image")
        uploaded_file = st.file_uploader(
            "Drop image here or click to browse",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            # Image metadata
            with st.expander("Image Information"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Format", image.format)
                with col_b:
                    st.metric("Width", f"{image.size[0]}px")
                with col_c:
                    st.metric("Height", f"{image.size[1]}px")
    
    with col2:
        if uploaded_file:
            st.markdown("### Demo Analysis")
            st.markdown("")
            
            if st.button("Run Demo Analysis"):
                with st.spinner("Processing image..."):
                    import time
                    time.sleep(2)  # Simulate AI processing
                    
                    # Store demo results
                    st.session_state.demo_results = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'filename': uploaded_file.name,
                        'width': image.size[0],
                        'height': image.size[1]
                    }
                
                st.success("Demo analysis complete")
                st.info("View results in the 'Demo Results' tab")
        else:
            st.markdown("### Demo Analysis")
            st.info("Upload an image to begin")

with tab2:
    if 'demo_results' in st.session_state:
        st.markdown("## Demo Analysis Results")
        
        st.markdown(f"**File**: {st.session_state.demo_results['filename']}")
        st.markdown(f"**Analyzed**: {st.session_state.demo_results['timestamp']}")
        
        st.markdown("---")
        
        # Classification Demo
        st.markdown("## Classification")
        
        col1, col2 = st.columns([2.5, 1], gap="large")
        
        with col1:
            st.markdown("**Top Predictions** (Demo Data)")
            
            demo_predictions = [
                ("Portrait Photography", 0.87),
                ("Professional Photography", 0.76),
                ("Natural Lighting", 0.68),
                ("Studio Portrait", 0.54),
                ("Documentary Style", 0.42)
            ]
            
            for label, score in demo_predictions:
                col_label, col_bar = st.columns([1, 3])
                with col_label:
                    st.write(label)
                with col_bar:
                    st.progress(score)
                    st.caption(f"{score:.1%}")
        
        with col2:
            st.markdown("**Primary Category**")
            st.metric(
                label="Portrait Photography",
                value="87.3%"
            )
        
        st.markdown("---")
        
        # Captions Demo
        st.markdown("## Generated Captions")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("**General Description**")
            st.markdown("_A professional portrait photograph captured with natural lighting and careful composition_")
        
        with col2:
            st.markdown("**Photography Context**")
            st.markdown("_A portrait of a person in natural lighting with professional composition and depth of field_")
        
        st.markdown("---")
        
        # Style Analysis Demo
        st.markdown("## Style Analysis")
        
        demo_styles = [
            ("Portrait", 0.89),
            ("Professional", 0.82),
            ("Natural", 0.75),
            ("Documentary", 0.61),
            ("Minimalist", 0.48)
        ]
        
        for label, score in demo_styles:
            col_label, col_bar = st.columns([1, 3])
            with col_label:
                st.write(label)
            with col_bar:
                st.progress(score)
                st.caption(f"{score:.1%}")
        
        # Download Demo
        st.markdown("---")
        st.markdown("### Export Demo Results")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            demo_json = json.dumps({
                "classification": [{"label": l, "score": s} for l, s in demo_predictions],
                "captions": {
                    "general": "A professional portrait photograph",
                    "photography": "A portrait with natural lighting"
                },
                "style": [{"label": l, "score": s} for l, s in demo_styles]
            }, indent=2)
            
            st.download_button(
                label="Download JSON",
                data=demo_json,
                file_name="demo_analysis.json",
                mime="application/json"
            )
        
        with col2:
            summary = f"""VISION STUDIO - DEMO RESULTS
Analysis Report
{"="*60}

File: {st.session_state.demo_results['filename']}
Date: {st.session_state.demo_results['timestamp']}

Classification
{"-"*60}
Primary: Portrait Photography
Confidence: 87.3%

Caption
{"-"*60}
A professional portrait photograph captured with natural lighting

Top Style
{"-"*60}
Portrait (89.0%)
"""
            
            st.download_button(
                label="Download Report",
                data=summary,
                file_name="demo_report.txt",
                mime="text/plain"
            )
    else:
        st.info("Upload and analyze an image in the 'Upload' tab to see demo results here")

with tab3:
    st.markdown("## About Vision Studio")
    
    st.markdown("""
    Vision Studio is an AI-powered image analysis platform that combines multiple state-of-the-art computer vision models for comprehensive image understanding.
    
    ### Architecture
    
    The full version integrates three powerful AI models:
    
    **1. Vision Transformer (ViT)**
    - Model: `google/vit-base-patch16-224`
    - Task: Image classification
    - Dataset: ImageNet-21k (14M images)
    - Parameters: 86M
    
    **2. BLIP (Bootstrapping Language-Image Pre-training)**
    - Model: `Salesforce/blip-image-captioning-base`
    - Task: Image-to-text generation
    - Dataset: COCO Captions
    - Parameters: 14M
    
    **3. CLIP (Contrastive Language-Image Pre-training)**
    - Model: `openai/clip-vit-base-patch32`
    - Task: Zero-shot style classification
    - Dataset: 400M image-text pairs
    - Use: Flexible semantic understanding
    """)
    
    st.markdown("---")
    
    st.markdown("## Technical Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Frontend**
        - Streamlit
        - Custom CSS/HTML
        - Plotly (visualizations)
        
        **Backend**
        - Python 3.9+
        - PyTorch
        - Hugging Face Transformers
        """)
    
    with col2:
        st.markdown("""
        **Models**
        - Vision Transformer (ViT)
        - BLIP
        - CLIP
        
        **Deployment**
        - Streamlit Cloud (Demo)
        - Local GPU (Full version)
        """)
    
    st.markdown("---")
    
    st.markdown("## Run Full Version Locally")
    
    st.markdown("""
    The full version with all AI models requires:
    - **RAM**: 4GB+ 
    - **Storage**: 2GB for model downloads
    - **Python**: 3.9 or higher
    - **GPU**: Optional but recommended
    """)
    
    st.code("""
# Clone repository
git clone https://github.com/radhika1801/streamlit.git
cd streamlit

# Install dependencies  
pip install streamlit transformers torch pillow plotly pandas

# Run full version
streamlit run app_full.py
    """, language="bash")
    
    st.markdown("---")
    
    st.markdown("## Why This Demo Version?")
    
    st.info("""
    **Streamlit Cloud Free Tier Limitations:**
    - Limited RAM (1GB)
    - Limited storage
    - CPU-only (no GPU)
    
    The AI models used in Vision Studio require ~2GB just to download, plus significant compute resources for inference. This demo showcases the interface design and user experience, while the full functionality is available when running locally with adequate resources.
    """)
    
    st.markdown("---")
    
    st.markdown("## Project Context")
    
    st.markdown("""
    **Course**: Design & Technology  
    **Institution**: Parsons School of Design  
    **Year**: 2024
    
    This project explores the intersection of:
    - Computer vision and deep learning
    - Human-AI interaction design
    - Multi-modal analysis systems
    - Professional interface development
    """)
    
    st.markdown("---")
    
    st.markdown("## Links")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("[GitHub Repository](https://github.com/radhika1801/streamlit)")
    
    with col2:
        st.markdown("[GitHub Pages](https://radhika1801.github.io/streamlit/)")
    
    with col3:
        st.markdown("[Parsons Design & Tech](https://www.newschool.edu/parsons/)")

