"""dspygen test suite."""
from pydantic import BaseModel

class TestModel(BaseModel):
    """Test model."""
    name: str
    age: int
    is_active: bool


tm = TestModel(name='John', age=25, is_active=True)

tm.m
