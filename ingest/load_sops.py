import os
from langchain.schema import Document
from config import BASE_SOP_FOLDER

def load_all_sops():
    documents = []

    for sector in os.listdir(BASE_SOP_FOLDER):
        sector_path = os.path.join(BASE_SOP_FOLDER, sector)
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
                        "plant": "default",
                        "sector": sector,
                        "sop_name": file.replace(".txt", ""),
                        "source": sop_path
                    }
                )
            )

    return documents
