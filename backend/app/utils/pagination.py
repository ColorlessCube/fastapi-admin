"""
分页工具
"""
from typing import Generic, List, TypeVar
from pydantic import BaseModel
from math import ceil

T = TypeVar('T')


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = 1
    size: int = 20
    
    @property
    def offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[T]":
        """创建分页响应"""
        pages = ceil(total / size) if size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
