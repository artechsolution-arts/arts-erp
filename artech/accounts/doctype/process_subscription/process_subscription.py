# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document
from artech_engine.utils import create_batch, getdate

from artech.accounts.doctype.subscription.subscription import DateTimeLikeObject


class ProcessSubscription(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		amended_from: DF.Link | None
		posting_date: DF.Date
		subscription: DF.Link | None
	# end: auto-generated types

	def on_submit(self):
		self.process_all_subscription()

	def process_all_subscription(self):
		filters = {"status": ("!=", "Cancelled")}

		if self.subscription:
			filters["name"] = self.subscription

		subscriptions = artech_engine.get_all("Subscription", filters, pluck="name")

		for subscription in create_batch(subscriptions, 500):
			artech_engine.enqueue(
				method="artech.accounts.doctype.subscription.subscription.process_all",
				queue="long",
				subscription=subscription,
				posting_date=self.posting_date,
			)


def create_subscription_process(
	subscription: str | None = None, posting_date: DateTimeLikeObject | None = None
):
	"""Create a new Process Subscription document"""
	doc = artech_engine.new_doc("Process Subscription")
	doc.subscription = subscription
	doc.posting_date = getdate(posting_date)
	doc.submit()
