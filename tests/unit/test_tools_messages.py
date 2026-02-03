"""Unit tests for message operation tools."""

from unittest.mock import MagicMock

from mcp.server.fastmcp import FastMCP

from instagram_mcp.client import InstagramClient
from instagram_mcp.models.schemas import DirectMessage
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
