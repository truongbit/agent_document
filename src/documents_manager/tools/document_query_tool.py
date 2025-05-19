import os
import pandas as pd
from typing import Optional, Type
from pydantic import BaseModel, Field
from rapidfuzz import fuzz
from crewai.tools import BaseTool

class QueryDocumentArgs(BaseModel):
    """Tham số đầu vào cho DocumentQueryTool"""
    id: Optional[str] = Field(None, description="ID của tài liệu cần tìm")
    title: Optional[str] = Field(None, description="Tiêu đề, tên hoặc mô tả của tài liệu (có thể gần đúng)")
    code: Optional[str] = Field(None, description="Mã (code) của tài liệu")
    created_by: Optional[str] = Field(None, description="ID của người tạo tài liệu")

class DocumentQueryTool(BaseTool):
    name: str = "Search Document Information"
    description: str = "Công cụ để tìm kiếm thông tin tài liệu theo ID tài liệu, tiêu đề, tên của tài liệu, mã (code) tài liệu hoặc ID người tạo tài liệu"
    args_schema: Type[BaseModel] = QueryDocumentArgs

    def __init__(self, csv_folder: Optional[str] = "data"):
        super().__init__()        
        self._df = self._load_csv(csv_folder)

    def _load_csv(self, csv_folder: str) -> pd.DataFrame:
        csv_path = os.path.join(csv_folder, "documents.csv")
        print('Tải dữ liệu csv cho tài liệu')
        try:
            return pd.read_csv(csv_path)
        except Exception as e:
            return pd.DataFrame()
        
    def _run(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        code: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> str:
        results = []
        if id and id.isdigit():
            results = self._df[self._df['id'] == int(id)]
        if title:
            results = self._df[self._df['title'].apply(lambda x: fuzz.partial_ratio(x.lower(), title.lower()) > 80)]
        if code:
            results = self._df[self._df['code'] == code]
        if created_by and created_by.isdigit():
            results = self._df[self._df['created_by'] == int(created_by)]
        return pd.DataFrame(results).to_dict(orient='records')