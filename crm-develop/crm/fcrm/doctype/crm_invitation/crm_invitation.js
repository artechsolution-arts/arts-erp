artech_engine.ui.form.on("CRM Invitation", {
  refresh(frm) {
    if (frm.doc.status != "Accepted") {
      frm.add_custom_button(__("Accept Invitation"), () => {
        return frm.call("accept_invitation");
      });
    }
  },
});
