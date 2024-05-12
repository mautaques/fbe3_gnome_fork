from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import GLib
from .base import PageMixin

class SystemEditor(PageMixin, Gtk.Box):
    def __init__(self, fb_project=None, current_tool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fb_project = fb_project
        self.current_tool = current_tool
        self.click_timer_id = None  # Used to differentiate between single and double clicks
        self.double_click_interval = 300  # Milliseconds to wait for double click
        
        self.open_menu = Gio.Menu.new()
        self.project_bar = Gtk.ActionBar(valign=Gtk.Align.START)
        self.vpaned = Gtk.Paned(wide_handle=True, orientation = Gtk.Orientation.VERTICAL)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.info_vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.info_vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.info_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.info_hbox.append(self.info_vbox_left)
        self.info_hbox.append(self.info_vbox_right)
        self.info_hbox.set_vexpand(True)
        self.info_hbox.set_homogeneous(True)
        self.info_vbox_left.set_homogeneous(True)
        self.info_vbox_right.set_homogeneous(True)
        
        self.vbox.set_vexpand(True)
        self.vpaned.set_start_child(self.project_bar)
        self.vpaned.set_resize_start_child(False)
        self.vpaned.set_end_child(self.info_hbox)
        self.vpaned.set_resize_end_child(True)
        self.vbox.append(self.vpaned)
        self.vbox.set_hexpand(True)
        self.append(self.vbox)
      
        self.sys_info_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_start=10, margin_top=10, margin_end=10, margin_bottom=10)
        self.sys_config_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_start=10, margin_top=10, margin_end=10, margin_bottom=10)
        self.applications_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin_start=10, margin_top=10, margin_end=10, margin_bottom=10)
      
        self.sys_info_expander = Gtk.Expander(label="System Information", margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.sys_info_expander.set_child(self.sys_info_vbox)
        self.sys_info_expander.set_expanded(True)
        self.sys_config_expander = Gtk.Expander(label="System Configuration", margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.sys_config_expander.set_child(self.sys_config_vbox)
        self.sys_config_expander.set_expanded(True)
        self.applications_expander = Gtk.Expander(label="Applications", margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.applications_expander.set_child(self.applications_vbox)
        self.applications_expander.set_expanded(True)
        
        self.sys_info_frame = Gtk.Frame(margin_start=5, margin_top=5, margin_end=5, margin_bottom=5, halign=Gtk.Align.FILL)
        self.sys_info_frame.set_child(self.sys_info_expander)
        
        self.sys_config_frame = Gtk.Frame(margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.sys_config_frame.set_child(self.sys_config_expander)
        
        self.applications_frame = Gtk.Frame(margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        self.applications_frame.set_child(self.applications_expander)
        
        self.info_vbox_left.append(self.sys_info_frame)
        self.info_vbox_left.append(self.applications_frame)
        self.info_vbox_right.append(self.sys_config_frame)
        
        # ------------- System Information ---------------- #
        
        self._create_entry_(self.sys_info_vbox, 'Standard: ')       
        self._create_entry_(self.sys_info_vbox, 'Classification: ')
        self._create_entry_(self.sys_info_vbox, 'Function: ')
        self._create_entry_(self.sys_info_vbox, 'Type: ')
        self._create_entry_(self.sys_info_vbox, 'Description: ')
        
        # ------------- Applications List ---------------- #
        
        self.applications_list = Gtk.ListBox()
        # self.applications_list.connect("row-activated", self.on_row_activated) 
        self.applications_vbox.append(self.applications_list)

        for app in self.fb_project.applications:
            if app.subapp_network.function_blocks:
                app_expander = Gtk.Expander(label=app.name)
                fb_list = Gtk.ListBox()
                app_expander.set_child(fb_list)
                self.applications_list.append(app_expander)
                for fb in app.subapp_network.function_blocks:
                    list_row = Gtk.ListBoxRow()
                    label = Gtk.Label(label=fb.name, halign=Gtk.Align.START, margin_start=20)
                    list_row.set_child(label)
                    fb_list.append(list_row)
                    
            else:
                list_row = Gtk.ListBoxRow()
                label = Gtk.Label(label=app.name, halign=Gtk.Align.START)
                list_row.set_child(label)
                self.applications_list.append(list_row)
                
        # ------------- System Config ---------------- #
        self.sys_config_list = Gtk.ListBox()
        self.sys_config_vbox.append(self.sys_config_list)

        for dev in self.fb_project.devices:
            if dev.resources:
                dev_expander = Gtk.Expander(label=dev.name)
                resources_list = Gtk.ListBox()
                dev_expander.set_child(resources_list)
                self.sys_config_list.append(dev_expander)
                for res in dev.resources:
                    list_row = Gtk.ListBoxRow()
                    label = Gtk.Label(label=res.name, halign=Gtk.Align.START, margin_start=20)
                    list_row.set_child(label)
                    resources_list.append(list_row)
                    
            else:
                list_row = Gtk.ListBoxRow()
                label = Gtk.Label(label=dev.name, halign=Gtk.Align.START)
                list_row.set_child(label)
                self.sys_config_list.append(list_row)
                
        # ----------------------------------------- #
        
        gesture_click = Gtk.GestureClick()
        gesture_click.set_button(2)  # Set to listen to left-click
        gesture_click.connect("pressed", self.on_gesture_click)  # Connect event handler
        self.applications_list.add_controller(gesture_click)  # Add to the list box
        self.sys_config_list.add_controller(gesture_click)  # Add to the list box

                
                    
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(self.open_menu)

        self.open_menu_button = Gtk.MenuButton()
        self.open_menu_button.set_popover(self.popover)
        self.open_menu_button.set_label(self.fb_project.name)

        self.project_bar.pack_start(self.open_menu_button)

    def _create_entry_(self, section, entry_name):
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        section.append(hbox)
        label = Gtk.Label(label=entry_name)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        label.set_width_chars(13)
        hbox.append(label)
        hbox.append(entry)
        
    def on_row_activated(self, list_box, row):
        list_box_row = list_box.get_selected_row()
        if list_box_row:
            label = list_box_row.get_child()  # Get the label
            print(label.get_label())
            
    def on_gesture_click(self, gesture, n_press, x, y):
        if n_press == 2:  # Check if it is a double-click
            target = gesture.get_widget().get_selected_row()
            if isinstance(target, Gtk.ListBoxRow):
                label = target.get_child()  # Get the label
                if label:
                    text = label.get_text()  # Get the text from the label
                    print(f"Double-clicked on row with text: {text}")  # Perform your action here

      
    def save(self, file_path_name=None):
        status = self.selected_fb.save(file_path_name)
        if status == True:
            self._changes_to_save = False
        return status

    def has_file_path_name(self):
        return self.selected_fb.get_file_path_name() is not None

    def get_tab_name(self):
        if self.selected_fb is not None:
            return self.selected_fb.get_name()
        return self

    def _create_action(self, action_name, callback, *args):
        app = self.get_ancestor_window()
        if app is not None:
            action = Gio.SimpleAction.new(action_name, None)
            if not args:
                action.connect("activate", callback)
                app.add_action(action)
            else:
                action.connect("activate", callback, args)
                app.add_action(action)
        else:
            action = Gio.SimpleAction.new(action_name, None)
            if not args:
                action.connect("activate", callback)
                self.add_action(action)
            else:
                action.connect("activate", callback, args)
                self.add_action(action)

    def on_my_app(self):
        print('app')

    def on_system_config(self):
        print('config')
