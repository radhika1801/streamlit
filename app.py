import streamlit as st
from PIL import Image
import io
import json
from datetime import datetime

from models.image_classifier import ImageClassifier
from models.caption_generator import CaptionGenerator
from models.style_analyzer import StyleAnalyzer
from utils.visualization import plot_predictions, plot_comparison, create_confidence_gauge

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
    
    /* Input fields */
    .stTextArea textarea {
        border: 1px solid #e0e0e0;
        border-radius: 0;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        padding: 1rem;
        background: #fafafa;
    }
    
    .stTextArea textarea:focus {
        border-color: #a0a0a0;
        background: #ffffff;
        box-shadow: 0 0 0 1px #a0a0a0;
    }
    
    /* Sliders */
    .stSlider {
        padding: 1rem 0;
    }
    
    /* Checkboxes */
    .stCheckbox {
        padding: 0.5rem 0;
    }
    
    .stCheckbox label {
        font-size: 0.95rem;
        font-weight: 300;
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
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #0a0a0a !important;
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
    
    /* Status */
    .stStatus {
        background: #fafafa;
        border-left: 2px solid #0a0a0a;
    }
    
    /* Select box */
    .stSelectbox {
        font-family: 'Outfit', sans-serif;
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
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Initialize models
@st.cache_resource
def initialize_models():
    return {
        'classifier': ImageClassifier(),
        'captioner': CaptionGenerator(),
        'style_analyzer': StyleAnalyzer()
    }

models = initialize_models()

# Sidebar
with st.sidebar:
    st.markdown("# Vision Studio")
    st.markdown("---")
    
    st.markdown("### Analysis Options")
    
    run_classification = st.checkbox("Image Classification", value=True)
    run_captioning = st.checkbox("Caption Generation", value=True)
    run_style = st.checkbox("Style Analysis", value=True)
    
    if run_style:
        st.markdown("**Style Categories**")
        default_styles = "portrait, landscape, abstract, documentary, street photography, nature, urban, minimalist"
        style_input = st.text_area(
            "Comma-separated styles",
            value=default_styles,
            height=100,
            label_visibility="collapsed"
        )
        style_labels = [s.strip() for s in style_input.split(',')]
    
    st.markdown("---")
    
    st.markdown("### Settings")
    top_k = st.slider("Number of predictions", 3, 10, 5)
    confidence_threshold = st.slider("Confidence threshold", 0.0, 1.0, 0.1, 0.05)
    
    st.markdown("---")
    
    if st.session_state.analysis_history:
        if st.button("Clear History"):
            st.session_state.analysis_history = []
            st.rerun()

# Main content
st.markdown("# Vision Studio")
st.markdown('<p class="subtitle">AI-powered image analysis platform</p>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Upload", "Results", "History"])

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
            st.markdown("### Analysis")
            st.markdown("")
            
            if st.button("Run Analysis"):
                results = {}
                
                with st.spinner("Processing image..."):
                    # Classification
                    if run_classification:
                        with st.status("Classifying image", expanded=False):
                            predictions = models['classifier'].classify(image, top_k=top_k)
                            predictions = [p for p in predictions if p['score'] >= confidence_threshold]
                            results['classification'] = predictions
                    
                    # Captioning
                    if run_captioning:
                        with st.status("Generating captions", expanded=False):
                            caption_uncond = models['captioner'].generate_caption(image, "unconditional")
                            caption_cond = models['captioner'].generate_caption(image, "conditional")
                            results['captions'] = {
                                'general': caption_uncond,
                                'photography': caption_cond
                            }
                    
                    # Style Analysis
                    if run_style:
                        with st.status("Analyzing style", expanded=False):
                            style_results = models['style_analyzer'].analyze_style(image, style_labels)
                            style_results = [s for s in style_results if s['score'] >= confidence_threshold]
                            results['style'] = style_results
                
                # Store in session state
                st.session_state.current_results = results
                st.session_state.current_image = image
                
                # Add to history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'filename': uploaded_file.name,
                    'results': results
                })
                
                st.success("Analysis complete")
                st.rerun()
        else:
            st.markdown("### Analysis")
            st.info("Upload an image to begin")

with tab2:
    if 'current_results' in st.session_state:
        results = st.session_state.current_results
        
        # Classification
        if 'classification' in results and results['classification']:
            st.markdown("## Classification")
            
            col1, col2 = st.columns([2.5, 1], gap="large")
            
            with col1:
                fig = plot_predictions(results['classification'], "")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                top_pred = results['classification'][0]
                st.markdown("**Primary Category**")
                st.metric(
                    label=top_pred['label'].replace('_', ' ').title(),
                    value=f"{top_pred['score']:.1%}"
                )
        
        st.markdown("---")
        
        # Captions
        if 'captions' in results:
            st.markdown("## Generated Captions")
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("**General Description**")
                st.markdown(f"*{results['captions']['general']}*")
            
            with col2:
                st.markdown("**Photography Context**")
                st.markdown(f"*{results['captions']['photography']}*")
        
        st.markdown("---")
        
        # Style
        if 'style' in results and results['style']:
            st.markdown("## Style Analysis")
            fig = plot_predictions(results['style'], "")
            st.plotly_chart(fig, use_container_width=True)
        
        # Download
        st.markdown("---")
        st.markdown("### Export Results")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="analysis.json",
                mime="application/json"
            )
        
        with col2:
            summary = f"""VISION STUDIO
Analysis Report
{"="*60}

Classification
{"-"*60}
Primary: {results.get('classification', [{}])[0].get('label', 'N/A')}
Confidence: {results.get('classification', [{}])[0].get('score', 0):.2%}

Caption
{"-"*60}
{results.get('captions', {}).get('general', 'N/A')}

Style
{"-"*60}
Primary: {results.get('style', [{}])[0].get('label', 'N/A')}
"""
            
            st.download_button(
                label="Download Report",
                data=summary,
                file_name="report.txt",
                mime="text/plain"
            )
    else:
        st.info("No results available. Upload and analyze an image to view results.")

with tab3:
    st.markdown("## Analysis History")
    
    if st.session_state.analysis_history:
        for idx, entry in enumerate(reversed(st.session_state.analysis_history)):
            with st.expander(f"{entry['filename']} — {entry['timestamp']}"):
                cols = st.columns(3)
                
                if 'classification' in entry['results'] and entry['results']['classification']:
                    with cols[0]:
                        st.markdown("**Classification**")
                        st.write(entry['results']['classification'][0]['label'].replace('_', ' ').title())
                
                if 'captions' in entry['results']:
                    with cols[1]:
                        st.markdown("**Caption**")
                        caption = entry['results']['captions']['general']
                        st.write(caption[:60] + "..." if len(caption) > 60 else caption)
                
                if 'style' in entry['results'] and entry['results']['style']:
                    with cols[2]:
                        st.markdown("**Style**")
                        st.write(entry['results']['style'][0]['label'].title())
    else:
        st.info("No analysis history available")
