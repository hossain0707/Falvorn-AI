import pytest
from falvorn.browser import pool, Session, observe
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_chromium_observation_and_action_guard():
    await pool.start()
    ctx = await pool.browser.new_context()
    try:
        page = await ctx.new_page()
        await page.set_content('<html><title>Test</title><body><a href="#x">Go</a><button>Submit</button><input placeholder="Input"></body></html>')
        session = Session(ctx, page)
        observation = await observe(page)
        assert observation['title'] == 'Test'
        assert observation['elements'][1]['label'] == 'Submit'
        with pytest.raises(HTTPException) as e:
            await session.action('click', index=1, allow_write_actions=True)
        assert e.value.status_code == 403
        snapshot = await session.action('snapshot')
        assert snapshot['url'] == 'about:blank'
    finally:
        await ctx.close()
        await pool.shutdown()
