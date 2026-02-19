from .folder_validator import FolderValidator
from .archive_analyzer import ArchiveAnalyzer


class ArchiveCreationController:
    def __init__(self, storage):
        self._storage = storage
        self._validator = FolderValidator()
        self._analyzer = ArchiveAnalyzer(storage)

    def create(self, archive_name: str, folder_path: str) -> tuple[str | None, str | None]:
        if not archive_name or not archive_name.strip():
            return None, "Archiefnaam mag niet leeg zijn."

        archive_name = archive_name.strip()

        if self._storage.archive_exists(archive_name):
            return None, f"Archiefnaam '{archive_name}' bestaat al."

        is_valid, error = self._validator.validate(folder_path)
        if not is_valid:
            return None, error

        archive_id = self._storage.create_archive(archive_name, folder_path.strip())
        return archive_id, None

    def run_analysis(self, archive_id: str) -> str | None:
        archive = self._storage.get_archive(archive_id)
        if not archive:
            return "Archief niet gevonden."
        self._analyzer.analyze(archive_id, archive["path"])
        return None
