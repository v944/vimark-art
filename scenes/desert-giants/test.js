const { chromium } = require('@playwright/test');
const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    let filePath = '.' + req.url;
    if (filePath === './') filePath = './index.html';
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
        '.html': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.webp': 'image/webp',
        '.glb': 'model/gltf-binary',
        '.hdr': 'application/octet-stream',
    };
    fs.readFile(filePath, (err, content) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found');
        } else {
            res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
            res.end(content);
        }
    });
});

server.listen(9090, '127.0.0.1', async () => {
    console.log('Server running at http://127.0.0.1:9090/');
    
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    const logs = [];
    page.on('console', msg => {
        const text = msg.text();
        logs.push(text);
        console.log(text);
    });
    
    await page.goto('http://127.0.0.1:9090/index.html');
    await page.waitForTimeout(10000);
    
    await page.screenshot({ path: 'test-result.png', fullPage: false });
    fs.writeFileSync('test-logs.json', JSON.stringify(logs, null, 2));
    console.log('Test complete. See test-result.png');
    
    await browser.close();
    server.close();
});
