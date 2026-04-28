# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from typing import Any

import artech_engine
from artech_engine import _
from artech_engine.query_builder.functions import Sum
from artech_engine.utils.dashboard import cache_source


@artech_engine.whitelist()
@cache_source
def get(
	chart_name: str | None = None,
	chart: Any = None,
	no_cache: Any = None,
	filters: dict | str | None = None,
	from_date: Any = None,
	to_date: Any = None,
	timespan: Any = None,
	time_interval: Any = None,
	heatmap_year: Any = None,
):
	if filters and isinstance(filters, str):
		filters = artech_engine.parse_json(filters)

	company = filters.get("company") if filters else None
	if not company:
		company = artech_engine.defaults.get_defaults().company

	labels, datasets = get_stock_value_by_item_group(company)

	return {
		"labels": labels,
		"datasets": [{"name": _("Stock Value"), "values": datasets}],
	}


def get_stock_value_by_item_group(company):
	doctype = artech_engine.qb.DocType("Bin")
	item_doctype = artech_engine.qb.DocType("Item")

	warehouse_filters = [["is_group", "=", 0]]
	if company:
		warehouse_filters.append(["company", "=", company])

	warehouses = artech_engine.get_list("Warehouse", pluck="name", filters=warehouse_filters)

	stock_value = Sum(doctype.stock_value)

	query = (
		artech_engine.qb.from_(doctype)
		.inner_join(item_doctype)
		.on(doctype.item_code == item_doctype.name)
		.select(item_doctype.item_group, stock_value.as_("stock_value"))
		.groupby(item_doctype.item_group)
		.orderby(stock_value, order=artech_engine.qb.desc)
		.limit(10)
	)

	if warehouses:
		query = query.where(doctype.warehouse.isin(warehouses))

	results = query.run(as_dict=True)

	labels = []
	datapoints = []

	for row in results:
		if not row.stock_value:
			continue

		labels.append(_(row.item_group))
		datapoints.append(row.stock_value)

	return labels, datapoints
