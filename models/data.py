from dataclasses import dataclass

@dataclass
class SessionMetrics:
    """Data class to hold metrics calculated for each focus session."""
    session_id: str
    user_id: str
    username: str
    start_time: str
    end_time: str
    active_duration: float
    pause_duration: float
    attention_span: float
    frequency_unfocus: int
    focus_duration: float
    unfocus_duration: float

@dataclass
class SessionLog:
    """Data class to hold the log of each focus session."""
    session_id: str
    svc_predictions: list[int]
    ear_values: list[float]

@dataclass
class ActivityPageConfig:
    """Data class to hold the configuration for an activity page."""
    page_name: str
    page_title: str
    description: str
    video_embed_link: str
    timer_duration: int
