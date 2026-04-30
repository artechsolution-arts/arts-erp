artech_engine.ui.form.on("Interview Type", {
	refresh: function (frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Create Interview"), function () {
				frm.events.create_interview(frm);
			});
		}
	},
	designation: function (frm) {
		if (frm.doc.designation) {
			artech_engine.db.get_doc("Designation", frm.doc.designation).then((designation) => {
				artech_engine.model.clear_table(frm.doc, "expected_skill_set");

				designation.skills.forEach((designation_skill) => {
					const row = frm.add_child("expected_skill_set");
					row.skill = designation_skill.skill;
				});

				refresh_field("expected_skill_set");
			});
		}
	},
	create_interview: function (frm) {
		artech_engine.call({
			method: "artech_hrms.hr.doctype.interview_type.interview_type.create_interview",
			args: {
				docname: frm.doc.name,
			},
			callback: function (r) {
				var doclist = artech_engine.model.sync(r.message);
				artech_engine.set_route("Form", doclist[0].doctype, doclist[0].name);
			},
		});
	},
});
