frappe.listview_settings['Contact'] = {
        onload: function(listview) {
                listview.refresh();
                listview.page.add_menu_item(__("vCard exchange with other systems"), function() {
			frappe.set_route('List', 'CardDav Contact', 'List');
                });
        }
}
