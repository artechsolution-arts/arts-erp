import artech_engine


def execute():
	if artech_engine.db.has_table("Serial and Batch Entry"):
		artech_engine.db.sql(
			"""
				UPDATE `tabSerial and Batch Entry` SABE, `tabSerial and Batch Bundle` SABB
				SET
					SABE.posting_datetime = SABB.posting_datetime,
					SABE.voucher_type = SABB.voucher_type,
					SABE.voucher_no = SABB.voucher_no,
					SABE.voucher_detail_no = SABB.voucher_detail_no,
					SABE.type_of_transaction = SABB.type_of_transaction,
					SABE.is_cancelled = SABB.is_cancelled,
					SABE.item_code = SABB.item_code
				WHERE SABE.parent = SABB.name
			"""
		)
