import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import web_scraper


class SentimentAnalysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "assemblyai/distilbert-base-uncased-sst2"
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "assemblyai/distilbert-base-uncased-sst2"
        )

    def getPrediction(self, text):
        tokenized_segments = self.tokenizer(
            [text],
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        tokenized_segments_input_ids, tokenized_segments_attention_mask = (
            tokenized_segments.input_ids,
            tokenized_segments.attention_mask,
        )
        model_predictions = F.softmax(
            self.model(
                input_ids=tokenized_segments_input_ids,
                attention_mask=tokenized_segments_attention_mask,
            )["logits"],
            dim=1,
        )
        return model_predictions[0]

    def getSentiment(self, company_name):
        headlines = web_scraper.get_headlines(company_name)
        predictions = []

        for i in range(len(headlines)):
            text = headlines[i]
            pred = self.getPrediction(text)
            pos_prob = pred[1].item()
            predictions.append(pos_prob)

        avg_pred = sum(predictions) / len(predictions)

        return avg_pred
