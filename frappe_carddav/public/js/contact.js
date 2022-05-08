frappe.ui.form.on("Contact", {
	refresh: function(frm) {
		frm.add_custom_button(__("vCard"), function() {
			// Before calling the doctype that I extend the contact with vCard version 4.0,
			// it checks that the record exists and if it does not exist, it creates it
			frappe.db.get_value("CardDav Contact",
                                {"contact": frm.doc.name},
                                ["contact", "name"])
                        .then(r => {
				var vcard = r.message;
				if (vcard.contact == frm.doc.name) {
					frappe.set_route("Form", "CardDav Contact", vcard.name);
				} else {
					frappe.db.insert({"doctype": "CardDav Contact", "contact": frm.doc.name
                                	}).then(function(vcard) {
                                        	 frappe.set_route("Form", "CardDav Contact", vcard.name);
                                	});
				}
                   	});

		});
	}
});

