from pydantic import BaseModel


class BaseReadModel(BaseModel):
    """Base class for read models, providing a template for querying data from the domain model."""
