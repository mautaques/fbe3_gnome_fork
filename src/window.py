# window.py
#
# Copyright 2024 Cabral
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

@Gtk.Template(resource_path='/com/lapas/Fbe/window.ui')
class FbeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FbeWindow'

    main_fbe = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name="open-project")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)

    def open_file_dialog(self, action, parameter):
        # Create a new file selection dialog, using the "open" mode
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filter_fbt = Gtk.FileFilter()
        filter_fbt.set_name("fbt Files")
        filter_fbt.add_pattern("*.fbt")
        filters.append(filter_fbt)
        native = Gtk.FileDialog()
        native.set_filters(filters)
        native.open(self, None, self.on_open_response)

    def on_open_response(self, dialog, result):
        file = dialog.open_finish(result)
        file_name = file.get_path()
        print(file_name)
        # If the user selected a file...
        if file is not None:
            # ... open it
            self.open_file(file)

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):

        contents = file.load_contents_finish(result)
        if not contents[0]:
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")
            return

        try:
            text = contents[1].decode('utf-8')
        except UnicodeError as err:
            path = file.peek_path()
            print(f"Unable to load the contents of {path}: the file is not encoded with UTF-8")
            return


