from sqlalchemy.orm import Session
from typing import List, Optional

from models import NewsRadarXPost
from schemas import NewsRadarXPostRead, NewsRadarXPostWrite


def get(db: Session, post_id: int) -> Optional[NewsRadarXPostRead]:
    """Récupère un post par son ID."""
    db_post = db.query(NewsRadarXPost).filter(NewsRadarXPost.id == post_id).first()
    if db_post:
        return NewsRadarXPostRead.model_validate(db_post)
    return None


def get_all(db: Session, limit: int = 50) -> List[NewsRadarXPostRead]:
    """Récupère tous les posts (limités par défaut à 50)."""
    posts = db.query(NewsRadarXPost).limit(limit).all()
    return [NewsRadarXPostRead.model_validate(p) for p in posts]


def save(db: Session, post: NewsRadarXPostWrite) -> NewsRadarXPostRead:
    """
    Insère ou met à jour un post.
    Si un post avec le même ID ou la même clé unique existe, il est mis à jour.
    """
    # Exemple avec une contrainte unique sur un champ 'external_id'
    db_post = db.query(NewsRadarXPost).filter(NewsRadarXPost.link == post.link).first()

    if db_post:
        # Mise à jour des champs
        for key, value in post.model_dump().items():
            setattr(db_post, key, value)
    else:
        # Création d'un nouveau post
        db_post = NewsRadarXPost(**post.model_dump())
        db.add(db_post)

    db.commit()
    db.refresh(db_post)
    return NewsRadarXPostRead.model_validate(db_post)


def delete(db: Session, post_id: int) -> bool:
    """
    Supprime un post par ID.
    Retourne True si suppression effectuée, False si l'ID n'existe pas.
    """
    db_post = db.query(NewsRadarXPost).filter(NewsRadarXPost.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
