"""`smartbrowser.handler` module.
Communication layer between the UI and the Browser Use.

"""

from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.browser import BrowserContext, BrowserContextConfig

from smartbrowser.llms import get_llm


async def handle_task(
    task: str,
    model_name: str,
    use_vision: bool,
    max_failures: int,
    use_vision_for_planner: bool,
    retry_delay: int,
    max_input_tokens: int,
    validate_output: bool,
    planner_interval: int,
    chrome_path: str | None,
    headless: bool,
    disable_security: bool,
    min_wait_page_load: float,
    max_wait_page_load: float,
    wait_between_actions: float,
    browser_window_height: int,
    browser_window_width: int,
    highlight_elements: bool,
) -> str:
    """Handles the task submission and agent creation."""

    llm = get_llm(model_name)  # TODO : How to handle unknown model names ?
    # => Limit model_name in frontend using a dropdown list.

    # Create browser config
    browser_config = BrowserConfig(
        headless=headless,
        disable_security=disable_security,
        chrome_instance_path=chrome_path,
    )

    # Create browser context config
    context_config = BrowserContextConfig(
        minimum_wait_page_load_time=min_wait_page_load,
        maximum_wait_page_load_time=max_wait_page_load,
        wait_between_actions=wait_between_actions,
        browser_window_size={
            "height": browser_window_height,
            "width": browser_window_width,
        },
        highlight_elements=highlight_elements,
    )

    # Create browser and context
    browser = Browser(config=browser_config)
    context = BrowserContext(browser=browser, config=context_config)

    agent = Agent(
        task=task,
        llm=llm,
        browser_context=context,
        max_failures=max_failures,
        retry_delay=retry_delay,
        max_input_tokens=max_input_tokens,
        use_vision=use_vision,
        use_vision_for_planner=use_vision_for_planner,
        validate_output=validate_output,
        planner_interval=planner_interval,
    )

    history = await agent.run()
    return f"Task completed. Results: {history.final_result()}"
