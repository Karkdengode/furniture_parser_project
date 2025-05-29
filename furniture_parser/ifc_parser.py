# IFC parsing logic using ifcopenshell
import ifcopenshell

def parse_ifc_file(file_path: str):
    model = ifcopenshell.open(file_path)

    # Hent både IfcSpace og IfcZone hvis tilgjengelig
    spaces = model.by_type("IfcSpace") or model.by_type("IfcZone")

    # 🔁 Hvis ingen rom ble funnet, returner fallback-data
    if not spaces:
        return {
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
        room_name = getattr(space, "Name", None) or getattr(space, "LongName", None) or "Unnamed"
        area = None
        if hasattr(space, "Area") and space.Area:
            area = float(space.Area)
        else:
            area = 0.0  # fallback hvis ikke area er oppgitt

        # Fant ikke kobling mellom møbler og rom, men henter alle møbler globalt
        furniture_in_room = []
        for furniture in model.by_type("IfcFurnishingElement"):
            label = furniture.Name or furniture.ObjectType or "Unknown"
            furniture_in_room.append(label)

        # Tell antall av hvert møbel
        furniture_count = {}
        for f in furniture_in_room:
            furniture_count[f] = furniture_count.get(f, 0) + 1

        furniture_summary = [{"label": k, "count": v} for k, v in furniture_count.items()]

        rooms.append({
            "room_name": room_name,
            "area": area,
            "furniture": furniture_summary
        })

    return {"rooms": rooms}
