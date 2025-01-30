import os
from io import BytesIO
from time import sleep

import helium
from dotenv import load_dotenv
from PIL import Image
from screeninfo import get_monitors
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from smolagents import CodeAgent, LiteLLMModel, tool
from smolagents.agents import ActionStep

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

agent = None
model = LiteLLMModel(
    model_id="gpt-4o",
    api_key=api_key,
)


def take_screenshot(current_step: ActionStep, agent: CodeAgent) -> Image.Image:
    """Captures a screenshot of the current browser window,

    Returns:
        Image.Image: PIL Image object containing the screenshot
    """
    sleep(0.5)
    driver = agent.driver

    for step in agent.logs:  # Remove previous screenshots from logs for lean processing
        if (
            isinstance(step, ActionStep)
            and step.step_number <= current_step.step_number - 2
        ):
            step.observations_images = None

    png_bytes = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(png_bytes))
    current_step.observations_images = [
        image.copy()
    ]  # Create a copy to ensure it persists, important!

    url_info = f"Current url: {driver.current_url}"
    step.observations = (
        url_info if step.observations is None else step.observations + "\n" + url_info
    )
    return image


@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
    driver = agent.driver
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(
            f"Match n°{nth_result} not found (only {len(elements)} matches found)"
        )
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result


@tool
def go_back() -> None:
    """Goes back to previous page."""
    driver = agent.driver
    driver.back()


@tool
def close_popups() -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows! This does not work on cookie consent banners.
    """
    # Common selectors for modal close buttons and overlay elements
    modal_selectors = [
        "button[class*='close']",
        "[class*='modal']",
        "[class*='modal'] button",
        "[class*='CloseButton']",
        "[aria-label*='close']",
        ".modal-close",
        ".close-modal",
        ".modal .close",
        ".modal-backdrop",
        ".modal-overlay",
        "[class*='overlay']",
    ]
    driver = agent.driver
    wait = WebDriverWait(driver, timeout=0.5)

    for selector in modal_selectors:
        try:
            elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )

            for element in elements:
                if element.is_displayed():
                    try:
                        driver.execute_script("arguments[0].click();", element)
                    except ElementNotInteractableException:
                        element.click()

        except TimeoutException:
            continue
        except Exception as e:
            print(f"Error handling selector {selector}: {str(e)}")
            continue
    return "Modals closed"


def create_agent() -> CodeAgent:
    """Creates and returns a configured CodeAgent with initialized Chrome driver."""
    primary_monitor = get_monitors()[0]
    screen_height = primary_monitor.height
    screen_width = primary_monitor.width
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument(f"--window-size={screen_width-550},{screen_height}")
    chrome_options.add_argument("--disable-pdf-viewer")
    chrome_options.add_argument("--window-position=550,0")

    driver = helium.start_chrome(headless=False, options=chrome_options)

    agent = CodeAgent(
        tools=[go_back, close_popups, search_item_ctrl_f],
        model=model,
        additional_authorized_imports=["helium"],
        max_steps=20,
        verbosity_level=0,
    )
    agent.driver = driver  # Store the driver instance in the agent
    return agent


helium_instructions = """
You can use helium to access websites. Don't bother about the helium driver, it's already managed.
First you need to import everything from helium, then you can do other actions!
Code:
```py
from helium import *
go_to('github.com/trending')
```<end_code>

You can directly click clickable elements by inputting the text that appears on them.
Code:
```py
click("Top products")
```<end_code>

If it's a link:
Code:
```py
click(Link("Top products"))
```<end_code>

If you try to interact with an element and it's not found, you'll get a LookupError.
In general stop your action after each button click to see what happens on your screenshot.
Never try to login in a page.

To scroll up or down, use scroll_down or scroll_up with as an argument the number of pixels to scroll from.
Code:
```py
scroll_down(num_pixels=1200) # This will scroll one viewport down
```<end_code>

When you have pop-ups with a cross icon to close, don't try to click the close icon by finding its element or targeting an 'X' element (this most often fails).
Just use your built-in tool `close_popups` to close them:
Code:
```py
close_popups()
```<end_code>

You can use .exists() to check for the existence of an element. For example:
Code:
```py
if Text('Accept cookies?').exists():
    click('I accept')
```<end_code>

Proceed in several steps rather than trying to solve the task in one shot.
And at the end, only when you have your answer, return your final answer.
Code:
```py
final_answer("YOUR_ANSWER_HERE")
```<end_code>

If pages seem stuck on loading, you might have to wait, for instance `import time` and run `time.sleep(2.0)`. But don't overuse this!
To list elements on page, DO NOT try code-based element searches like 'contributors = find_all(S("ol > li"))': just look at the latest screenshot you have and read it visually, or use your tool search_item_ctrl_f.
Of course, you can act on buttons like a user would do when navigating.
After each code blob you write, you will be automatically provided with an updated screenshot of the browser and the current browser url.
But beware that the screenshot will only be taken at the end of the whole action, it won't see intermediate states.
Don't kill the browser.
"""

search_request = """
Find flights from New York to San Francisco on 2025-02-01. Give me the cheapest flight.
"""


def browser_agent_streamer(prompt: str):
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    global agent
    if agent is None:
        agent = create_agent()
    for step in agent.run(prompt + helium_instructions, stream=True):
        if isinstance(step, ActionStep):
            yield str(step.llm_output.strip())
            yield take_screenshot(step, agent)
        else:
            yield "**Final Answer:**\n\n" + str(step)  # Return the final answer
            return


if __name__ == "__main__":
    browser_agent_streamer(search_request)
