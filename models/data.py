from dataclasses import dataclass

@dataclass
class SessionMetrics:
    user_id: int
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
    svc_predictions: list[int]
    ear_values: list[float]

@dataclass
class ActivityPageConfig:
    title: str
    text: str
    video_embed_link: str
    timer_duration: int
    page_name: str
