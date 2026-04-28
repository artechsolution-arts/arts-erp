// Copyright (c) 2015, Artech and Contributors

artech_engine.provide("artech");

// preferred modules for breadcrumbs
$.extend(artech_engine.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	Territory: "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
	Brand: "Stock",
	"Maintenance Schedule": "Support",
	"Maintenance Visit": "Support",
});

$.extend(artech_engine.breadcrumbs.module_map, {
	"Artech Integrations": "Integrations",
	Geo: "Settings",
	Portal: "Website",
	Utilities: "Settings",
	"E-commerce": "Website",
	Contacts: "CRM",
});
