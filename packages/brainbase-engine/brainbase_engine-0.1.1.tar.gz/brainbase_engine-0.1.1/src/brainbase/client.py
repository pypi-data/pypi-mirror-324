from typing import List
from datetime import datetime
from .models import Team, Worker
from .json_client import JsonApiClient

class BrainbaseClient:
    def __init__(self, api_key: str):
        self.api = JsonApiClient(api_key)
        self.api_key = api_key
        self.team = self._get_team()

    def _get_team(self) -> Team:
        """Fetch team information associated with the API key"""
        response = self.api.get("/teams")
        if len(response["data"]) == 0:
            raise Exception("No team found for the given API key")
        data = response["data"][0]
        return Team(
            id=data["id"],
            name=data["attributes"]["name"],
            created_at=datetime.fromisoformat(
                data["attributes"]["createdAt"].rstrip("Z")
            ),
            updated_at=datetime.fromisoformat(
                data["attributes"]["updatedAt"].rstrip("Z")
            ),
        )

    def list_workers(self) -> List[Worker]:
        """List all workers in the team"""
        response = self.api.get("/workers")
        return [Worker.from_json_api(item, self.api_key) for item in response["data"]]

    def create_worker(self, name: str, flow_code: str) -> Worker:
        """Create a new worker with an initial flow"""
        # First create the worker
        worker_data = {
            "data": {
                "type": "workers",
                "attributes": {"name": name},
                "relationships": {
                    "team": {"data": {"type": "teams", "id": self.team.id}}
                },
            }
        }

        response = self.api.post("/workers", worker_data)
        worker = Worker.from_json_api(response["data"], self.api_key)

        # Create initial flow
        flow_data = {
            "data": {
                "type": "flows",
                "attributes": {
                    "name": "Initial Flow",
                    "code": flow_code,
                    "label": "initial"  # Optional: provide a default label
                },
                "relationships": {
                    "worker": {"data": {"type": "workers", "id": worker.id}},
                },
            }
        }

        self.api.post("/flows", flow_data)

        return worker

    def read_worker(self, worker_id: str) -> Worker:
        """
        Fetch a single worker by ID
        
        Args:
            worker_id: The ID of the worker to fetch
            
        Returns:
            Worker: The worker object
            
        Raises:
            HTTPError: If the worker is not found or other API errors occur
        """
        response = self.api.get(f"/workers/{worker_id}")
        return Worker.from_json_api(response["data"], self.api_key)
