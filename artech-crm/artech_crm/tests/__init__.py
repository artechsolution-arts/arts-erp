import json
import os

import artech_engine


def before_tests():
	load_crm_user_test_records()


def load_crm_user_test_records():
	"""Load CRM user test records from artech_crm/tests/test_records.json"""
	test_records_path = os.path.join(os.path.dirname(__file__), "test_records.json")

	if os.path.exists(test_records_path):
		with open(test_records_path) as f:
			test_records = json.load(f)

		for record in test_records:
			if not artech_engine.db.exists("User", record.get("email")):
				doc = artech_engine.get_doc(record)
				doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
