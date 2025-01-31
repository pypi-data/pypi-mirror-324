import asyncio

import pyperclip

from openoperator import LLM, Agent, Controller
from openoperator.agent.views import ActionResult
from openoperator.browser.browser import Browser, BrowserConfig
from openoperator.browser.context import BrowserContext

browser = Browser(
    config=BrowserConfig(
        headless=False,
    )
)
controller = Controller()


@controller.registry.action('Copy text to clipboard')
def copy_to_clipboard(text: str):
    pyperclip.copy(text)
    return ActionResult(extracted_content=text)


@controller.registry.action('Paste text from clipboard', requires_browser=True)
async def paste_from_clipboard(browser: BrowserContext):
    text = pyperclip.paste()
    # send text to browser
    page = await browser.get_current_page()
    await page.keyboard.type(text)

    return ActionResult(extracted_content=text)


async def main():
    model = LLM(model='openai/gpt-4o')
    agent = Agent(
        llm=model,
        controller=controller,
        browser=browser,
    )

    agent.add_task('Copy the text "Hello, world!" to the clipboard, then go to google.com and paste the text')

    await agent.run()
    await browser.close()

    input('Press Enter to close...')


if __name__ == '__main__':
    asyncio.run(main())
