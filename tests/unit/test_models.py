"""Unit tests for Pydantic models."""

from datetime import datetime

import pytest

from instagram_mcp.models.schemas import (
    DirectMessage,
    DirectThread,
    MediaType,
    MessageContent,
    ThreadUser,
)


class TestMediaType:
    def test_media_type_values(self) -> None:
        assert MediaType.TEXT.value == "text"
        assert MediaType.PHOTO.value == "photo"
        assert MediaType.VIDEO.value == "video"
        assert MediaType.VOICE.value == "voice"
        assert MediaType.LINK.value == "link"
        assert MediaType.MEDIA_SHARE.value == "media_share"
        assert MediaType.PROFILE.value == "profile"
        assert MediaType.REEL_SHARE.value == "reel_share"
        assert MediaType.STORY_SHARE.value == "story_share"
        assert MediaType.UNKNOWN.value == "unknown"


class TestThreadUser:
    def test_thread_user_required_fields(self) -> None:
        user = ThreadUser(user_id="123", username="test")

        assert user.user_id == "123"
        assert user.username == "test"
        assert user.full_name == ""
        assert user.profile_pic_url is None
        assert user.is_verified is False

    def test_thread_user_all_fields(self) -> None:
        user = ThreadUser(
            user_id="123",
            username="test",
            full_name="Test User",
            profile_pic_url="https://example.com/pic.jpg",
            is_verified=True,
        )

        assert user.full_name == "Test User"
        assert user.profile_pic_url == "https://example.com/pic.jpg"
        assert user.is_verified is True

    def test_thread_user_missing_required(self) -> None:
        with pytest.raises(ValueError):
            ThreadUser(username="test")  # type: ignore[call-arg]


class TestMessageContent:
    def test_message_content_defaults(self) -> None:
        content = MessageContent()

        assert content.text is None
        assert content.media_url is None
        assert content.media_type == MediaType.TEXT

    def test_message_content_text(self) -> None:
        content = MessageContent(text="Hello!")

        assert content.text == "Hello!"

    def test_message_content_media(self) -> None:
        content = MessageContent(
            media_url="https://example.com/photo.jpg",
            media_type=MediaType.PHOTO,
        )

        assert content.media_url == "https://example.com/photo.jpg"
        assert content.media_type == MediaType.PHOTO


class TestDirectMessage:
    def test_direct_message_required_fields(self) -> None:
        user = ThreadUser(user_id="123", username="test")
        content = MessageContent(text="Hello!")
        timestamp = datetime(2024, 1, 15, 10, 30, 0)

        msg = DirectMessage(
            message_id="111111111",
            thread_id="thread_001",
            sender=user,
            content=content,
            timestamp=timestamp,
        )

        assert msg.message_id == "111111111"
        assert msg.thread_id == "thread_001"
        assert msg.sender.username == "test"
        assert msg.content.text == "Hello!"
        assert msg.timestamp == timestamp
        assert msg.is_sent_by_viewer is False

    def test_direct_message_sent_by_viewer(self) -> None:
        user = ThreadUser(user_id="123", username="test")
        content = MessageContent(text="Hello!")
        timestamp = datetime(2024, 1, 15, 10, 30, 0)

        msg = DirectMessage(
            message_id="111111111",
            thread_id="thread_001",
            sender=user,
            content=content,
            timestamp=timestamp,
            is_sent_by_viewer=True,
        )

        assert msg.is_sent_by_viewer is True


class TestDirectThread:
    def test_direct_thread_required_fields(self) -> None:
        thread = DirectThread(thread_id="thread_001")

        assert thread.thread_id == "thread_001"
        assert thread.thread_title == ""
        assert thread.users == []
        assert thread.last_activity_at is None
        assert thread.is_group is False
        assert thread.is_muted is False
        assert thread.unread is False
        assert thread.message_count == 0
        assert thread.messages == []

    def test_direct_thread_all_fields(self) -> None:
        user = ThreadUser(user_id="123", username="test")
        content = MessageContent(text="Hello!")
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        msg = DirectMessage(
            message_id="111111111",
            thread_id="thread_001",
            sender=user,
            content=content,
            timestamp=timestamp,
        )

        thread = DirectThread(
            thread_id="thread_001",
            thread_title="Test Thread",
            users=[user],
            last_activity_at=timestamp,
            is_group=True,
            is_muted=True,
            unread=True,
            message_count=1,
            messages=[msg],
        )

        assert thread.thread_title == "Test Thread"
        assert len(thread.users) == 1
        assert thread.last_activity_at == timestamp
        assert thread.is_group is True
        assert thread.is_muted is True
        assert thread.unread is True
        assert thread.message_count == 1
        assert len(thread.messages) == 1
