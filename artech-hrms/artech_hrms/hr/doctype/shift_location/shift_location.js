artech_engine.ui.form.on("Shift Location", {
	refresh: async (frm) => {
		const allow_geolocation_tracking = await artech_engine.db.get_single_value(
			"HR Settings",
			"allow_geolocation_tracking",
		);

		if (!allow_geolocation_tracking)
			hide_field([
				"checkin_radius",
				"fetch_geolocation",
				"latitude",
				"longitude",
				"geolocation",
			]);

		if (!frm.doc.__islocal)
			artech_hrms.add_shift_tools_button_to_form(frm, {
				action: "Assign Shift",
				shift_location: frm.doc.name,
			});
	},

	fetch_geolocation: (frm) => {
		artech_hrms.fetch_geolocation(frm);
	},
});
