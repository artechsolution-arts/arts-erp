import artech_engine


def execute():
	FnF = artech_engine.qb.DocType("Full and Final Asset")
	artech_engine.qb.update(FnF).set(FnF.action, "Return").where((FnF.action.isnull()) | (FnF.action == "")).run()
