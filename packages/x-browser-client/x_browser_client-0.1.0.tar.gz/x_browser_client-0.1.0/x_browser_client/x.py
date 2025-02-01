"""
This module provides the `XClient` class, which uses Playwright to automate
browser interactions with the x.com platform (formerly Twitter). It supports
actions such as logging in, posting, scraping timelines and posts, replying,
liking, reposting, quoting, bookmarking, following/unfollowing, and more.
"""

from typing import Literal, Union
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, Locator
import logging as log
import os
from .config import labels, endpoints, locators
from urllib.parse import urljoin
from .data_types import PostStatusData, UserProfileData
from dotenv import load_dotenv
load_dotenv()
log.basicConfig(level=log.DEBUG)

class XClient:
    """
    The main client class for automating interactions with x.com (formerly Twitter)
    through Playwright. It facilitates browser setup, session management, login,
    posting, and a variety of user and post actions (e.g., scraping, replying,
    following, liking).
    """

    def __init__(self, context_dir: str = './context', locale: str = 'en-US',
                 timeout: int = 0, post_character_limit: int = 280):
        """
        Initializes the XClient instance.

        Args:
            context_dir (str): Directory for storing context (cookies/session data).
            locale (str): Locale for UI labels (default is 'en-US').
            timeout (int): Default timeout (seconds) for browser actions.
            post_character_limit (int): Character limit for new posts; typically 280.
        """
        self.base_url = "https://x.com"
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.context_dir = context_dir
        self.timeout = timeout
        self.locale = locale
        self.labels = labels[locale]
        os.makedirs(context_dir, exist_ok=True)
        self.playwright = sync_playwright().start()
        self.logged_in = False
        self.char_limit = post_character_limit
        self.login = None
        self.password = None
        self.username = None
        self.set_login_details()
        self._current_context_name = None
        self._very_short_wait = 1
        self._short_wait = 2
        self._medium_wait = 5
        self._long_wait = 10
        self.own_profile: UserProfileData = None
        
    def set_wait_times_seconds(self, short: int = None, medium: int = None, long: int = None):
        """
        Adjusts the default waiting durations used by the client.

        Args:
            short (int): New short wait duration in seconds.
            medium (int): New medium wait duration in seconds.
            long (int): New long wait duration in seconds.
        """
        if short:
            self._short_wait = short
        if medium:
            self._medium_wait = medium
        if long:
            self._long_wait = long
    
    def set_login_details(self, login: str = os.getenv('X_LOGIN'),
                          password: str = os.getenv('X_PASSWORD'),
                          username: str = os.getenv('X_USERNAME')):
        """
        Sets the login credentials for x.com. Falls back to environment variables
        if parameters are not provided.

        Args:
            login (str): The email/phone/username used to log in.
            password (str): The account password.
            username (str): The username handle (if prompted separately).
        """
        self.login = login
        self.password = password
        self.username = username
        
    def _set_browser_timeouts_seconds(self, timeout: int = 30):
        """
        Sets the default timeouts (in seconds) for the browser context and page.

        Args:
            timeout (int): The desired timeout in seconds.
        """
        self.timeout = timeout
        if self.context and self.page:
            self.context.set_default_timeout(timeout * 1000)
            self.page.set_default_timeout(timeout * 1000)
            self.page.set_default_navigation_timeout(timeout * 1000)
        
    def _open_browser(self, context_name: str = None):
        """
        Launches a Chromium browser with a fresh or named context, optionally
        loading previously saved session data.

        Args:
            context_name (str): The name of the session context file to load or create.
        """
        log.info("Opening browser")
        self.browser = self.playwright.chromium.launch(
            headless=False,
        )
        context_path = f"{self.context_dir}/{context_name}.json" if context_name else None
        self._current_context_name = context_name
        self.context = self.browser.new_context(locale=self.locale)
        self.page = self.context.new_page()
        
        if context_path:
            self.connect_context(context_name)

        self._set_browser_timeouts_seconds(self.timeout)

    def check_account_menu_button(self):
        """
        Checks whether the account menu button is visible, which indicates
        that the user is logged in.

        Returns:
            bool: True if the account menu button is visible (logged in), else False.
        """
        log.info("Checking if logged in...")
        try:
            self.page.wait_for_load_state("domcontentloaded")
            present = self.page.locator(locators["account_menu_button"]).is_visible()
            if present:    
                log.info("Found account menu button.")
                return True
            else:
                log.error("Not logged in.")
                return False
        except:
            log.error("Not logged in.")
            return False    
  
    def connect_context(self, context_name: str):
        """
        Saves the current browser context (cookies/session) to a specified JSON file.

        Args:
            context_name (str): The name of the file (without extension) in `./context/`.
        """
        log.info(f"Saving context as '{context_name}'...")
        self.page.context.storage_state(path=f"./context/{context_name}.json")
        
    def close_browser(self):
        """
        Closes the browser and Playwright instance, cleaning up resources.
        """
        self.browser.close()
        self.browser = None
        self.page = None
        self.playwright.stop()
        
    def go_to(self, url: str, force_reload: bool = False):
        """
        Navigates the browser to a specific URL.

        Args:
            url (str): The URL to navigate to.
            force_reload (bool): If True, forces navigation even if already on that URL.
        """
        if not self.page:
            self._open_browser()
        if self.page.url != url or force_reload:
            log.info(f"Going from {self.page.url} to {url}")
            self.page.goto(url)
            self.wait_seconds(self._medium_wait)
        
    def go_home(self):
        """
        Navigates the browser to the home timeline if not already there.
        """
        if self.page is not None:
            current_url = self.page.url
            home_url = urljoin(self.base_url, endpoints["home"])
            root_url = urljoin(self.base_url, endpoints["root"])
            if current_url != home_url and current_url != root_url:
                self.go_to(home_url)
        else:
            self.go_to(urljoin(self.base_url, endpoints["home"]))
        
    def go_login(self):
        """
        Navigates the browser to the login flow (login page).
        """
        self.go_to(urljoin(self.base_url, endpoints["login"]))
    
    def wait_seconds(self, seconds: float):
        """
        Pauses execution for the specified number of seconds.

        Args:
            seconds (float): The number of seconds to wait.
        """
        log.info(f"Waiting for {seconds}s...")
        self.page.wait_for_timeout(seconds * 1000)
    
    def _wait_until_error(self):
        """
        Loops indefinitely (with hour-long pauses) until an error/exception
        interrupts or the process is stopped. Used to keep the browser open.
        """
        try:
            while True:
                self.wait_seconds(3600)
        except:
            pass
        
    def manual_login(self):
        """
        Attempts a manual login sequence:
        1. Goes to login page.
        2. Prompts user to log in manually in the open browser window.
        3. Resumes script when user is on the home page.
        """
        self.go_login()
        log.info("If you are not logged in, please do so now, the process will resume as soon as you are logged in.")
        self.page.wait_for_url(urljoin(self.base_url, endpoints["home"]))
        self.page.locator(locators["account_menu_button"]).wait_for(state="visible")
        self.logged_in = True
        
    def auto_login(self, login: str = None, password: str = None, username: str = None):
        """
        Attempts to log in automatically using provided or previously set credentials.

        Args:
            login (str): Email/phone/username for login.
            password (str): Account password.
            username (str): Actual username if prompted separately.

        Returns:
            bool: True if login succeeded, otherwise False.
        """
        if login and password and username:
            self.set_login_details(login, password, username)
        else:
            if not self.login or not self.password or not self.username:
                log.error("No login details provided.")
                return False
            else:
                login = self.login
                password = self.password
                username = self.username

        log.info("Attempting to log in automatically...")
        self.go_login()
        
        
        self.page.get_by_text(self.labels["login_input"], exact=True).wait_for(state="visible")
        log.info("Filling login details...")
        self.page.get_by_text(self.labels["login_input"], exact=True).fill(login)
        self.page.get_by_text(self.labels["login_next_button"], exact=True).click()
        
        try:
            self.page.get_by_text(self.labels["login_phone_or_user_name_input"], exact=True).wait_for(state="visible", timeout=5000)
            log.info("Filling username...")
            self.page.get_by_text(self.labels["login_phone_or_user_name_input"], exact=True).fill(username)
            self.page.get_by_text(self.labels["login_next_button"], exact=True).click()
        except:
            pass
        
        self.page.get_by_text(self.labels["login_password_input"], exact=True).wait_for(state="visible")
        log.info("Filling password...")
        self.page.get_by_text(self.labels["login_password_input"], exact=True).fill(password)
        self.page.get_by_text(self.labels["login_login_button"], exact=True).click()
        # wait for load
        self.wait_seconds(self._medium_wait)
        if self.page.url == urljoin(self.base_url, endpoints["home"]):
            self.logged_in = True
            log.info("Successfully logged in.")
            return True
        return False
        
    def ensure_login(self):
        """
        Ensures the user is logged in:
        1. Checks for account menu button.
        2. If not found, attempts to log in automatically or manually.
        3. Returns the page to its original URL if successful.
        """
        if self.check_account_menu_button():
            self.logged_in = True
        else:
            current_url = self.page.url
            self.go_home()
            if self.check_account_menu_button():
                self.logged_in = True
            if not self.logged_in:
                log.error("Not logged in, trying to log in...")
                self.manual_login() if not self.auto_login() else None
            self.go_to(current_url) if current_url != "about:blank" else None

        if self.logged_in:
            log.info("Login confirmed.")
        
    def _accept_cookies(self, all=True, timeout_seconds=5):
        """
        Attempts to accept or refuse cookies if a cookie banner appears.

        Args:
            all (bool): If True, clicks "Accept all cookies"; otherwise refuses them.
            timeout_seconds (int): Time to wait for the banner before skipping.
        """
        label = self.labels["cookies_accept_all" if all else "cookies_accept_essential"]
        log.info(f"Waiting up to {timeout_seconds}s for cookies pop-up...")
        try:
            self.page.locator(f"text={label}").wait_for(state="visible", timeout=timeout_seconds * 1000)
            log.info(f"Clicking: '{label}'")
            self.page.locator(f"text={label}").click()
        except Exception as e:
            log.error(f"Pop up didn't appear, skipping...")
    
    def _skip_notifications(self, timeout_seconds=5):
        """
        Skips or refuses notification pop-ups if they appear.

        Args:
            timeout_seconds (int): Time to wait for the notification pop-up before skipping.
        """
        label = self.labels["notifications_skip"]
        log.info(f"Waiting up to {timeout_seconds}s for notifications pop-up...")
        try:
            self.page.locator(f"text={label}").wait_for(state="visible", timeout=timeout_seconds * 1000)
            log.info(f"Clicking: '{label}'")
            self.page.locator(f"text={label}").click()
        except Exception as e:
            log.error(f"Pop up didn't appear, skipping...")
            
    def start_client(self, context_name=None, accept_cookies=True, skip_notifications=True):
        """
        Opens the browser, optionally loads session state, navigates to the home page,
        accepts/refuses cookies, skips notifications, and ensures the user is logged in.

        Args:
            context_name (str): Name of the browser context/session to load or create.
            accept_cookies (bool): Whether to auto-accept cookies if prompted.
            skip_notifications (bool): Whether to skip notification prompts if they appear.
        """
        self._open_browser(context_name=context_name) 
        self.go_home()
        self._accept_cookies() if accept_cookies else None
        self._skip_notifications() if skip_notifications else None
        self.ensure_login()
        
    def exit_client(self, save_context: bool = True, close_browser_after: int = 0,
                    context_name_override: str = None):
        """
        Shuts down the client after performing optional waits and context saving.

        Args:
            save_context (bool): Whether to save session context (cookies) on exit.
            close_browser_after (int): 
                - If < 0, keeps the browser open indefinitely.
                - If > 0, waits that many seconds before closing.
                - If 0, closes immediately.
            context_name_override (str): If provided, uses this name instead of the one
                originally passed when opening the browser context.

        Raises:
            ValueError: If saving context is requested but no context name is available.
        """
        if close_browser_after < 0:
            log.info("Keeping browser open.")
            self._wait_until_error()
        elif close_browser_after > 0:
            log.info(f"Waiting for {close_browser_after}s before closing browser...")
            self.wait_seconds(close_browser_after)
        else:
            pass
        
        if save_context:
            if context_name_override:
                self.connect_context(context_name_override)
            elif self._current_context_name:
                self.connect_context(self._current_context_name)
            else:
                log.error("No context name provided nor available on the client, did not save context.")
                raise ValueError("No context name provided nor available on the client, did not save context.")
        self.close_browser()
        return
            
    def new_post(self, text: str):
        """
        Creates a new post (tweet).

        Args:
            text (str): The content of the post.

        Raises:
            ValueError: If the post exceeds the character limit set (default 280).
        """
        if len(text) > 280:
            log.error(f"Post too long, must be less than {self.char_limit} characters.")
            raise ValueError(f"Post too long, must be less than {self.char_limit} characters.")
        self.go_to(urljoin(self.base_url, endpoints["new_post"]))
        text_input = self.page.locator(locators["post_input_editor_div"])
        text_input.click()
        log.info("Writing post...")
        text_input.fill(text)
        self.wait_seconds(self._short_wait)
        post_overlay = self.page.locator(locators["post_overlay"])
        if post_overlay.is_visible():
            log.info("Closing overlay...")
            self.page.mouse.click(0, 0)
            self.wait_seconds(self._very_short_wait)
        
        button = self.page.locator(locators["post_editor_submit_button"])
        log.debug(f"Found button: {button}")
        button.click()
        log.info("Posted.")
        
    def close_popup(self):
        """
        Tries to close any open notification pop-up if present.
        """
        try:
            notification_popup_close = self.page.locator(locators["close_notifications_popup"])
            notification_popup_close.click()
            log.info("Closed pop-up.")
        except:
            pass
            
    def scrape_new_posts(self, num_posts: int = 10,
                         tab: Literal["for_you", "following"] = "for_you",
                         skip_own: bool = True) -> list[PostStatusData]:
        """
        Scrapes recent posts from the 'For You' or 'Following' tabs on the home timeline.

        Args:
            num_posts (int): How many posts to collect before stopping.
            tab (Literal["for_you", "following"]): Which tab to scrape from.
            skip_own (bool): Whether to skip the bot's own posts.

        Returns:
            list[PostStatusData]: A list of extracted post data objects.

        Raises:
            ValueError: If an invalid tab is supplied.
        """
        self.go_home()
        tabs = self.page.locator(locators["home_timeline_tabs"]).all()
        for_you, following_tab = tabs[:2]
        if tab == "for_you":
            for_you.click()
            self.wait_seconds(self._medium_wait)
        elif tab == "following":
            log.info("Switching to following tab...")
            following_tab.click()
            self.wait_seconds(self._long_wait)
        else:
            log.error("Invalid tab.")
            raise ValueError("Invalid tab.")
        previous_amount = 0
        found_posts = 0 
        posts = []
        while found_posts < num_posts:
            self.wait_seconds(self._very_short_wait)
            posts_section = self.page.locator(locators["posts_list_div"]).first()
            new_posts = posts_section.locator(locators["post"]).all()
            for post in new_posts:
                social_context = post.locator(locators["post_simple_repost"]).all()
                if len(social_context) > 0:
                    log.warning("Detected a simple repost post, scraping not implemented. Skipping...")
                    continue
                if skip_own:
                    user_handle = post.locator(locators["post_user_name_div"]).locator("a").nth(1).inner_text()
                    if user_handle == "@wild_robot_":
                        log.info("Skipping own post...")
                        continue
                show_more = post.locator(locators["post_content_show_more"]).all()
                for sm in show_more:
                    sm.click()
                    self.wait_seconds(self._short_wait)
                post_data = self.extract_post_data(post)
                if post_data.post_url not in [t.post_url for t in posts]:
                    posts.append(post_data)
                    found_posts += 1
            log.info(f"Found total of so far {len(posts)}/{num_posts} posts.")

            if found_posts >= num_posts:
                break
            elif found_posts == previous_amount:
                log.info("No more new posts found in the previous load, stopping.")
                break
            else:
                log.info("Scrolling down to load more posts...")
                last_post = new_posts[-1]
                last_post.scroll_into_view_if_needed()
                previous_amount = found_posts
                log.info("Waiting for new posts...")
                self.wait_seconds(self._medium_wait)
                log.info("Finished waiting.")

        posts = posts[:num_posts] if num_posts < len(posts) else posts
        log.info(f"Returning {len(posts)} posts.")
        return posts
    
    def scrape_post(self, url: str = None) -> PostStatusData:
        """
        Scrapes a single post from a given URL or the current page.

        Args:
            url (str, optional): The URL to navigate to before scraping the post.
                If None, the current page is used.

        Returns:
            PostStatusData: The extracted post data.

        Raises:
            ValueError: If no post is found at the given/current URL.
        """
        self.go_to(url=url) if url is not None else None
        content_section_containers = self.page.locator(locators["post_page_content_container"]).all()
        if len(content_section_containers) > 0:
            for container in content_section_containers:
                post = container.locator(locators["post_page_comments_and_post"]).all()
                if len(post) > 0:
                    show_more = post[0].locator(locators["post_content_show_more"]).all()
                    if len(show_more) > 0:
                        show_more[0].click()
                        self.wait_seconds(self._very_short_wait)
                    post_data = self.extract_post_data(post[0], main_post=True)
                    return post_data
        log.error(f"Unable to find any posts at the current url: {self.page.url}")
        raise ValueError(f"Unable to find any posts at the current url: {self.page.url}")
    
    @classmethod            
    def _is_duplicate_attachment(cls, new_attachment: dict, existing_attachments: list) -> bool:
        """
        Checks whether a new attachment dict is already in the list
        of existing attachments.

        Args:
            new_attachment (dict): The attachment to check for duplication.
            existing_attachments (list): The list of existing attachments.

        Returns:
            bool: True if the exact attachment already exists, False otherwise.
        """
        for att in existing_attachments:
            if att == new_attachment:
                return True
        return False        
    
    def extract_post_data(self, post_locator: Locator, main_post: bool = False) -> PostStatusData:
        """
        Extracts metadata, text, attachments, and stats from a post element.

        Args:
            post_locator (Locator): A Playwright Locator pointing to the post's DOM element.
            main_post (bool): True if this is the main post on a page. Affects how
                              posted time/URL is parsed.

        Returns:
            PostStatusData: An object containing all relevant metadata.

        Notes:
            - Attachments can be images, videos, polls, or quoted posts.
            - Stats (replies, reposts, likes, views) can differ in indexing for the
              main post vs. a timeline post.
        """
        log.info("Building post...")
        post_url = None
        posted = None
        user_url = None
        user_handle = None
        username_div = post_locator.locator(locators["post_user_name_div"])
        username_links = username_div.locator("a").all()
        log.debug(f"Found {len(username_links)} links in username div.")
        post_data = {}
        if len(username_links) >= 2:
            log.debug(username_links[0].inner_html())
            user_url = username_links[0].get_attribute("href")
            user_name = username_links[0].inner_text()
            user_handle = username_links[1].inner_text()
        if not main_post:
            post_url = username_links[2].get_attribute("href") 
            posted = username_links[2].inner_text() 
        else:
            post_page_posted_datetime = post_locator.locator(locators["post_page_posted_datetime"]).all()
            if len(post_page_posted_datetime) == 1:
                posted = post_page_posted_datetime[0].inner_text()
            post_url = self.page.url.replace(self.base_url, "")
            
        log.info(f"User: {user_handle}")
        log.info(f"User URL: {user_url}")
        log.info(f"Posted: {posted}")
        log.info(f"Post URL: {post_url}")
        
        post_data["user_handle"] = user_handle
        post_data["user_name"] = user_name
        post_data["user_url"] = user_url
        post_data["posted"] = posted
        post_data["post_url"] = post_url
        
        post_text_div = post_locator.locator(locators["post_text_div"]).all()
        post_text = None
        if len(post_text_div) == 1:
            post_text = post_text_div[0].inner_text()
            log.info(f"Post: {post_text}")
        post_data["post_text"] = post_text
        attachments = []
        post_attachments = post_locator.locator(locators["post_attachments"]).all()
        if len(post_attachments) > 0:
            for post_attachment_section in post_attachments:
                attachment_with_link = post_attachment_section.locator("a").all()
                attachment_with_video = post_attachment_section.locator(locators["post_video_attachment"]).all()
                attachment_with_poll = post_attachment_section.locator(locators["post_poll_attachment"]).all()
                attachments_with_post = post_attachment_section.locator(locators["post_post_attachment"]).all()
                if len(attachment_with_link) > 0:
                    add_attachments = []
                    for post_attachment in attachment_with_link:
                        attachment = {}
                        attachment_url = post_attachment.get_attribute("href")
                        attachment_text = post_attachment.inner_text()
                        log.info(f"Attachment: {attachment_text}")
                        log.info(f"Attachment URL: {attachment_url}")
                        attachment["text"] = attachment_text
                        attachment["url"] = attachment_url
                        attachment_image = post_attachment.locator("img").all()
                        if len(attachment_image) == 1:
                            attachment_image = attachment_image[0].get_attribute("src")
                            attachment["image"] = attachment_image
                        if not self._is_duplicate_attachment(attachment, attachments):
                            log.info(f"Detected link attachment.") if not attachment_image else log.info(f"Detected image attachment.")
                            add_attachments.append(attachment)
                    for att in add_attachments:
                        att["type"] = "image" if "image" in att.keys() else "link"
                    attachments.extend(add_attachments)
                        
                if len(attachment_with_video) > 0:
                    add_attachments = []
                    for post_attachment in attachment_with_video:
                        attachment = {}
                        attachment["video"] = "Not supported"
                        if not self._is_duplicate_attachment(attachment, attachments):
                            log.info(f"Detected video attachment, not supported.")
                            add_attachments.append(attachment)
                    for att in add_attachments:
                        att["type"] = "video"
                    attachments.extend(add_attachments)
                        
                if len(attachment_with_poll) > 0:
                    add_attachments = []
                    for post_attachment in attachment_with_poll:
                        attachment = {}
                        poll_options = post_attachment.locator(locators["post_poll_attachment_option"]).all()
                        poll_data = []
                        for option in poll_options:
                            poll_data.append(option.inner_text())
                        poll_info = post_attachment.locator(locators["post_poll_attachment_info"]).all()
                        if len(poll_info) >= 1:
                            poll_time_left = poll_info[-1].inner_text()
                            attachment["time_left"] = poll_time_left

                        attachment["options"] = poll_data
                        if not self._is_duplicate_attachment(attachment, attachments):
                            log.info(f"Detected poll attachment.")
                            add_attachments.append(attachment)
                            log.info(f"Poll options: {poll_data}")
                            log.info(f"Poll time left: {poll_time_left}")
                    for att in add_attachments:
                        att["type"] = "poll"
                    attachments.extend(add_attachments)
        
                if len(attachments_with_post) > 0:
                    add_attachments = []
                    for post_attachment in attachments_with_post:
                        attachment = {}
                        attached_post_user_div = post_attachment.locator(locators["post_post_attachment_user_div"]).all()
                        attached_post_user_name = attached_post_user_div[0].locator(locators["post_post_attachment_user_name"]).nth(0).inner_text()
                        attached_post_user_handle = attached_post_user_div[0].locator(locators["post_post_attachment_user_handle"]).nth(1).inner_text()
                        attached_post_text_div = post_attachment.locator(locators["post_post_attachment_text_div"]).all()
                        attached_post_text = attached_post_text_div[0].inner_text()
                        attachment["user_name"] = attached_post_user_name
                        attachment["user_handle"] = attached_post_user_handle
                        attachment["text"] = attached_post_text
                        if not self._is_duplicate_attachment(attachment, attachments):
                            log.info(f"Detected post attachment.")
                            add_attachments.append(attachment)
                            log.info(f"Attached post user: {attached_post_user_name} ({attached_post_user_handle})")
                            log.info(f"Attached post: {attached_post_text}")
                    for att in add_attachments:
                        att["type"] = "quoted_post"
                    attachments.extend(add_attachments)
                        
        post_data["post_attachments"] = attachments
        post_stats = post_locator.locator(locators["post_stat"]).all()
        if len(post_stats) < 4:
            log.error("Not enough post stats found.")
            input("Press Enter to continue...")
        if not main_post:
            replies = post_stats[0].inner_text().strip()
            if len(replies) == 0:
                replies = "0"
            post_data["replies"] = replies
            reposts = post_stats[1].inner_text().strip()
            if len(reposts) == 0:
                reposts = "0"
            post_data["reposts"] = reposts
            likes = post_stats[2].inner_text().strip()
            if len(likes) == 0:
                likes = "0"
            post_data["likes"] = likes
            views = post_stats[3].inner_text().strip()
            if len(views) == 0:
                views = "0"
            post_data["views"] = views
        else:
            replies = post_stats[1].inner_text().strip()
            if len(replies) == 0:
                replies = "0"
            post_data["replies"] = replies
            reposts = post_stats[2].inner_text().strip()
            if len(reposts) == 0:
                reposts = "0"
            post_data["reposts"] = reposts
            likes = post_stats[3].inner_text().strip()
            if len(likes) == 0:
                likes = "0"
            post_data["likes"] = likes
            views = post_stats[0].inner_text().strip()
            if len(views) == 0:
                views = "0"
            post_data["views"] = views
        return PostStatusData.from_dict(post_data) 

    def open_post(self, post: PostStatusData):
        """
        Deprecated. Opens a given post by navigating to its URL.

        Args:
            post (PostStatusData): The post to open.
        """
        log.warning("Deprecated method, use go_to_post instead.")
        if self.page.url != urljoin(self.base_url, post.post_url):
            self.go_to(urljoin(self.base_url, post.post_url))
        
    def post_reply(self, post: PostStatusData, reply: str):
        """
        Replies to a given post with the provided text.

        Args:
            post (PostStatusData): The post to reply to.
            reply (str): The reply text.
        """
        log.info(f"Replying to post: {post.post_url}")
        self.open_post(post)
        reply_input = self.page.locator(locators["post_page_reply_input"]).all()
        if len(reply_input) == 1:
            log.info("Filling reply input...")
            reply_input[0].fill(reply)
            reply_input[0].scroll_into_view_if_needed()
            self.wait_seconds(self._medium_wait)
            reply_button = self.page.locator(locators["post_page_reply_button"]).all()
            if len(reply_button) == 1:
                log.info("Clicking reply button...")
                reply_button[0].click()
            else:
                log.error("Reply button not found.")
        else:
            log.error("Reply input not found.")
            
    def post_vote_in_poll(self, post: PostStatusData, option: Union[str, int] = 0):
        """
        Votes in a poll if the post has a poll attachment.

        Args:
            post (PostStatusData): The post containing the poll.
            option (Union[str, int]): The option to vote for, either by index (int)
                or exact text match (str).

        Notes:
            If the poll or option is not found, logs an error and does nothing.
        """
        if not post.has_poll_attachments():
            log.error("Post does not have a poll attachment, cannot vote.")
            return
        self.open_post(post)
        post_locator = self.page.locator(locators["post"]).all()
        if len(post_locator) > 0:
            poll_section = post_locator[0].locator(locators["post_poll_attachment"]).all()
            if len(poll_section) > 0:
                poll_options = poll_section[0].locator(locators["post_poll_attachment_option"]).all()
                if isinstance(option, int):
                    if option < len(poll_options):
                        poll_options[option].click()
                    else:
                        log.error("Option index out of range.")
                elif isinstance(option, str):
                    for poll_option in poll_options:
                        if poll_option.inner_text().strip() == option.strip():
                            poll_option.click()
                            break
                    else:
                        log.error("Option not found.")
                else:
                    log.error("Invalid option type.")
            else:
                log.error("Poll options not found.")
        else:
            log.error("Post not found.")
            
    def post_repost_quote(self, post: PostStatusData, quote: str):
        """
        Reposts a given post with a quote/comment.

        Args:
            post (PostStatusData): The post to quote repost.
            quote (str): The quote or comment text.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            repost_buttons = post_page_buttons.locator(locators["post_page_repost_buttons"]).all()
            if len(repost_buttons) > 0:
                log.info("Clicking repost button...")
                repost_button = repost_buttons[0]
                repost_button.click()
                self.wait_seconds(self._short_wait)
                if quote:
                    confirm_quote = self.page.locator(locators["post_page_repost_mode_quote"]).all()
                    if len(confirm_quote) > 0:
                        log.info("Quoting post...")
                        confirm_quote[0].click()
                        self.wait_seconds(self._short_wait)
                        quote_input = self.page.locator(locators["post_repost_quote_input"]).all()
                        if len(quote_input) > 0:
                            log.info("Filling quote input...")
                            quote_input[0].fill(quote)
                            quote_input[0].scroll_into_view_if_needed()
                            self.wait_seconds(self._medium_wait)
                            quote_button = self.page.locator(locators["post_repost_quote_button"]).all()
                            if len(quote_button) > 0:
                                log.info("Clicking quote button...")
                                quote_button[0].click()
                            else:
                                log.error("Quote button not found.")
                        else:
                            log.error("Quote input not found.")     
            else:
                log.error("Repost button not found.")
                
    def post_repost_simple(self, post: PostStatusData):
        """
        Performs a simple repost (retweet) of a given post.

        Args:
            post (PostStatusData): The post to repost.
        """
        self.open_post(post)
        log.info("Preparing to repost post...")
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            repost_buttons = post_page_buttons.locator(locators["post_page_repost_buttons"]).all()
            if len(repost_buttons) > 0:
                log.info("Reposting post...")
                repost_buttons[0].click()
                confirm_simple = self.page.locator(locators["post_page_repost_mode_simple"]).all()
                if len(confirm_simple) > 0:
                    log.info("Confirming repost...")
                    confirm_simple[0].click()
                    log.info("Reposted.")
                    self.wait_seconds(self._short_wait)
                else:
                    log.error("Confirm repost button not found.")
            else:
                log.error("Repost button not found.")
                
    def post_unrepost_simple(self, post: PostStatusData):
        """
        Cancels or undoes a previously reposted post.

        Args:
            post (PostStatusData): The post to un-repost.
        """
        self.open_post(post)
        log.info("Preparing to unrepost post...")
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            repost_buttons = post_page_buttons.locator(locators["post_page_unrepost_buttons"]).all()
            if len(repost_buttons) > 0:
                log.info("Unreposting post...")
                repost_buttons[0].click()
                confirm_simple = self.page.locator(locators["post_page_unrepost_mode_simple"]).all()
                if len(confirm_simple) > 0:
                    log.info("Confirming unrepost...")
                    confirm_simple[0].click()
                    log.info("Unreposted.")
                else:
                    log.error("Confirm unrepost button not found.")
            else:
                log.error("Repost button not found.")
        else:
            log.error("Repost button not found.")
    
    def post_check_if_reposted(self, post: PostStatusData):
        """
        Checks if the currently logged-in user has reposted the given post.

        Args:
            post (PostStatusData): The post to check.

        Returns:
            bool: True if the post is currently reposted, False if not.

        Raises:
            Exception: If neither repost nor unrepost buttons can be found.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            repost_buttons = post_page_buttons.locator(locators["post_page_repost_buttons"]).all()
            if len(repost_buttons) > 0:
                return True
            else:
                unrepost_buttons = post_page_buttons.locator(locators["post_page_unrepost_buttons"]).all()
                if len(unrepost_buttons) > 0:
                    return False
                else:
                    raise Exception("Repost buttons not found.")
                            
    def post_like(self, post: PostStatusData):
        """
        Likes the specified post.

        Args:
            post (PostStatusData): The post to like.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            like_buttons = post_page_buttons.locator(locators["post_page_like_button"]).all()
            if len(like_buttons) > 0:
                log.info("Liking post...")
                like_buttons[0].click()
                log.info("Liked.")
            else:
                log.error("Like button not found.")
            
    def post_unlike(self, post: PostStatusData):
        """
        Unlikes the specified post.

        Args:
            post (PostStatusData): The post to unlike.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            unlike_buttons = post_page_buttons.locator(locators["post_page_unlike_button"]).all()
            if len(unlike_buttons) > 0:
                log.info("Unliking post...")
                unlike_buttons[0].click()
                log.info("Unliked.")
            else:
                log.error("Unlike button not found.")
            
    def post_check_if_liked(self, post: PostStatusData):
        """
        Checks if the specified post is currently liked by the logged-in user.

        Args:
            post (PostStatusData): The post to check.

        Returns:
            bool: True if liked, False otherwise.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            like_buttons = post_page_buttons.locator(locators["post_page_like_button"]).all()
            if len(like_buttons) > 0:
                return True
            else:
                return False
        return False
        
    def post_bookmark(self, post: PostStatusData):
        """
        Bookmarks the specified post.

        Args:
            post (PostStatusData): The post to bookmark.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            bookmark_buttons = post_page_buttons.locator(locators["post_page_bookmark_button"]).all()
            if len(bookmark_buttons) > 0:
                log.info("Bookmarking post...")
                bookmark_buttons[0].click()
                log.info("Bookmarked.")
            else:
                log.error("Bookmark button not found.")
                
    def post_unbookmark(self, post: PostStatusData):
        """
        Removes a bookmark from the specified post.

        Args:
            post (PostStatusData): The post to unbookmark.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            unbookmark_buttons = post_page_buttons.locator(locators["post_page_unbookmark_button"]).all()
            if len(unbookmark_buttons) > 0:
                log.info("Unbookmarking post...")
                unbookmark_buttons[0].click()
                log.info("Unbookmarked.")
            else:
                log.error("Unbookmark button not found.")
                
    def post_check_if_bookmarked(self, post: PostStatusData):
        """
        Checks if the specified post is currently bookmarked by the logged-in user.

        Args:
            post (PostStatusData): The post to check.

        Returns:
            bool: True if bookmarked, False otherwise.
        """
        self.open_post(post)
        posts_page_buttons = self.page.locator(locators["post_page_buttons"]).all()
        if len(posts_page_buttons) > 0:
            post_page_buttons = posts_page_buttons[0]
            bookmark_buttons = post_page_buttons.locator(locators["post_page_bookmark_button"]).all()
            if len(bookmark_buttons) > 0:
                return True
            else:
                return False
        return False
    
    def go_to_post(self, post: PostStatusData):
        """
        Navigates directly to a post's URL.

        Args:
            post (PostStatusData): The post whose URL will be navigated to.
        """
        self.go_to(urljoin(self.base_url, post.post_url))

    def scrape_comments(self, post: PostStatusData = None, n_comments: int = -1,
                       show_all_replies: bool = True) -> list[list[str]]:
        """
        Scrapes comment threads from a specified post. Optionally loads more replies.

        Args:
            post (PostStatusData, optional): If provided, navigates to this post's URL first.
            n_comments (int): Maximum number of comments to gather (-1 means no limit).
            show_all_replies (bool): If True, attempts to click “Show more replies”.

        Returns:
            list[list[str]]: A list of threads, where each thread is a list of PostStatusData.
                             The method returns them in nested lists representing separate
                             conversation chains.

        Notes:
            - The scraping logic can be complex due to dynamically loading “show more replies”.
            - Threads are separated by separators or the “Discover more” section.
        """
        if post is not None:
            self.go_to_post(post)
        else:
            post = self.scrape_post()
        found_comments = 0 
        all_comments_data = []

        current_thread = []
        last_added_comment_url = None
        correct_index = True
        reload_comments = True
        end = False
        while True:
            last_found_comments = found_comments
            if end:
                if len(current_thread) > 0:
                    all_comments_data.append(current_thread)
                log.debug("Marked for ending, stopping.")
                break
            if reload_comments:
                log.debug("Reloading container locators...")
                content_section_containers = self.page.locator(locators["post_page_content_container"]).all()
                reload_comments = False
            for container in content_section_containers:
                add_post = container.locator(locators["post_page_comment_ad"]).all()
                if len(add_post) > 0:
                    log.debug("Detected add post, skipping...")
                    continue
                if show_all_replies:
                    show_more_replies = container.locator(locators["post_page_show_more_replies_button"]).all()
                    if len(show_more_replies) > 0:
                        log.debug("Detected show more replies button, clicking...")
                        show_more_replies[0].click()
                        self.wait_seconds(self._very_short_wait)
                        reload_comments = True
                        correct_index = False
                        log.debug("Locators marked for reloading.")
                        break
                separator = container.locator(locators["post_page_separator"]).all()
                if len(separator) > 0:
                    if len(current_thread) > 0:
                        log.debug("Separator found, ending thread.")
                        all_comments_data.append(current_thread)
                        current_thread = []
                        continue
                discover_more = container.locator(locators["post_discover_more_header"]).all()
                if len(discover_more) > 0:
                    log.debug("Discover more comments header found, marking for ending.")
                    end = True
                    break
                comment = container.locator(locators["post_page_comments_and_post"]).all()
                if len(comment) > 0:
                    log.debug("Comment found...")
                    try:
                        log.debug("Trying to extract comment...")
                        comment_data = self.extract_post_data(comment[0])
                        log.debug("Successfully extracted comment.")
                    except:
                        log.debug("Failed to extract comment, checking if it's the main post...")
                        comment_data = self.extract_post_data(comment[0], main_post=True)
                        log.debug("Successfully extracted main post, skipping...")
                        continue
                    log.debug("Checking if the comment should be added...")
                    if not correct_index:
                        log.debug("Checking if this comment is the last one added...")
                        if comment_data.post_url == last_added_comment_url:
                            correct_index = True
                            log.debug("Correct index found, will resume adding from the next comment")
                            continue
                        else:
                            log.debug("Incorrect index, skipping...")
                            continue
                    log.debug("Adding comment to thread...")
                    current_thread.append(comment_data)
                    last_added_comment_url = comment_data.post_url
                    found_comments += 1
            if n_comments > 0 and found_comments >= n_comments:
                log.debug("Found all comments requested, marking for ending.")
                end = True
                continue
            elif found_comments == last_found_comments:
                log.info("No more comments found, marking for ending.")
                end = True
                continue
            else:
                log.info("Need more comments. Scrolling down the lowest comment currently visible...")
                content_section_containers[-1].scroll_into_view_if_needed()
                reload_comments = True
                correct_index = False
                self.wait_seconds(self._very_short_wait)
                log.info("Finished scrolling.")
                continue          
        posts = all_comments_data[:n_comments] if n_comments > 0 and n_comments < len(all_comments_data) else all_comments_data
        log.info(f"Returning {len(posts)} comment threads with a total of {n_comments if n_comments > 0 and n_comments < found_comments else found_comments} comments.")
        return posts
    
    def acquire_own_profile_info(self):
        """
        Navigates to the user's own profile page and scrapes the profile information,
        storing it in `self.own_profile`.
        """
        log.info("Acquiring own profile info...")
        self.go_home()
        self.page.locator(locators["profile_page_menu_button"]).click()
        self.wait_seconds(self._short_wait)
        self.own_profile = self.scrape_user_profile()
        log.info("Own profile info acquired.")
        
    def scrape_user_profile(self, user_url: str = None) -> UserProfileData:
        """
        Scrapes profile data from the user's profile page.

        Args:
            user_url (str, optional): A relative or full URL to the user's profile.
                                      If not provided, uses the current page.

        Returns:
            UserProfileData: The scraped profile data (name, handle, stats, etc.).
        """
        if user_url:
            self.go_to(urljoin(self.base_url, user_url))
        log.info("Scraping user profile...")
        user_divs = self.page.locator(locators["profile_page_user_div"])
        user_name = user_divs.nth(0).inner_text()
        user_handle = user_divs.nth(1).inner_text()
        log.info(f"User: {user_name} ({user_handle})")
        headline_items = self.page.locator(locators["profile_headline_items"]).nth(0)
        join_date = headline_items.locator(locators["profile_headline_item_user_join_date"]).inner_text()
        location_div = headline_items.locator(locators["profile_headline_item_user_location"])
        location = location_div.nth(0).inner_text() if location_div.count() > 0 else None
        url_div = headline_items.locator(locators["profile_headline_item_user_url"])
        url = url_div.nth(0).get_attribute("href") if url_div.count() > 0 else None
        birthday_div = headline_items.locator(locators["profile_headline_item_user_birthday"])
        birthday = birthday_div.nth(0).inner_text() if birthday_div.count() > 0 else None
        log.info(f"Join date: {join_date}")
        log.info(f"Location: {location}")
        log.info(f"URL: {url}")
        log.info(f"Birthday: {birthday}")
        bio_div = headline_items.locator(locators["profile_headline_item_user_bio"])
        bio = bio_div.nth(0).inner_text() if bio_div.count() > 0 else None
        log.info(f"Bio: {bio}")
        follows = self.page.locator(locators["profile_headline_follows"])
        followers = follows.nth(1).inner_text().strip().split(" ")[0]
        following = follows.nth(0).inner_text().strip().split(" ")[0]
        log.info(f"Followers: {followers}")
        log.info(f"Following: {following}")
        user_url = self.page.url.replace(self.base_url, "")
        log.info(f"User URL: {user_url}")
        user_data = {
            "user_name": user_name,
            "user_handle": user_handle,
            "join_date": join_date,
            "location": location,
            "url": url,
            "birthday": birthday,
            "bio": bio,
            "followers": followers,
            "following": following,
            "user_url": user_url
        }
        return UserProfileData.from_dict(user_data)
    
    def is_following_user(self, user: UserProfileData):
        """
        Checks if the bot is following a given user.

        Args:
            user (UserProfileData): The user to check.

        Returns:
            bool: True if not following (follow button is visible), otherwise False.
        """
        log.info(f"Checking if following user: {user.user_handle}")
        self.go_to(urljoin(self.base_url, user.user_url))
        follow_button = self.page.locator(locators["profile_follow_unfollow_button"]).all()
        if len(follow_button) > 0:
            return follow_button[0].inner_text() == self.labels["follow"]
        return False
    
    def follow_user(self, user: UserProfileData):
        """
        Follows the specified user, if not already following.

        Args:
            user (UserProfileData): The user to follow.
        """
        log.info(f"Trying to follow user: {user.user_handle}")
        self.go_to(urljoin(self.base_url, user.user_url))
        follow_button = self.page.locator(locators["profile_follow_unfollow_button"]).all()
        if len(follow_button) > 0:
            if follow_button[0].inner_text() == self.labels["follow"]:
                follow_button[0].click()
                log.info("Followed.")
            else:
                log.info("Already following.")
        else:
            log.error("Follow button not found.")
    
    def unfollow_user(self, user: UserProfileData):
        """
        Unfollows the specified user, if currently following.

        Args:
            user (UserProfileData): The user to unfollow.
        """
        log.info(f"Trying to unfollow user: {user.user_handle}")
        self.go_to(urljoin(self.base_url, user.user_url))
        follow_button = self.page.locator(locators["profile_follow_unfollow_button"]).all()
        if len(follow_button) > 0:
            if follow_button[0].inner_text() == self.labels["following"] or follow_button[0].inner_text() == self.labels["unfollow"]:
                follow_button[0].click()
                self.wait_seconds(self._very_short_wait)
                pop_up_confirmation_button = self.page.locator(locators["profile_unfollow_popup_confirm_button"]).all()
                if len(pop_up_confirmation_button) > 0:
                    log.info("Unfollowing...")
                    pop_up_confirmation_button[0].click()
                    self.wait_seconds(self._very_short_wait)
                log.info("Unfollowed.")
            else:
                log.info("Not following.")
        else:
            log.error("Follow button not found.")
        
