import pytest
from falvorn.browser import pool


@pytest.mark.asyncio
async def test_browser_screenshot_bytes():
    await pool.start()
    context=await pool.browser.new_context(viewport={'width':900,'height':600})
    try:
        page=await context.new_page()
        await page.set_content('<html><title>Capture</title><body><h1>Local demo</h1></body></html>')
        screenshot=await page.screenshot(type='png')
        assert screenshot[:8]==b'\x89PNG\r\n\x1a\n'
    finally:
        await context.close()
        await pool.shutdown()
