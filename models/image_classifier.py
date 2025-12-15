from transformers import pipeline
import streamlit as st

class ImageClassifier:
    def __init__(self):
        self.model = None
    
    @st.cache_resource
    def load_model(_self):
        return pipeline("image-classification", 
                       model="google/vit-base-patch16-224")
    
    def classify(self, image, top_k=5):
        if self.model is None:
            self.model = self.load_model()
        
        predictions = self.model(image)
        return predictions[:top_k]