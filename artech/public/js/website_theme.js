// Copyright (c) 2019, Artech and Contributors
// MIT License. See license.txt

artech_engine.ui.form.on("Website Theme", {
	validate(frm) {
		let theme_scss = frm.doc.theme_scss;
		if (
			theme_scss &&
			theme_scss.includes("artech_engine/public/scss/website") &&
			!theme_scss.includes("artech/public/scss/website")
		) {
			frm.set_value("theme_scss", `${frm.doc.theme_scss}\n@import "artech/public/scss/website";`);
		}
	},
});
