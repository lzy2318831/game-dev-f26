"""Offline experiment safeguards; no changes to runtime candidate powers."""
from copy import deepcopy
import unittest
from fusion.geometry_power_experiment import doubled_power,aggregate,simulate
from fusion.engine import Episode


def result(**values):
    row=dict(settled=True,foul=False,simulation_limit=False,potted=[],points=0,
        cue_object_contact_radius_sample=True,intended_contact_radius_sample=True,
        intended_target_moved=True,target_potted=False)
    row.update(values)
    return row


class PowerExperiment(unittest.TestCase):
    def test_exact_doubling_and_cap(self):
        self.assertEqual([doubled_power(p) for p in (1,25,50,51,100)],[2,50,100,100,100])
        for p in (0,101,True,1.5):
            with self.assertRaises(ValueError):doubled_power(p)

    def test_new_limit_rejects_even_with_provisional_pots(self):
        rows=[dict(original=result(),doubled=result(settled=False,simulation_limit=True,potted=[1,2],points=200))]
        summary=aggregate(rows)
        self.assertEqual(summary['decision'],'KEEP_STABILIZED_RUNTIME_UNCHANGED')
        self.assertEqual(summary['totals']['doubled']['settled_pots'],0)
        self.assertEqual(summary['paired_changes']['new_simulation_limits'],1)

    def test_five_percentage_point_scratch_regression_rejects(self):
        rows=[dict(original=result(),doubled=result(foul=i==0)) for i in range(20)]
        self.assertEqual(aggregate(rows)['decision'],'KEEP_STABILIZED_RUNTIME_UNCHANGED')

    def test_equal_safe_results_do_not_automatically_enable(self):
        self.assertEqual(aggregate([dict(original=result(),doubled=result())])['decision'],
            'ELIGIBLE_FOR_FURTHER_REVIEW_NOT_AUTOMATIC_ENABLEMENT')

    def test_public_observation_is_not_modified_by_simulator(self):
        episode=Episode(layout=((230,250),(700,250)))
        observation=episode.observe('p1');before=deepcopy(observation)
        output=simulate(observation,dict(angle=0,power=1),1)
        self.assertEqual(observation,before)
        self.assertTrue(output['settled'])
        self.assertFalse(output['intended_target_moved'])


if __name__=='__main__':unittest.main()
