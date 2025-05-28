from pdfminer.high_level import extract_text
import re

def parse_pdf(file_path: str):
    text = extract_text(file_path)

    # Eksempel: Finn linjer som inneholder romnavn og areal
    pattern = re.compile(r"(.*?)\\s?[–-]\\s?(\\d+)\\s?m²", re.IGNORECASE)
    rooms = []

    for match in pattern.finditer(text):
        name, area = match.groups()
        rooms.append({
            "name": name.strip(),
            "area": int(area),
            "objects": []  # Vi legger inn møbler senere
        })

    return {"rooms": rooms}
