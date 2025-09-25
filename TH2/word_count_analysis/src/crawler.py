#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os
import sys

class VnExpressCrawler:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.base_url = "https://vnexpress.net"
    
    def get_latest_tech_article(self):
        try:
            response = requests.get("https://vnexpress.net/khoa-hoc", headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_links = soup.find_all('h3', class_='title-news') or soup.find_all('h2', class_='title-news')
            if article_links:
                first_article = article_links[0].find('a')
                if first_article and first_article.get('href'):
                    url = first_article['href']
                    return url if url.startswith('http') else self.base_url + url
        except Exception as e:
            print(f"Error: {e}")
        
        return "https://vnexpress.net/ai-co-the-thay-the-con-nguoi-trong-nhung-cong-viec-nao-4693847.html"
    
    def crawl_article(self, url):
        """Crawl nội dung bài báo từ URL"""
        try:
            print(f"Đang crawl: {url}")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Lấy tiêu đề
            title = soup.find('h1', class_='title-detail') or soup.find('h1')
            title = title.get_text().strip() if title else "No title"
            
            # Lấy mô tả
            desc = soup.find('p', class_='description')
            description = desc.get_text().strip() if desc else ""
            
            # Lấy nội dung
            content_parts = []
            selectors = ['article.fck_detail', 'div.fck_detail', 'div#article_content', 'div.Normal']
            
            for selector in selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    for elem in content_div.find_all(['p', 'div', 'span']):
                        text = elem.get_text().strip()
                        if text and len(text) > 20:
                            content_parts.append(text)
                    break
            
            # Fallback: lấy từ body
            if len(' '.join(content_parts).split()) < 200:
                body_text = soup.find('body')
                if body_text:
                    lines = [line.strip() for line in body_text.get_text().split('\n') if len(line.strip()) > 30]
                    content_parts.extend(lines[:50])
            
            content = '\n'.join(content_parts)
            full_text = f"{title}\n\n{description}\n\n{content}"
            
            metadata = {'url': url, 'title': title, 'word_count': len(full_text.split()), 'char_count': len(full_text)}
            
            return full_text, metadata
            
        except Exception as e:
            print(f"Lỗi crawl: {e}")
            return None, None
    
    def save_article(self, text, metadata, data_dir):
        """Lưu bài báo và metadata"""
        try:
            with open(os.path.join(data_dir, 'raw_article.txt'), 'w', encoding='utf-8') as f:
                f.write(text)
            
            with open(os.path.join(data_dir, 'article_metadata.json'), 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Crawl thành công: {metadata['word_count']:,} từ, {metadata['char_count']:,} ký tự")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi lưu file: {e}")
            return False

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    crawler = VnExpressCrawler()
    
    text, metadata = crawler.crawl_article(crawler.get_latest_tech_article())
    
    if text and metadata:
        crawler.save_article(text, metadata, data_dir)
        print(f"\n🎉 Crawl thành công! Sẵn sàng cho bước tiếp theo.")
    else:
        print("❌ Crawl thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main()
