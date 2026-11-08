"""Widget-controller smoke tests without a desktop or display dependency."""
import unittest
from unittest.mock import patch

from pool.ui import TableApp


class Var:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class Widget:
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class Root(Widget):
    def __init__(self):
        self.pending = []

    def after(self, delay, callback):
        self.pending.append(callback)


class UITests(unittest.TestCase):
    def setUp(self):
        self.patchers = [patch('pool.ui.tk.IntVar', Var), patch('pool.ui.tk.StringVar', Var)]
        self.patchers += [patch('pool.ui.' + path, Widget) for path in ('tk.Canvas', 'tk.Spinbox', 'ttk.Label', 'ttk.Frame', 'ttk.Radiobutton', 'ttk.Button')]
        for p in self.patchers:
            p.start()
            self.addCleanup(p.stop)

    def test_human_baseline_complete_and_restart(self):
        root = Root()
        app = TableApp(root, 'hvb')
        for _ in range(12):
            if app.episode.reason:
                break
            app.shoot()
            self.assertEqual(app.episode.active_player, 'p2')
            while root.pending:
                root.pending.pop(0)()
        self.assertEqual(app.episode.outcome()['status'], 'terminal')
        self.assertFalse(app.episode.outcome()['failure'])
        app.restart()
        self.assertEqual(app.episode.attempts, 0)
        self.assertEqual(app.episode.active_player, 'p1')

    def test_human_human_aim_and_alternate(self):
        app = TableApp(Root(), 'hvh')
        event = type('Event', (), {'x': 270, 'y': 100})()
        app.aim(event)
        self.assertEqual(app.angle.get(), 270)
        app.shoot()
        self.assertEqual(app.episode.active_player, 'p2')
        app.shoot()
        self.assertEqual(app.episode.active_player, 'p1')
        self.assertEqual(app.episode.attempts, 2)
