import re
import emoji
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from langdetect import detect
from googletrans import Translator

class KleanTextProcessor:
    def __init__(self, remove_stopwords=True, spell_check=False, stemming=False, lemmatization=True,
                 custom_stopwords=None, case_sensitive=False, detect_language=False, target_language="en"):
        self.remove_stopwords = remove_stopwords
        self.spell_check = spell_check
        self.stemming = stemming
        self.lemmatization = lemmatization
        self.stop_words = set(stopwords.words("english"))
        if custom_stopwords:
            self.stop_words.update(custom_stopwords)
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.case_sensitive = case_sensitive
        self.detect_language = detect_language
        self.target_language = target_language
        self.translator = Translator()

    def preprocess(self, text):
        """Cleans and preprocesses text."""
        if not isinstance(text, str):
            return ""
        
        if not self.case_sensitive:
            text = text.lower()

        text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
        text = re.sub(r"\d+", "", text)  # Remove numbers
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
        text = emoji.demojize(text)  # Convert emojis to text
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces

        if self.remove_stopwords:
            text = " ".join([word for word in text.split() if word not in self.stop_words])

        if self.stemming:
            text = " ".join([self.stemmer.stem(word) for word in text.split()])

        if self.lemmatization:
            text = " ".join([self.lemmatizer.lemmatize(word) for word in text.split()])

        if self.spell_check:
            text = str(TextBlob(text).correct())

        if self.detect_language:
            lang = detect(text)
            if lang != self.target_language:
                text = self.translator.translate(text, src=lang, dest=self.target_language).text

        return text
