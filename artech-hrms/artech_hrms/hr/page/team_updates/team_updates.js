artech_engine.pages["team-updates"].on_page_load = function (wrapper) {
	var page = artech_engine.ui.make_app_page({
		parent: wrapper,
		title: __("Team Updates"),
		single_column: true,
	});

	artech_engine.team_updates.make(page);
	artech_engine.team_updates.run();

	if (artech_engine.model.can_read("Daily Work Summary Group")) {
		page.add_menu_item(__("Daily Work Summary Group"), function () {
			artech_engine.set_route("Form", "Daily Work Summary Group");
		});
	}
};

artech_engine.team_updates = {
	start: 0,
	make: function (page) {
		var me = artech_engine.team_updates;
		me.page = page;
		me.body = $("<div></div>").appendTo(me.page.main);
		me.more = $(
			'<div class="for-more"><button class="btn btn-sm btn-default btn-more">' +
				__("More") +
				"</button></div>",
		)
			.appendTo(me.page.main)
			.find(".btn-more")
			.on("click", function () {
				me.start += 40;
				me.run();
			});
	},
	run: function () {
		var me = artech_engine.team_updates;
		artech_engine.call({
			method: "hrms.hr.page.team_updates.team_updates.get_data",
			args: {
				start: me.start,
			},
			callback: function (r) {
				if (r.message && r.message.length > 0) {
					r.message.forEach(function (d) {
						me.add_row(d);
					});
				} else {
					artech_engine.show_alert({ message: __("No more updates"), indicator: "gray" });
					me.more.parent().addClass("hidden");
				}
			},
		});
	},
	add_row: function (data) {
		var me = artech_engine.team_updates;

		data.by = artech_engine.user.full_name(data.sender);
		data.avatar = artech_engine.avatar(data.sender);
		data.when = comment_when(data.creation);

		var date = artech_engine.datetime.str_to_obj(data.creation);
		var last = me.last_feed_date;

		if (
			(last && artech_engine.datetime.obj_to_str(last) != artech_engine.datetime.obj_to_str(date)) ||
			!last
		) {
			var diff = artech_engine.datetime.get_day_diff(
				artech_engine.datetime.get_today(),
				artech_engine.datetime.obj_to_str(date),
			);
			var pdate;
			if (diff < 1) {
				pdate = "Today";
			} else if (diff < 2) {
				pdate = "Yesterday";
			} else {
				pdate = artech_engine.datetime.global_date_format(date);
			}
			data.date_sep = pdate;
			data.date_class = pdate == "Today" ? "date-indicator blue" : "date-indicator";
		} else {
			data.date_sep = null;
			data.date_class = "";
		}
		me.last_feed_date = date;

		$(artech_engine.render_template("team_update_row", data)).appendTo(me.body);
	},
};
