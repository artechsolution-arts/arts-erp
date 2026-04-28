import artech_engine


def execute():
	if (
		artech_engine.db.sql(
			"""select data_type FROM information_schema.columns
            where column_name = 'name' and table_name = 'tabTax Withheld Vouchers'"""
		)[0][0]
		== "bigint"
	):
		artech_engine.db.change_column_type("Tax Withheld Vouchers", "name", "varchar(140)")
