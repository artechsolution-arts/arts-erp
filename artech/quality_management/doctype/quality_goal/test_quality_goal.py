# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestQualityGoal(ArtechTestSuite):
	def test_quality_goal(self):
		# no code, just a basic sanity check
		goal = get_quality_goal()
		self.assertTrue(goal)
		goal.delete()


def get_quality_goal():
	return artech_engine.get_doc(
		doctype="Quality Goal",
		goal="Test Quality Module",
		frequency="Daily",
		objectives=[dict(objective="Check test cases", target="100", uom="Percent")],
	).insert()
