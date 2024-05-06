from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from .base import PageMixin

class SystemEditor(PageMixin, Gtk.Box):
    def __init__(self, fb_project=None, current_tool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fb_project = fb_project
        self.current_tool = current_tool
        
        self.paned = Gtk.Paned(wide_handle=True)
        self.project_bar = Gtk.ActionBar()
        self.project_frame = Gtk.Frame()
        self.open_menu = Gio.Menu.new()
        self.sidebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign=Gtk.Align.FILL)
        self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign=Gtk.Align.FILL)

        self.project_frame.set_child(self.project_bar)
        self.vbox.append(self.project_frame)
        self.append(self.vbox)
        self.append(self.paned)
        self.paned.set_vexpand(True)
        self.paned.set_hexpand(True)
        self.paned.set_start_child(self.scrolled)
        self.paned.set_resize_start_child(True)
        self.paned.set_shrink_start_child(False)
        self.paned.set_end_child(self.sidebox)
        self.paned.set_resize_end_child(False)
        self.paned.set_shrink_end_child(False)

        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(self.open_menu)

        self.open_menu_button = Gtk.MenuButton()
        self.open_menu_button.set_popover(self.popover)
        self.open_menu_button.set_label("This Project")

        self.project_bar.pack_start(self.open_menu_button)


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
