"""Module de traitement vidéo pour la détection de jonglage"""

import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO
from collections import deque
from .config import (
    BALL_CLASS_ID,
    CONFIDENCE_THRESHOLD,
    TRACKER_RETRY_FRAMES,
    SMOOTHING_WINDOW,
    YOLO_CHECK_INTERVAL
)

# Initialisation de MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

class FootTouchCounter:
    """Classe pour compter les touches de balle avec les pieds"""
    
    def __init__(self, min_time=10, touch_threshold=50):
        """
        Initialise le compteur de touches.
        
        Args:
            min_time (int): Temps minimum entre deux touches
            touch_threshold (int): Distance seuil pour considérer une touche
        """
        self.left_foot_touches = 0
        self.right_foot_touches = 0
        self.last_touch_frame = 0
        self.frame_count = 0
        self.min_time = min_time
        self.touch_threshold = touch_threshold
        self.touch_sequence = []  # Liste pour stocker la séquence des touches

    def update_touch(self, left_foot, right_foot, ball_x, ball_y):
        """Met à jour le compteur de touches"""
        left_distance = np.linalg.norm(np.array(left_foot) - np.array([ball_x, ball_y]))
        right_distance = np.linalg.norm(np.array(right_foot) - np.array([ball_x, ball_y]))

        if self.frame_count - self.last_touch_frame > self.min_time:
            if left_distance < self.touch_threshold or right_distance < self.touch_threshold:
                if left_distance < right_distance:
                    self.left_foot_touches += 1
                    self.touch_sequence.append('Left')
                else:
                    self.right_foot_touches += 1
                    self.touch_sequence.append('Right')
                self.last_touch_frame = self.frame_count

    def get_touches(self):
        """Retourne le nombre de touches pour chaque pied"""
        return self.left_foot_touches, self.right_foot_touches

    def get_touch_sequence(self):
        """Retourne la séquence des touches"""
        return self.touch_sequence

def rotate_point(x, y, frame_width, frame_height, rotation_angle):
    """
    Ajuste les coordonnées en fonction de la rotation de la vidéo.
    
    Args:
        x, y (int): Coordonnées du point
        frame_width, frame_height (int): Dimensions de l'image
        rotation_angle (int): Angle de rotation (0, 90, 180, 270)
        
    Returns:
        tuple: Nouvelles coordonnées (x, y)
    """
    if rotation_angle == 90:
        return y, frame_width - x
    elif rotation_angle == 180:
        return frame_width - x, frame_height - y
    elif rotation_angle == 270:
        return frame_height - y, x
    else:
        return x, y

def track_ball_and_feet(video_source, output_video, rotation_angle, output_file=None, save_output_video=True, save_output_file=True, background=False):
    """
    Fonction principale pour suivre la balle et les pieds dans une vidéo.
    
    Args:
        video_source (str): Chemin vers la vidéo source
        output_video (str): Chemin pour la vidéo de sortie
        rotation_angle (int): Angle de rotation (0, 90, 180, 270)
        output_file (str, optional): Fichier de sortie pour les résultats
        save_output_video (bool): Sauvegarder la vidéo de sortie
        save_output_file (bool): Sauvegarder les résultats dans un fichier
        background (bool): Exécution en arrière-plan sans affichage
    """
    # Initialisation
    model = YOLO("yolo11x.pt")
    tracker = cv2.legacy.TrackerCSRT_create()
    tracking = False
    last_ball_position = None
    tracker_fail_count = 0
    ball_history = deque(maxlen=SMOOTHING_WINDOW)
    frame_count = 0
    foot_touch_counter = FootTouchCounter(min_time=10, touch_threshold=50)

    # Ouverture de la vidéo
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la vidéo.")
        return

    # Configuration de la sortie vidéo
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) if cap.get(cv2.CAP_PROP_FPS) > 0 else 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    if save_output_video:
        out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

    # Boucle principale de traitement
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fin de la vidéo.")
            break

        foot_touch_counter.frame_count += 1
        frame_count += 1

        # Rotation de la vidéo si nécessaire
        if rotation_angle != 0:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE if rotation_angle == 90 else cv2.ROTATE_180 if rotation_angle == 180 else cv2.ROTATE_90_COUNTERCLOCKWISE)
            if rotation_angle in [90, 270]:
                frame_width, frame_height = frame_height, frame_width

        # Détection de la balle avec YOLO
        if not tracking or tracker_fail_count > TRACKER_RETRY_FRAMES or frame_count % YOLO_CHECK_INTERVAL == 0:
            results = model(frame)
            for result in results[0].boxes.data:
                x1, y1, x2, y2, conf, class_id = result.tolist()
                if int(class_id) == BALL_CLASS_ID and conf > CONFIDENCE_THRESHOLD:
                    ball_x, ball_y = (int((x1 + x2) / 2), int(y2))
                    ball_bbox = (int(x1), int(y1), int(x2 - x1), int(y2 - y1))
                    tracker = cv2.legacy.TrackerCSRT_create()
                    tracker.init(frame, ball_bbox)
                    tracking = True
                    tracker_fail_count = 0
                    last_ball_position = (ball_x, ball_y)
                    break

        # Suivi de la balle
        if tracking:
            success, ball_bbox = tracker.update(frame)
            if success:
                x1, y1, w, h = [int(v) for v in ball_bbox]
                ball_x, ball_y = int(x1 + w / 2), int(y1 + h)
                last_ball_position = (ball_x, ball_y)
                ball_history.append(last_ball_position)
                tracker_fail_count = 0
                cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
                cv2.putText(frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                tracker_fail_count += 1
                if tracker_fail_count > TRACKER_RETRY_FRAMES:
                    tracking = False

        # Détection des pieds avec MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_pose = pose.process(frame_rgb)

        if results_pose.pose_landmarks:
            landmarks = results_pose.pose_landmarks.landmark
            left_foot = (int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * frame_width),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * frame_height))
            right_foot = (int(landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * frame_width),
                          int(landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * frame_height))

            left_foot = rotate_point(left_foot[0], left_foot[1], frame_width, frame_height, rotation_angle)
            right_foot = rotate_point(right_foot[0], right_foot[1], frame_width, frame_height, rotation_angle)

            if tracking:
                ball_x, ball_y = rotate_point(ball_x, ball_y, frame_width, frame_height, rotation_angle)
                foot_touch_counter.update_touch(left_foot, right_foot, ball_x, ball_y)

        # Affichage des résultats
        left_touches, right_touches = foot_touch_counter.get_touches()
        if not background:
            cv2.putText(frame, f"Left Foot: {left_touches}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Right Foot: {right_touches}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Foot Tracking", frame)

        # Sauvegarde de la vidéo
        if save_output_video and out is not None:
            out.write(frame)

        # Gestion de la sortie
        if not background and cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Nettoyage des ressources
    cap.release()
    if out is not None:
        out.release()
    if not background:
        cv2.destroyAllWindows()

    # Sauvegarde des résultats
    if save_output_file and output_file:
        with open(output_file, 'w') as f:
            f.write(f"Left Foot Touches: {left_touches}\n")
            f.write(f"Right Foot Touches: {right_touches}\n")
            f.write("\nTouch Sequence:\n")
            for i, touch in enumerate(foot_touch_counter.get_touch_sequence(), 1):
                f.write(f"Touch {i}: {touch}\n")
