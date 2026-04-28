import artech_engine
from artech_engine.utils.verified_command import verify_request


def get_context(context):
	if not verify_request():
		context.success = False
		return context

	email = artech_engine.form_dict["email"]
	appointment_name = artech_engine.form_dict["appointment"]

	if email and appointment_name:
		appointment = artech_engine.get_doc("Appointment", appointment_name)
		appointment.set_verified(email)
		context.success = True
		return context
	else:
		context.success = False
		return context
