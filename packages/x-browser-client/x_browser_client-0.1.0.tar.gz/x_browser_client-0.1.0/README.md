# x_browser_client

**x_browser_client** is a Python package that automates **x.com** (formerly Twitter) interactions using [Playwright](https://playwright.dev/python/). This library can log in, post new tweets, scrape timelines and posts, reply, like, repost, quote, bookmark, and follow/unfollow accounts.

## Features

- **Automatic or manual login** to x.com  
- **Posting and replying** to tweets  
- **Scraping** timelines, individual posts, and comment threads  
- **Liking, reposting, quoting, bookmarking** tweets  
- **Following and unfollowing** users  
- **Session management** to persist cookies (via Playwright contexts)

## Installation

### Via PyPI

```bash
pip install x_browser_client
```

### Via GitHub

```bash
git clone https://github.com/laelhalawani/x_browser_client
cd x_browser_client
pip install .
```

> **Note**: If you have not installed Playwright browsers before, you may need to run:
>
> ```bash
> playwright install chromium
> ```
>
> This ensures that Playwright can automate the Chromium browser.

## Requirements

- Python 3.7 or higher
- [Playwright for Python](https://pypi.org/project/playwright/)
- (Optional) [dotenv](https://pypi.org/project/python-dotenv/) for loading environment variables

## Basic Usage

Below is a minimal example of how to use **x_browser_client**:

```python
from x_browser_client import XClient, PostStatusData

# Create an XClient instance
client = XClient(
    timeout=60,         # default timeout (seconds) for browser interactions
    locale="en-US",     # language/locale
    post_character_limit=280
)

# Start the client, which:
# 1) Opens the browser
# 2) Loads or creates a session context if context_name is passed
# 3) Attempts login (auto or manual)
client.start_client(context_name="my_session", accept_cookies=True, skip_notifications=True)

# Scrape some of the latest posts from the 'for_you' tab
new_posts = client.scrape_new_posts(num_posts=5, tab="for_you")

# Iterate over posts and optionally interact
for post in new_posts:
    print(post)  # shows basic info about the post
    if post.has_text():
        # Like the post
        client.post_like(post)

# Exit the client, optionally saving context so next time it can reuse login
client.exit_client(save_context=True, close_browser_after=0)
```

### Environment Variables

You can store your X credentials (login, password, username) in environment variables (e.g., in a `.env` file):

```
X_LOGIN=myEmailOrPhone
X_PASSWORD=mySecurePassword
X_USERNAME=myActualUsername
```

The **XClient** will automatically pick them up if you do not explicitly set them:

```python
client = XClient()
client.start_client()
```

## Additional Examples

Refer to [examples.py](examples.py) or the repository's `examples.py` file for more in-depth usage, including:
- Replying to a post with AI-generated content
- Scraping specific post threads
- Following or unfollowing a user
- Manually controlling cookies and contexts

## Contributing

Contributions are welcome! To set up a development environment:
1. Clone the repository and install in editable mode:
   ```bash
   git clone https://github.com/laelhalawani/x_browser_client
   cd x_browser_client
   pip install -e .
   ```
2. (Optional) Install additional dev dependencies for linting/testing as needed.

Please open issues or submit pull requests on [GitHub](https://github.com/laelhalawani/x_browser_client).

---

**Disclaimer**: This package is intended solely for educational and testing purposes. Be aware of any usage constraints or policies on x.com, and ensure compliance with all terms of service and legal requirements.
