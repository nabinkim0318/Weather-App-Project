# app/debug_svc.py

from app.services import user_location as svc

print("svc:", dir(svc))

functions = [
    "save_user_location",
    "get_locations_by_user",
    "update_location",
    "toggle_favorite",
    "delete_location",
]

for func in functions:
    print(f"svc.{func}:", getattr(svc, func, "❌ Not found"))
