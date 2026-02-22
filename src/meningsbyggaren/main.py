import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gdk, Gio
import gettext, locale, os, json, time

__version__ = "0.1.0"
APP_ID = "se.danielnylander.meningsbyggaren"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'share', 'locale')
if not os.path.isdir(LOCALE_DIR): LOCALE_DIR = "/usr/share/locale"
try:
    locale.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.textdomain(APP_ID)
except Exception: pass
_ = gettext.gettext
def N_(s): return s


WORD_CATEGORIES = [
    {"name": N_("People"), "words": [N_("I"), N_("You"), N_("Mom"), N_("Dad"), N_("Friend")]},
    {"name": N_("Actions"), "words": [N_("want"), N_("eat"), N_("drink"), N_("play"), N_("read"), N_("go"), N_("sleep")]},
    {"name": N_("Things"), "words": [N_("food"), N_("water"), N_("ball"), N_("book"), N_("toy"), N_("car")]},
    {"name": N_("Places"), "words": [N_("home"), N_("school"), N_("park"), N_("store")]},
    {"name": N_("Feelings"), "words": [N_("happy"), N_("sad"), N_("tired"), N_("hungry"), N_("thirsty")]},
]

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(_('Sentence Builder'))
        self.set_default_size(600, 500)
        self._sentence = []
        
        header = Adw.HeaderBar()
        menu_btn = Gtk.MenuButton(icon_name='open-menu-symbolic')
        menu = Gio.Menu()
        menu.append(_('Clear'), 'win.clear')
        menu.append(_('About'), 'app.about')
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)
        
        clear_action = Gio.SimpleAction.new('clear', None)
        clear_action.connect('activate', lambda a,p: self._clear())
        self.add_action(clear_action)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main.append(header)
        
        # Sentence display
        self._sentence_label = Gtk.Label(label=_('Tap words to build a sentence'))
        self._sentence_label.add_css_class('title-2')
        self._sentence_label.set_wrap(True)
        self._sentence_label.set_margin_top(16)
        self._sentence_label.set_margin_start(16)
        self._sentence_label.set_margin_end(16)
        main.append(self._sentence_label)
        
        # Word categories
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(16)
        content.set_margin_start(16)
        content.set_margin_end(16)
        content.set_margin_bottom(16)
        
        for cat in WORD_CATEGORIES:
            label = Gtk.Label(label=_(cat['name']), xalign=0)
            label.add_css_class('title-4')
            content.append(label)
            
            flow = Gtk.FlowBox()
            flow.set_max_children_per_line(6)
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_homogeneous(True)
            
            for word in cat['words']:
                btn = Gtk.Button(label=_(word))
                btn.add_css_class('pill')
                btn.connect('clicked', self._on_word, word)
                flow.insert(btn, -1)
            content.append(flow)
        
        scroll.set_child(content)
        main.append(scroll)
        
        # Bottom controls
        btns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btns.set_margin_bottom(12)
        btns.set_margin_start(16)
        btns.set_margin_end(16)
        btns.set_halign(Gtk.Align.CENTER)
        
        undo_btn = Gtk.Button(label=_('Undo'))
        undo_btn.add_css_class('pill')
        undo_btn.connect('clicked', lambda b: self._undo())
        btns.append(undo_btn)
        
        clear_btn = Gtk.Button(label=_('Clear'))
        clear_btn.add_css_class('destructive-action')
        clear_btn.add_css_class('pill')
        clear_btn.connect('clicked', lambda b: self._clear())
        btns.append(clear_btn)
        
        main.append(btns)
        self.set_content(main)
    
    def _on_word(self, btn, word):
        self._sentence.append(_(word))
        self._update_sentence()
    
    def _undo(self):
        if self._sentence:
            self._sentence.pop()
            self._update_sentence()
    
    def _clear(self):
        self._sentence.clear()
        self._update_sentence()
    
    def _update_sentence(self):
        if self._sentence:
            self._sentence_label.set_text(' '.join(self._sentence))
        else:
            self._sentence_label.set_text(_('Tap words to build a sentence'))

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id='se.danielnylander.meningsbyggaren')
        self.connect('activate', self._on_activate)
        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', self._on_about)
        self.add_action(about)
    def _on_activate(self, app):
        win = MainWindow(application=app)
        win.present()
    def _on_about(self, a, p):
        d = Adw.AboutDialog(application_name=_('Sentence Builder'), application_icon=APP_ID,
            version=__version__, developer_name='Daniel Nylander',
            website='https://github.com/yeager/meningsbyggaren',
            license_type=Gtk.License.GPL_3_0,
            comments=_('Build sentences with word cards'),
            developers=['Daniel Nylander <daniel@danielnylander.se>'])
        d.present(self.get_active_window())


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
