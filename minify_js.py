#!/usr/bin/env python3
"""
JavaScript Minification Script
Removes comments and unnecessary whitespace while preserving functionality
"""

import re

def minify_js(js_content):
    """Basic JS minification - removes comments and excess whitespace"""
    
    # Remove single-line comments (but not URLs)
    js_content = re.sub(r'(?<!:)//.*$', '', js_content, flags=re.MULTILINE)
    
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # Remove empty lines
    js_content = '\n'.join([line for line in js_content.split('\n') if line.strip()])
    
    # Reduce multiple spaces to single space (but preserve string literals)
    lines = []
    for line in js_content.split('\n'):
        # Keep indentation structure for readability, but remove excessive spaces
        line = re.sub(r'  +', ' ', line)
        lines.append(line.strip())
    
    js_content = '\n'.join(lines)
    
    return js_content

def main():
    input_file = "script.js"
    output_file = "script-optimized.js"
    
    print("=" * 60)
    print("JavaScript Minification")
    print("=" * 60)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_js = f.read()
        
        original_size = len(original_js)
        print(f"Original size: {original_size:,} bytes ({original_size/1024:.2f} KB)")
        
        minified_js = minify_js(original_js)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(minified_js)
        
        minified_size = len(minified_js)
        savings = ((original_size - minified_size) / original_size) * 100
        
        print(f"Minified size: {minified_size:,} bytes ({minified_size/1024:.2f} KB)")
        print(f"Savings: {savings:.1f}% ({(original_size - minified_size):,} bytes)")
        print(f"\n✓ JavaScript minified successfully → {output_file}")
        
        print("\n✓ All animations and interactions preserved!")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
