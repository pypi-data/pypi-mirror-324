"""
footap - Package de détection et suivi de jonglage de football
"""

from .video_processing import track_ball_and_feet
from .counter import videoCounter
from .config import BALL_CLASS_ID, CONFIDENCE_THRESHOLD, TRACKER_RETRY_FRAMES, SMOOTHING_WINDOW, YOLO_CHECK_INTERVAL

__version__ = "1.0.0"
__author__ = "Dims"

# Exposer les fonctions principales
__all__ = ['videoCounter', 'track_ball_and_feet']
