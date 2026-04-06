#!/usr/bin/env python3
"""
CSS Minification Script
Removes comments, extra whitespace, and optimizes CSS
"""

import re

def minify_css(css_content):
    """Minify CSS by removing comments and unnecessary whitespace"""
    
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove newlines
    css_content = css_content.replace('\n', '')
    
    # Remove excessive whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Remove spaces around certain characters
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)
    
    # Remove trailing semicolons before }
    css_content = re.sub(r';}', '}', css_content)
    
    return css_content.strip()

def main():
    input_file = "styles.css"
    output_file = "styles-optimized.css"
    
    print("=" * 60)
    print("CSS Minification")
    print("=" * 60)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_css = f.read()
        
        original_size = len(original_css)
        print(f"Original size: {original_size:,} bytes ({original_size/1024:.2f} KB)")
        
        minified_css = minify_css(original_css)
        
        # Update Google Fonts import to include font-display=swap
        minified_css = re.sub(
            r"@import url\('https://fonts\.googleapis\.com/css2\?family=Inter[^']+'\);",
            "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');",
            minified_css
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        minified_size = len(minified_css)
        savings = ((original_size - minified_size) / original_size) * 100
        
        print(f"Minified size: {minified_size:,} bytes ({minified_size/1024:.2f} KB)")
        print(f"Savings: {savings:.1f}% ({(original_size - minified_size):,} bytes)")
        print(f"\n✓ CSS minified successfully → {output_file}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
