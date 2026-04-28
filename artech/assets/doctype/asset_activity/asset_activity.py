# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import artech_engine
from artech_engine.model.document import Document
from artech_engine.utils import now_datetime


class AssetActivity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from artech_engine.types import DF

		asset: DF.Link
		date: DF.Datetime
		subject: DF.SmallText
		user: DF.Link
	# end: auto-generated types

	pass


def add_asset_activity(asset, subject):
	artech_engine.get_doc(
		{
			"doctype": "Asset Activity",
			"asset": asset,
			"subject": subject,
			"user": artech_engine.session.user,
			"date": now_datetime(),
		}
	).insert(ignore_permissions=True, ignore_links=True)
