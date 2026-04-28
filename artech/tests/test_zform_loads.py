""" smoak tests to check basic functionality calls on known form loads."""

import artech_engine
from artech_engine.desk.form.load import getdoc
from artech_engine.www.printview import get_html_and_style

from artech.tests.utils import ArtechTestSuite


class TestFormLoads(ArtechTestSuite):
	@ArtechTestSuite.change_settings("Print Settings", {"allow_print_for_cancelled": 1})
	def test_load(self):
		artech_modules = artech_engine.get_all("Module Def", filters={"app_name": "artech"}, pluck="name")
		doctypes = artech_engine.get_all(
			"DocType",
			{"istable": 0, "issingle": 0, "is_virtual": 0, "module": ("in", artech_modules)},
			pluck="name",
		)

		for doctype in doctypes:
			last_doc = artech_engine.db.get_value(doctype, {}, "name", order_by="creation desc")
			if not last_doc:
				continue
			with self.subTest(msg=f"Loading {doctype} - {last_doc}", doctype=doctype, last_doc=last_doc):
				self.assertFormLoad(doctype, last_doc)
				self.assertDocPrint(doctype, last_doc)

	def assertFormLoad(self, doctype, docname):
		# reset previous response
		artech_engine.response = artech_engine._dict({"docs": []})
		artech_engine.response.docinfo = None

		try:
			getdoc(doctype, docname)
		except Exception as e:
			self.fail(f"Failed to load {doctype}-{docname}: {e}")

		self.assertTrue(
			artech_engine.response.docs, msg=f"expected document in reponse, found: {artech_engine.response.docs}"
		)
		self.assertTrue(
			artech_engine.response.docinfo, msg=f"expected docinfo in reponse, found: {artech_engine.response.docinfo}"
		)

	def assertDocPrint(self, doctype, docname):
		doc = artech_engine.get_doc(doctype, docname)
		doc.set("__onload", artech_engine._dict())
		doc.run_method("onload")

		messages_before = artech_engine.get_message_log()
		ret = get_html_and_style(doc=doc.as_json(), print_format="Standard", no_letterhead=1)
		messages_after = artech_engine.get_message_log()

		if len(messages_after) > len(messages_before):
			new_messages = messages_after[len(messages_before) :]
			self.fail("Print view showing error/warnings: \n" + "\n".join(str(msg) for msg in new_messages))

		# html should exist
		self.assertTrue(bool(ret["html"]))
