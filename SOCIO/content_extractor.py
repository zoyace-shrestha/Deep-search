import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import json
import re

class ContentExtractor:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

    def extract_content(self, url: str) -> Dict:
        """Extract content and return structured data"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        extracted_data = {
            'metadata': {
                'url': url,
                'title': self._get_title(soup),
                'timestamp': response.headers.get('date', '')
            },
            'content': self._get_content(soup),
            'media': {
                'images': self._get_images(soup, url)
            },
            'theme': self._get_theme(soup)
        }
        
        return extracted_data

    def _get_title(self, soup) -> str:
        return soup.title.text.strip() if soup.title else ''

    def _get_content(self, soup) -> Dict:
        return {
            'text_content': {
                'paragraphs': [p.text.strip() for p in soup.find_all('p') if p.text.strip()],
                'headings': [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3']) if h.text.strip()],
                'divs': [d.text.strip() for d in soup.find_all('div') if d.text.strip()]
            },
            'statistics': {
                'paragraph_count': len(soup.find_all('p')),
                'heading_count': len(soup.find_all(['h1', 'h2', 'h3'])),
                'div_count': len(soup.find_all('div'))
            }
        }

    def _get_images(self, soup, base_url: str) -> List[Dict]:
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if not src.startswith('http'):
                    src = f"{base_url.rstrip('/')}/{src.lstrip('/')}"
                images.append({
                    'url': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        return images

    def _get_theme(self, soup) -> Dict:
        """Extract theme-related information"""
        theme_data = {
            'colors': self._extract_colors(soup),
            'fonts': self._extract_fonts(soup),
            'layout': self._analyze_layout(soup),
            'style_elements': self._extract_style_elements(soup)
        }
        return theme_data

    def _extract_colors(self, soup) -> Dict:
        """Extract color scheme from the website"""
        colors = {
            'background_colors': set(),
            'text_colors': set(),
            'accent_colors': set()
        }
        
        # Extract colors from style tags
        for style in soup.find_all('style'):
            if style.string:
                # Find color values in CSS
                color_matches = re.findall(r'#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)', style.string)
                for color in color_matches:
                    colors['accent_colors'].add(color)

        # Extract inline styles
        for element in soup.find_all(style=True):
            style = element.get('style')
            if 'background' in style.lower():
                colors['background_colors'].add(style)
            if 'color:' in style.lower():
                colors['text_colors'].add(style)

        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in colors.items()}

    def _extract_fonts(self, soup) -> Dict:
        """Extract font information"""
        fonts = {
            'families': set(),
            'sizes': set()
        }
        
        # Check style tags
        for style in soup.find_all('style'):
            if style.string:
                # Find font-family declarations
                font_families = re.findall(r'font-family:\s*([^;}]+)', style.string)
                fonts['families'].update(font_families)
                
                # Find font-size declarations
                font_sizes = re.findall(r'font-size:\s*([^;}]+)', style.string)
                fonts['sizes'].update(font_sizes)

        # Check inline styles
        for element in soup.find_all(style=True):
            style = element.get('style')
            if 'font-family' in style:
                family = re.search(r'font-family:\s*([^;}]+)', style)
                if family:
                    fonts['families'].add(family.group(1))
            if 'font-size' in style:
                size = re.search(r'font-size:\s*([^;}]+)', style)
                if size:
                    fonts['sizes'].add(size.group(1))

        return {k: list(v) for k, v in fonts.items()}

    def _analyze_layout(self, soup) -> Dict:
        """Analyze website layout structure"""
        layout = {
            'has_header': bool(soup.find('header') or soup.find(class_=re.compile(r'header|nav|menu', re.I))),
            'has_footer': bool(soup.find('footer') or soup.find(class_=re.compile(r'footer', re.I))),
            'has_sidebar': bool(soup.find('sidebar') or soup.find(class_=re.compile(r'sidebar|side-nav', re.I))),
            'responsive_elements': bool(soup.find('meta', attrs={'name': 'viewport'})),
            'grid_system': bool(soup.find(class_=re.compile(r'grid|row|col|flex', re.I)))
        }
        return layout

    def _extract_style_elements(self, soup) -> Dict:
        """Extract common style elements"""
        elements = {
            'buttons': len(soup.find_all('button')) + len(soup.find_all(class_=re.compile(r'btn|button', re.I))),
            'forms': len(soup.find_all('form')),
            'links': len(soup.find_all('a')),
            'cards': len(soup.find_all(class_=re.compile(r'card', re.I))),
            'icons': len(soup.find_all('i')) + len(soup.find_all(class_=re.compile(r'icon|fa-|material-icons', re.I)))
        }
        return elements

    def get_structured_data(self, url: str) -> str:
        """Extract and return data as JSON string"""
        data = self.extract_content(url)
        return json.dumps(data, indent=2)


