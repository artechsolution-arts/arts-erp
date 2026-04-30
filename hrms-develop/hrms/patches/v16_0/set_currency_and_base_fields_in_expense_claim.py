import artech_engine


def execute():
	ExpenseClaim = artech_engine.qb.DocType("Expense Claim")
	Company = artech_engine.qb.DocType("Company")

	# set currency and exchange rate
	(
		artech_engine.qb.update(ExpenseClaim)
		.join(Company)
		.on(ExpenseClaim.company == Company.name)
		.set(ExpenseClaim.currency, Company.default_currency)
		.set(ExpenseClaim.exchange_rate, 1)
		.where(ExpenseClaim.currency.isnull() | (ExpenseClaim.currency == ""))
	).run()

	# set base fields in expense claim
	(
		artech_engine.qb.update(ExpenseClaim)
		.join(Company)
		.on(ExpenseClaim.company == Company.name)
		.set(ExpenseClaim.base_total_sanctioned_amount, ExpenseClaim.total_sanctioned_amount)
		.set(ExpenseClaim.base_total_advance_amount, ExpenseClaim.total_advance_amount)
		.set(ExpenseClaim.base_grand_total, ExpenseClaim.grand_total)
		.set(
			ExpenseClaim.base_total_claimed_amount,
			ExpenseClaim.total_claimed_amount,
		)
		.set(
			ExpenseClaim.base_total_taxes_and_charges,
			ExpenseClaim.total_taxes_and_charges,
		)
		.where(ExpenseClaim.currency == Company.default_currency)
	).run()

	# set base fields in expense table
	ExpenseClaimDetail = artech_engine.qb.DocType("Expense Claim Detail")
	(
		artech_engine.qb.update(ExpenseClaimDetail)
		.join(ExpenseClaim)
		.on(ExpenseClaimDetail.parent == ExpenseClaim.name)
		.join(Company)
		.on(ExpenseClaim.company == Company.name)
		.set(ExpenseClaimDetail.base_amount, ExpenseClaimDetail.amount)
		.set(
			ExpenseClaimDetail.base_sanctioned_amount,
			ExpenseClaimDetail.sanctioned_amount,
		)
		.where(ExpenseClaim.currency == Company.default_currency)
	).run()

	# set base fields in advance table
	ExpenseClaimAdvance = artech_engine.qb.DocType("Expense Claim Advance").as_("eca")
	(
		artech_engine.qb.update(ExpenseClaimAdvance)
		.join(ExpenseClaim)
		.on(ExpenseClaimAdvance.parent == ExpenseClaim.name)
		.join(Company)
		.on(ExpenseClaim.company == Company.name)
		.set(ExpenseClaimAdvance.base_advance_paid, ExpenseClaimAdvance.advance_paid)
		.set(ExpenseClaimAdvance.base_unclaimed_amount, ExpenseClaimAdvance.unclaimed_amount)
		.set(ExpenseClaimAdvance.base_allocated_amount, ExpenseClaimAdvance.allocated_amount)
		.set(ExpenseClaimAdvance.exchange_rate, 1)
		.where(ExpenseClaim.currency == Company.default_currency)
	).run()

	# set base fields in taxes table
	ExpenseTaxesAndCharges = artech_engine.qb.DocType("Expense Taxes and Charges")
	(
		artech_engine.qb.update(ExpenseTaxesAndCharges)
		.join(ExpenseClaim)
		.on(ExpenseTaxesAndCharges.parent == ExpenseClaim.name)
		.join(Company)
		.on(ExpenseClaim.company == Company.name)
		.set(ExpenseTaxesAndCharges.base_tax_amount, ExpenseTaxesAndCharges.tax_amount)
		.set(ExpenseTaxesAndCharges.base_total, ExpenseTaxesAndCharges.total)
		.where(ExpenseClaim.currency == Company.default_currency)
	).run()
