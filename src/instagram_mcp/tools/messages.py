"""Message operation tools for Instagram MCP Server.

This module provides MCP tools for sending, receiving, and managing
Instagram Direct Messages.
"""

import logging
import time
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

    @mcp.tool()
    def wait_for_reply(
        thread_id: str,
        timeout_minutes: int = 5,
        poll_interval_seconds: int = 3,
        double_text_grace_period_seconds: int = 10,
    ) -> dict[str, Any]:
        """Wait for new messages in a thread. Blocks until reply arrives or timeout.

        This tool polls Instagram for new messages and waits for the other person
        to respond. Once a response is detected, it waits an additional grace period
        to catch double/triple texts, then returns all new messages at once.

        Use variable timeout_minutes based on your strategy:
        - 5 minutes: Quick checkpoint, good for active conversations
        - 30-60 minutes: Medium wait after soft resistance
        - 120-180 minutes: Longer cooldown after backing off
        - Longer: Waiting until morning, respecting their schedule

        Args:
            thread_id: ID of the thread to monitor.
            timeout_minutes: How long to wait before returning (default: 5).
                Use shorter times for active convos, longer for cooldowns.
            poll_interval_seconds: How often to check for new messages (default: 3).
            double_text_grace_period_seconds: Extra wait time after first reply
                to catch rapid follow-up messages (default: 10).

        Returns:
            On reply: Object with 'success', 'new_messages' array, 'waited_seconds'.
            On timeout: Object with 'timeout', 'waited_minutes'.
        """
        try:
            # Get current messages to establish baseline
            current_messages = client.get_messages(thread_id=thread_id, amount=10)

            # Find OUR latest sent message as baseline (not the newest overall)
            # This prevents a race condition where they send a message while we're
            # responding - if we used the newest message overall as baseline, we'd
            # miss their message because it would BE the baseline
            our_last_message_id = None
            for msg in current_messages:
                if msg.is_sent_by_viewer:
                    our_last_message_id = msg.message_id
                    break

            logger.info(
                "Waiting for reply in thread %s (baseline: our msg %s)",
                thread_id,
                our_last_message_id,
            )

            timeout_seconds = timeout_minutes * 60
            start_time = time.time()
            first_new_message_time = None

            while True:
                elapsed = time.time() - start_time

                # Check for timeout
                if elapsed >= timeout_seconds:
                    waited_minutes = int(elapsed / 60)
                    return {
                        "timeout": True,
                        "thread_id": thread_id,
                        "waited_minutes": waited_minutes,
                    }

                # Poll for new messages
                messages = client.get_messages(thread_id=thread_id, amount=10)

                # Find new messages (not from us, newer than our last message)
                new_messages = []
                for msg in messages:
                    # Stop if we hit our baseline (our last sent message)
                    if our_last_message_id and msg.message_id == our_last_message_id:
                        break
                    # Only include messages NOT from us
                    if not msg.is_sent_by_viewer:
                        new_messages.append(msg)

                if new_messages:
                    # First new message detected
                    if first_new_message_time is None:
                        first_new_message_time = time.time()
                        logger.info(
                            "New message detected, waiting %ds for double texts...",
                            double_text_grace_period_seconds,
                        )

                    # Check if grace period has passed
                    grace_elapsed = time.time() - first_new_message_time
                    if grace_elapsed >= double_text_grace_period_seconds:
                        # Grace period done, return all new messages
                        # Reverse so oldest is first (natural reading order)
                        new_messages.reverse()

                        return {
                            "success": True,
                            "thread_id": thread_id,
                            "new_messages": [
                                {
                                    "message_id": m.message_id,
                                    "sender": m.sender.username,
                                    "text": m.content.text,
                                    "media_type": m.content.media_type.value,
                                    "timestamp": m.timestamp.isoformat(),
                                }
                                for m in new_messages
                            ],
                            "message_count": len(new_messages),
                            "waited_seconds": int(elapsed),
                        }

                # Sleep before next poll
                time.sleep(poll_interval_seconds)

        except Exception as e:
            logger.exception("Error waiting for reply in thread %s", thread_id)
            return {"error": str(e), "thread_id": thread_id}
