# from typing import Union

# from sqlalchemy.orm import Session

# from app.models.user_location import UserLocation
# from app.schemas.user_location import , UpdateLocationRequest
# from crud import user_location as crud


# def save_user_location(
#     db: Session, user_id: int, data: CreateLocationRequest
# ) -> UserLocation:
#     existing = (
#         db.query(UserLocation)
#         .filter(
#             UserLocation.user_id == user_id,
#             UserLocation.latitude == data.latitude,
#             UserLocation.longitude == data.longitude,
#         )
#         .first()
#     )

#     if existing:
#         return existing

#     new_location = UserLocation(user_id=user_id, **data.dict())
#     db.add(new_location)
#     db.commit()
#     db.refresh(new_location)
#     return new_location


# def get_locations_by_user(db: Session, user_id: int) -> list[UserLocation]:
#     return crud.get_locations_by_user(db, user_id)


# def update_location(
#     db: Session, location_id: int, update_data: UpdateLocationRequest
# ) -> Union[UserLocation, None]:
#     return crud.update_location(db, location_id, update_data)


# def toggle_favorite(
#     db: Session, location_id: int, is_favorite: bool
# ) -> Union[UserLocation, None]:
#     return crud.toggle_favorite(db, location_id, is_favorite)


# # def enforce_single_favorite(
# #     db: Session, user_id: int, location_id: int
# # ) -> Union[UserLocation, None]:
# #     # Unset all previous favorites for this user
# #     db.query(UserLocation).filter(
# #         UserLocation.user_id == user_id, UserLocation.is_favorite == True
# #     ).update(
# #         {UserLocation.is_favorite: False}
# #     )

# #     # Set the specified location as favorite
# #     location = db.query(UserLocation).filter_by(id=location_id,
#           user_id=user_id).first()
# #     if not location:
# #         return None

# #     location.is_favorite = True  # type: ignore
# #     db.commit()
# #     db.refresh(location)
# #     return location


# def delete_location(db: Session, location_id: int) -> bool:
#     return crud.delete_location(db, location_id)
