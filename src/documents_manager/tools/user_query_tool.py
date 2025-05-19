import os
from typing import Optional, Type
import pandas as pd
from fuzzywuzzy import fuzz
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class QueryUserInfoArgs(BaseModel):
    """Tham số đầu vào cho UserInfoQueryTool"""
    id: Optional[str] = Field(default=None, description="ID của người dùng/ người tạo tài liệu")
    name: Optional[str] = Field(default=None, description="Tên của người dùng/ người tạo tài liệu (có thể không chính xác hoàn toàn)")

class UserInfoQueryTool(BaseTool):
    name: str = "Tìm kiếm thông tin người dùng/ Người tạo tài liệu"
    description: str = "Công cụ để tìm kiếm thông tin của người dùng/ người tạo tài liệu khi có tuỳ chọn dữ liệu như ID hoặc tên"
    args_schema: Type[BaseModel] = QueryUserInfoArgs

    def __init__(self, csv_folder: Optional[str] = "data"):
        super().__init__()
        self._df = self._load_csv(csv_folder)

    def _load_csv(self, csv_folder: str) -> pd.DataFrame:
        csv_path = os.path.join(csv_folder, "user.csv")
        print('Tải dữ liệu csv cho user')
        try:
            return pd.read_csv(csv_path)
        except Exception as e:
            return pd.DataFrame()

    def _run(self, id: Optional[str] = None, name: Optional[str] = None) -> str:
        try:
            if id and id.isdigit():
                result = self._df[self._df["id"] == int(id)]
                if result.empty:
                    return f"Không tìm thấy thông tin"
                return result.to_json(orient="records", force_ascii=False)

            if name:
                matched = self._df[self._df["name"].apply(
                    lambda x: fuzz.partial_ratio(x.lower(), name.lower()) > 80
                )]
                if matched.empty:
                    return f"Không tìm thấy thông tin"
                return matched.to_json(orient="records", force_ascii=False)

        except Exception as e:
            return f"Lỗi khi tìm kiếm thông tin"