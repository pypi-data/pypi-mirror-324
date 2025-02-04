from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import re

def summarize_text(text, model_name="t5-small", max_length=50, min_length=25, cache_dir="./model_cache"):
    """Summarize long texts."""
    summarizer = pipeline("summarization", model=model_name, cache_dir=cache_dir)
    summary = summarizer(text, max_length=max_length, min_length=min_length, truncation=True)
    return summary[0]["summary_text"]

def named_entity_recognition(text, model_name="dbmdz/bert-large-cased-finetuned-conll03-english", cache_dir="./model_cache"):
    """Perform NER on a given text."""
    ner_pipeline = pipeline("ner", model=model_name, cache_dir=cache_dir, grouped_entities=True)
    return ner_pipeline(text)

def text_generation(prompt, model_name="gpt2", max_length=50, cache_dir="./model_cache"):
    """Generate text from a given prompt using GPT-2."""
    tokenizer = GPT2Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    model = GPT2LMHeadModel.from_pretrained(model_name, cache_dir=cache_dir)
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, do_sample=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def sentiment_analysis(text, model_name="nlptown/bert-base-multilingual-uncased-sentiment", cache_dir="./model_cache"):
    """Perform sentiment analysis on a given text."""
    sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, cache_dir=cache_dir)
    return sentiment_pipeline(text)

def remove_stopwords(text, stopwords=None):
    """Remove stopwords from text."""
    if stopwords is None:
        stopwords = {"and", "or", "but", "so", "the", "a", "an", "of", "in", "on"}
    return " ".join([word for word in text.split() if word.lower() not in stopwords])

def word_frequency_analysis(text):
    """Calculate word frequency in a text."""
    words = re.findall(r'\b\w+\b', text.lower())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
