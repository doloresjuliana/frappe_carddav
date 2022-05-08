// Copyright (c) 2022, Dolores Juliana and contributors
// For license information, please see license.txt

frappe.ui.form.on('CardDav Contact', {
	// refresh: function(frm) {

	// }
	download(frm) {
		if (frm && frm.doc) {
			frappe.call({
				method: "run_doc_method",
				args: {'docs': frm.doc, 'method': 'download' },
				callback: function(r) {
					if(!r.exc) {
						window.location.href = r.message;
					}
				}
			});
		}
	}
});
