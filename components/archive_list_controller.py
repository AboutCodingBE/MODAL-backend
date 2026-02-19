class ArchiveListController:
    def __init__(self, storage):
        self._storage = storage

    def get_archives(self) -> list:
        result = []
        for archive in self._storage.get_all_archives():
            summary = {
                "archive_id": archive["id"],
                "name": archive["name"],
                "path": archive["path"],
                "status": archive["status"],
                "created_at": archive["created_at"],
                "total_files": None,
            }
            if archive["status"] == "ready":
                analysis = self._storage.get_analysis(archive["id"])
                if analysis:
                    summary["total_files"] = analysis["total_files"]
            result.append(summary)
        return result
