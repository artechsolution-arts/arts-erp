artech_engine.ui.form.on("Sales Invoice", {
	refresh: (frm) => {
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Generate E-Invoice"), () => {
				frm.call({
					method: "artech.regional.italy.utils.generate_single_invoice",
					args: {
						docname: frm.doc.name,
					},
					callback: function (r) {
						frm.reload_doc();
						if (r.message) {
							open_url_post(artech_engine.request.url, {
								cmd: "artech_engine.core.doctype.file.file.download_file",
								file_url: r.message,
							});
						}
					},
				});
			});
		}
	},
});
