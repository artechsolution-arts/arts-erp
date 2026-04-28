import artech_engine


# accounts
class PartyFrozen(artech_engine.ValidationError):
	pass


class InvalidAccountCurrency(artech_engine.ValidationError):
	pass


class InvalidCurrency(artech_engine.ValidationError):
	pass


class PartyDisabled(artech_engine.ValidationError):
	pass


class InvalidAccountDimensionError(artech_engine.ValidationError):
	pass


class MandatoryAccountDimensionError(artech_engine.ValidationError):
	pass


class ReportingCurrencyExchangeNotFoundError(artech_engine.ValidationError):
	pass
