artech_engine.ui.form.on("Lead Sync Source", {
  refresh(frm) {
    frm.add_custom_button(__("Sync Now"), () => {
      frm.call("sync_leads").then(() => {
        artech_engine.msgprint(__("Lead sync initiated."));
      });
    });
  },
});
