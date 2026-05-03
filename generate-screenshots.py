#!/usr/bin/env python3
"""Generate demo screenshots for SOC Dashboard"""

from PIL import Image, ImageDraw, ImageFont
import os

docs_images = './docs/images'
os.makedirs(docs_images, exist_ok=True)

def create_screenshot(name, title, sections):
    """Create a demo screenshot with title and sections"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color=(15, 23, 42))  # slate-950
    draw = ImageDraw.Draw(img)
    
    # Header background
    draw.rectangle([(0, 0), (width, 80)], fill=(30, 41, 59))  # slate-800
    
    try:
        # Try to use system fonts, fall back to default
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw title
    draw.text((40, 25), f"🛡️ {title}", fill=(34, 211, 238), font=title_font)  # cyan-400
    
    # Draw content sections
    y_pos = 120
    for i, section in enumerate(sections):
        # Section title
        draw.text((40, y_pos), f"📊 {section['title']}", fill=(165, 243, 252), font=text_font)  # cyan-200
        y_pos += 50
        
        # Sample content
        if section.get('type') == 'metrics':
            # Draw metric cards
            metric_colors = [
                (229, 62, 62),    # red-500
                (245, 158, 11),   # amber-500
                (16, 185, 129),   # emerald-500
                (59, 130, 246),   # blue-500
            ]
            x_start = 40
            for j, metric in enumerate(section.get('items', [])):
                x = x_start + (j * 420)
                draw.rectangle([(x, y_pos), (x + 400, y_pos + 120)], 
                             fill=(55, 65, 81),  # gray-700
                             outline=metric_colors[j % len(metric_colors)])
                draw.text((x + 20, y_pos + 20), metric, fill=(229, 231, 235), font=text_font)  # gray-200
            y_pos += 150
        elif section.get('type') == 'chart':
            draw.rectangle([(40, y_pos), (600, y_pos + 200)], 
                         fill=(55, 65, 81),
                         outline=(34, 211, 238))
            draw.text((320, y_pos + 85), "📈 Chart", fill=(100, 116, 139), font=text_font)  # slate-500
            y_pos += 230
        elif section.get('type') == 'list':
            for item in section.get('items', [])[:3]:
                draw.rectangle([(40, y_pos), (940, y_pos + 70)], 
                             fill=(55, 65, 81),
                             outline=(71, 85, 105))  # slate-600
                draw.text((60, y_pos + 20), item, fill=(209, 213, 219), font=text_font)  # gray-300
                y_pos += 80
        else:
            y_pos += 80
    
    # Footer
    draw.text((40, height - 40), "WiFi Security Analyzer - SOC Dashboard", fill=(107, 114, 128), font=small_font)  # gray-500
    
    path = os.path.join(docs_images, f'{name}.png')
    img.save(path)
    print(f'✅ Created: {path}')

# Generate screenshots for each page
print('📸 Generating dashboard screenshots...\n')

create_screenshot('dashboard', 'Dashboard', [
    {'title': 'Security Metrics', 'type': 'metrics', 'items': ['Total Networks: 12', 'High Risk: 3', 'Medium Risk: 4', 'Low Risk: 5']},
    {'title': 'Risk Distribution', 'type': 'chart'},
    {'title': 'Recent Alerts', 'type': 'list', 'items': ['⚠️ High: Weak encryption detected', '⚡ Medium: Network broadcast enabled', '✅ Low: WPA3 enabled']}
])

create_screenshot('scanner', 'Network Scanner', [
    {'title': 'Network Scan Results', 'type': 'metrics', 'items': ['Status: Complete', 'Networks Found: 12', 'Scan Time: 2.5s', 'High Risk: 3']},
    {'title': 'Detected Networks', 'type': 'list', 'items': ['Home-WiFi (Risk: High, Signal: 85%)', 'Office-Network (Risk: Medium, Signal: 92%)', 'Guest-5G (Risk: Low, Signal: 78%)']}
])

create_screenshot('password', 'Password Analyzer', [
    {'title': 'Password Strength Analysis', 'type': 'metrics', 'items': ['Strength: Strong', 'Crack Time: 2.5 years', 'Entropy: 128 bits', 'Score: 95/100']},
    {'title': 'Recommendations', 'type': 'list', 'items': ['✅ Use mix of uppercase and lowercase', '✅ Include special characters', '✅ Avoid dictionary words']}
])

create_screenshot('traffic', 'Traffic Analysis', [
    {'title': 'Network Traffic Analysis', 'type': 'metrics', 'items': ['Packets: 1,245', 'Anomalies: 3', 'Suspicious: 1', 'Status: Normal']},
    {'title': 'Traffic Patterns', 'type': 'chart'}
])

create_screenshot('alerts', 'Alerts Panel', [
    {'title': 'Security Alerts', 'type': 'metrics', 'items': ['Critical: 0', 'High: 3', 'Medium: 5', 'Low: 8']},
    {'title': 'Alert Timeline', 'type': 'list', 'items': ['🚨 High: Weak WEP encryption', '⚠️ Medium: Open network broadcast', '⚡ Low: Outdated firmware detected']}
])

create_screenshot('reports', 'Reports Generator', [
    {'title': 'Report Generation', 'type': 'metrics', 'items': ['Status: Ready', 'Format: Markdown', 'Networks: 12', 'Threats: 8']},
    {'title': 'Report Details', 'type': 'list', 'items': ['Executive Summary generated', 'Risk Assessment completed', 'Recommendations compiled']}
])

print('\n✨ All screenshots generated successfully!')
