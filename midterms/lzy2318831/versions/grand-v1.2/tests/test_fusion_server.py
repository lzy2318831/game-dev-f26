import unittest
from fusion.server import GameSession


class FusionSessionTests(unittest.TestCase):
    def test_playback_lock_and_modes(self):
        s=GameSession()
        state=s.reset('hvh')
        self.assertEqual(state['mode'],'hvh')
        result=s.shoot({'angle':0,'power':40})
        self.assertTrue(result['shot']['accepted'])
        self.assertTrue(result['shot']['frames'])
        with self.assertRaises(ValueError): s.shoot({'angle':180,'power':40})
        s.ready()
        self.assertEqual(s.state()['observation']['active_player'],'p2')
        s.shoot({'angle':180,'power':40})
        s.ready()
        self.assertEqual(s.state()['observation']['shots_remaining'],{'p1':5,'p2':5})

    def test_baseline_selects_own_action_and_reset(self):
        s=GameSession()
        s.reset('hvb')
        s.shoot({'angle':0,'power':30})
        s.ready()
        with self.assertRaises(ValueError): s.shoot({'angle':180,'power':50})
        response=s.shoot(baseline=True)
        self.assertEqual(response['source'],'baseline')
        self.assertTrue(s.episode.valid(response['action']))
        s.reset('hvh')
        self.assertEqual(s.episode.shots,0)
        self.assertFalse(s.playback_pending)
