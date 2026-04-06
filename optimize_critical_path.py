#!/usr/bin/env python3
"""
Critical Path Optimization Script
Fixes LCP, FCP by:
1. Inlining critical CSS for above-the-fold content
2. Deferring non-critical CSS  
3. Optimizing font loading
4. Removing render-blocking resources
"""

import re

# Critical CSS for above-the-fold (Nav + Hero only)
CRITICAL_CSS = """
/* Variables */
:root{--bg-primary:#0E1116;--bg-secondary:#131722;--bg-tertiary:#161B26;--bg-card:#1B2130;--bg-card-hover:#212738;--border:#2A3142;--border-subtle:#232A3A;--text-primary:#E8ECF1;--text-secondary:#9AA4B2;--text-tertiary:#6B7280;--accent:#4F46E5;--accent-light:#6366F1;--accent-lighter:#818CF8;--accent-glow:rgba(79,70,229,0.25);--success:#22C55E;--warning:#38BDF8;--danger:#EF4444;--font-heading:'Inter',system-ui,-apple-system,sans-serif;--font-body:'Inter',system-ui,-apple-system,sans-serif;--font-mono:'JetBrains Mono','Fira Code',monospace;--max-width:1160px;--radius-sm:8px;--radius-md:12px;--radius-lg:16px;--transition-fast:0.25s cubic-bezier(0.4,0,0.2,1);--transition-smooth:0.4s cubic-bezier(0.4,0,0.2,1)}

/* Reset */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}html{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}body{font-family:var(--font-body);background-color:var(--bg-primary);background-image:linear-gradient(180deg,#0E1116 0%,#131722 50%,#161B26 100%);color:var(--text-primary);line-height:1.7;font-size:16px;overflow-x:hidden}a{color:inherit;text-decoration:none}img{max-width:100%;display:block}

/* Container */
.container{max-width:var(--max-width);margin:0 auto;padding:0 32px}.section{padding:120px 0;position:relative;z-index:1}

/* Navigation */
.nav{position:fixed;top:0;left:0;right:0;z-index:1000;padding:0 32px;transition:var(--transition-smooth)}.nav.scrolled{background:rgba(14,17,22,0.85);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border-bottom:1px solid rgba(42,49,66,0.5);box-shadow:0 1px 3px rgba(0,0,0,0.2)}.nav-inner{max-width:var(--max-width);margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:72px}.nav-logo{font-family:var(--font-heading);font-weight:700;font-size:18px;color:var(--text-primary);letter-spacing:-0.02em}.nav-logo span{color:var(--accent-light)}.nav-links{display:flex;align-items:center;gap:36px;list-style:none}.nav-links a{font-size:14px;font-weight:500;color:var(--text-secondary);transition:color var(--transition-fast)}.nav-cta{font-size:13px!important;font-weight:600!important;color:white!important;background:var(--accent);padding:8px 20px;border-radius:8px;transition:all var(--transition-fast)!important}.nav-toggle{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:4px;background:none;border:none}.nav-toggle span{width:22px;height:2px;background:var(--text-primary);border-radius:2px}

/* Hero - LCP ELEMENT */
.hero{min-height:100vh;display:flex;align-items:center;position:relative;overflow:hidden;padding-top:72px;background:linear-gradient(170deg,#0E1116 0%,#111520 40%,#161B26 100%)}.hero-grid-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px);background-size:64px 64px;mask-image:radial-gradient(ellipse 60% 50% at 50% 50%,black 15%,transparent 65%);-webkit-mask-image:radial-gradient(ellipse 60% 50% at 50% 50%,black 15%,transparent 65%)}.hero-glow{position:absolute;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(79,70,229,0.20) 0%,rgba(79,70,229,0.08) 35%,transparent 65%);top:10%;right:5%;pointer-events:none;filter:blur(80px)}.hero-content{display:flex;flex-direction:column;gap:48px;align-items:flex-start;position:relative;z-index:2}.hero-text{max-width:800px}

/* Hero Elements */
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.15);border-radius:20px;font-size:13px;font-weight:500;color:var(--accent-lighter);margin-bottom:24px}.hero-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--success);animation:pulse 2s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}.hero-name{font-family:var(--font-heading);font-size:clamp(48px,8vw,88px);font-weight:800;line-height:1.05;letter-spacing:-0.04em;color:var(--text-primary);margin-bottom:24px;background:linear-gradient(135deg,#E8ECF1 0%,#9AA4B2 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.hero-headline{font-size:clamp(20px,3vw,26px);font-weight:600;color:var(--text-primary);line-height:1.4;margin-bottom:16px}.hero-credibility{font-size:17px;color:var(--accent-lighter);line-height:1.65;margin-bottom:12px}.hero-subtext{font-size:16px;color:var(--text-secondary);line-height:1.7;margin-bottom:32px;max-width:680px}

/* Buttons */
.hero-ctas{display:flex;gap:16px;flex-wrap:wrap}.btn-primary,.btn-secondary{display:inline-flex;align-items:center;gap:10px;padding:14px 28px;border-radius:12px;font-size:15px;font-weight:600;transition:all var(--transition-fast);cursor:pointer}.btn-primary{background:var(--accent);color:white}.btn-primary:hover{background:var(--accent-light);transform:translateY(-2px)}.btn-secondary{background:var(--bg-card);color:var(--text-primary);border:1px solid var(--border)}.btn-secondary:hover{background:var(--bg-card-hover);transform:translateY(-2px)}

/* KPI Cards */
.hero-visual{width:100%}.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;width:100%}.kpi-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-md);padding:20px;transition:all var(--transition-smooth)}.kpi-label{font-size:13px;font-weight:500;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px}.kpi-value{font-size:32px;font-weight:700;font-family:var(--font-heading);margin-bottom:6px}.kpi-value.accent{color:var(--accent-light)}.kpi-value.warning{color:var(--warning)}.kpi-value.success{color:var(--success)}.kpi-change{font-size:13px;color:var(--text-tertiary);margin-bottom:12px}.kpi-sparkline{display:flex;align-items:flex-end;gap:4px;height:32px}.kpi-sparkline .bar{flex:1;background:var(--accent);border-radius:2px;min-height:4px;opacity:0.3;transition:all 0.5s ease}

/* CRITICAL: Show content immediately */
.fade-in{opacity:1;transform:translateY(0)}

/* Mobile */
@media(max-width:768px){.container{padding:0 20px}.nav{padding:0 20px}.nav-links{position:fixed;top:72px;left:0;right:0;background:rgba(14,17,22,0.98);backdrop-filter:blur(24px);flex-direction:column;align-items:flex-start;gap:0;padding:24px;border-bottom:1px solid var(--border);transform:translateX(-100%);transition:transform 0.3s ease}.nav-links.open{transform:translateX(0)}.nav-links li{width:100%;border-bottom:1px solid var(--border-subtle);padding:16px 0}.nav-toggle{display:flex}.hero{padding-top:92px}.section{padding:80px 0}.hero-ctas{flex-direction:column;width:100%}.btn-primary,.btn-secondary{justify-content:center;width:100%}.kpi-grid{grid-template-columns:1fr}}
"""

def create_optimized_html(input_file, output_file):
    """Create optimized HTML with critical CSS inlined"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Build the optimized head section
    head_replacement = '''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Raj Jaiswal — Applied Machine Learning &amp; Product Analytics</title>
  <meta name="description"
    content="Product Analytics and Applied ML engineer. I build retention, forecasting, and revenue systems using ML + analytics. Open to internship and full-time opportunities.">
  <meta name="keywords"
    content="product analytics, applied machine learning, ML engineer, data analytics, A/B testing, forecasting">
  <meta name="author" content="Raj Jaiswal">
  <meta property="og:title" content="Raj Jaiswal — Product Analytics &amp; Applied ML">
  <meta property="og:description"
    content="I help teams improve retention, forecasting, and revenue using ML + analytics systems.">
  <meta property="og:type" content="website">
  <meta name="theme-color" content="#0E1116">
  
  <!-- Preconnect to font servers ASAP -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  
  <!-- CRITICAL CSS INLINED -->
  <style>''' + CRITICAL_CSS + '''</style>
  
  <!-- Load fonts async -->
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap"></noscript>
  
  <!-- Defer non-critical CSS -->
  <link rel="preload" as="style" href="styles.css" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
  
  <link rel="icon"
    href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
</head>'''
    
    # Replace the head section
    html = re.sub(r'<head>.*?</head>', head_replacement, html, flags=re.DOTALL)
    
    # Update script tag to defer
    html = html.replace('<script src="script.js"></script>', '<script src="script.js" defer></script>')
    
    # Write optimized HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Created {output_file}")
    print(f"  - Critical CSS inlined ({len(CRITICAL_CSS)} bytes)")
    print(f"  - Fonts loading asynchronously")
    print(f"  - Non-critical CSS deferred")
    print(f"  - JavaScript deferred")

def update_css_remove_import(css_file, output_file):
    """Remove @import from CSS (already loaded in HTML)"""
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Remove the @import line
    css = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2[^']+'\);", '', css)
    
    # Remove extra whitespace at start
    css = css.lstrip()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(css)
    
    print(f"✓ Created {output_file}")
    print(f"  - Removed @import (now loaded async in HTML)")

def main():
    print("=" * 70)
    print("CRITICAL PATH OPTIMIZATION")
    print("=" * 70)
    print("\nThis will fix LCP and FCP by:")
    print("  1. Inlining critical CSS for hero section")
    print("  2. Loading fonts asynchronously")
    print("  3. Deferring non-critical CSS")
    print("  4. Deferring JavaScript")
    print("\n" + "=" * 70)
    
    # Optimize HTML
    create_optimized_html('index.html', 'index-lcp-optimized.html')
    
    # Update CSS
    update_css_remove_import('styles.css', 'styles-no-import.css')
    
    print("\n" + "=" * 70)
    print("OPTIMIZATION COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Test locally:")
    print("     python -m http.server 8000")
    print("     Open: http://localhost:8000/index-lcp-optimized.html")
    print("\n  2. Run Lighthouse audit (Mobile, Slow 4G)")
    print("     Target: LCP < 2.5s, FCP < 2s")
    print("\n  3. If good, deploy:")
    print("     cp index-lcp-optimized.html index.html")
    print("     cp styles-no-import.css styles.css")
    print("\n" + "=" * 70)
    print("\n✓ Critical CSS inlined - hero renders immediately")
    print("✓ Fonts load async - no render blocking")
    print("✓ Non-critical CSS deferred - faster FCP")
    print("✓ JavaScript deferred - non-blocking")
    print("\nExpected improvement:")
    print("  LCP: 5.1s → <2.5s (50%+ faster)")
    print("  FCP: 3.3s → <2s (40%+ faster)")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
