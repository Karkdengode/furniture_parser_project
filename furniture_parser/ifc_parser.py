# IFC parsing logic using ifcopenshell
import ifcopenshell

def parse_ifc_file(file_path: str):
    model = ifcopenshell.open(file_path)

    rooms = []

    for space in model.by_type("IfcSpace"):
        room_name = space.Name or "Unnamed"
        area = None
        if hasattr(space, "Area") and space.Area:
            area = float(space.Area)
        elif hasattr(space, "LongName") and space.LongName:
            area = 0.0  # fallback if area missing

        # Find furniture in room (not always possible in IFCs)
        furniture_in_room = []
        for furniture in model.by_type("IfcFurnishingElement"):
            label = furniture.Name or furniture.ObjectType or "Unknown"
            furniture_in_room.append(label)

        # Count occurrences
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
