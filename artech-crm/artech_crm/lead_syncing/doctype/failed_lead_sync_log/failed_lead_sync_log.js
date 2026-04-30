artech_engine.ui.form.on("Failed Lead Sync Log", {
  refresh(frm) {
    const btn = frm.add_custom_button(__("Retry Sync"), () => {
      frm
        .call({
          doc: frm.doc,
          method: "retry_sync",
          btn,
        })
        .then(({ message }) => {
          artech_engine.show_alert(
            __("Sync Successful, CRM Lead: {0}!", [
              artech_engine.utils.get_form_link("CRM Lead", message.name, true),
            ]),
          );
        });
    });
  },
});
