from transformers import CLIPProcessor, CLIPModel
import streamlit as st
import torch

class StyleAnalyzer:
    def __init__(self):
        self.processor = None
        self.model = None
    
    @st.cache_resource
    def load_model(_self):
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        return processor, model
    
    def analyze_style(self, image, style_labels):
        if self.processor is None:
            self.processor, self.model = self.load_model()
        
        inputs = self.processor(
            text=style_labels,
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        
        results = []
        for label, prob in zip(style_labels, probs[0]):
            results.append({
                'label': label,
                'score': prob.item()
            })
        
        return sorted(results, key=lambda x: x['score'], reverse=True)