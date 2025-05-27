from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ...db.session import get_db
from ...models.users import User as UserModel
from ..schemas.users import User, UserCreate, UserUpdate
from ...repositories.users import UserRepository
from ...services.users import UserService
from ..dependencies import get_current_active_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_admin_user)
) -> Any:
    """
    Récupère la liste de tous les utilisateurs (admin uniquement).
    """
    service = UserService(UserRepository(UserModel, db))
    return service.get_multi(skip=skip, limit=limit)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user = Depends(get_current_admin_user)
) -> Any:
    """
    Crée un nouvel utilisateur (admin uniquement).
    """
    service = UserService(UserRepository(UserModel, db))
    try:
        return service.create(obj_in=user_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=User)
def read_own_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
) -> Any:
    """
    Récupère le profil de l'utilisateur actuellement connecté.
    """
    return current_user


@router.put("/me", response_model=User)
def update_own_profile(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user = Depends(get_current_active_user)
) -> Any:
    """
    Met à jour les informations de l'utilisateur actuellement connecté.
    """
    service = UserService(UserRepository(UserModel, db))
    return service.update(db_obj=current_user, obj_in=user_in)


@router.get("/{id}", response_model=User)
def read_user_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user = Depends(get_current_admin_user)
) -> Any:
    """
    Récupère un utilisateur par son ID (admin uniquement).
    """
    service = UserService(UserRepository(UserModel, db))
    user = service.get(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put("/{id}", response_model=User)
def update_user_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    user_in: UserUpdate,
    current_user = Depends(get_current_admin_user)
) -> Any:
    """
    Met à jour un utilisateur spécifique (admin uniquement).
    """
    service = UserService(UserRepository(UserModel, db))
    user = service.get(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return service.update(db_obj=user, obj_in=user_in)


@router.delete("/{id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user = Depends(get_current_admin_user)
) -> Any:
    """
    Supprime un utilisateur par son ID (admin uniquement).
    """
    service = UserService(UserRepository(UserModel, db))
    user = service.get(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return service.remove(id=id)


@router.get("/by-email/{email}", response_model=User)
def get_user_by_email(
    *,
    db: Session = Depends(get_db),
    email: str,
    current_user = Depends(get_current_admin_user)
) -> Any:
    """
    Recherche un utilisateur par email (admin uniquement).
    """
    service = UserService(UserRepository(UserModel, db))
    user = service.get_by_email(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user
