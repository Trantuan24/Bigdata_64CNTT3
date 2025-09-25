#!/usr/bin/env python3
import re
import os
import sys

class VietnameseTextCleaner:
    def __init__(self):
        # Vietnamese stopwords
        self.stopwords = {'và', 'của', 'trong', 'với', 'là', 'có', 'được', 'này', 'đó', 'các', 'một', 'để', 'cho', 'từ', 'về', 'theo', 'như', 'khi', 'đã', 'sẽ', 'không', 'còn', 'đang', 'bị', 'hay', 'hoặc', 'nhưng', 'mà', 'nếu', 'thì', 'vì', 'do', 'nên', 'tại', 'trên', 'dưới', 'giữa', 'sau', 'trước', 'bên', 'cạnh', 'gần', 'xa', 'nhiều', 'ít', 'lớn', 'nhỏ', 'cao', 'thấp', 'mới', 'cũ', 'tốt', 'xấu', 'đẹp'}
        
        # Pattern để remove
        self.html_pattern = re.compile(r'<[^>]+>')
        self.url_pattern = re.compile(r'http[s]?://[^\s]+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.number_pattern = re.compile(r'\b\d+\b')
        self.punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~""''…–—'
    
    def clean_text(self, text, remove_numbers=False, remove_stopwords=False, min_word_length=2):
        """Pipeline làm sạch text"""
        print("🧹 Cleaning text...")
        original_words = len(text.split())
        
        # Clean pipeline
        text = self.html_pattern.sub('', text)
        text = self.url_pattern.sub('', text)
        text = self.email_pattern.sub('', text)
        if remove_numbers:
            text = self.number_pattern.sub('', text)
        text = text.translate(str.maketrans('', '', self.punctuation))
        text = re.sub(r'\s+', ' ', text).strip().lower()
        
        words = [word for word in text.split() if len(word) >= min_word_length]
        if remove_stopwords:
            words = [word for word in words if word not in self.stopwords]
        
        text = ' '.join(words)
        final_words = len(words)
        print(f"📊 {original_words:,} → {final_words:,} words ({((original_words - final_words) / original_words * 100):.1f}% reduction)")
        
        return text
    
    
    def save_cleaned_text(self, text, output_file):
        """Lưu text đã clean"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"✅ Saved: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    raw_file = os.path.join(data_dir, 'raw_article.txt')
    cleaned_file = os.path.join(data_dir, 'cleaned_article.txt')
    
    if not os.path.exists(raw_file):
        print(f"❌ File not found. Run crawler.py first!")
        sys.exit(1)
    
    try:
        with open(raw_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        print(f"📖 Read: {raw_file}")
        
        cleaner = VietnameseTextCleaner()
        cleaned_text = cleaner.clean_text(raw_text)
        
        with open(cleaned_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"✅ Saved: {cleaned_file}")
        print(f"🎉 Ready for MapReduce!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
