# Function Block Editor

An application for modelling function blocks based on IEC 61499.

Requirements:
 - Python3
 - GNOME Builder (Available only for LINUX)
 - Flatpak (Required for installing GNOME Builder)

How to install Builder:
 1. Install Flatpak:
    '''sudo apt install flatpak'''
 2. Add the flathub repository:
    '''flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo'''
 3. Restart your system
 4. Install GNOME Builder:
    '''flatpak install flathub org.gnome.Builder'''

To run FBE:
 1. Clone the FBE repository:
    ```git clone https://github.com/cabralbonin/fbe3_gnome.git```
 2. Open Builder and then open FBE project
 3. Run project (Shift+Ctrl+Space)

