const { chromium } = require('@playwright/test');

(async () => {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('http://localhost:8080/index.html');
    console.log('Browser opened at http://localhost:8080');
})();
