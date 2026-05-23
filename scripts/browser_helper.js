const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe';
const profileDir = path.join(path.dirname(__dirname), 'study', 'cache', 'chrome_profile');

function parseArgs() {
    const args = {};
    for (let i = 2; i < process.argv.length; i++) {
        const arg = process.argv[i];
        if (arg.startsWith('--')) {
            const key = arg.slice(2);
            const val = process.argv[i + 1];
            if (val && !val.startsWith('--')) {
                args[key] = val;
                i++;
            } else {
                args[key] = true;
            }
        }
    }
    return args;
}

async function run() {
    const args = parseArgs();
    const action = args.action || 'scrape';
    const url = args.url;
    const output = args.output;
    const headless = args.headed ? false : true;

    if (!url) {
        console.error('Error: --url parameter is required.');
        process.exit(1);
    }

    console.log(`Launching Chrome (action=${action}, headless=${headless})...`);
    
    const browser = await puppeteer.launch({
        executablePath: chromePath,
        headless: headless,
        userDataDir: profileDir,
        args: [
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });

    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });
        
        console.log(`Navigating to: ${url}`);
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });

        if (action === 'scrape') {
            console.log('Extracting page text...');
            // Wait for main content layout if present
            try {
                await page.waitForSelector('main, .layout-body-main, #main', { timeout: 5000 });
            } catch (e) {
                console.log('Selector wait timed out, scraping raw body text.');
            }
            
            const data = await page.evaluate(() => {
                const title = document.title;
                // Focus on main content area if available, fallback to body
                const mainEl = document.querySelector('main') || document.querySelector('.layout-body-main') || document.body;
                return {
                    title: title,
                    text: mainEl.innerText
                };
            });

            if (output) {
                fs.mkdirSync(path.dirname(output), { recursive: true });
                fs.writeFileSync(output, `Title: ${data.title}\n\nSource: ${url}\n\n---\n\n${data.text}`, 'utf-8');
                console.log(`Scraped content saved to: ${output}`);
            } else {
                console.log('Scraped Content:\n', data.text.slice(0, 1000));
            }

        } else if (action === 'screenshot') {
            if (!output) {
                console.error('Error: --output parameter is required for screenshot action.');
                process.exit(1);
            }
            console.log('Capturing screenshot...');
            fs.mkdirSync(path.dirname(output), { recursive: true });
            await page.screenshot({ path: output, fullPage: true });
            console.log(`Screenshot saved to: ${output}`);

        } else if (action === 'progress') {
            console.log('Analyzing profile progress...');
            
            // Check if we need to wait for login
            const loggedIn = await page.evaluate(() => {
                // Microsoft Learn profile button check
                return !document.body.innerText.includes('Sign in');
            });

            if (!loggedIn) {
                console.log('User is not signed in. Launching in headed mode is required to log in once.');
                console.log('Please run this helper with --headed to log in.');
                await browser.close();
                process.exit(2);
            }

            // Extract modules progress from the shared plan page or profile lists page
            const progressData = await page.evaluate(() => {
                const modules = [];
                // Look for checked/completed classes or list items
                const items = document.querySelectorAll('.skillingplan-item, .collection-item, [data-test-id="list-item"]');
                items.forEach(el => {
                    const title = el.querySelector('.skillingplan-item-title, .title')?.innerText || '';
                    const progress = el.querySelector('.progress-percentage, .status')?.innerText || 'Not started';
                    modules.append({ title, progress });
                });
                return modules;
            });
            
            console.log('Progress data extracted:', progressData);
            if (output) {
                fs.mkdirSync(path.dirname(output), { recursive: true });
                fs.writeFileSync(output, JSON.stringify(progressData, null, 2), 'utf-8');
            }
        }

    } catch (e) {
        console.error('An error occurred during browser automation:', e);
    } finally {
        await browser.close();
        console.log('Chrome closed.');
    }
}

run();
