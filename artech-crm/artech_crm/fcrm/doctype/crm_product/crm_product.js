artech_engine.ui.form.on("CRM Product", {
  product_code: function (frm) {
    if (!frm.doc.product_name)
      frm.set_value("product_name", frm.doc.product_code);
  },
});
