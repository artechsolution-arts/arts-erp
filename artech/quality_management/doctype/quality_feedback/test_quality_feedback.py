# Copyright (c) 2019, Artech and Contributors
# See license.txt

import artech_engine

from artech.tests.utils import ArtechTestSuite


class TestQualityFeedback(ArtechTestSuite):
	def test_quality_feedback(self):
		template = artech_engine.get_doc(
			doctype="Quality Feedback Template",
			template="Test Template",
			parameters=[dict(parameter="Test Parameter 1"), dict(parameter="Test Parameter 2")],
		).insert()

		feedback = artech_engine.get_doc(
			doctype="Quality Feedback",
			template=template.name,
			document_type="User",
			document_name=artech_engine.session.user,
		).insert()

		self.assertEqual(template.parameters[0].parameter, feedback.parameters[0].parameter)

		feedback.delete()
		template.delete()
