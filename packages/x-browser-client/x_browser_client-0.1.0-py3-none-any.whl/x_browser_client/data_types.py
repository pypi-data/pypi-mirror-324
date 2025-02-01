"""
This module defines data structures for posts and user profiles:
- PostStatusData: encapsulates tweet-like data such as user handle,
  text, attachments, replies, likes, etc.
- UserProfileData: encapsulates basic user profile data such as name,
  handle, join date, location, followers, etc.
"""

import re
from typing import Literal, Union


def _prefixed_string_number_to_int(number_string: str) -> int:
    """
    Converts a string potentially containing a 'k' or 'm' suffix into an integer.
    For example, "1.2k" -> 1200, "15.6M" -> 15600000.

    Args:
        number_string (str): A string representing a number with optional suffix ('k' or 'm').

    Returns:
        int: The integer conversion of the string.

    Raises:
        Exception: If the conversion fails for any reason.
    """
    try:
        number_string = number_string.replace(",", "").strip()
        mult = 1
        if 'k' in number_string.lower():
            mult = 1000
        elif 'm' in number_string.lower():
            mult = 1000000
        # preserve only digits and decimal points
        number_string = re.sub(r'[^\d.]', '', number_string)
        if len(number_string) == 0:
            return 0
        return int(float(number_string) * mult)
    except Exception as e:
        print(f"Error converting {number_string} to int")
        raise e


class PostStatusData:
    """
    Represents a single post (tweet) on x.com, including
    user info, text, attachments, and engagement stats.
    """

    def __init__(
        self,
        user_handle: str,
        user_name: str,
        user_url: str,
        posted: str,
        post_url: str,
        post_text: str,
        post_attachments: list[dict[str, str]],
        replies: str,
        reposts: str,
        likes: str,
        views: str,
    ) -> None:
        """
        Initializes a PostStatusData object.

        Args:
            user_handle (str): The username handle (e.g., "@somebody").
            user_name (str): The display name of the user.
            user_url (str): The relative URL to the user's profile.
            posted (str): The posted time string (may be raw or partial).
            post_url (str): The URL (or relative path) to the post.
            post_text (str): The text content of the post.
            post_attachments (list[dict[str, str]]): A list of attachments (images, links, polls, etc.).
            replies (str): A string representing the number of replies (including suffixes like 'k', 'm').
            reposts (str): A string representing the number of reposts (retweets).
            likes (str): A string representing the number of likes.
            views (str): A string representing the number of views.
        """
        self.user_handle = user_handle
        self.user_name = user_name
        self.user_url = user_url
        self.posted = posted
        self.post_url = post_url
        self.post_text = post_text
        self.post_attachments = post_attachments if post_attachments else []
        self.post_id = self._post_id_from_url(post_url) 
        self.replies = _prefixed_string_number_to_int(replies) if isinstance(replies, str) else replies
        self.reposts = _prefixed_string_number_to_int(reposts) if isinstance(reposts, str) else reposts 
        self.likes = _prefixed_string_number_to_int(likes) if isinstance(likes, str) else likes
        self.views = _prefixed_string_number_to_int(views) if isinstance(views, str) else views
        
    def __repr__(self) -> str:
        return (
            f"PostData(user_handle={self.user_handle}, user_name={self.user_name}, "
            f"user_url={self.user_url}, posted={self.posted}, post_url={self.post_url}, "
            f"post_text={self.post_text}, post_attachments={self.post_attachments}, "
            f"post_id={self.post_id}, replies={self.replies}, reposts={self.reposts}, "
            f"likes={self.likes}, views={self.views})"
        )
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def _post_id_from_url(self, url: str) -> str:
        """
        Extracts the numeric post ID from a post URL using regex.

        Args:
            url (str): The post URL (or relative path).

        Returns:
            str or None: The extracted numeric ID if found, otherwise None.
        """
        post_id = re.search(r"/status/(\d+)", url)
        return post_id.group(1) if post_id else None
    
    def to_dict(self) -> dict:
        """
        Serializes this post into a dictionary.

        Returns:
            dict: A dictionary containing post fields.
        """
        return {
            "user_handle": self.user_handle,
            "user_name": self.user_name,
            "user_url": self.user_url,
            "posted": self.posted,
            "post_url": self.post_url,
            "post_text": self.post_text,
            "post_attachments": self.post_attachments,
            "post_id": self.post_id,
            "replies": self.replies,
            "reposts": self.reposts,
            "likes": self.likes,
            "views": self.views,
        }

    @staticmethod
    def from_dict(data: dict) -> "PostStatusData":
        """
        Reconstructs a PostStatusData object from a dictionary.

        Args:
            data (dict): A dictionary containing post fields.

        Returns:
            PostStatusData: A new instance populated with the dictionary data.
        """
        return PostStatusData(
            user_handle=data["user_handle"],
            user_name=data["user_name"],
            user_url=data["user_url"],
            posted=data["posted"],
            post_url=data["post_url"],
            post_text=data["post_text"],
            post_attachments=data["post_attachments"],
            replies=data["replies"],
            reposts=data["reposts"],
            likes=data["likes"],
            views=data["views"],
        )
        
    def has_text(self) -> bool:
        """
        Checks if the post has any text.

        Returns:
            bool: True if the post_text is non-empty, else False.
        """
        return self.post_text is not None and len(self.post_text) > 0
    
    def has_attachments(self,
                        attachment_type: Literal["image","video","poll","link","quoted_post","all"] = "all",
                        only_with_text: bool = False) -> bool:
        """
        Determines if the post has attachments of a specified type.

        Args:
            attachment_type (Literal["image","video","poll","link","quoted_post","all"]):
                The type of attachment to check for. 'all' checks for any type.
            only_with_text (bool): If True, only consider attachments that have non-empty "text" field.

        Returns:
            bool: True if matching attachments exist, else False.
        """
        if attachment_type == "any":
            if len(self.post_attachments) > 0:
                for attachment in self.post_attachments:
                    if not only_with_text or attachment["text"].strip() != "":
                        return True
                return False
            return False
        for attachment in self.post_attachments:
            if attachment["type"] == attachment_type:
                if not only_with_text or ("text" in attachment.keys() and attachment["text"].strip() != ""):
                    return True
        return False
    
    def has_attachments_with_text(self, attachment_type: Literal["image","video","poll","link","quoted_post","all"] = "all") -> bool:
        """
        Checks if the post has attachments of a certain type that also contain text.

        Args:
            attachment_type: The type of attachment to look for.

        Returns:
            bool: True if such attachments exist, False otherwise.
        """
        return self.has_attachments(attachment_type, only_with_text=True)
    
    def has_link_attachments(self, only_with_text=False) -> bool:
        """Shortcut to check if there are any link attachments."""
        return self.has_attachments("link", only_with_text)
    
    def has_image_attachments(self, only_with_text=False) -> bool:
        """Shortcut to check if there are any image attachments."""
        return self.has_attachments("image", only_with_text)
    
    def has_video_attachments(self, only_with_text=False) -> bool:
        """Shortcut to check if there are any video attachments."""
        return self.has_attachments("video", only_with_text)
    
    def has_poll_attachments(self, only_with_text=False) -> bool:
        """Shortcut to check if there are any poll attachments."""
        return self.has_attachments("poll", only_with_text)
    
    def has_post_attachments(self, only_with_text=False) -> bool:
        """Shortcut to check if there are any quoted post attachments."""
        return self.has_attachments("quoted_post", only_with_text)  
    
    def get_attachments(self,
                        attachment_type: Literal["image","video","poll","link","quoted_post","all"] = "all",
                        only_with_text: bool = False) -> list[dict[str, Union[list[str], str]]]:
        """
        Retrieves a list of attachments of a given type, optionally filtered
        to only those with non-empty text.

        Args:
            attachment_type: The type of attachments to return.
            only_with_text (bool): If True, only returns attachments that have non-empty text.

        Returns:
            list[dict[str, Union[list[str], str]]]: A list of matching attachment dictionaries.
        """
        if attachment_type == "any":
            if len(self.post_attachments) > 0:
                attachments = []
                for attachment in self.post_attachments:
                    if not only_with_text or attachment["text"].strip() != "":
                        attachments.append(attachment)
                return attachments
            return []
        filtered_attachments = []
        for attachment in self.post_attachments:
            if attachment["type"] == attachment_type:
                if not only_with_text or ("text" in attachment.keys() and attachment["text"].strip() != ""):
                    filtered_attachments.append(attachment)
        return filtered_attachments
    
    def get_attachments_with_text(self, attachment_type: Literal["image","video","poll","link","quoted_post","all"] = "all") -> list[dict[str, Union[list[str], str]]]:
        """
        Retrieves attachments of a certain type that also have non-empty text.

        Args:
            attachment_type: The type of attachments to look for.

        Returns:
            list[dict[str, Union[list[str], str]]]: A list of matching attachment dictionaries.
        """
        return self.get_attachments(attachment_type, only_with_text=True)
    
    def get_video_attachments(self) -> list[dict[str, str]]:
        """Returns all video attachments."""
        return self.get_attachments(attachment_type="video")
    
    def get_image_attachments(self) -> list[dict[str, str]]:
        """Returns all image attachments."""
        return self.get_attachments(attachment_type="image")
    
    def get_poll_attachments(self) -> list[dict[str, list[str]]]:
        """Returns all poll attachments."""
        return self.get_attachments(attachment_type="poll")
    
    def get_link_attachments(self) -> list[dict[str, str]]:
        """Returns all link attachments."""
        return self.get_attachments(attachment_type="link")
    
    def get_post_attachments(self) -> list[dict[str, str]]:
        """Returns all quoted post attachments."""
        return self.get_attachments(attachment_type="quoted_post")
    
    @classmethod
    def get_poll_options(cls, poll_attachment: dict[str, list[str]]) -> list[str]:
        """
        Extracts the poll options from a poll attachment.

        Args:
            poll_attachment (dict): A dictionary with a "options" key containing poll choices.

        Returns:
            list[str]: The list of poll options.
        """
        return poll_attachment["options"]
    
    def get_views(self) -> int:
        """Returns the integer number of views."""
        return self.views
    
    def get_likes(self) -> int:
        """Returns the integer number of likes."""
        return self.likes
    
    def get_reposts(self) -> int:
        """Returns the integer number of reposts."""
        return self.reposts
    
    def get_replies(self) -> int:
        """Returns the integer number of replies."""
        return self.replies
    

class UserProfileData:
    """
    Represents a user profile on x.com, including:
    name, handle, join date, location, URL, birthday, bio, follower and following counts, etc.
    """

    def __init__(
        self,
        user_name: str,
        user_handle: str,
        join_date: str,
        followers: Union[str, int],
        following: Union[str, int],
        user_url: str,
        location: str = None,
        url: str = None,
        birthday: str = None,
        bio: str = None
    ) -> None:
        """
        Initializes a UserProfileData object.

        Args:
            user_name (str): The display name of the user.
            user_handle (str): The user handle (e.g., "@someone").
            join_date (str): The user's join date string.
            followers (Union[str,int]): Number of followers (raw or integer).
            following (Union[str,int]): Number of following (raw or integer).
            user_url (str): Relative or full URL of the user's profile.
            location (str, optional): The user's location.
            url (str, optional): A homepage or external link from profile.
            birthday (str, optional): The user's birthday string.
            bio (str, optional): The user's bio text.
        """
        self.user_name = user_name
        self.user_handle = user_handle
        self.join_date = join_date
        self.location = location
        self.url = url
        self.birthday = birthday
        self.bio = bio
        self.followers = _prefixed_string_number_to_int(followers) if isinstance(followers, str) else followers
        self.following = _prefixed_string_number_to_int(following) if isinstance(following, str) else following
        self.user_url = user_url
        
    def __repr__(self) -> str:
        return (
            f"UserProfileData(user_name={self.user_name}, user_handle={self.user_handle}, "
            f"join_date={self.join_date}, location={self.location}, url={self.url}, "
            f"birthday={self.birthday}, bio={self.bio}, followers={self.followers}, "
            f"following={self.following}, user_url={self.user_url})"
        )
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def to_dict(self) -> dict:
        """
        Serializes the user profile data into a dictionary.

        Returns:
            dict: A dictionary containing all fields in this user profile.
        """
        return {
            "user_name": self.user_name,
            "user_handle": self.user_handle,
            "join_date": self.join_date,
            "location": self.location,
            "url": self.url,
            "birthday": self.birthday,
            "bio": self.bio,
            "followers": self.followers,
            "following": self.following,
            "user_url": self.user_url
        }
        
    @staticmethod
    def from_dict(data: dict) -> "UserProfileData":
        """
        Reconstructs a UserProfileData object from a dictionary.

        Args:
            data (dict): A dictionary containing user profile fields.

        Returns:
            UserProfileData: A new instance populated with the dictionary data.
        """
        return UserProfileData(
            user_name=data["user_name"],
            user_handle=data["user_handle"],
            join_date=data["join_date"],
            location=data["location"],
            url=data["url"],
            birthday=data["birthday"],
            bio=data["bio"],
            followers=data["followers"],
            following=data["following"],
            user_url=data["user_url"]
        )
        
    def has_location(self) -> bool:
        """Checks if a location is set."""
        return self.location is not None and len(self.location) > 0
    
    def has_url(self) -> bool:
        """Checks if a URL is present in the profile."""
        return self.url is not None and len(self.url) > 0
    
    def has_birthday(self) -> bool:
        """Checks if a birthday is listed."""
        return self.birthday is not None and len(self.birthday) > 0
    
    def has_bio(self) -> bool:
        """Checks if a bio is present."""
        return self.bio is not None and len(self.bio) > 0
    
    def get_followers(self) -> int:
        """Returns the integer number of followers."""
        return self.followers
    
    def get_following(self) -> int:
        """Returns the integer number of following."""
        return self.following
    
    def get_user_name(self) -> str:
        """Returns the user's display name."""
        return self.user_name
    
    def get_user_handle(self) -> str:
        """Returns the user's handle (e.g. '@someone')."""
        return self.user_handle
    
    def get_join_date(self) -> str:
        """Returns the join date string."""
        return self.join_date
    
    def get_location(self) -> str:
        """Returns the location string (if any)."""
        return self.location
    
    def get_url(self) -> str:
        """Returns the external URL (if any)."""
        return self.url
    
    def get_birthday(self) -> str:
        """Returns the birthday string (if any)."""
        return self.birthday
    
    def get_bio(self) -> str:
        """Returns the bio text (if any)."""
        return self.bio
    
    def get_user_url(self) -> str:
        """Returns the relative or full URL to the user’s profile page."""
        return self.user_url
    
