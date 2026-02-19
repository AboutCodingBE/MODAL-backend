# Use Case

The goal of this use case is to allow users to select a folder on their system, create an "archive" record for it, perform an initial analysis of the folder structure, and then browse the archive contents with folder summaries.

The input of this use case:
- A folder path selected by the user through a folder picker UI component
- An archive name (string) provided by the user

Input mechanism of this use case:
- Streamlit UI with a folder selection widget (can use text input for folder path since Streamlit doesn't have native folder picker)
- Text input field for the archive name
- Submit button to trigger archive creation

The output of this feature:
1. **Archive creation confirmation**: Display success message with archive name and path
2. **Analysis progress indicator**: Show that background analysis is running
3. **Archive list view**: Display all created archives with their status (analyzing/ready)
4. **Archive detail view**: When user selects an archive, show:
    - Archive name and folder path
    - Total number of files (excluding directories)
    - File type breakdown (dictionary of extension → count)
    - Interactive folder tree browser where each folder shows:
        - Folder name
        - Number of files in that folder (not including subdirectories)
        - List of subfolders (clickable to drill down)

Example archive storage structure:
```python
archives = {
    "archive_id_1": {
        "name": "Project_Antwerpen_2026",
        "path": "/home/user/documents/project",
        "status": "ready",  # or "analyzing"
        "created_at": "2026-02-18T10:30:00"
    }
}

analysis_results = {
    "archive_id_1": {
        "total_files": 438,
        "file_types": {
            ".pdf": 120,
            ".docx": 85,
            ".jpg": 150,
            ".txt": 83
        },
        "folder_structure": {
            "/": {
                "files_count": 5,
                "subfolders": ["documents", "images", "data"]
            },
            "/documents": {
                "files_count": 85,
                "subfolders": ["reports", "drafts"]
            },
            # ... more folders
        }
    }
}
```

# Business Rules

- Archive names must be unique within the application
- Archive names cannot be empty
- Folder paths must be valid and accessible on the filesystem
- Only count actual files, not directories, in the file count
- File type analysis should extract the file extension (e.g., ".pdf", ".docx")
- Files without extensions should be counted under "no_extension" category
- Hidden files (starting with ".") should be included in the analysis
- Analysis should traverse all subdirectories recursively
- For folder summaries, only count files directly in that folder (not in subdirectories)
- Use simple in-memory dictionaries for storage (this is a PoC)
- Generate unique archive IDs automatically (e.g., using timestamp or UUID)
- Archive status starts as "analyzing" and changes to "ready" when analysis completes
- If folder path doesn't exist or is inaccessible, show error message and don't create archive
- Analysis should handle file access errors gracefully (skip files that can't be read)

# Component Overview

## ArchiveManagementUI

This is the main Streamlit UI component that orchestrates the entire feature. It manages the page state and decides which view to show (archive creation form, archive list, or archive detail view).

The input of this component:
- User interactions with Streamlit widgets (button clicks, text inputs, selections)

The output of this component:
- Rendered Streamlit UI with appropriate views based on current state
- Updates to session state for navigation between views

This component depends on:
- ArchiveCreationController
- ArchiveListController
- ArchiveDetailController
- Streamlit session state for managing navigation

## ArchiveCreationController

Handles the logic for creating a new archive record when the user submits the folder selection form.

The input of this component:
- archive_name (string): The name provided by the user
- folder_path (string): The path to the folder selected by the user

The output of this component:
- Success: Returns the newly created archive_id (string)
- Failure: Returns None and an error message (string)

Validation performed:
- Check if archive name is not empty
- Check if archive name is unique
- Verify folder path exists and is accessible
- Create archive record in the archives dictionary
- Set initial status to "analyzing"
- Trigger background analysis

This component depends on:
- ArchiveStorage (for storing archive record)
- FolderValidator (for validating folder path)
- ArchiveAnalyzer (to trigger analysis in background)

## ArchiveStorage

Manages the in-memory storage of archive records using Python dictionaries.

The input of this component:
- For create_archive: name (string), path (string)
- For get_archive: archive_id (string)
- For get_all_archives: no parameters
- For archive_exists: name (string)

The output of this component:
- create_archive: Returns archive_id (string)
- get_archive: Returns archive dictionary or None
- get_all_archives: Returns list of all archive dictionaries
- archive_exists: Returns boolean

This component maintains two dictionaries:
```python
archives = {}  # archive_id -> archive_record
analysis_results = {}  # archive_id -> analysis_data
```

This component depends on:
- No dependencies (pure storage layer)

## FolderValidator

Validates that a folder path is accessible and suitable for archiving.

The input of this component:
- folder_path (string): The path to validate

The output of this component:
- is_valid (boolean): Whether the path is valid
- error_message (string or None): Description of validation failure if any

Validation checks:
- Path exists
- Path is a directory (not a file)
- Path is readable
- Path is not empty (contains at least one item)

This component depends on:
- Python os and pathlib modules

## ArchiveAnalyzer

Performs the recursive analysis of the folder structure in the background (simulated for Streamlit - actually runs synchronously but updates status).

The input of this component:
- archive_id (string): The ID of the archive to analyze
- folder_path (string): The root folder to analyze

The output of this component:
- Updates the analysis_results dictionary with:
    - total_files (int)
    - file_types (dict mapping extension to count)
    - folder_structure (dict mapping folder path to folder info)
- Updates archive status to "ready" when complete

Analysis process:
1. Recursively walk through all folders starting from root
2. For each file encountered:
    - Increment total file count
    - Extract file extension and increment type counter
3. For each folder encountered:
    - Count files directly in that folder
    - Record list of immediate subfolders
4. Store all results in analysis_results dictionary
5. Update archive status to "ready"

This component depends on:
- ArchiveStorage (to update status and store results)
- Python os.walk for directory traversal

## ArchiveListController

Prepares data for displaying the list of all archives.

The input of this component:
- No direct parameters (reads from storage)

The output of this component:
- List of archive summaries, each containing:
    - archive_id
    - name
    - path
    - status
    - total_files (if analysis complete)

This component depends on:
- ArchiveStorage (to fetch all archives)

## ArchiveDetailController

Prepares data for displaying a single archive's details and folder browser.

The input of this component:
- archive_id (string): The archive to display

The output of this component:
- Archive details including:
    - name
    - path
    - total_files
    - file_types breakdown
- Current folder view containing:
    - current_folder_path
    - files_count in current folder
    - list of subfolders

Maintains navigation state:
- Tracks current folder being viewed
- Allows drilling down into subfolders
- Allows navigating back up to parent folders

This component depends on:
- ArchiveStorage (to fetch archive and analysis data)

## FolderBrowserUI

Renders the interactive folder tree browser for navigating through archive contents.

The input of this component:
- archive_id (string)
- current_folder_path (string): The folder currently being viewed

The output of this component:
- Rendered Streamlit UI showing:
    - Breadcrumb navigation for current path
    - Number of files in current folder
    - Clickable list of subfolders
    - Back button to go to parent folder

This component depends on:
- Streamlit session state for navigation
- ArchiveDetailController for data

# Implementation Notes

**Streamlit-specific considerations:**
- Use `st.session_state` to maintain archive storage between reruns
- Initialize dictionaries in session_state on first load
- Use `st.text_input()` for folder path (since no native folder picker)
- Use `st.button()` for navigation between views
- Use `st.selectbox()` or clickable links for archive selection
- Use `st.expander()` or columns to organize the folder browser
- Consider using `st.spinner()` during analysis (even though it's synchronous)
- Use `st.success()` and `st.error()` for user feedback

**File traversal:**
- Use `os.walk()` for recursive directory traversal
- Use `os.path.splitext()` to extract file extensions
- Handle exceptions when accessing files (permission errors, etc.)
- Count only files (use `os.path.isfile()` to filter)

**Data structure tips:**
- Generate archive_id using timestamp: `str(int(time.time()))`
- Store folder_structure as nested dictionary with folder paths as keys
- Use relative paths from archive root for folder keys
- For breadcrumb navigation, split folder path on "/" and create clickable segments

**Error handling:**
- Wrap file operations in try-except blocks
- Show user-friendly error messages in Streamlit UI
- Skip files that can't be read but continue analysis
- Validate all user inputs before processing

**UI Flow:**
1. Default view: Show archive creation form at top, archive list below
2. When archive created: Show success message, automatically show new archive in list
3. When archive clicked: Navigate to detail view with folder browser
4. Provide "Back to List" button in detail view