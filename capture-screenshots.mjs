import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const screenshotDir = './docs/images';

// Ensure screenshots directory exists
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

const pages = [
  { name: 'dashboard', selector: '[data-page="dashboard"]', navButton: 0, label: 'Dashboard' },
  { name: 'scanner', selector: '[data-page="scanner"]', navButton: 1, label: 'Network Scanner' },
  { name: 'password', selector: '[data-page="password"]', navButton: 2, label: 'Password Analyzer' },
  { name: 'traffic', selector: '[data-page="traffic"]', navButton: 3, label: 'Traffic Analysis' },
  { name: 'alerts', selector: '[data-page="alerts"]', navButton: 4, label: 'Alerts Panel' },
  { name: 'reports', selector: '[data-page="reports"]', navButton: 5, label: 'Reports' },
];

async function takeScreenshots() {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const context = await browser.createBrowserContext({
      viewport: { width: 1920, height: 1080 },
    });

    const page = await context.newPage();

    console.log('📸 Starting screenshot capture...\n');
    console.log('Navigating to http://localhost:3000...');
    
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);

    for (let i = 0; i < pages.length; i++) {
      const screenPage = pages[i];
      try {
        console.log(`Capturing (${i + 1}/${pages.length}): ${screenPage.label}...`);
        
        // Click nav button
        const navButtons = page.locator('button');
        const button = navButtons.nth(i + 4); // offset by header buttons
        
        try {
          await button.click({ timeout: 5000 });
          await page.waitForTimeout(1500);
        } catch (e) {
          console.log(`  ⚠️  Could not click nav button, using fallback`);
        }
        
        const screenshotPath = path.join(screenshotDir, `${screenPage.name}.png`);
        await page.screenshot({ path: screenshotPath });
        
        console.log(`✅ Saved: ${screenshotPath}`);
      } catch (error) {
        console.error(`❌ Error capturing ${screenPage.label}:`, error.message);
      }
    }

    await context.close();
    console.log('\n✨ Screenshot capture complete!');
  } catch (error) {
    console.error('Fatal error:', error);
  } finally {
    await browser.close();
  }
}

takeScreenshots().catch(console.error);
