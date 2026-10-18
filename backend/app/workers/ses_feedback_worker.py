import asyncio
import json
from typing import Any

import boto3
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import worker_logger
from app.db.core import AsyncSessionLocal
from app.db.models.email_suppression import (
    EmailSuppression,
    EmailSuppressionReason,
)

MAX_MESSAGES = 10
WAIT_TIME_SECONDS = 20


def parse_ses_event(sqs_message_body: str) -> dict[str, Any]:
    # Extract the SES event from the SNS message stored in SQS.
    notification = json.loads(sqs_message_body)

    if not isinstance(notification, dict):
        raise ValueError("SQS message body must contain a JSON object")

    # SNS wraps the actual SES event inside its Message field.
    if notification.get("Type") == "Notification":
        ses_event = json.loads(notification["Message"])
    else:
        ses_event = notification

    if not isinstance(ses_event, dict):
        raise ValueError("SES event must be a JSON object")

    return ses_event


def get_suppressed_recipients(
    ses_event: dict[str, Any],
) -> list[tuple[str, EmailSuppressionReason]]:
    # Return email addresses that should be added to the suppression list.
    event_type = (
        ses_event.get("eventType") or ses_event.get("notificationType") or ""
    ).casefold()

    if event_type == "bounce":
        bounce_details = ses_event.get("bounce") or {}

        # Only permanent bounces should suppress an email address.
        if (bounce_details.get("bounceType") or "").casefold() != "permanent":
            return []

        recipients = bounce_details.get("bouncedRecipients", [])
        reason = EmailSuppressionReason.HARD_BOUNCE

    elif event_type == "complaint":
        complaint_details = ses_event.get("complaint") or {}
        recipients = complaint_details.get("complainedRecipients", [])
        reason = EmailSuppressionReason.COMPLAINT

    else:
        # Ignore delivery and other event types.
        return []

    suppressed_recipients = []
    seen_emails = set()

    for recipient in recipients:
        if not isinstance(recipient, dict):
            continue

        email = recipient.get("emailAddress")

        if not isinstance(email, str):
            continue

        email = email.strip().lower()

        # Avoid duplicate addresses in the same event.
        if email and email not in seen_emails:
            seen_emails.add(email)
            suppressed_recipients.append((email, reason))

    return suppressed_recipients


async def save_suppression(
    db_session: AsyncSession,
    email: str,
    reason: EmailSuppressionReason,
) -> None:
    # Insert a suppression record without duplicating an existing email.
    statement = (
        insert(EmailSuppression)
        .values(
            email=email.strip().lower(),
            reason=reason,
        )
        .on_conflict_do_nothing(index_elements=[EmailSuppression.email])
    )

    await db_session.execute(statement)


async def process_ses_event(sqs_message_body: str) -> None:
    # Parse an SES event and save its suppression records.
    ses_event = parse_ses_event(sqs_message_body)
    recipients = get_suppressed_recipients(ses_event)

    if not recipients:
        worker_logger.info(
            "No addresses to suppress for SES event type: %s",
            ses_event.get("eventType")
            or ses_event.get("notificationType")
            or "unknown",
        )
        return

    # Commit all recipient records together.
    async with AsyncSessionLocal() as db_session:
        async with db_session.begin():
            for email, reason in recipients:
                await save_suppression(db_session, email, reason)

    worker_logger.info(
        "Processed suppression records for %d recipient(s)",
        len(recipients),
    )


async def process_sqs_message(
    sqs_client: Any,
    message: dict[str, Any],
) -> None:
    # Process a message and delete it only after successful handling.
    await process_ses_event(message["Body"])

    # The database transaction has committed before the message is deleted.
    await asyncio.to_thread(
        sqs_client.delete_message,
        QueueUrl=settings.ses_feedback_queue_url,
        ReceiptHandle=message["ReceiptHandle"],
    )


async def run_worker() -> None:
    # Continuously fetch and process SQS messages.
    if not settings.ses_feedback_queue_url:
        raise RuntimeError("SES feedback queue URL is not configured")

    sqs_client = boto3.client(
        "sqs",
        region_name=settings.sqs_region,
    )

    worker_logger.info("SES feedback worker started")

    while True:
        try:
            response = await asyncio.to_thread(
                sqs_client.receive_message,
                QueueUrl=settings.ses_feedback_queue_url,
                MaxNumberOfMessages=MAX_MESSAGES,
                WaitTimeSeconds=WAIT_TIME_SECONDS,
            )
        except Exception:
            worker_logger.exception("Failed to receive SQS messages")
            await asyncio.sleep(5)
            continue

        for message in response.get("Messages", []):
            try:
                await process_sqs_message(sqs_client, message)
            except Exception:
                worker_logger.exception(
                    "Failed to process an SQS message; it will be retried"
                )


def main() -> None:
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        worker_logger.info("SES feedback worker stopped")


if __name__ == "__main__":
    main()
