"""Message operation tools for Instagram MCP Server.

This module provides MCP tools for sending, receiving, and managing
Instagram Direct Messages.
"""

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from instagram_mcp.client import InstagramClient

logger = logging.getLogger("instagram_mcp")


def register_message_tools(mcp: "FastMCP", client: "InstagramClient") -> None:
    """Register message operation tools with the MCP server.

    Args:
        mcp: FastMCP server instance.
        client: Instagram client instance.
    """

    @mcp.tool()
    def send_message(
        text: str,
        user_ids: list[str] | None = None,
        thread_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Send a text message to users or existing threads.

        Args:
            text: Message text to send.
            user_ids: List of user IDs to send to (creates new threads if needed).
            thread_ids: List of thread IDs to send to (existing conversations).

        Returns:
            Object with 'success', 'message_id', and 'thread_id' on success,
            or 'error' on failure. Must provide either user_ids or thread_ids.
        """
        if not user_ids and not thread_ids:
            return {"error": "Must specify either user_ids or thread_ids"}

        try:
            message = client.send_message(
                text=text,
                user_ids=user_ids,
                thread_ids=thread_ids,
            )
            if message:
                return {
                    "success": True,
                    "message_id": message.message_id,
                    "thread_id": message.thread_id,
                    "text": text,
                }
            return {"success": False, "error": "Failed to send message"}
        except Exception as e:
            logger.exception("Error sending message")
            return {"error": str(e)}

    @mcp.tool()
    def reply_to_thread(thread_id: str, text: str) -> dict[str, Any]:
        """Reply to an existing conversation thread.

        Args:
            thread_id: ID of the thread to reply to.
            text: Message text to send.

        Returns:
            Object with 'success', 'message_id', and 'thread_id' on success.
        """
        try:
            message = client.reply_to_thread(thread_id=thread_id, text=text)
            if message:
                return {
                    "success": True,
                    "message_id": message.message_id,
                    "thread_id": message.thread_id,
                    "text": text,
                }
            return {"success": False, "error": "Failed to send reply"}
        except Exception as e:
            logger.exception("Error replying to thread %s", thread_id)
            return {"error": str(e), "thread_id": thread_id}

    @mcp.tool()
    def get_messages(thread_id: str, amount: int = 20) -> dict[str, Any]:
        """Get messages from a thread.

        Args:
            thread_id: ID of the thread to get messages from.
            amount: Maximum number of messages to fetch (default: 20).

        Returns:
            Object with 'thread_id', 'messages' array containing objects with
            message_id, sender, text, media_type, timestamp, is_sent_by_viewer.
        """
        try:
            messages = client.get_messages(thread_id=thread_id, amount=amount)
            return {
                "thread_id": thread_id,
                "messages": [
                    {
                        "message_id": m.message_id,
                        "sender": m.sender.username,
                        "sender_id": m.sender.user_id,
                        "text": m.content.text,
                        "media_type": m.content.media_type.value,
                        "media_url": m.content.media_url,
                        "timestamp": m.timestamp.isoformat(),
                        "is_sent_by_viewer": m.is_sent_by_viewer,
                        "seen_since": m.seen_since,
                    }
                    for m in messages
                ],
                "count": len(messages),
            }
        except Exception as e:
            logger.exception("Error getting messages for thread %s", thread_id)
            return {"error": str(e), "thread_id": thread_id}

    @mcp.tool(annotations={"destructive": True})
    def delete_message(thread_id: str, message_id: str) -> dict[str, Any]:
        """Delete a message from a thread.

        Args:
            thread_id: ID of the thread containing the message.
            message_id: ID of the message to delete.

        Returns:
            Object with 'success' boolean, 'thread_id', and 'message_id'.
        """
        try:
            success = client.delete_message(thread_id=thread_id, message_id=message_id)
            return {
                "success": success,
                "thread_id": thread_id,
                "message_id": message_id,
            }
        except Exception as e:
            logger.exception(
                "Error deleting message %s from thread %s", message_id, thread_id
            )
            return {"error": str(e), "thread_id": thread_id, "message_id": message_id}
