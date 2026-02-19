import os


class FolderValidator:
    def validate(self, folder_path: str) -> tuple[bool, str | None]:
        if not folder_path or not folder_path.strip():
            return False, "Pad mag niet leeg zijn."

        path = folder_path.strip()

        if not os.path.exists(path):
            return False, f"Pad bestaat niet: {path}"

        if not os.path.isdir(path):
            return False, f"Pad is geen map: {path}"

        if not os.access(path, os.R_OK):
            return False, f"Geen leesrechten voor: {path}"

        try:
            contents = os.listdir(path)
        except PermissionError:
            return False, f"Geen toegang tot map: {path}"

        if len(contents) == 0:
            return False, f"Map is leeg: {path}"

        return True, None
