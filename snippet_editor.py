import sublime, sublime_plugin
import os, re
from glob import iglob

TEMPLATE = """<snippet>
  <!-- Example: Hello, ${1:this} is a ${2:snippet}. -->
  <content><![CDATA[
%s
]]></content>
  <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
  <tabTrigger></tabTrigger>
  <description></description>
  <!-- Optional: Set a scope to limit where the snippet will trigger -->
  <scope>%s</scope>
</snippet>"""

class MakeSnippetCommand(sublime_plugin.TextCommand):
    @property
    def snippet_text(self):
        return "\n".join([self.view.substr(i) for i in self.view.sel()])

    @property
    def scopes(self):
        scope_name = self.view.scope_name(self.view.sel()[0].begin())
        return scope_name.strip().replace(' ', ', ')

    def run(self, edit):
        self.ask_file_name()
        

    def ask_file_name(self):
        self.view.window().show_input_panel('File Name', '', self.make_snippet, None, None)

    def make_snippet_file(self, filename):
        with open(filename, 'wb') as f:
            doc = TEMPLATE % (self.snippet_text, self.scopes)

            if int(sublime.version()) >= 3000:
                file.write(bytes(doc, 'UTF-8'))
            else: # To support Sublime Text 2
                file.write(bytes(doc))

    def confirm_file(self, filename):
        if os.path.exists(filename):
            if sublime.ok_cancel_dialog('Override %s?' % filename) is False:
                self.ask_file_name()
                return False
 
        return True

    def make_snippet(self, filepath):
        status_message(sublime.packages_path())
        # filename = filepath + '.sublime-snippet'
        # filename = os.path.join(sublime.packages_path(), 'User', filename)

        # if self.confirm_file(filename):
        #     self.make_snippet(filename)
        #     self.view.window().open_file(filename)
        

class EditSnippetCommand(sublime_plugin.WindowCommand):
    def run(self):
        snippets = [
            [os.path.basename(filepath), filepath]
                for filepath
                    in iglob(os.path.join(sublime.packages_path(), 'User', '*.sublime-snippet'))]

        def on_done(index):
            if index >= 0:
                self.window.open_file(snippets[index][1])
            else:
                view = self.window.active_view()
                if self.window.get_view_index(view)[1] == -1:
                    view.close()

        def on_highlight(index):
            if index >= 0:
                self.window.open_file(snippets[index][1], sublime.TRANSIENT)

        self.window.show_quick_panel([_[0] for _ in snippets], on_done, sublime.MONOSPACE_FONT, -1, on_highlight)