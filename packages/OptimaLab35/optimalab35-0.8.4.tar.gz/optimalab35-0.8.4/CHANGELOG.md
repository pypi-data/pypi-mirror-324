# Changelog

## 0.8.x
### 0.8.4: Minor Enhancements & Cleanup
- Updated window titles.
- Improved error handling for updater: now displays the specific error message instead of just **"error"** when an issue occurs during update checks.
- Ensured all child windows close when the main window is closed.

### 0.8.3: Fix – OptimaLab35 Not Closing After Update
- Fixed an issue where **OptimaLab35** would not close properly when updating, resulting in an unresponsive instance and multiple running processes.

### 0.8.2: Patch for New PyPiUpdater Version
- Updated to support **PyPiUpdater 0.4.0**.
- Now stores version information locally, preventing an "unknown" state on the first updater launch.
  - Users still need to press the **Update** button to verify the latest version, ensuring an internet connection is available.

### 0.8.1: Fix
- Fixed a misspelling of `PyPiUpdater` in the build file, which prevented v0.8.0 from being installed.

### 0.8.0: Updater Feature
- Added an updater function utilizing my new package [PyPiUpdater](https://gitlab.com/CodeByMrFinchum/PyPiUpdater).
- New updater window displaying the local version and checking for updates online.
- Added an option to update and restart the app from the menu.

---

## 0.7.0: Enhanced Preview
- Images loaded into the preview window are now scaled while maintaining aspect ratio.
- Added live updates: changes to brightness, contrast, or grayscale are applied immediately.
  - This may crush the system depending on image size and system specifications.
- Removed Settings from menuBar, and extended the about window.

---

## 0.6.0: Initial Flatpak Support
- Started Flatpak package building.
- Not added to Flathub yet, as only stable software is hosted there.
- Not fully completed, icon, name, and description are included, but the version is missing for some reason.
- Local build and installation work. The Bash script `build_flatpak.sh` in the `flatpak/` directory generates all pip dependencies, then builds and installs the app locally.
- `requirements-parser` has to be installed from pip to finish installing the flatpak (maybe more pypi packages..)

---

## 0.5.0
- Removed all leftover of tui code that was hiding in some classes.

---

## 0.4.0
- Fixed a critical issue that prevented the program from functioning.
- Updated compatibility to align with the **upcoming** optima35 **release**.

**Removal of TUI:**
- The TUI version is no longer compatible with optima35 v1.0.
- Maintaining two UIs has become too time-consuming, as the primary focus is on the GUI, which provides the best user experience. Recently, the TUI version was only receiving patches without any meaningful enhancements.

---

## 0.3.x
### 0.3.7: prepear for optima35 release
- Added a maximum version of dependencies list.

### 0.3.6: Patch
- Added check if any exif options are empty.
- Also made the exif editor aviable without checking the exif box.

### 0.3.5: Fix
- Fixed an issue where renaming images, while converting could result in wrong numbering.

### 0.3.1 - 0.3.4
- Repo only: Fix building pipeline

### 0.3.0
- Repo only: adding pipeline

---

## 0.2.x
### 0.2.3
- Refactored code for improved readability.

### 0.2.2
- Moved processing images into a different thread, making the UI responsiable while processing

### 0.2.1
- Insert exif to image file (i.e. without changing the file).

### 0.2.0
- Now spaces in rename string are replaces with `_`.
- version check of `optima35`, incase pip did not update it.
- Sorting entries from exif file.

### 0.2.0-a1
- Main UI received a facelift.
- Added a new experimental preview window to display an image and show how changing values affects it.
- Programm now warns for potential overwrite of existing files.

---

## 0.1.x
### 0.1.1
- Update metadata, preview, readme, bump in version for pip

### 0.1.0
- Preserved the current working GUI by pinning `optima35` to a specific version for guaranteed compatibility.

---

## 0.0.x
### 0.0.4-a2
- Adding __version__ to `__init__.py` so version is automaticly updated in program as well as pypi.

### 0.0.4-a1
- Refactored project structure, moving all code to the `src` directory.
- Adjusted imports and setup to accommodate the new folder structure.
- Skipped version numbers to `.4` due to PyPI versioning constraints (testing purposes).

### 0.0.1 - Initial UI-Focused Release
- Forked from OPTIMA35.
- Removed core OPTIMA35 files to focus exclusively on UI components.
- Integrated OPTIMA35 functionality via the pip package.
- Ensured both TUI and GUI modes operate seamlessly.
- Revised the README for improved clarity and structure.
