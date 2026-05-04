from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from backend.Database.database import get_db
from backend.Database.models import Notification, NotificationRecipient, User
from backend.schema import NotificationCreate, NotificationOut, NotificationReadResponse

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_notification(payload: NotificationCreate, db: db_dependency):
    sender = db.query(User).filter(User.id == payload.sent_by).first()
    if not sender:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender not found")
    if sender.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can send notifications",
        )

    recipients = db.query(User).filter(User.id.in_(payload.recipient_ids)).all()
    if len(recipients) != len(set(payload.recipient_ids)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more recipients were not found",
        )

    notification = Notification(
        title=payload.title,
        message=payload.message,
        category=payload.category,
        amount=payload.amount,
        due_date=payload.due_date,
        sent_by=payload.sent_by,
    )
    db.add(notification)
    db.flush()

    for recipient in recipients:
        db.add(
            NotificationRecipient(
                notification_id=notification.id,
                user_id=recipient.id,
            )
        )

    db.commit()

    return {"message": "Notification sent successfully", "notification_id": notification.id}


@router.get("/", response_model=list[NotificationOut])
def list_notifications(user_id: int = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    assignments = (
        db.query(NotificationRecipient)
        .options(joinedload(NotificationRecipient.notification).joinedload(Notification.sender))
        .filter(NotificationRecipient.user_id == user_id)
        .order_by(NotificationRecipient.id.desc())
        .all()
    )

    return [
        NotificationOut(
            id=assignment.notification.id,
            title=assignment.notification.title,
            message=assignment.notification.message,
            category=assignment.notification.category,
            amount=assignment.notification.amount,
            due_date=assignment.notification.due_date,
            created_at=assignment.notification.created_at,
            sender_name=assignment.notification.sender.username,
            is_read=assignment.is_read,
            read_at=assignment.read_at,
        )
        for assignment in assignments
    ]


@router.patch("/{notification_id}/read", response_model=NotificationReadResponse)
def mark_notification_as_read(
    notification_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    assignment = (
        db.query(NotificationRecipient)
        .filter(
            NotificationRecipient.notification_id == notification_id,
            NotificationRecipient.user_id == user_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification assignment not found",
        )

    assignment.is_read = True
    assignment.read_at = datetime.utcnow()
    db.commit()

    return NotificationReadResponse(message="Notification marked as read")
