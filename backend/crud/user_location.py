# from typing import Union

# from sqlalchemy.orm import Session

# from app.models.user_location import UserLocation
# from app.schemas.user_location import CreateLocationRequest, UpdateLocationRequest


# def create_location(db: Session, location_data: CreateLocationRequest) -> UserLocation:
#     location = UserLocation(**location_data.dict())
#     db.add(location)
#     db.commit()
#     db.refresh(location)
#     return location


# def get_locations_by_user(db: Session, user_id: int) -> list[UserLocation]:
#     return db.query(UserLocation).filter(UserLocation.user_id == user_id).all()


# def update_location(
#     db: Session, location_id: int, update_data: UpdateLocationRequest
# ) -> Union[UserLocation, None]:
#     location = db.query(UserLocation).filter(UserLocation.id == location_id).first()
#     if not location:
#         return None

#     for field, value in update_data.dict(exclude_unset=True).items():
#         setattr(location, field, value)

#     db.commit()
#     db.refresh(location)
#     return location


# def toggle_favorite(
#     db: Session, location_id: int, is_favorite: bool
# ) -> Union[UserLocation, None]:
#     location = db.query(UserLocation).filter(UserLocation.id == location_id).first()
#     if not location:
#         return None

#     location.is_favorite = is_favorite  # type: ignore
#     db.commit()
#     db.refresh(location)
#     return location


# def delete_location(db: Session, location_id: int) -> bool:
#     location = db.query(UserLocation).filter(UserLocation.id == location_id).first()
#     if not location:
#         return False

#     db.delete(location)
#     db.commit()
#     return True
