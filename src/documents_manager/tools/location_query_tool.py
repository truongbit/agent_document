import os
import pandas as pd
from typing import Optional, Dict, Type
from pydantic import BaseModel
from crewai.tools import BaseTool

class QueryLocationParams(BaseModel):
    """Tham số đầu vào cho LocationQueryTool"""
    building_id: Optional[int] = None
    floor_id: Optional[int] = None
    room_id: Optional[int] = None
    shelf_id: Optional[int] = None
    drawer_id: Optional[int] = None
    slot_id: Optional[int] = None

class LocationQueryTool(BaseTool):
    name: str = "Search Location Information"
    description: str = "Công cụ để tìm kiếm thông tin vị trí của tài liệu từ các ID thành phần: building_id, floor_id, room_id, shelf_id, drawer_id, slot_id."
    args_schema: Type[BaseModel] = QueryLocationParams

    def __init__(self, csv_folder: Optional[str] = "data"):
        super().__init__()
        self._tables = self._load_csvs(csv_folder)

    def _load_csvs(self, folder: str) -> Dict[str, pd.DataFrame]:
        tables = {}
        print('Tải dữ liệu csv cho vị trí')
        for file in ["building.csv", "floor.csv", "room.csv", "shelf.csv", "drawer.csv", "slot.csv"]:
            path = os.path.join(folder, file)
            try:
                tables[file] = pd.read_csv(path)
            except Exception as e:
                tables[file] = pd.DataFrame()
        return tables

    def _run(
        self,
        building_id: Optional[int] = None,
        floor_id: Optional[int] = None,
        room_id: Optional[int] = None,
        shelf_id: Optional[int] = None,
        drawer_id: Optional[int] = None,
        slot_id: Optional[int] = None,
    ) -> str:
        location_ids = {
            "building_id": building_id,
            "floor_id": floor_id,
            "room_id": room_id,
            "shelf_id": shelf_id,
            "drawer_id": drawer_id,
            "slot_id": slot_id,
        }
        result = {}
        for key, file in [
            ("building_id", "building.csv"),
            ("floor_id", "floor.csv"),
            ("room_id", "room.csv"),
            ("shelf_id", "shelf.csv"),
            ("drawer_id", "drawer.csv"),
            ("slot_id", "slot.csv"),
        ]:
            if location_ids.get(key) is not None:
                df = self._tables.get(file, pd.DataFrame())
                row = df[df["id"] == location_ids[key]]
                if not row.empty:
                    result[key.replace("_id", "")] = row["name"].iloc[0]

        if not result:
            return "Không tìm thấy thông tin vị trí phù hợp"
        return "\n".join([f"{k.capitalize()}: {v}" for k, v in result.items()])