#!/usr/bin/env python3
"""
Image Optimization Script for Portfolio Website
Converts PNGs to WebP format while maintaining quality
Generates responsive image variants for different screen sizes
"""

import os
from PIL import Image
import sys

# Configuration
INPUT_DIR = "images"
OUTPUT_DIR = "images/optimized"
ORIGINAL_BACKUP_DIR = "images/originals"

# Responsive breakpoints (width in pixels)
SIZES = {
    "mobile-sm": 375,
    "mobile": 640,
    "tablet": 768,
    "desktop-sm": 1024,
    "desktop": 1280,
}

# Quality settings
WEBP_QUALITY = 85  # 85 quality gives ~70-80% size reduction with minimal visual loss
PNG_QUALITY = 90   # For optimized PNG fallbacks

def ensure_dir(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def optimize_image(input_path, output_base_name):
    """
    Optimize a single image:
    1. Create responsive variants
    2. Convert to WebP
    3. Create optimized PNG fallback
    """
    try:
        print(f"\nProcessing: {input_path}")
        img = Image.open(input_path)
        
        # Get original dimensions
        original_width, original_height = img.size
        aspect_ratio = original_height / original_width
        
        print(f"  Original size: {original_width}x{original_height} ({os.path.getsize(input_path) // 1024} KB)")
        
        # Generate responsive variants
        for size_name, target_width in SIZES.items():
            # Skip if target is larger than original
            if target_width >= original_width:
                continue
            
            # Calculate new height maintaining aspect ratio
            target_height = int(target_width * aspect_ratio)
            
            # Resize image
            resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Save as WebP
            webp_filename = f"{output_base_name}-{size_name}.webp"
            webp_path = os.path.join(OUTPUT_DIR, webp_filename)
            resized.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=6)
            webp_size = os.path.getsize(webp_path) // 1024
            print(f"  ✓ {size_name}: {target_width}x{target_height} WebP ({webp_size} KB)")
        
        # Save full-size WebP
        webp_full_filename = f"{output_base_name}.webp"
        webp_full_path = os.path.join(OUTPUT_DIR, webp_full_filename)
        img.save(webp_full_path, "WEBP", quality=WEBP_QUALITY, method=6)
        webp_full_size = os.path.getsize(webp_full_path) // 1024
        print(f"  ✓ Full size WebP: {original_width}x{original_height} ({webp_full_size} KB)")
        
        # Save optimized PNG fallback
        png_filename = f"{output_base_name}-optimized.png"
        png_path = os.path.join(OUTPUT_DIR, png_filename)
        img.save(png_path, "PNG", optimize=True)
        png_size = os.path.getsize(png_path) // 1024
        print(f"  ✓ Optimized PNG fallback: {png_size} KB")
        
        print(f"  Savings: {((os.path.getsize(input_path) - os.path.getsize(webp_full_path)) / os.path.getsize(input_path) * 100):.1f}% (WebP vs original)")
        
    except Exception as e:
        print(f"  ✗ Error processing {input_path}: {e}")

def main():
    """Main optimization workflow"""
    print("=" * 60)
    print("Portfolio Website Image Optimization")
    print("=" * 60)
    
    # Create necessary directories
    ensure_dir(OUTPUT_DIR)
    ensure_dir(ORIGINAL_BACKUP_DIR)
    
    # List of images to optimize
    images_to_optimize = [
        "dashboard-churn.png",
        "dashboard-forecast.png",
        "dashboard-restaurant.png",
        "dashboard-abtesting.png",
        "analytics_dashboard_thumbnail.png",
        "dashboard_thumbnail_contrast.png",
    ]
    
    total_original = 0
    total_optimized = 0
    
    for image_name in images_to_optimize:
        input_path = os.path.join(INPUT_DIR, image_name)
        
        if not os.path.exists(input_path):
            print(f"\nWarning: {input_path} not found, skipping...")
            continue
        
        # Backup original
        backup_path = os.path.join(ORIGINAL_BACKUP_DIR, image_name)
        if not os.path.exists(backup_path):
            img = Image.open(input_path)
            img.save(backup_path)
            print(f"✓ Backed up original to: {backup_path}")
        
        # Get base name without extension
        base_name = os.path.splitext(image_name)[0]
        
        # Track sizes
        original_size = os.path.getsize(input_path)
        total_original += original_size
        
        # Optimize
        optimize_image(input_path, base_name)
        
        # Calculate optimized size
        webp_path = os.path.join(OUTPUT_DIR, f"{base_name}.webp")
        if os.path.exists(webp_path):
            total_optimized += os.path.getsize(webp_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("OPTIMIZATION SUMMARY")
    print("=" * 60)
    print(f"Total original size: {total_original // 1024} KB ({total_original / 1024 / 1024:.2f} MB)")
    print(f"Total optimized size: {total_optimized // 1024} KB ({total_optimized / 1024 / 1024:.2f} MB)")
    if total_original > 0:
        savings = ((total_original - total_optimized) / total_original * 100)
        print(f"Total savings: {savings:.1f}%")
        print(f"Reduction: {(total_original - total_optimized) // 1024} KB")
    print("\n✓ All images optimized successfully!")
    print(f"✓ Optimized files saved to: {OUTPUT_DIR}/")
    print(f"✓ Original backups saved to: {ORIGINAL_BACKUP_DIR}/")
    print("\nNext steps:")
    print("1. Review the optimized images to ensure quality")
    print("2. Run the HTML update script to use the new images")
    print("3. Test the website locally before deploying")

if __name__ == "__main__":
    main()
