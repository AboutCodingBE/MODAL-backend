import uuid
import time


class ArchiveStorage:
    def __init__(self, archives_dict: dict, analysis_results_dict: dict):
        self._archives = archives_dict
        self._analysis_results = analysis_results_dict

    def create_archive(self, name: str, path: str) -> str:
        archive_id = str(uuid.uuid4())[:8]
        self._archives[archive_id] = {
            "id": archive_id,
            "name": name,
            "path": path,
            "status": "ingested",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        return archive_id

    def get_archive(self, archive_id: str) -> dict | None:
        return self._archives.get(archive_id)

    def get_all_archives(self) -> list:
        return list(self._archives.values())

    def archive_exists(self, name: str) -> bool:
        return any(a["name"] == name for a in self._archives.values())

    def update_status(self, archive_id: str, status: str):
        if archive_id in self._archives:
            self._archives[archive_id]["status"] = status

    def store_analysis(self, archive_id: str, analysis: dict):
        self._analysis_results[archive_id] = analysis

    def get_analysis(self, archive_id: str) -> dict | None:
        return self._analysis_results.get(archive_id)
