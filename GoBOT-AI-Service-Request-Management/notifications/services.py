from .models import Notification


def notify(user, message: str, link: str = "") -> Notification:
    return Notification.objects.create(user=user, message=message[:255], link=link)


def notify_many(users, message: str, link: str = "") -> None:
    Notification.objects.bulk_create(
        [Notification(user=u, message=message[:255], link=link) for u in users]
    )
