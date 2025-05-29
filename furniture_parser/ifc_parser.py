# IFC parsing logic using ifcopenshell
# IFC parsing logic using ifcopenshell

import ifcopenshell

def parse_ifc_file(file_path: str):
    model = ifcopenshell.open(file_path)

    # Forsøk å hente IfcSpace, eller bruk IfcZone som fallback
    spaces = model.by_type("IfcSpace") or model.by_type("IfcZone")

    # 🚨 Fallback hvis ingen rom finnes
    if not spaces:
        print("[parser] Ingen IfcSpace funnet – returnerer fallback-data")
        return {
            "fallback": True,
            "rooms": [
                {
                    "room_name": "Fallback Room",
                    "area": 12.5,
                    "furniture": [
                        { "label": "Chair", "count": 2 },
                        { "label": "Table", "count": 1 }
                    ]
                }
            ]
        }

    rooms = []

    for space in spaces:
        room_name = (
            getattr(space, "Name", None)
            or getattr(space, "LongName", None)
            or "Unnamed"
        )

        area = 0.0
        if hasattr(space, "Area") and space.Area:
            try:
                area = float(space.Area)
            except:
                area = 0.0

        # Hent alle møbler i modellen (kan forbedres senere med kobling til rom)
        furniture_in_room = []
        for furniture in model.by_type("IfcFurnishingElement"):
            label = furniture.Name or furniture.ObjectType or "Unknown"
            furniture_in_room.append(label)

        # Tell antall møbler
        furniture_count = {}
        for f in furniture_in_room:
            furniture_count[f] = furniture_count.get(f, 0) + 1

        furniture_summary = [
            {"label": label, "count": count}
            for label, count in furniture_count.items()
        ]

        rooms.append({
            "room_name": room_name,
            "area": area,
            "furniture": furniture_summary
        })

    return {
        "fallback": False,
        "rooms": rooms
    }
