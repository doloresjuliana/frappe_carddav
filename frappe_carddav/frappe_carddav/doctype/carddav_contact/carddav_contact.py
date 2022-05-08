# Copyright (c) 2022, Dolores Juliana and contributors
# For license information, please see license.txt

import frappe
import os
from frappe import _
from frappe.utils import get_files_path, get_url
from frappe.model.document import Document


class CardDavContact(Document):
	def after_insert(self):
		if self.prodid.startswith("Frappe CardDav"):
			vcard = build_vcard(self.name)
			self.vcard = vcard_txt(vcard)
			frappe.db.set_value('CardDav Contact', self.name, {
				'uid': self.name,
				'vcard': self.vcard
				}, update_modified=False)

	@frappe.whitelist()
	def download(self):
		# Upgrade vCard
		build_vcard(self.name)
		# Prepare or Clean old file
		vcffile = prepare_file(self.name)
		# Write vcf file
		vcf = open(vcffile, "w")
		vcf.write(self.vcard)
		vcf.close()
		# Return the download url to the client
		url = get_url("/files/" + self.name + ".vcf")
		return url

@frappe.whitelist()
def download_book():
	# Prepare and open the file
	vcffile = prepare_file('contact_book')
	vcf = open(vcffile, "w")
	# Go through all the contacts generating or regenerating your vCard
	for contact in frappe.db.get_list('Contact', pluck='name'):
		list = frappe.db.get_list('CardDav Contact', filters={'contact': contact}, pluck='name')
		if list and list[0] != "":
			doc = frappe.get_doc('CardDav Contact', list[0])
			vcard = build_vcard(doc.name)
			doc.vcard = vcard_txt(vcard)
			doc.save()
		else:
			doc = frappe.get_doc(doctype='CardDav Contact', contact=contact)
			doc.insert()
		doc.reload()

		vcf.write(doc.vcard)

	# Close file vcf and return the download url to the client
	vcf.close()
	url = get_url("/files/contact_book.vcf")
	return url

def build_vcard(name):
	# With the data of a Frappe contact, build a vCard in version 4.0
	doc = frappe.get_doc('CardDav Contact', name, ['contact','prodid']) 
	c = frappe.get_doc('Contact', doc.contact)
	if not c: return "Build vcard error"

	vcard = ['BEGIN:VCARD', 'VERSION:4.0', 'KIND:individual']
	txt = "PRODID:-//{}".format(nn(doc.prodid))
	vcard.append(txt)
	txt = "UID:{}".format(name)
	vcard.append(txt)

	txt = "FN:{}".format(c.name)
	vcard.append(txt)

	txt = "N:{};{};{};{};".format(nn(c.last_name), nn(c.first_name), nn(c.middle_name), nn(c.salutation))
	vcard.append(txt)

	if c.image and c.image.startswith('/files/'):
		urlphoto = frappe.utils.get_url() + c.image
		txt = "PHOTO:{}".format(urlphoto)
		vcard.append(txt)

	gender = ""
	if c.gender == "Male": gender = "M"
	elif c.gender == "Female": gender = "F"
	if gender != "":
		txt = "GENDER:{}".format(gender)
		vcard.append(txt)

	if c.address:
		add = frappe.get_doc('Address', c.address)
		txt = 'ADR;Label="{}":;{};{};{};{};{};{}'.format(nn(add.address_title), nn(add.address_line2),
		nn(add.address_line1), nn(add.city), nn(add.state), nn(add.pincode), nn(add.country))
		vcard.append(txt)

	if c.email_id:
		txt = 'EMAIL;PREF=1:{}'.format(c.email_id)
		vcard.append(txt)
	i = 1
	if c.phone:
		txt = 'TEL;PREF={};TYPE="voice":{}'.format( i, c.phone)
		vcard.append(txt)
		i +=1
	if c.mobile_no:
		txt = 'TEL;PREF={};TYPE="cell":{}'.format( i, c.mobile_no)
		vcard.append(txt)
	if c.designation:
		txt = 'TITLE:{}'.format(c.designation)
		vcard.append(txt)
	if c.company_name:
		txt = 'ORG:{}'.format(c.company_name) + ';{}'.format(c.department) if c.department else ''
		vcard.append(txt)

	datetime = c.modified.strftime("%Y%m%dT%f")
	txt = 'REV;VALUE=DATE-AND-OR-TIME:{}'.format(datetime)
	vcard.append(txt)

	vcard.append('END:VCARD')
	return vcard

def nn(value):
	return value if value else ""

def vcard_txt(vcard):
	txt = ""
	for lin in vcard:
		if lin != "":
			txt += lin.rstrip() + '\n'
	return txt

def prepare_file(filename):
	# Prepare a file that is not private and can be downloaded
	file_path = get_files_path(is_private=False)
	file_name = filename + ".vcf"
	vcffile = os.path.join(file_path, file_name)
	try:
		if os.path.exists(vcffile):
			os.remove(vcffile)
	except:
		pass
	return vcffile
