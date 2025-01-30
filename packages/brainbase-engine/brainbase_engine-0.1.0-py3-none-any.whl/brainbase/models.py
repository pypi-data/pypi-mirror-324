from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from .connection import Connection
from .json_client import JsonApiClient
from .utils import get_api_url, get_ws_url

@dataclass
class Team:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Worker:
    id: str
    name: str
    description: Optional[str]
    status: Optional[str]
    team_id: str
    created_at: datetime
    updated_at: datetime
    last_refreshed_at: Optional[datetime]
    _api_key: str
    _base_url: str

    def run(
        self,
        flow_id: Optional[str] = None,
        streaming: bool = True,
        monitor: bool = False,
        functions: Optional[List[Dict[str, Any]]] = None,
        verify_ssl: bool = True,
    ) -> Connection:
        """
        Establish a WebSocket connection to the worker.

        Args:
            flow_id (str, optional): The ID of the flow to run. Defaults to None.
            streaming (bool, optional): Enable message streaming. Defaults to True.
            monitor (bool, optional): Enable connection monitoring. Defaults to True.
            functions (List[Dict[str, Any]], optional): List of function definitions. Defaults to None.
            verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True.

        Returns:
            Connection: A connection instance that can be used to send/receive messages

        Example:
            >>> connection = worker.run(streaming=True)
            >>> connection.on("message", handle_message)
        """
        if flow_id is None:
            flow = self.get_latest_flow()
            flow_id = flow["id"]


        connection = Connection(
            api_key=self._api_key, flow_id=flow_id, base_url=self._base_url
        )

        connection.connect(
            streaming=streaming, monitor=monitor, functions=functions or [], verify_ssl=verify_ssl
        )
        return connection

    def get_latest_flow(self) -> str:
        """
        Gets the most recently updated flow ID for this worker.

        Returns:
            str: The ID of the most recently updated flow

        Raises:
            ValueError: If no flows are found for the worker
        """
        client = JsonApiClient(
            self._api_key, get_api_url()
        )
        response = client.get(f"/workers/{self.id}/flows")

        flows = response.get("data", [])
        if not flows:
            raise ValueError(f"No flows found for worker {self.id}")

        # Sort flows by updatedAt timestamp and get the most recent
        latest_flow = max(
            flows,
            key=lambda f: datetime.fromisoformat(
                f["attributes"]["updatedAt"].rstrip("Z")
            ),
        )

        return latest_flow

    @classmethod
    def from_json_api(cls, data: Dict, api_key: str) -> "Worker":
        attrs = data["attributes"]
        worker = cls(
            id=data["id"],
            name=attrs["name"],
            description=attrs.get("description"),
            status=attrs.get("status"),
            team_id=attrs["teamId"],
            created_at=datetime.fromisoformat(attrs["createdAt"].rstrip("Z")),
            updated_at=datetime.fromisoformat(attrs["updatedAt"].rstrip("Z")),
            last_refreshed_at=(
                datetime.fromisoformat(attrs["lastRefreshedAt"].rstrip("Z"))
                if attrs.get("lastRefreshedAt")
                else None
            ),
            _api_key=api_key,
            _base_url=get_ws_url(),
        )
        return worker
