frappe.listview_settings['CardDav Contact'] = {
	onload: function(listview) {
		listview.refresh();
		listview.page.add_menu_item(__("Download Contact Book"), function() {
		   frappe.call({
		      method:'frappe_carddav.frappe_carddav.doctype.carddav_contact.carddav_contact.download_book',
		      callback: function(r) {
				if(!r.exc) {
                                                window.location.href = r.message;
                                }
		      }
		   });
		});
	}
}
