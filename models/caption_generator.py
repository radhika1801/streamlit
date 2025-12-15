from transformers import BlipProcessor, BlipForConditionalGeneration
import streamlit as st
import torch

class CaptionGenerator:
    def __init__(self):
        self.processor = None
        self.model = None
    
    @st.cache_resource
    def load_model(_self):
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        return processor, model
    
    def generate_caption(self, image, mode="unconditional"):
        if self.processor is None:
            self.processor, self.model = self.load_model()
        
        if mode == "unconditional":
            inputs = self.processor(image, return_tensors="pt")
            out = self.model.generate(**inputs, max_length=50)
        else:
            # Conditional captioning with custom prompt
            text = "a photography of"
            inputs = self.processor(image, text, return_tensors="pt")
            out = self.model.generate(**inputs, max_length=50)
        
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption