 # Function Block Editor

An application for modelling function blocks based on IEC 61499. 

## Requirements:
 - Python3
 - GNOME Builder (Available only for LINUX)
 - Flatpak (Required for installing GNOME Builder)

**How to install Builder:**
 1. Install Flatpak:
    ```
    sudo apt install flatpak
    ```
 3. Add the flathub repository:
    ```
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    ```
 4. Restart your system
 5. Install GNOME Builder:
    ```
    flatpak install flathub org.gnome.Builder
    ```

## To run FBE:
 1. Clone the FBE repository:
    ```
    git clone https://github.com/cabralbonin/fbe3_gnome.git
    ```
 3. Open Builder then add the FBE project.
 4. Open the project
 5. Run project (Shift+Ctrl+Space)

