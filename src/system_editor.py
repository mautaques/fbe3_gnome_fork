from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import GLib
from .base import PageMixin

class SystemEditor(PageMixin, Gtk.Box):
    
    def __init__(self, window, system=None, current_tool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.system = system
        self.current_tool = current_tool
        self.window = window
        
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_margin_start(5)
        self.set_margin_top(5)
        self.set_margin_end(5)
        self.set_margin_bottom(5)
        self.set_homogeneous(True)
        self.set_vexpand(True)
        self.info_vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.info_vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.info_vbox_left.set_homogeneous(True)
        self.info_vbox_right.set_homogeneous(True)
        self.append(self.info_vbox_left)
        self.append(self.info_vbox_right)
        
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
        
        # -------------- Gesture Handling ---------------- #
        
        gesture_click_applications = Gtk.GestureClick()
        gesture_click_applications.set_button(1)  # Set to listen to left-click
        gesture_click_applications.connect("pressed", self.on_gesture_click_applications)  # Connect event handler
        
        gesture_click_sys_device = Gtk.GestureClick()
        gesture_click_sys_device.set_button(1)  # Set to listen to left-click
        gesture_click_sys_device.connect("pressed", self.on_gesture_click_device)  # Connect event handler
       
        gesture_click_sys_resource = Gtk.GestureClick()
        gesture_click_sys_resource.set_button(1)  # Set to listen to left-click
        gesture_click_sys_resource.connect("pressed", self.on_gesture_click_resource)  # Connect event handler
        
        # ------------- Applications List ---------------- #
        
        self.applications_list = Gtk.ListBox()
        self.applications_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.applications_vbox.append(self.applications_list)

        for app in self.system.applications:
            if app.subapp_network.function_blocks:
                app_expander = Gtk.Expander(label=app.name)
                fb_list = Gtk.ListBox()
                fb_list.set_show_separators(True)
                fb_list.set_selection_mode(Gtk.SelectionMode.NONE)
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
                
        # ---------------- System Config ------------------- #
        
        self.sys_config_list = Gtk.ListBox()
        self.sys_config_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.sys_config_vbox.append(self.sys_config_list)

        for dev in self.system.devices:
            if dev.resources:
                dev_expander = Gtk.Expander(label=dev.name)
                resources_list = Gtk.ListBox()
                resources_list.set_show_separators(True)
                resources_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
                resources_list.add_controller(gesture_click_sys_resource)
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
        
        
        self.applications_list.add_controller(gesture_click_applications)  # Add to the list box
        self.sys_config_list.add_controller(gesture_click_sys_device)  # Add to the list box                
        

    def _create_entry_(self, section, entry_name):
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, margin_start=5, margin_top=5, margin_end=5, margin_bottom=5)
        section.append(hbox)
        label = Gtk.Label(label=entry_name)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        label.set_width_chars(13)
        hbox.append(label)
        hbox.append(entry)
            
    def on_gesture_click_applications(self, gesture, n_press, x, y):
        if n_press == 2:  # Check if it is a double-click
            target = gesture.get_widget().get_selected_row()
            if isinstance(target, Gtk.ListBoxRow):
                app = target.get_child()  # Get the label
                if isinstance(app, Gtk.Expander):
                    application = self.system.application_get(app.get_label())
                    print(application.name)
                    # editor = Fun
                elif isinstance(app, Gtk.Label):
                    print("here")
                    if not isinstance(app.get_parent(), Gtk.Expander):
                        application = self.system.application_get(app.get_label())
                        print(application.name)
    
    def on_gesture_click_device(self, gesture, n_press, x, y):
        if n_press == 2:  # Check if it is a double-click
            target = gesture.get_widget().get_selected_row()
            if isinstance(target, Gtk.ListBoxRow):
                dev = target.get_child()  # Get the label
                if isinstance(dev, Gtk.Expander):
                    device = self.system.device_get(dev.get_label())
                    print(device.name)
                    # editor = Fun
                elif isinstance(dev, Gtk.Label):
                    device = self.system.device_get(dev.get_label())
                    print(device.name)
    
    def on_gesture_click_resource(self, gesture, n_press, x, y):
        self.sys_config_list.unselect_all()
        if n_press == 2:
            target = gesture.get_widget().get_selected_row()
            if isinstance(target, Gtk.ListBoxRow):
                res = target.get_child()
                while(not isinstance(target, Gtk.Expander)):
                    target = target.get_parent()
                dev = self.system.device_get(target.get_label())
                resource = dev.resource_get(res.get_label())
                print(resource.name)

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

    def on_my_app(self):
        print('app')

    def on_system_config(self):
        print('config')
