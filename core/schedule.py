from datetime import datetime, time
from enum import Enum
from zoneinfo import ZoneInfo

from core.config import settings


class Activity(str, Enum):
    SLEEPING = "sleeping"
    WORKING = "working"
    FREE = "free"


def _parse_time(value: str) -> time:
    hour, minute = map(int, value.strip().split(":"))
    return time(hour, minute)


def _is_in_range(current: time, start: time, end: time) -> bool:
    if start <= end:
        return start <= current < end
    return current >= start or current < end


def get_now() -> datetime:
    return datetime.now(ZoneInfo(settings.APP_TIMEZONE))


def get_current_activity(now: datetime | None = None) -> Activity:
    now = now or get_now()
    current = now.time().replace(second=0, microsecond=0)

    sleep_start = _parse_time(settings.SLEEP_START)
    sleep_end = _parse_time(settings.SLEEP_END)
    work_start = _parse_time(settings.WORK_START)
    work_end = _parse_time(settings.WORK_END)

    if _is_in_range(current, sleep_start, sleep_end):
        return Activity.SLEEPING
    if _is_in_range(current, work_start, work_end):
        return Activity.WORKING
    return Activity.FREE


def get_activity_label(activity: Activity) -> str:
    if activity == Activity.SLEEPING:
        return "Sleeping"
    if activity == Activity.WORKING:
        return f"Busy ({settings.GF_PROFESSION})"
    return "Free & available"


def get_schedule_context(now: datetime | None = None) -> str:
    now = now or get_now()
    activity = get_current_activity(now)
    time_str = now.strftime("%A, %B %d, %Y, %I:%M %p")
    tz_label = settings.APP_TIMEZONE.replace("_", " ").split("/")[-1]

    if activity == Activity.SLEEPING:
        behavior = (
            "You are asleep right now. If he texts, you might reply very slowly, "
            "groggily, or with short half-asleep messages. You can say you were sleeping "
            "or just woke up to check your phone. Do not act fully energetic unless the "
            "conversation genuinely pulls you awake."
        )
    elif activity == Activity.WORKING:
        behavior = (
            f"You are busy with {settings.GF_PROFESSION.lower()} duties during work hours "
            f"({settings.WORK_START}–{settings.WORK_END}). You can still text, but keep replies "
            "shorter and more distracted. Mention being in class, studying, or busy only "
            "when it fits naturally — do not announce your schedule every message."
        )
    else:
        behavior = (
            "You are free right now and can chat normally. You are relaxed and have time "
            "for a proper conversation."
        )

    return (
        f"CURRENT TIME & AVAILABILITY:\n"
        f"It is currently {time_str} ({tz_label}).\n"
        f"Your current state: {get_activity_label(activity)}.\n"
        f"{behavior}"
    )


def get_status() -> dict:
    now = get_now()
    activity = get_current_activity(now)
    return {
        "timezone": settings.APP_TIMEZONE,
        "current_time": now.isoformat(),
        "activity": activity.value,
        "activity_label": get_activity_label(activity),
        "work_hours": f"{settings.WORK_START}–{settings.WORK_END}",
        "sleep_hours": f"{settings.SLEEP_START}–{settings.SLEEP_END}",
    }
