#!/usr/bin/env python3
"""
HTML Optimization Script
Converts image tags to use picture elements with WebP and responsive images
Adds performance hints and optimizations
"""

import re

def create_picture_element(img_src, alt_text, loading="lazy", width=1200, height=675, classes=""):
    """Generate optimized picture element with WebP + responsive images"""
    
    # Extract base filename
    base_name = img_src.replace("images/", "").replace(".png", "")
    
    # Create srcset for responsive images
    srcset_webp = f"images/optimized/{base_name}-mobile.webp 640w, "
    srcset_webp += f"images/optimized/{base_name}-tablet.webp 768w, "
    srcset_webp += f"images/optimized/{base_name}-desktop-sm.webp 1024w, "
    srcset_webp += f"images/optimized/{base_name}.webp 1280w"
    
    srcset_png = f"images/optimized/{base_name}-optimized.png"
    
    picture = f'''<picture>
      <source type="image/webp" srcset="{srcset_webp}" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 90vw, 1200px">
      <img src="{srcset_png}" 
           alt="{alt_text}" 
           {f'class="{classes}"' if classes else ''}
           loading="{loading}"
           width="{width}" 
           height="{height}"
           decoding="async" />
    </picture>'''
    
    return picture

def optimize_html_file(input_file, output_file):
    """Read HTML, optimize images, add performance hints"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add performance hints in <head>
    head_additions = '''
  <!-- Performance Optimizations -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
  '''
    
    # Insert before </head>
    html = html.replace('</head>', head_additions + '</head>')
    
    # Update Google Fonts URL to include font-display=swap
    html = re.sub(
        r'https://fonts\.googleapis\.com/css2\?family=Inter[^"]+',
        r'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap',
        html
    )
    
    # Replace CSS link with optimized version
    html = html.replace('href="styles.css"', 'href="styles-optimized.css"')
    
    # Replace JS link with optimized version
    html = html.replace('src="script.js"', 'src="script-optimized.js" defer')
    
    # Pattern to match img tags
    img_pattern = r'<img\s+src="images/([^"]+)"\s+alt="([^"]+)"(?:\s+loading="lazy")?(?:\s+class="([^"]+)")?(?:\s+/?>)'
    
    def replace_img(match):
        src = f"images/{match.group(1)}"
        alt = match.group(2)
        classes = match.group(3) if match.group(3) else ""
        
        # Determine if above-the-fold (no lazy loading needed - but none are above fold in this site)
        loading = "lazy"
        
        return create_picture_element(src, alt, loading, 1200, 675, classes)
    
    html = re.sub(img_pattern, replace_img, html)
    
    # Write optimized HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Optimized {input_file} → {output_file}")

def main():
    """Optimize all HTML files"""
    files_to_optimize = [
        ('index.html', 'index-optimized.html'),
        ('case-churn.html', 'case-churn-optimized.html'),
        ('case-forecast.html', 'case-forecast-optimized.html'),
        ('case-synlitics.html', 'case-synlitics-optimized.html'),
        ('case-experimentation.html', 'case-experimentation-optimized.html'),
    ]
    
    print("=" * 60)
    print("HTML Optimization")
    print("=" * 60)
    
    for input_file, output_file in files_to_optimize:
        try:
            optimize_html_file(input_file, output_file)
        except FileNotFoundError:
            print(f"⚠ {input_file} not found, skipping...")
        except Exception as e:
            print(f"✗ Error processing {input_file}: {e}")
    
    print("\n✓ All HTML files optimized!")
    print("\nNext steps:")
    print("1. Review the optimized files")
    print("2. Test locally to ensure everything works")
    print("3. Replace original files with optimized versions")
    print("   - cp index-optimized.html index.html")
    print("   - cp case-churn-optimized.html case-churn.html")
    print("   - etc.")

if __name__ == "__main__":
    main()
