from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from workhub.db_connection import Base


class Conversation(Base):
    """
    One chat session with the AI Assistant (SRS Module 11).

    Kept deliberately minimal: a conversation is just "who owns it" + an
    optional title + when it was started. All the actual back-and-forth
    lives in the Message table below, linked by conversation_id.
    """

    __tablename__ = "chat_conversations"

    conversation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # updated_at lets you sort "most recently active" conversations first in
    # a chat list UI, instead of only "most recently created" -- this is
    # what every real chat product (ChatGPT, Slack, Intercom) actually sorts
    # by, since a conversation started yesterday but replied to just now
    # should show up at the top.
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Message(Base):
    """
    A single message inside a conversation (SRS Module 11).

    - role: "user" or "assistant" -- who said this message. Kept as a plain
      string (like Task.status) rather than a separate table, since there
      are only ever these two values.
    - content: the actual prompt or AI response text.

    Every "turn" of the chat is 2 rows: one role="user" row for what the
    person typed, one role="assistant" row for what Grok replied. This is
    what lets /chat/{conversation_id} rebuild the full history to send back
    to the LLM on the next message, and what "View previous conversations"
    reads from.
    """

    __tablename__ = "chat_messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(
        Integer, ForeignKey("chat_conversations.conversation_id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # model: which Grok model actually generated this row (only meaningful
    # for role="assistant"). Worth keeping once you start comparing models
    # or the model lineup changes over time -- otherwise old replies become
    # unattributable.
    model = Column(String, nullable=True)
    # token_count: lets you show usage/cost per conversation later, and is
    # standard in every production chat table (OpenAI, Anthropic consoles
    # both expose this per-message).
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
