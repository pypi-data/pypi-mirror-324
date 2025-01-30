"""BirdNET Program Configuration Options."""

import datetime
from typing import Optional

from acoupi.programs.templates import (
    AudioConfiguration,
    DetectionProgramConfiguration,
)
from pydantic import BaseModel, Field


class BirdNETAudioConfig(AudioConfiguration):
    """Audio Configuration schema."""

    schedule_start: datetime.time = Field(
        default=datetime.time(hour=4, minute=0, second=0),
    )
    """Start time for recording schedule."""

    schedule_end: datetime.time = Field(
        default=datetime.time(hour=23, minute=0, second=0),
    )
    """End time for recording schedule."""


class ModelConfig(BaseModel):
    """Model output configuration."""

    detection_threshold: float = 0.4
    """Detection threshold for filtering model outputs."""


class SaveRecordingFilter(BaseModel):
    """Saving Filters for audio recordings configuration."""

    starttime: datetime.time = datetime.time(hour=17, minute=0, second=0)
    """Start time of the interval for which to save recordings."""

    endtime: datetime.time = datetime.time(hour=21, minute=0, second=0)
    """End time of the interval for which to save recordings."""

    before_dawndusk_duration: int = 30
    """Optional duration in minutes before dawn/dusk to save recordings."""

    after_dawndusk_duration: int = 30
    """Optional duration in minutes after dawn/dusk to save recordings."""

    frequency_duration: int = 0
    """Optional duration in minutes to save recordings using the frequency filter."""

    frequency_interval: int = 0
    """Optional periodic interval in minutes to save recordings."""


class SaveRecordingManager(BaseModel):
    """Saving configuration for audio recordings.

    (path to storage, name of files, saving threshold).
    """

    true_dir: str = "birds"
    """Directory for saving recordings with confident detections."""

    false_dir: str = "no_birds"
    """Directory for saving recordings with uncertain detections."""

    timeformat: str = "%Y%m%d_%H%M%S"
    """Time format for naming the audio recording files."""

    saving_threshold: float = 0.2
    """Minimum threshold of detections from a recording to save it."""


class Summariser(BaseModel):
    """Summariser configuration."""

    interval: Optional[float] = 3600  # interval in seconds
    """Interval (in seconds) for summarising detections."""

    low_band_threshold: Optional[float] = 0.0
    """Optional low band threshold to summarise detections."""

    mid_band_threshold: Optional[float] = 0.0
    """Optional mid band threshold to summarise detections."""

    high_band_threshold: Optional[float] = 0.0
    """Optional high band threshold to summarise detections."""


class BirdNETConfig(DetectionProgramConfiguration):
    """BirdNET Program Configuration schema.

    This schema extends the _acoupi_ `DetectionProgramConfiguration` to
    include settings for the BirdNET program, such as custom audio recording,
    model setup, file management, messaging, and summarisation.
    """

    recording: AudioConfiguration = Field(
        default_factory=BirdNETAudioConfig,
    )
    """Audio recording configuration."""

    model: ModelConfig = Field(
        default_factory=ModelConfig,
    )
    """Model output configuration."""

    saving_filters: SaveRecordingFilter = Field(
        default_factory=SaveRecordingFilter,
    )
    """Recording Saving Filters configuration for audio recordings."""

    saving_managers: SaveRecordingManager = Field(
        default_factory=SaveRecordingManager,
    )
    """Recording Saving Managers configuration for audio recordings."""

    summariser_config: Optional[Summariser] = Field(
        default_factory=Summariser,
    )
    """Summariser configuration."""
