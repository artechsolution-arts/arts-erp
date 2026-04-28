artech_engine.treeview_settings["BOM"] = {
	get_tree_nodes: "artech.manufacturing.doctype.bom.bom.get_children",
	filters: [
		{
			fieldname: "bom",
			fieldtype: "Link",
			options: "BOM",
			label: __("BOM"),
		},
	],
	title: "BOM",
	breadcrumb: "Manufacturing",
	disable_add_node: true,
	root_label: "BOM", //fieldname from filters
	get_tree_root: false,
	show_expand_all: false,
	get_label: function (node) {
		if (node.is_root && node.data.value != "BOM") {
			artech_engine.model.with_doc("BOM", node.data.value, function () {
				var bom = artech_engine.model.get_doc("BOM", node.data.value);
				node.data.item_name = bom.item_name || "";
				node.data.item_code = bom.item || "";
				node.data.qty = bom.quantity || "";
				node.data.stock_uom = bom.uom || "";
				return get_bom_node(node);
			});
		}

		return get_bom_node(node);
	},
	onload: function (me) {
		var label = artech_engine.get_route()[0] + "/" + artech_engine.get_route()[1];
		if (artech_engine.pages[label]) {
			delete artech_engine.pages[label];
		}

		var filter = me.opts.filters[0];
		if (artech_engine.route_options && artech_engine.route_options[filter.fieldname]) {
			var val = artech_engine.route_options[filter.fieldname];
			delete artech_engine.route_options[filter.fieldname];
			filter.default = "";
			me.args[filter.fieldname] = val;
			me.root_label = val;
			me.page.set_title(val);
		}
		me.make_tree();
	},
	toolbar: [
		{ toggle_btn: true },
		{
			label: __("Edit"),
			condition: function (node) {
				return node.expandable;
			},
			click: function (node) {
				artech_engine.set_route("Form", "BOM", node.data.value);
			},
		},
	],
	menu_items: [
		{
			label: __("New BOM"),
			action: function () {
				artech_engine.new_doc("BOM", true);
			},
			condition: 'artech_engine.boot.user.can_create.indexOf("BOM") !== -1',
		},
	],
	onrender: function (node) {
		if (node.is_root && node.data.value != "BOM") {
			artech_engine.model.with_doc("BOM", node.data.value, function () {
				var bom = artech_engine.model.get_doc("BOM", node.data.value);
				node.data.image = bom.image || "";
				node.data.description = bom.description || "";
				node.data.item_code = bom.item || "";
			});
		}
	},
	view_template: "bom_item_preview",
};

function get_bom_node(node) {
	if (node.data.qty) {
		const escape = artech_engine.utils.escape_html;
		let label = escape(node.data.item_code);
		if (node.is_root && node.data.value != "BOM") {
			label = escape(node.data.value);
		}

		if (node.data.item_name && node.data.item_code !== node.data.item_name) {
			label += `: ${escape(node.data.item_name)}`;
		}
		return `${label} <span class="badge badge-pill badge-light">${node.data.qty} ${escape(
			__(node.data.stock_uom)
		)}</span>`;
	} else {
		return node.data.item_code || node.data.value;
	}
}
