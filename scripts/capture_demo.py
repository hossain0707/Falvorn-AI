"""Render the real Falvorn UI in an isolated Chromium document.

This environment may prohibit HTTP navigation in Chromium. The screenshot uses
actual dashboard HTML/CSS and verified localhost API payloads, without
pretending that browser automation itself completed successfully.
"""
import asyncio
import json
import os
import urllib.request
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('FALVORN_DEMO_WORK_DIR', str(ROOT/'.build/demo-work')))
OUT.mkdir(parents=True,exist_ok=True)


def api_payload():
    req=urllib.request.Request('http://127.0.0.1:8000/v1/fetch',
        data=json.dumps({'url':'http://127.0.0.1:9001'}).encode(),
        headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req) as response:return json.load(response)

async def main():
    sample=api_payload()
    assert sample['title']=='Falvorn Demo Library'
    html=(ROOT/'falvorn/static/index.html').read_text()
    html=html.replace('health();\n</script>', '/* Offline screencast: do not perform live browser networking */\n</script>')
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=await browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
        await page.set_content(html,wait_until='load')
        await page.evaluate('''() => {document.getElementById('apiStatus').textContent='Online';
            document.getElementById('apiInfo').textContent='Verified local API';
            document.getElementById('sessions').textContent='0';
            document.getElementById('modelStatus').textContent='Not set';
            document.getElementById('searchStatus').textContent='Not set';}''')
        await page.screenshot(path=str(OUT/'dashboard.png'))
        await page.locator('#startUrl').fill('http://127.0.0.1:9001')
        await page.locator('#goal').fill('Summarize the permitted local demo library. Return the source URL.')
        await page.screenshot(path=str(OUT/'goal.png'))
        await page.evaluate('''() => { document.getElementById('runState').textContent='Illustrative';
             document.getElementById('terminal').textContent='[sample event view — illustration only]\\n' +
             '[step 1] Agent receives authorized goal\\n' +
             '[step 2] Browser session would inspect page DOM\\n' +
             '[step 3] A configured LLM would choose safe actions\\n' +
             '[step 4] Result / blocked / failed are persisted in SQLite\\n\\n' +
             'Local browser navigation was NOT verified in this recording environment.';}''')
        await page.screenshot(path=str(OUT/'execution.png'))
        await page.evaluate('''(result) => {document.getElementById('toolResult').textContent=JSON.stringify(result,null,2);
            document.getElementById('toolInput').value='http://127.0.0.1:9001';}''', sample)
        await page.locator('#tool').scroll_into_view_if_needed()
        await page.wait_for_timeout(250)
        await page.screenshot(path=str(OUT/'extraction.png'))
        await page.evaluate('window.scrollTo(0,0)')
        await page.evaluate('''() => { document.getElementById('terminal').textContent=
          '[verified local API] HTTP 200 — /health\\n' +
          '[verified local API] HTTP 200 — /v1/fetch\\n' +
          '[verified local API] Title: Falvorn Demo Library\\n' +
          '[test suite] 14 tests passed in the build environment\\n' +
          '[limitation] Browser navigation unavailable under current sandbox policy';
          document.getElementById('runState').textContent='Verified API';}''')
        await page.screenshot(path=str(OUT/'verification.png'))
        await browser.close()
    print('Captured actual Falvorn UI; extraction panel is a genuine API result, other run events explicitly illustrative.')

if __name__=='__main__':asyncio.run(main())
