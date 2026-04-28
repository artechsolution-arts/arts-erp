// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

artech_engine.ui.form.on("Fiscal Year", {
	onload: function (frm) {
		if (frm.doc.__islocal) {
			frm.set_value("year_start_date", artech_engine.datetime.year_start());
		}
	},
	year_start_date: function (frm) {
		if (!frm.doc.is_short_year) {
			let year_end_date = artech_engine.datetime.add_days(
				artech_engine.datetime.add_months(frm.doc.year_start_date, 12),
				-1
			);
			frm.set_value("year_end_date", year_end_date);
		}
	},
});
