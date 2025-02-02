"""Configuration pour le suivi de balle et de pieds"""

# Constantes globales
BALL_CLASS_ID = 32  # ID de classe pour la balle dans YOLO
CONFIDENCE_THRESHOLD = 0.4  # Seuil de confiance pour la détection
TRACKER_RETRY_FRAMES = 10  # Nombre de frames avant de réessayer la détection
SMOOTHING_WINDOW = 5  # Fenêtre de lissage pour le suivi
YOLO_CHECK_INTERVAL = 10  # Intervalle de vérification YOLO
