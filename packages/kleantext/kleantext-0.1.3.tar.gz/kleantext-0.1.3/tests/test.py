import unittest
from kleantext import TextPreprocessor  # Updated import

class TestKleanTextProcessor(unittest.TestCase):
    def setUp(self):
        """Initialize the TextPreprocessor instance before each test."""
        self.processor = TextPreprocessor(
            remove_stopwords=False,
            use_stemming=False,
            use_lemmatization=True,
            case_sensitive=False,
            detect_language=False,
            perform_spellcheck=False
        )
    
    def test_basic_preprocessing(self):
        """Test basic text preprocessing."""
        text = "This is an example! Visit https://example.com"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "this is an example visit", "Basic text preprocessing failed.")
    
    def test_special_character_removal(self):
        """Test special character and punctuation removal."""
        text = "Hello!!! This... is, amazing? Right: @#test"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "hello this is amazing right test", "Special character removal failed.")
    
    def test_number_removal(self):
        """Test number removal from text."""
        text = "The price is 100 dollars for 2 items."
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "the price is dollars for items", "Number removal failed.")
    
    def test_stopword_removal(self):
        """Test stopword removal."""
        self.processor.remove_stopwords = True
        text = "This is an example sentence with stopwords."
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "example sentence stopwords", "Stopword removal failed.")
    
    def test_empty_input(self):
        """Test preprocessing with empty input."""
        text = ""
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "", "Preprocessing failed for empty input.")
    
    def test_url_removal(self):
        """Test preprocessing when text contains only URLs."""
        text = "https://example.com https://test.com"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "", "URL removal failed.")
    
    def test_emoji_handling(self):
        """Test emoji conversion to text."""
        text = "I love Python! 😍🔥"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "i love python heart_eyes fire", "Emoji conversion failed.")
    
    def test_ner_masking(self):
        """Test Named Entity Recognition (NER) masking."""
        text = "Barack Obama was the 44th President of the USA."
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "[PERSON] was the 44th president of the [LOCATION]", "NER masking failed.")
    
    def test_profanity_filtering(self):
        """Test profanity filtering."""
        text = "This is a f***ing bad idea!"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "this is a **** bad idea", "Profanity filtering failed.")
    
    def test_translation(self):
        """Test language detection and translation."""
        self.processor.detect_language = True
        self.processor.target_language = "en"
        text = "Bonjour tout le monde"
        cleaned = self.processor.clean_text(text)
        self.assertEqual(cleaned, "hello everyone", "Translation failed.")

if __name__ == "__main__":
    unittest.main()
