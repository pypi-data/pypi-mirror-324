"""Module principal pour le comptage de touches de balle"""

from .video_processing import track_ball_and_feet

def videoCounter(video_source, output_video, output_file=None, save_output_video=True, save_output_file=True, background=False):
    """
    Fonction principale pour compter les touches de balle dans une vidéo.
    
    Args:
        video_source (str): Chemin vers la vidéo source
        output_video (str): Chemin pour la vidéo de sortie
        output_file (str, optional): Fichier de sortie pour les résultats
        save_output_video (bool): Sauvegarder la vidéo de sortie
        save_output_file (bool): Sauvegarder les résultats dans un fichier
        background (bool): Exécution en arrière-plan sans affichage
    """
    track_ball_and_feet(
        video_source=video_source,
        output_video=output_video,
        rotation_angle=0,
        output_file=output_file if save_output_file else None,
        save_output_video=save_output_video,
        save_output_file=save_output_file,
        background=background
    )
