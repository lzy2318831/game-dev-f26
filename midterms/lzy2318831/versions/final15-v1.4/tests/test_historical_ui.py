import unittest
from unittest.mock import patch

from test_ui import Var,Widget,Root
from historical.ui import ArcadeApp


class HistoricalUI(unittest.TestCase):
    def setUp(self):
        for path, replacement in [('tk.IntVar',Var),('tk.StringVar',Var),('tk.BooleanVar',Var),
            ('tk.Canvas',Widget),('tk.Frame',Widget),('tk.Label',Widget),('tk.Button',Widget),
            ('tk.Radiobutton',Widget),('tk.Checkbutton',Widget),('tk.Spinbox',Widget)]:
            p=patch('historical.ui.'+path,replacement)
            p.start()
            self.addCleanup(p.stop)

    def test_start_steer_pause_restart_and_game_over(self):
        app=ArcadeApp(Root(),mode='hvh')
        self.assertEqual(app.screen,'start')
        app.start()
        self.assertEqual(app.screen,'playing')
        x=app.episode.balls[0].x
        app.keys.add('right')
        app.advance()
        app.advance()
        self.assertGreater(app.episode.balls[0].x,x)
        app.pause()
        frames=app.episode.frames
        app.advance()
        self.assertEqual(app.episode.frames,frames)
        app.pause()
        app.episode.active_player='p2'
        app.episode.heat=2
        app.episode.timer=0
        app.episode.frames=63
        app.advance()
        self.assertEqual(app.screen,'over')
        app.start()
        self.assertEqual(app.episode.frames,0)
        self.assertEqual(app.episode.scores,{'p1':0,'p2':0})

    def test_baseline_turn_and_mouse_controls_use_valid_actions(self):
        app=ArcadeApp(Root(),mode='hvb')
        app.start()
        app.episode._end_segment('scratch')
        app.advance()
        self.assertTrue(app.episode.valid(app.action))
        app.start()
        app.mouse_down=True
        app.mouse=(100,152)
        self.assertTrue(app.episode.valid(app.human_action()))
