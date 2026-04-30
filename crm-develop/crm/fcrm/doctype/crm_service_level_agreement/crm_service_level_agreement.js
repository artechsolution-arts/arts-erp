artech_engine.ui.form.on("CRM Service Level Agreement", {
  refresh(frm) {
    if (frm.doc.rolling_responses) {
      frm.fields_dict.priorities.grid.update_docfield_property(
        "first_response_time",
        "label",
        "Rolling Response Time",
      );
    } else {
      frm.fields_dict.priorities.grid.update_docfield_property(
        "first_response_time",
        "label",
        "First Response Time",
      );
    }
  },
  validate(frm) {
    let default_priority_count = 0;
    frm.doc.priorities.forEach(function (row) {
      if (row.default_priority) {
        default_priority_count++;
      }
    });
    if (default_priority_count > 1) {
      artech_engine.throw(
        __("There can only be one default priority in Priorities table"),
      );
    }
  },
});
