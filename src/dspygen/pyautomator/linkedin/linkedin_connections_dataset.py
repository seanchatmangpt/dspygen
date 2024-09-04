import csv
from typing import List, Optional
from datetime import datetime, timedelta
from dspy.datasets.dataset import Dataset
import dspy
from pydantic import BaseModel, Field

class LinkedInConnectionModel(BaseModel):
    first_name: str = Field(..., description="First name of the connection")
    last_name: str = Field(..., description="Last name of the connection")
    url: str = Field(..., description="LinkedIn profile URL of the connection")
    email: Optional[str] = Field(None, description="Email address of the connection")
    company: Optional[str] = Field(None, description="Company where the connection works")
    position: Optional[str] = Field(None, description="Position of the connection at their company")
    connected_on: Optional[datetime] = Field(None, description="Date when the connection was made")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data.get('First Name', ''),
            last_name=data.get('Last Name', ''),
            url=data.get('URL', ''),
            email=data.get('Email Address'),
            company=data.get('Company'),
            position=data.get('Position'),
            connected_on=cls._parse_date(data.get('Connected On', ''))
        )

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        try:
            return datetime.strptime(date_str, '%d %b %Y')
        except ValueError:
            return None

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position} at {self.company}"

class LinkedInConnectionsDataset(Dataset):
    def __init__(self, file_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = self._load_connections(file_path)
        self._train_ = [dspy.Example(connection=conn) for conn in self.connections]
        self._dev_ = self._train_  # Using the same data for dev set
        self._test_ = []  # No test set for this dataset

    def _load_connections(self, file_path: str) -> List[LinkedInConnectionModel]:
        connections = []
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                connections.append(LinkedInConnectionModel.from_dict(row))
        return connections

    def get_connection_by_name(self, first_name: str, last_name: str) -> Optional[LinkedInConnectionModel]:
        for conn in self.connections:
            if conn.first_name.lower() == first_name.lower() and conn.last_name.lower() == last_name.lower():
                return conn
        return None

    def get_connections_by_company(self, company: str) -> List[LinkedInConnectionModel]:
        return [conn for conn in self.connections if company.lower() in (conn.company or '').lower()]

    def get_connections_by_position(self, position: str) -> List[LinkedInConnectionModel]:
        return [conn for conn in self.connections if position.lower() in (conn.position or '').lower()]

    def get_recent_connections(self, days: int) -> List[LinkedInConnectionModel]:
        cutoff_date = datetime.now() - timedelta(days=days)
        return [conn for conn in self.connections if conn.connected_on and conn.connected_on >= cutoff_date]

def main():
    dataset_path = "/Users/sac/dev/dspygen/data/21KLinkedInConnections.csv"
    dataset = LinkedInConnectionsDataset(dataset_path)

    print(f"Total connections: {len(dataset.connections)}")

    # Get all Apple connections
    apple_connections = dataset.get_connections_by_company("Apple")
    
    print(f"\nTotal Apple connections: {len(apple_connections)}")
    print("\nApple connections:")
    for conn in apple_connections:
        print(f"{conn.first_name} {conn.last_name} - {conn.position}")

if __name__ == "__main__":
    main()