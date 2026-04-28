import functools
import inspect
from typing import TypeVar

import artech_engine
from artech_engine.model.document import Document
from artech_engine.utils.user import is_website_user

__version__ = "17.0.0-dev"


def get_default_company(user=None):
	"""Get default company for user"""
	from artech_engine.defaults import get_user_default_as_list

	if not user:
		user = artech_engine.session.user

	companies = get_user_default_as_list("company", user)
	if companies:
		default_company = companies[0]
	else:
		default_company = artech_engine.db.get_single_value("Global Defaults", "default_company")

	return default_company


def get_default_currency():
	"""Returns the currency of the default company"""
	company = get_default_company()
	if company:
		return artech_engine.get_cached_value("Company", company, "default_currency")


def get_default_cost_center(company):
	"""Returns the default cost center of the company"""
	if not company:
		return None

	if not artech_engine.flags.company_cost_center:
		artech_engine.flags.company_cost_center = {}
	if company not in artech_engine.flags.company_cost_center:
		artech_engine.flags.company_cost_center[company] = artech_engine.get_cached_value("Company", company, "cost_center")
	return artech_engine.flags.company_cost_center[company]


def get_company_currency(company):
	"""Returns the default company currency"""
	if not artech_engine.flags.company_currency:
		artech_engine.flags.company_currency = {}
	if company not in artech_engine.flags.company_currency:
		artech_engine.flags.company_currency[company] = artech_engine.db.get_value(
			"Company", company, "default_currency", cache=True
		)
	return artech_engine.flags.company_currency[company]


def set_perpetual_inventory(enable=1, company=None):
	if not company:
		company = "_Test Company" if artech_engine.in_test else get_default_company()

	company = artech_engine.get_doc("Company", company)
	company.enable_perpetual_inventory = enable
	company.save()


def encode_company_abbr(name, company=None, abbr=None):
	"""Returns name encoded with company abbreviation"""
	company_abbr = abbr or artech_engine.get_cached_value("Company", company, "abbr")
	parts = name.rsplit(" - ", 1)

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)


def is_perpetual_inventory_enabled(company):
	if not company:
		company = "_Test Company" if artech_engine.in_test else get_default_company()

	if not hasattr(artech_engine.local, "enable_perpetual_inventory"):
		artech_engine.local.enable_perpetual_inventory = {}

	if company not in artech_engine.local.enable_perpetual_inventory:
		artech_engine.local.enable_perpetual_inventory[company] = (
			artech_engine.get_cached_value("Company", company, "enable_perpetual_inventory") or 0
		)

	return artech_engine.local.enable_perpetual_inventory[company]


def get_default_finance_book(company=None):
	if not company:
		company = get_default_company()

	if not hasattr(artech_engine.local, "default_finance_book"):
		artech_engine.local.default_finance_book = {}

	if company not in artech_engine.local.default_finance_book:
		artech_engine.local.default_finance_book[company] = artech_engine.get_cached_value(
			"Company", company, "default_finance_book"
		)

	return artech_engine.local.default_finance_book[company]


def get_party_account_type(party_type):
	if not hasattr(artech_engine.local, "party_account_types"):
		artech_engine.local.party_account_types = {}

	if party_type not in artech_engine.local.party_account_types:
		artech_engine.local.party_account_types[party_type] = (
			artech_engine.db.get_value("Party Type", party_type, "account_type") or ""
		)

	return artech_engine.local.party_account_types[party_type]


def get_region(company=None):
	"""Return the default country based on flag, company or global settings

	You can also set global company flag in `artech_engine.flags.company`
	"""

	if not company:
		company = artech_engine.local.flags.company

	if company:
		return artech_engine.get_cached_value("Company", company, "country")

	return artech_engine.flags.country or artech_engine.get_system_settings("country")


def allow_regional(fn):
	"""Decorator to make a function regionally overridable

	Example:
	@artech.allow_regional
	def myfunction():
	  pass"""

	@functools.wraps(fn)
	def caller(*args, **kwargs):
		overrides = artech_engine.get_hooks("regional_overrides", {}).get(get_region())
		function_path = f"{inspect.getmodule(fn).__name__}.{fn.__name__}"

		if not overrides or function_path not in overrides:
			return fn(*args, **kwargs)

		# Priority given to last installed app
		return artech_engine.get_attr(overrides[function_path][-1])(*args, **kwargs)

	return caller


def check_app_permission():
	if artech_engine.session.user == "Administrator":
		return True

	if is_website_user():
		return False

	return True


T = TypeVar("T")


def normalize_ctx_input(T: type) -> callable:
	"""
	Normalizes the first argument (ctx) of the decorated function by:
	- Converting Document objects to dictionaries
	- Parsing JSON strings
	- Casting the result to the specified type T
	"""

	def decorator(func: callable):
		# conserve annotations for artech_engine.utils.typing_validations
		@functools.wraps(func, assigned=(a for a in functools.WRAPPER_ASSIGNMENTS if a != "__annotations__"))
		def wrapper(ctx: T | Document | dict | str, *args, **kwargs):
			if isinstance(ctx, Document):
				ctx = T(**ctx.as_dict())
			elif isinstance(ctx, dict):
				ctx = T(**ctx)
			else:
				ctx = T(**artech_engine.parse_json(ctx))

			return func(ctx, *args, **kwargs)

		# set annotations from function
		wrapper.__annotations__.update({k: v for k, v in func.__annotations__.items() if k != "ctx"})
		return wrapper

	return decorator
