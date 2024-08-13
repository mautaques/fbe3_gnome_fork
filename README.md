# Function Block Editor

An application for modelling function blocks based on IEC 61499. 

## Requirements:
 - Python3
 - GNOME Builder (Available only for LINUX)
 - Flatpak (Required for installing GNOME Builder)
    
### How to install Builder:
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

## How to use:
#### When no project is open, this is what the application looks like:
!["Testing"](https://github.com/user-attachments/assets/063bae90-5ae6-4098-8046-632c894e5f50)

#### On the left side there's the editor workspace with basic tools like add, move, inspect, delete and connect. 
![editorworkspace](https://github.com/user-attachments/assets/ba16acda-1554-4ab0-b3c4-74049b2f5d5c)

#### Right below there's the import library space, where you can load a path (e.g., home/user/documents/mylibrary) and also refresh once there's a change in the directory.
![loadlibrary](https://github.com/user-attachments/assets/04dc3313-73e9-4332-a20b-f762cf60ae1f)
![loadinglibrary](https://github.com/user-attachments/assets/5c9c80bc-5cfe-4c0c-a33c-1596eb74d66d)
![loaledlibrary](https://github.com/user-attachments/assets/9ed03a2f-88ba-48f1-accb-fc3918b41ae2)

#### The header bar also holds some important functions:
![headerbar](https://github.com/user-attachments/assets/c9778672-4c1f-4199-93f0-c160ca552779)

#### The left button presents the options to create, open, save, save as and export a project

#### While the right button is where you can access preferences, keyboard shortcuts, read about FBE and also quit the application 
