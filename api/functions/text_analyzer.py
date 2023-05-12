from textblob import TextBlob

def analyzeText(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    # Text type
    text_type = "neutral"

    if sentiment > 0:
        text_type = "positive"
    elif sentiment < 0:
        text_type = "negative"
    
    return {
        "sentiment": sentiment,
        "text_type": text_type
    }