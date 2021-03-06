import xlwt
from datetime import datetime as dt
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.tools.translate import _
import time
import datetime
from openerp import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class sale_hsn_summary(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(sale_hsn_summary, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'datetime': dt,
            })
        self.context = context
    

class HsnReport(report_xls):

    def generate_xls_report(self, parser, xls_styles, data, objects, wb):
        cr, uid = self.cr, self.uid
        report_name = 'HSN Sale Summary Report '
        ws = wb.add_sheet(report_name)
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        cols = range(10)
        for col in cols:
            ws.col(col).width = 4000
        title2          = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz centre;')
        normal          = xlwt.easyxf('font: height 200, name Arial, colour_index black; align: horiz left;')
        number          = xlwt.easyxf(num_format_str='#,##0;(#,##0)')
        number2d        = xlwt.easyxf(num_format_str='#,##0.00;(#,##0.00)')
        number2d_bold   = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on;',num_format_str='#,##0.00;(#,##0.00)')

        headers = {0:"HSN", 1:"Description", 2:'UQC', 3:"Total Quantity", 4:'Total Value', 5:'Taxable Value', 6:'Integrated Tax Amount', 7:'Central Tax Amount', 8:'State/UT Tax Amount', 9:'Cess Amount'}

        for header in headers:
            ws.write(3, header, headers[header], title2)

        invoice_obj = self.pool.get("account.invoice")
        invoice_id = invoice_obj.search(cr, uid, [('state','not in',('draft', 'cancel')), ("date_invoice", ">=", data['form']["from_date"]), ("date_invoice", "<=", data['form']['to_date']), ("company_id", "=", data['form']['company'][0])])
        invoices = invoice_obj.browse(cr, uid, invoice_id)
        hsn_obj = self.pool.get("hs.code")
        hsn_search = hsn_obj.search(cr, uid, [])
        hsn_code_id = hsn_obj.browse(cr, uid, hsn_search)
        hsn_temp = []
        
        hsn_total_taxable = 0
        hsn_total_amount = 0
        hsn_total_igst = 0
        hsn_total_cgst = 0
        hsn_total_sgst = 0
        hsn_total_cess = 0
        hsn_count = 0

        count = 4

        if invoice_id:
            for hsn_code in hsn_code_id:
                if hsn_code.code[0:4] in hsn_temp:
                    continue
                hsn_temp.append(hsn_code.code[0:4])
                
                hsn_qty = 0
                hsn_untaxed = 0
                discount_rate = 0
                hsn_cgst_total = 0
                hsn_sgst_total = 0
                hsn_igst_total = 0
                hsn_cess_total = 0
                hsn_taxed = 0

                for invoice in invoices:

                    for line in invoice.invoice_line:
                        if hsn_code.code[0:4] != line.product_id.hs_code_id.code[0:4]:
                            continue
                        discount_rate = round(line.price_unit - ((line.price_unit * line.discount)/100), 2)
                        hsn_qty += line.quantity
                        hsn_untaxed += line.price_subtotal
                        for tax in line.invoice_line_tax_id:
                            if tax.gst_type == "cgst":
                                hsn_cgst_total += round((line.price_subtotal * tax.amount), 2)
                            elif tax.gst_type == "sgst":
                                hsn_sgst_total += round((line.price_subtotal * tax.amount), 2)
                            elif tax.gst_type == "igst":
                                hsn_igst_total += round((line.price_subtotal * tax.amount), 2)
                            elif tax.gst_type == "cess":
                                hsn_cess_total += round((line.price_subtotal * tax.amount), 2)
                        temp_prod_id = line.product_id       
            
                hsn_taxed = hsn_untaxed + hsn_cgst_total + hsn_sgst_total + hsn_igst_total + hsn_cess_total
                hsn_total_taxable += hsn_untaxed
                hsn_total_amount += hsn_taxed
                hsn_total_igst += hsn_igst_total
                hsn_total_cgst += hsn_cgst_total
                hsn_total_sgst += hsn_sgst_total
                hsn_total_cess += hsn_cess_total

                if hsn_qty:
                    hsn_count += 1
                    categ = temp_prod_id.categ_id.name
                    categ = categ.split('/')
                    ws.write(count, 0, hsn_code.code[0:4], number2d)
                    ws.write(count, 1, categ[len(categ) - 1], normal)
                    ws.write(count, 2, 'NOS-NUMBERS', normal)
                    ws.write(count, 3, hsn_qty, number2d)
                    ws.write(count, 4, hsn_taxed, number2d)
                    ws.write(count, 5, hsn_untaxed, number2d)
                    ws.write(count, 6, hsn_igst_total, number2d)
                    ws.write(count, 7, hsn_cgst_total, number2d)
                    ws.write(count, 8, hsn_sgst_total, number2d)
                    ws.write(count, 9, hsn_cess_total, number2d)
                    count += 1

        ws.write(0, 0, 'Summary For HSN(12)', title2)
        headers = {0:"No.of HSN", 4:'Total Value', 5:'Taxable Value', 6:'Total Integrated Tax', 7:'Total Central Tax', 8:'Total State/UT Tax', 9:'Total Cess'}
        for header in headers:
            ws.write(1, header, headers[header], title2)
        ws.write(2, 0, hsn_count, number2d)
        ws.write(2, 4, round(hsn_total_amount, 2), number2d)
        ws.write(2, 5, round(hsn_total_taxable, 2), number2d)
        ws.write(2, 6, round(hsn_total_igst, 2), number2d)
        ws.write(2, 7, round(hsn_total_cgst, 2), number2d)
        ws.write(2, 8, round(hsn_total_sgst, 2), number2d)
        ws.write(2, 9, round(hsn_total_cess, 2), number2d)
HsnReport('report.gstr.hsn_report', "gstr.hsn_report", parser=sale_hsn_summary)