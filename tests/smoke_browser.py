"""Browser-only smoke: python tests/smoke_browser.py. Does NOT require Internet."""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from falvorn.browser import pool, observe, Session

async def main():
    await pool.start()
    context = await pool.browser.new_context()
    try:
        page = await context.new_page()
        await page.set_content('<html><head><title>Test page</title></head><body>'
            '<h1>Browser works</h1><a href="#details">Read more</a>'
            '<input placeholder="Keyword"/><button>Submit</button><p id="details">Healthy</p></body></html>')
        session = Session(context, page)
        first = await observe(page)
        assert first['title'] == 'Test page'
        assert len(first['elements']) == 3
        try:
            await session.action('click', index=2)
            raise AssertionError('Unsafe button click was not blocked')
        except Exception as error:
            assert '403' in str(error)
        result = await session.action('snapshot')
        assert 'Browser works' in result['text']
        print('PASS: Chromium launches, observes DOM, snapshots and blocks unsafe button actions')
        print('NOTE: This test uses in-memory HTML; live external page navigation is unverified here.')
    finally:
        await context.close()
        await pool.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
