import os
from langchain.schema import Document
from config import BASE_SOP_FOLDER

def load_all_sops():
    documents = []

    for plant in os.listdir(BASE_SOP_FOLDER):
        plant_path = os.path.join(BASE_SOP_FOLDER, plant)
        if not os.path.isdir(plant_path):
            continue

        for sector in os.listdir(plant_path):
            sector_path = os.path.join(plant_path, sector)
            if not os.path.isdir(sector_path):
                continue

            for file in os.listdir(sector_path):
                if not file.endswith(".txt"):
                    continue

                sop_path = os.path.join(sector_path, file)

                with open(sop_path, "r", encoding="utf-8") as f:
                    text = f.read()

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "plant": plant,
                            "sector": sector,
                            "sop_name": file.replace(".txt", ""),
                            "source": sop_path
                        }
                    )
                )

    return documents
