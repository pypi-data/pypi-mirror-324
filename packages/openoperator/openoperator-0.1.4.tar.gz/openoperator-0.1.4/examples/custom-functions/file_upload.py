import asyncio
import logging
from pathlib import Path

from openoperator import LLM, Agent, Controller
from openoperator.agent.views import ActionResult
from openoperator.browser.browser import Browser, BrowserConfig
from openoperator.browser.context import BrowserContext

CV = Path.cwd() / 'examples/test_cv.txt'

logger = logging.getLogger(__name__)

# Initialize controller first
browser = Browser(
    config=BrowserConfig(
        headless=False,
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    )
)
controller = Controller()


@controller.action(
    'Upload file to element ',
    requires_browser=True,
)
async def upload_file(index: int, browser: BrowserContext):
    path = str(CV.absolute())
    dom_el = await browser.get_dom_element_by_index(index)

    if dom_el is None:
        return ActionResult(error=f'No element found at index {index}')

    file_upload_dom_el = dom_el.get_file_upload_element()

    if file_upload_dom_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)

    if file_upload_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    try:
        await file_upload_el.set_input_files(path)
        msg = f'Successfully uploaded file to index {index}'
        logger.info(msg)
        return ActionResult(extracted_content=msg)
    except Exception as e:
        logger.debug(f'Error in set_input_files: {str(e)}')
        return ActionResult(error=f'Failed to upload file to index {index}')


@controller.action('Close file dialog', requires_browser=True)
async def close_file_dialog(browser: BrowserContext):
    page = await browser.get_current_page()
    await page.keyboard.press('Escape')


async def main():
    agent = Agent(
        llm=LLM(model='openai/gpt-4o'),
        controller=controller,
        browser=browser,
    )

    agent.add_task('go to https://kzmpmkh2zfk1ojnpxfn1.lite.vusercontent.net/ and upload to each upload field my file')

    await agent.run()

    await browser.close()

    input('Press Enter to close...')


if __name__ == '__main__':
    asyncio.run(main())
