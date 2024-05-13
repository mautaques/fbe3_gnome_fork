from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import GLib
from .base import PageMixin
from .system_editor import SystemEditor
from .fb_editor import FunctionBlockEditor

@Gtk.Template(resource_path='/com/lapas/Fbe/menu.ui')
class ProjectEditor(PageMixin, Gtk.Box):
    __gtype_name__ = 'ProjectEditor'
    
    project_menu_button = Gtk.Template.Child()
    system_config_menu = Gtk.Template.Child()
    primary_menu = Gtk.Template.Child()
    
    def __init__(self, window, system=None, current_editor=None, current_tool=None, system_editor=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print(type(current_editor))
        self.window = window
        self.system = system
        self.current_editor = current_editor  # Either a system editor or application editor
        self.current_tool = current_tool
        self.system_editor = SystemEditor(window, system)
        self.applications_editors = list()
        
        if current_editor is None:
            self.current_editor = self.system_editor  # Always open in system editor 
        
        self.open_menu = Gio.Menu.new()
        self.project_bar = Gtk.ActionBar(valign=Gtk.Align.START)
        self.vpaned = Gtk.Paned(wide_handle=True, orientation = Gtk.Orientation.VERTICAL)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.vbox.set_vexpand(True)
        self.vpaned.set_start_child(self.project_bar)
        self.vpaned.set_resize_start_child(False)
        self.vpaned.set_end_child(self.current_editor)
        self.vpaned.set_resize_end_child(True)
        self.vbox.append(self.vpaned)
        self.vbox.set_hexpand(True)
        self.append(self.vbox)
        
        self.project_menu_button.set_label(self.system.name)
        
        for app in self.system.applications:
            label = app.name
            label_action = label+"-app"
            self._create_action(label_action, self.on_application_editor, app)
            self.primary_menu.append(label, "win."+label_action)
        
        for dev in self.system.devices:
            label = dev.name
            label_action = label+"-dev"
            self._create_action(label_action, self.on_application_editor)
            self.system_config_menu.append(label, "win."+label_action)
            
        self.project_bar.pack_start(self.project_menu_button)
          
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
        action = Gio.SimpleAction.new(action_name, None)
        if not args:
            action.connect("activate", callback)
            self.window.add_action(action)
        else:
            action.connect("activate", callback, args)
            self.window.add_action(action)

    def on_application_editor(self, action, param=None, app=None):
        app_editor = FunctionBlockEditor(app[0])
        self.current_editor = app_editor
        self.vpaned.set_end_child(self.current_editor)

    def on_system_config(self):
        print('config')
