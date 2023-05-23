import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import web_scraper


class SentimentAnalysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "ProsusAI/finBERT")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "ProsusAI/finBERT")

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

            # Scale probability to be more polarizing; for probabilities above 0.5, scale up, and for those below, scale down.
            # This way, articles that elicit a stronger opinion from the model will contribute more to the average.
            # We can play around with this / how we weight the average.
            # temp_prob = max(pos_prob, 1 - pos_prob)
            # weight = temp_prob / 0.5
            # if pos_prob < 0.5:
            #     pos_prob = pos_prob / weight
            # else:
            #     pos_prob = min(1, pos_prob * weight)

            if pos_prob > .5:
                pos_prob = min(1, 2-(1-pos_prob)**2)

            predictions.append(pos_prob)

        # Check if predictions list is not empty
        if len(predictions) > 0:
            avg_pred = sum(predictions) / len(predictions)
        else:
            avg_pred = 0 

        return avg_pred
