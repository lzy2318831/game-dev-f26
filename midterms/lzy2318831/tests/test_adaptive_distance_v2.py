"""Adaptive intended range, not a floor; no changes to the rollback modes."""
import unittest
from copy import deepcopy
from fusion.geometry_adaptive_power import adaptive_recommendations


class AdaptiveDistanceV2(unittest.TestCase):
    def test_boundaries_interpolation_rounding_and_cap(self):
        from fusion.geometry_adaptive_power import distance_power
        cases=[(-5,30),(0,30),(7.5,31),(75,35),(149.9,40),(150,40),
               (150.1,40),(155,41),(250,60),(349.9,80),(350,80),
               (350.1,80),(675,90),(1000,100),(2000,100)]
        for distance,power in cases:self.assertEqual(distance_power(distance),power,(distance,power))

    def test_monotone_legal_integer_profile(self):
        from fusion.geometry_adaptive_power import distance_power
        values=[distance_power(i/10) for i in range(12001)]
        self.assertEqual(values,sorted(values));self.assertTrue(all(type(p) is int and 30<=p<=100 for p in values))

    def test_intended_power_ignores_base_floor_and_preserves_identity(self):
        rows=[dict(id=i,route=route,travel=distance,power=base,angle=17,target=i,risk='base')
              for i,(route,distance,base) in enumerate([('contact',75,90),('pot',250,95),('bank-contact',675,1)],1)]
        before=deepcopy(rows);changed=adaptive_recommendations(rows)
        self.assertEqual([r['power'] for r in changed],[35,60,90])
        self.assertEqual(rows,before)
        for a,b in zip(rows,changed):
            self.assertEqual((a['id'],a['angle'],a['target'],a['route']),(b['id'],b['angle'],b['target'],b['route']))
            self.assertNotIn('adaptive_floor',b)

    def test_escape_fallback_and_device_keep_prior_separate_treatment(self):
        rows=[dict(id=i,route=route,travel=800,power=base,angle=0,target=None,risk='base')
              for i,(route,base) in enumerate([('escape',5),('fallback-escape',1),('device',65)],1)]
        self.assertEqual([r['power'] for r in adaptive_recommendations(rows)],[10,2,100])

    def test_mandatory_266_position_on_unchanged_current_physics(self):
        from fusion.geometry_power_calibration import observations
        from fusion.engine import DEVICES
        from fusion.geometry_candidates import candidates
        from fusion.smart import Simulation
        case=next(c for c in observations() if c['source'].endswith('8dbde2c0c71f') and c['model_shot']==4)
        observation=deepcopy(case['observation']);observation['devices']=deepcopy(DEVICES)
        row=next(r for r in adaptive_recommendations(candidates(observation,case['legal'])) if r['angle']==266 and r['route']=='contact' and r['target']==5)
        self.assertEqual(row['power'],32)
        sim=Simulation(observation,dict(angle=266,power=32));sim.advance(9600)
        self.assertTrue(sim.result()['settled']);self.assertEqual(sim.result()['ticks'],2217)


if __name__=='__main__':unittest.main()
