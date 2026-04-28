import artech_engine


def execute():
	"""Set the payment gateway account as Email for all the existing payment channel."""
	doc_meta = artech_engine.get_meta("Payment Gateway Account")
	if doc_meta.get_field("payment_channel"):
		return

	artech_engine.reload_doc("Accounts", "doctype", "Payment Gateway Account")
	set_payment_channel_as_email()


def set_payment_channel_as_email():
	artech_engine.db.sql(
		"""
		UPDATE `tabPayment Gateway Account`
		SET `payment_channel` = "Email"
	"""
	)
