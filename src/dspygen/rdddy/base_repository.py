import json
from pathlib import Path
from typing import TypeVar, Generic, Type, List, Optional

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], storage_file: Path):
        self.model = model
        self.storage_file = storage_file
        self.storage_file.touch(exist_ok=True)  # Ensure file exists

    def _read_data(self) -> List[T]:
        """Reads and returns all model instances from the storage file."""
        try:
            with self.storage_file.open('r', encoding='utf-8') as file:
                data = json.load(file)
            return [self.model.parse_obj(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[T]) -> None:
        """Writes the provided list of model instances to the storage file."""
        with self.storage_file.open('w', encoding='utf-8') as file:
            json.dump([item.dict() for item in data], file, indent=4)

    def add(self, item: T) -> None:
        """Adds a new model instance to the storage."""
        items = self._read_data()
        items.append(item)
        self._write_data(items)

    def get(self, **criteria) -> Optional[T]:
        """Retrieves a single model instance that matches the provided criteria."""
        items = self._read_data()
        for item in items:
            if all(getattr(item, field) == value for field, value in criteria.items()):
                return item
        return None

    def remove(self, **criteria) -> bool:
        """Removes model instances that match the provided criteria."""
        items = self._read_data()
        items_before = len(items)
        items = [item for item in items if not all(getattr(item, field) == value for field, value in criteria.items())]
        self._write_data(items)
        return len(items) < items_before

    def update(self, item: T) -> None:
        """Updates a model instance in the storage."""
        items = self._read_data()
        for i, existing_item in enumerate(items):
            if existing_item.id == item.id:  # Assuming each model has a unique 'id' field
                items[i] = item
                break
        self._write_data(items)

    def save(self, item: T) -> None:
        """Updates a model instance if it exists, otherwise inserts it."""
        items = self._read_data()
        for i, existing_item in enumerate(items):
            if existing_item.id == item.id:  # Assuming each model has a unique 'id' field
                items[i] = item
                self._write_data(items)
                return
        self.add(item)

    def list_all(self) -> List[T]:
        """Returns a list of all model instances."""
        return self._read_data()


def main():
    """Main function"""
    # Conversation Learnng Through Dialog Repository

    class ConversationRepository(BaseRepository[Conversation]):
        def __init__(self, storage_file: Path):
            super().__init__(Conversation, storage_file)


if __name__ == '__main__':
    main()



