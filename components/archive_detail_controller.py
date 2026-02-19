class ArchiveDetailController:
    def __init__(self, storage):
        self._storage = storage

    def get_detail(self, archive_id: str, current_folder: str = "/") -> dict | None:
        archive = self._storage.get_archive(archive_id)
        if not archive:
            return None

        analysis = self._storage.get_analysis(archive_id)

        result = {
            "archive_id": archive_id,
            "name": archive["name"],
            "path": archive["path"],
            "status": archive["status"],
            "created_at": archive["created_at"],
            "total_files": None,
            "file_types": {},
            "current_folder": current_folder,
            "folder_info": None,
        }

        if analysis:
            result["total_files"] = analysis["total_files"]
            result["file_types"] = analysis["file_types"]
            result["folder_info"] = analysis["folder_structure"].get(current_folder)

        return result
