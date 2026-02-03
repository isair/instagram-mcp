"""Unit tests for message operation tools."""

from datetime import datetime
from unittest.mock import MagicMock, patch

from mcp.server.fastmcp import FastMCP

from instagram_mcp.client import InstagramClient
from instagram_mcp.models.schemas import (
    DirectMessage,
    MediaType,
    MessageContent,
    ThreadUser,
)
from instagram_mcp.tools.messages import register_message_tools


class TestMessageTools:
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mcp = FastMCP("test")
        self.mock_client = MagicMock(spec=InstagramClient)
        register_message_tools(self.mcp, self.mock_client)

    def _get_tool_fn(self, name: str):
        """Get tool function by name."""
        for tool in self.mcp._tool_manager._tools.values():
            if tool.name == name:
                return tool.fn
        return None

    def test_send_message_to_users(self, sample_message: DirectMessage) -> None:
        self.mock_client.send_message.return_value = sample_message

        tool_fn = self._get_tool_fn("send_message")
        assert tool_fn is not None
        result = tool_fn(text="Hello", user_ids=["123"], thread_ids=None)

        assert result["success"] is True
        assert result["message_id"] == "111111111"
        assert result["text"] == "Hello"
        self.mock_client.send_message.assert_called_once_with(
            text="Hello", user_ids=["123"], thread_ids=None
        )

    def test_send_message_to_threads(self, sample_message: DirectMessage) -> None:
        self.mock_client.send_message.return_value = sample_message

        tool_fn = self._get_tool_fn("send_message")
        result = tool_fn(text="Hello", user_ids=None, thread_ids=["123456789"])

        assert result["success"] is True

    def test_send_message_no_target(self) -> None:
        tool_fn = self._get_tool_fn("send_message")
        result = tool_fn(text="Hello", user_ids=None, thread_ids=None)

        assert "error" in result
        assert "Must specify either user_ids or thread_ids" in result["error"]

    def test_send_message_failure(self) -> None:
        self.mock_client.send_message.return_value = None

        tool_fn = self._get_tool_fn("send_message")
        result = tool_fn(text="Hello", user_ids=["123"], thread_ids=None)

        assert result["success"] is False
        assert "error" in result

    def test_send_message_error(self) -> None:
        self.mock_client.send_message.side_effect = Exception("API Error")

        tool_fn = self._get_tool_fn("send_message")
        result = tool_fn(text="Hello", user_ids=["123"], thread_ids=None)

        assert "error" in result
        assert "API Error" in result["error"]

    def test_reply_to_thread_success(self, sample_message: DirectMessage) -> None:
        self.mock_client.reply_to_thread.return_value = sample_message

        tool_fn = self._get_tool_fn("reply_to_thread")
        assert tool_fn is not None
        result = tool_fn(thread_id="123456789", text="Reply")

        assert result["success"] is True
        assert result["message_id"] == "111111111"
        self.mock_client.reply_to_thread.assert_called_once_with(
            thread_id="123456789", text="Reply"
        )

    def test_reply_to_thread_failure(self) -> None:
        self.mock_client.reply_to_thread.return_value = None

        tool_fn = self._get_tool_fn("reply_to_thread")
        result = tool_fn(thread_id="123456789", text="Reply")

        assert result["success"] is False
        assert "error" in result

    def test_get_messages_success(self, sample_message: DirectMessage) -> None:
        self.mock_client.get_messages.return_value = [sample_message]

        tool_fn = self._get_tool_fn("get_messages")
        assert tool_fn is not None
        result = tool_fn(thread_id="123456789", amount=20)

        assert result["thread_id"] == "123456789"
        assert result["count"] == 1
        assert result["messages"][0]["message_id"] == "111111111"
        assert result["messages"][0]["sender"] == "test_user"

    def test_get_messages_empty(self) -> None:
        self.mock_client.get_messages.return_value = []

        tool_fn = self._get_tool_fn("get_messages")
        result = tool_fn(thread_id="123456789", amount=20)

        assert result["count"] == 0
        assert result["messages"] == []

    def test_get_messages_error(self) -> None:
        self.mock_client.get_messages.side_effect = Exception("API Error")

        tool_fn = self._get_tool_fn("get_messages")
        result = tool_fn(thread_id="123456789", amount=20)

        assert "error" in result
        assert "API Error" in result["error"]

    def test_delete_message_success(self) -> None:
        self.mock_client.delete_message.return_value = True

        tool_fn = self._get_tool_fn("delete_message")
        assert tool_fn is not None
        result = tool_fn(thread_id="123456789", message_id="111111111")

        assert result["success"] is True
        assert result["thread_id"] == "123456789"
        assert result["message_id"] == "111111111"
        self.mock_client.delete_message.assert_called_once_with(
            thread_id="123456789", message_id="111111111"
        )

    def test_delete_message_failure(self) -> None:
        self.mock_client.delete_message.return_value = False

        tool_fn = self._get_tool_fn("delete_message")
        result = tool_fn(thread_id="123456789", message_id="111111111")

        assert result["success"] is False

    def test_delete_message_error(self) -> None:
        self.mock_client.delete_message.side_effect = Exception("API Error")

        tool_fn = self._get_tool_fn("delete_message")
        result = tool_fn(thread_id="123456789", message_id="111111111")

        assert "error" in result
        assert "API Error" in result["error"]


class TestWaitForReplyTool:
    """Tests for the wait_for_reply tool."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mcp = FastMCP("test")
        self.mock_client = MagicMock(spec=InstagramClient)
        register_message_tools(self.mcp, self.mock_client)

    def _get_tool_fn(self, name: str):
        """Get tool function by name."""
        for tool in self.mcp._tool_manager._tools.values():
            if tool.name == name:
                return tool.fn
        return None

    def _create_message(
        self,
        message_id: str,
        text: str,
        is_sent_by_viewer: bool = False,
        username: str = "other_user",
    ) -> DirectMessage:
        """Create a mock DirectMessage for testing."""
        return DirectMessage(
            message_id=message_id,
            thread_id="123456789",
            sender=ThreadUser(user_id="999", username=username),
            content=MessageContent(text=text, media_type=MediaType.TEXT),
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            is_sent_by_viewer=is_sent_by_viewer,
        )

    @patch("instagram_mcp.tools.messages.time.sleep")
    @patch("instagram_mcp.tools.messages.time.time")
    def test_wait_for_reply_success(
        self, mock_time: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """Test successful detection of new reply."""
        # Simulate time progression: start, poll 1, poll 2 (message found), grace period
        mock_time.side_effect = [0, 3, 6, 6, 17]  # Extra calls for grace period check

        # First call: baseline (our last message)
        baseline_msg = self._create_message("100", "Hello", is_sent_by_viewer=True)
        # Second call: new message from other person
        new_msg = self._create_message("101", "Hey there!", is_sent_by_viewer=False)

        self.mock_client.get_messages.side_effect = [
            [baseline_msg],  # Initial baseline
            [baseline_msg],  # First poll - no new messages
            [new_msg, baseline_msg],  # Second poll - new message!
            [new_msg, baseline_msg],  # Grace period poll
        ]

        tool_fn = self._get_tool_fn("wait_for_reply")
        assert tool_fn is not None

        result = tool_fn(
            thread_id="123456789",
            timeout_minutes=5,
            poll_interval_seconds=3,
            double_text_grace_period_seconds=10,
        )

        assert result["success"] is True
        assert result["message_count"] == 1
        assert result["new_messages"][0]["text"] == "Hey there!"
        assert result["new_messages"][0]["sender"] == "other_user"

    @patch("instagram_mcp.tools.messages.time.sleep")
    @patch("instagram_mcp.tools.messages.time.time")
    def test_wait_for_reply_double_text(
        self, mock_time: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """Test catching double texts within grace period."""
        mock_time.side_effect = [0, 3, 3, 8, 8, 15]

        baseline_msg = self._create_message("100", "Hello", is_sent_by_viewer=True)
        msg1 = self._create_message("101", "Hey!", is_sent_by_viewer=False)
        msg2 = self._create_message("102", "Also...", is_sent_by_viewer=False)

        self.mock_client.get_messages.side_effect = [
            [baseline_msg],  # Initial
            [msg1, baseline_msg],  # First message detected
            [msg2, msg1, baseline_msg],  # Second message during grace period
            [msg2, msg1, baseline_msg],  # Grace period done
        ]

        tool_fn = self._get_tool_fn("wait_for_reply")
        result = tool_fn(
            thread_id="123456789",
            timeout_minutes=5,
            poll_interval_seconds=3,
            double_text_grace_period_seconds=10,
        )

        assert result["success"] is True
        assert result["message_count"] == 2
        # Should be in chronological order (oldest first)
        assert result["new_messages"][0]["text"] == "Hey!"
        assert result["new_messages"][1]["text"] == "Also..."

    @patch("instagram_mcp.tools.messages.time.sleep")
    @patch("instagram_mcp.tools.messages.time.time")
    def test_wait_for_reply_short_timeout(
        self, mock_time: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """Test short timeout behavior (5 minutes)."""
        # Simulate time passing until 5 min timeout (300 seconds)
        mock_time.side_effect = [0, 150, 301]  # Third call exceeds 5 min

        baseline_msg = self._create_message("100", "Hello", is_sent_by_viewer=True)
        self.mock_client.get_messages.return_value = [baseline_msg]

        tool_fn = self._get_tool_fn("wait_for_reply")
        result = tool_fn(
            thread_id="123456789",
            timeout_minutes=5,
            poll_interval_seconds=3,
            double_text_grace_period_seconds=10,
        )

        assert result["timeout"] is True
        assert result["waited_minutes"] == 5

    @patch("instagram_mcp.tools.messages.time.sleep")
    @patch("instagram_mcp.tools.messages.time.time")
    def test_wait_for_reply_long_timeout(
        self, mock_time: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """Test long timeout behavior (e.g., 120 minutes cooldown)."""
        # Simulate 2 hour wait - 120 minutes = 7200 seconds
        mock_time.side_effect = [0, 3600, 7201]  # Exceeds 120 min

        baseline_msg = self._create_message("100", "Hello", is_sent_by_viewer=True)
        self.mock_client.get_messages.return_value = [baseline_msg]

        tool_fn = self._get_tool_fn("wait_for_reply")
        result = tool_fn(
            thread_id="123456789",
            timeout_minutes=120,  # 2 hour cooldown
            poll_interval_seconds=3,
            double_text_grace_period_seconds=10,
        )

        assert result["timeout"] is True
        assert "waited_minutes" in result
        assert result["waited_minutes"] == 120

    @patch("instagram_mcp.tools.messages.time.sleep")
    @patch("instagram_mcp.tools.messages.time.time")
    def test_wait_for_reply_ignores_own_messages(
        self, mock_time: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """Test that our own messages are ignored."""
        mock_time.side_effect = [0, 3, 6, 6, 17]

        baseline_msg = self._create_message("100", "Hello", is_sent_by_viewer=True)
        our_msg = self._create_message("101", "Anyone there?", is_sent_by_viewer=True)
        their_msg = self._create_message("102", "Yeah!", is_sent_by_viewer=False)

        self.mock_client.get_messages.side_effect = [
            [baseline_msg],
            [our_msg, baseline_msg],  # Our follow-up - should be ignored
            [their_msg, our_msg, baseline_msg],  # Their reply
            [their_msg, our_msg, baseline_msg],
        ]

        tool_fn = self._get_tool_fn("wait_for_reply")
        result = tool_fn(
            thread_id="123456789",
            timeout_minutes=5,
            poll_interval_seconds=3,
            double_text_grace_period_seconds=10,
        )

        assert result["success"] is True
        assert result["message_count"] == 1
        assert result["new_messages"][0]["text"] == "Yeah!"

    def test_wait_for_reply_error(self) -> None:
        """Test error handling."""
        self.mock_client.get_messages.side_effect = Exception("Connection failed")

        tool_fn = self._get_tool_fn("wait_for_reply")
        result = tool_fn(thread_id="123456789", timeout_minutes=5)

        assert "error" in result
        assert "Connection failed" in result["error"]

    @patch("instagram_mcp.tools.messages.time.sleep")
    @patch("instagram_mcp.tools.messages.time.time")
    def test_wait_for_reply_race_condition(
        self, mock_time: MagicMock, mock_sleep: MagicMock
    ) -> None:
        """Test race condition: message arrives while we're responding.

        Scenario:
        1. They send msg 100
        2. We respond with msg 101
        3. They send msg 102 WHILE we're responding (arrives before we call wait_for_reply)
        4. We call wait_for_reply - should detect msg 102!

        The bug: if baseline is set to newest message overall (102), we miss it.
        The fix: baseline should be OUR newest message (101), so 102 is detected.
        """
        # Use iterator to simulate time passing - buggy code will loop until timeout
        # Each call increments by 100 seconds to quickly hit timeout
        time_counter = {"value": 0}

        def mock_time_fn():
            time_counter["value"] += 100
            return time_counter["value"]

        mock_time.side_effect = mock_time_fn

        # Their message that triggered our response
        their_first_msg = self._create_message("100", "Hey!", is_sent_by_viewer=False)
        # Our response
        our_response = self._create_message("101", "Hi there!", is_sent_by_viewer=True)
        # Their message that arrived WHILE we were responding (race condition)
        their_race_msg = self._create_message(
            "102", "Also wanted to ask...", is_sent_by_viewer=False
        )

        # When wait_for_reply is called, the thread already has all 3 messages
        # (their race msg arrived before we started waiting)
        self.mock_client.get_messages.return_value = [
            their_race_msg,
            our_response,
            their_first_msg,
        ]

        tool_fn = self._get_tool_fn("wait_for_reply")
        result = tool_fn(
            thread_id="123456789",
            timeout_minutes=5,
            poll_interval_seconds=3,
            double_text_grace_period_seconds=10,
        )

        # Should detect msg 102 even though it arrived before we started waiting
        # Because it arrived AFTER our last sent message (101)
        # BUG: Current code will return 'timeout' because it misses msg 102
        assert result.get("success") is True, f"Expected success, got: {result}"
        assert result["message_count"] == 1
        assert result["new_messages"][0]["text"] == "Also wanted to ask..."
