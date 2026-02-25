import os
import json
import torch
import numpy as np
from transformers import RobertaForSequenceClassification, RobertaTokenizer
import logging

logger = logging.getLogger(__name__)

class JokeModel:
    def __init__(self, artifacts_dir='artifacts'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.artifacts_dir = artifacts_dir
        self.model = None
        self.tokenizer = None
        self.loaded = False
        
        self.load_model()
    
    def load_model(self):
        """Load the trained model and tokenizer"""
        try:
            model_path = os.path.join(self.artifacts_dir, 'best_model.pth')
            
            if not os.path.exists(model_path):
                logger.warning("Model file not found")
                return False
            
            # Load tokenizer
            tokenizer_path = os.path.join(self.artifacts_dir, 'tokenizer')
            if os.path.exists(tokenizer_path):
                self.tokenizer = RobertaTokenizer.from_pretrained(tokenizer_path)
            else:
                self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
            
            # Load model config
            config_path = os.path.join(self.artifacts_dir, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                num_labels = config.get('num_labels', 1)
            else:
                num_labels = 1
            
            # Initialize model
            self.model = RobertaForSequenceClassification.from_pretrained(
                'roberta-base',
                num_labels=num_labels
            )
            
            # Load weights
            state_dict = torch.load(model_path, map_location=self.device)
            if 'model_state_dict' in state_dict:
                state_dict = state_dict['model_state_dict']
            
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            self.loaded = True
            logger.info(f"Model loaded on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def predict(self, joke_text):
        """Make prediction for a single joke"""
        if not self.loaded:
            return None
        
        try:
            inputs = self.tokenizer(
                joke_text,
                truncation=True,
                padding='max_length',
                max_length=128,
                return_tensors='pt'
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Convert to score
            if logits.shape[1] == 1:
                score = torch.sigmoid(logits).item() * 100
            else:
                probs = torch.softmax(logits, dim=1)
                score = probs[0][1].item() * 100 if probs.shape[1] > 1 else probs[0][0].item() * 100
            
            return max(0, min(100, score))
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return None
    
    def batch_predict(self, jokes):
        """Predict for multiple jokes"""
        return [self.predict(joke) for joke in jokes]