artech_engine.ui.form.on("CRM Form Script", {
  refresh(frm) {
    frm.set_query("dt", {
      filters: {
        istable: 0,
      },
    });

    if (frm.doc.is_standard && !artech_engine.boot.developer_mode) {
      frm.disable_form();
      artech_engine.show_alert(
        __(
          "Standard Form Scripts can not be modified, duplicate the Form Script instead.",
        ),
      );
    }

    if (!artech_engine.boot.developer_mode) {
      frm.toggle_enable("is_standard", 0);
    }

    frm.trigger("add_enable_button");
  },

  add_enable_button(frm) {
    frm.add_custom_button(
      frm.doc.enabled ? __("Disable") : __("Enable"),
      () => {
        frm.set_value("enabled", !frm.doc.enabled);
        frm.save();
      },
    );
  },

  view(frm) {
    let has_form_boilerplate = frm.doc.script.includes("function setupForm(");
    let has_list_boilerplate = frm.doc.script.includes("function setupList(");

    if (frm.doc.view == "Form" && !has_form_boilerplate) {
      frm.doc.script = `
function setupForm({ doc }) {
	return {
		actions: [],
		statuses: [],
	}
}`.trim();
    }
    if (frm.doc.view == "List" && !has_list_boilerplate) {
      frm.doc.script = `
function setupList({ list }) {
	return {
		actions: [],
		bulk_actions: [],
	}
}`.trim();
    }
  },
});
