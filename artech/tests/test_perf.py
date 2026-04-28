import artech_engine

from artech.tests.utils import ArtechTestSuite

INDEXED_FIELDS = {
	"Bin": ["item_code"],
	"GL Entry": ["voucher_no", "posting_date", "company", "party"],
	"Purchase Order Item": ["item_code"],
}


class TestPerformance(ArtechTestSuite):
	def test_ensure_indexes(self):
		# These fields are not explicitly indexed BUT they are prefix in some
		# other composite index. If those are removed this test should be
		# updated accordingly.
		for doctype, fields in INDEXED_FIELDS.items():
			for field in fields:
				self.assertTrue(
					artech_engine.db.sql(
						f"""SHOW INDEX FROM `tab{doctype}`
						WHERE Column_name = "{field}" AND Seq_in_index = 1"""
					)
				)
