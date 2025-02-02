# FootAP

FootAP (FOOTball trAcking Package) est un package Python pour la détection et le suivi de jonglage de football. Il utilise YOLO pour la détection de balle et MediaPipe pour la détection des pieds.

## Installation

```bash
pip install footap
```

## Utilisation

Il y a deux façons principales d'utiliser le package :

### 1. Utilisation simple avec videoCounter

```python
from footap import videoCounter

# Analyse d'une vidéo
videoCounter(
    video_source='video.mp4',
    output_video='output.mp4',
    output_file='output.txt',
    save_output_video=True,
    save_output_file=True,
    background=False
)
```

### 2. Utilisation avancée avec track_ball_and_feet

```python
from footap import track_ball_and_feet

# Exemple simple
track_ball_and_feet(
    video_source='video.mp4',
    output_video='output.mp4',
    rotation_angle=0
)

# Exemple avec toutes les options
track_ball_and_feet(
    video_source='video.mp4',
    output_video='output.mp4',
    rotation_angle=0,
    output_file='resultats.txt',
    save_output_video=True,
    save_output_file=True,
    background=False
)
```

## Fonctionnalités

- Détection de balle avec YOLO
- Suivi de balle avec OpenCV
- Détection des pieds avec MediaPipe
- Comptage des touches de balle pour chaque pied
- Support de rotation vidéo (0°, 90°, 180°, 270°)
- Mode arrière-plan pour le traitement sans affichage
- Sauvegarde des résultats dans un fichier texte
- Sauvegarde de la vidéo annotée

## Dépendances

- OpenCV (opencv-python, opencv-contrib-python)
- MediaPipe
- NumPy
- Ultralytics (YOLO)
- Pillow

## Licence

Ce projet est sous licence MIT.
