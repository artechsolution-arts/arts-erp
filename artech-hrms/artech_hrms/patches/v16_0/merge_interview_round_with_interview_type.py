import artech_engine
from artech_engine.model.rename_doc import rename_doc


def execute():
	if artech_engine.db.has_table("Interview Round"):
		for interview_round, interview_type in artech_engine.get_all(
			"Interview Round", fields=["name", "interview_type"], as_list=True
		):
			if interview_type != interview_round and interview_type and interview_round:
				rename_doc("Interview Type", interview_type, interview_round)
