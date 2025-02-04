from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader


class Budget(canvas.Canvas):

    def __init__(self, filename, context):
        super().__init__(filename, pagesize=A4)
        self.largura, self.altura = A4
        self.num_page = 1
        self.context = context
        self.current_height = 0
        # extra
        self.h1 = "Orçamento"
        self.main_stroke_color = '#c9c9c9'
        self.main_font = 'Helvetica'
        self.main_font_size = 12
        self.h1_font_size = 25
        self.h2_font_size = 18
        self.h2_font_primary = '#000000'
        self.h2_font_secondary = '#444544'

    def draw(self):
        self.setStrokeColor(colors.HexColor(self.main_stroke_color))
        self.header()
        self.title()
        self.seller()
        self.valid()
        self.production_time()
        self.product()
        self.condition_title()
        self.condition_list()
        self.footer()

    def draw_logo(canvas, logo_bytes, x, y, largura, altura):
        logo_image = ImageReader(BytesIO(logo_bytes))
        canvas.drawImage(logo_image, x, y, width=largura, height=altura)

    def header(self):
        logo = self.context['logo']
        img = Image.open(BytesIO(logo))
        img_largura, img_altura = img.size
        largura_desejada = 150
        proporcao = largura_desejada / img_largura
        nova_altura = img_altura * proporcao
        x_logo = 50
        y_logo = self.altura - nova_altura - 20
        self.drawImage(ImageReader(BytesIO(logo)), x_logo, y_logo, width=largura_desejada, height=nova_altura)
        y_linha = y_logo - 10
        self.line(50, y_linha, self.largura - 50, y_linha)
        self.current_height = nova_altura + 30

    def title(self):
        self.current_height = self.altura - self.current_height - 30
        self.setFont(self.main_font, self.h1_font_size)
        self.drawString(50, self.current_height, self.h1)
        self.setFont(self.main_font, 12)
        self.setFillColor(colors.HexColor(self.h2_font_secondary))
        self.current_height = self.current_height - 30
        self.drawString(50, self.current_height, f"Nº {self.context['id']}, emitido em {self.context['generated_in']['value']}")
        self.current_height = self.current_height - 10
        self.line(50, self.current_height, self.largura - 50, self.current_height)

    def seller(self):
        self.current_height = self.current_height - 20
        self.setFillColor(colors.HexColor(self.h2_font_secondary))
        self.setFont(self.main_font, 12)
        title = self.context['seller']['text']
        value = self.context['seller']['value']
        self.drawString(50, self.current_height, title)
        self.drawRightString(self.largura - 50, self.current_height, value)
        self.current_height = self.current_height - 10
        self.line(50, self.current_height, self.largura - 50, self.current_height)

    def valid(self):
        self.current_height = self.current_height - 20
        self.setFillColor(colors.HexColor(self.h2_font_secondary))
        self.setFont(self.main_font, 12)
        title = self.context['valid']['text']
        value = self.context['valid']['value']
        self.drawString(50, self.current_height, title)
        self.drawRightString(self.largura - 50, self.current_height, value)
        self.current_height = self.current_height - 10
        self.line(50, self.current_height, self.largura - 50, self.current_height)

    def production_time(self):
        self.current_height = self.current_height - 20
        self.setFillColor(colors.HexColor(self.h2_font_secondary))
        self.setFont(self.main_font, 12)
        title = self.context['production_time']['text']
        value = self.context['production_time']['value']
        self.drawString(50, self.current_height, title)
        self.drawRightString(self.largura - 50, self.current_height, value)
        self.current_height = self.current_height - 10
        self.line(50, self.current_height, self.largura - 50, self.current_height)

    def product(self):
        self.product_title()
        self.product_table()
        self.product_total()

    def product_title(self):
        self.current_height -= 35
        self.setFont(self.main_font, self.h2_font_size)
        self.drawString(50, self.current_height, "Produtos")

    def product_table(self):
        self.current_height -= 10
        products = self.context['products']
        self.setFont(self.main_font, 12)
        table_width = self.largura - 100
        colWidths = [table_width * 0.45, table_width * 0.15, table_width * 0.20, table_width * 0.20]
        styles = getSampleStyleSheet()
        header_style = styles["Normal"]
        header_style.alignment = 1
        body_style = styles["BodyText"]
        body_style.wordWrap = 'CJK'
        data = [[
            Paragraph("Produto", header_style), 
            Paragraph("Quantidade", header_style), 
            Paragraph("Valor Unitário (R$)", header_style), 
            Paragraph("Subtotal (R$)", header_style)
        ]]
        row_heights = [30]
        for product in products:
            product_style = getSampleStyleSheet()["BodyText"]
            product_style.wordWrap = 'CJK'
            product_style.alignment = 0
            product_paragraph = Paragraph(product["name"], product_style)
            td_style = getSampleStyleSheet()["BodyText"]
            td_style.alignment = 1
            quantity_paragraph = Paragraph(product["quantity"], td_style)
            unit_price_paragraph = Paragraph(product["unit_price"], td_style)
            subtotal_paragraph = Paragraph(product["subtotal"], td_style)
            _, product_height = product_paragraph.wrap(colWidths[0], 0)
            _, quantity_height = quantity_paragraph.wrap(colWidths[1], 0)
            _, unit_price_height = unit_price_paragraph.wrap(colWidths[2], 0)
            _, subtotal_height = subtotal_paragraph.wrap(colWidths[3], 0)
            row_height = max(product_height, quantity_height, unit_price_height, subtotal_height)
            row_heights.append(row_height + 5)
            data.append([product_paragraph, quantity_paragraph, unit_price_paragraph, subtotal_paragraph])
        table = Table(data, colWidths=colWidths, rowHeights=row_heights)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)
        total_table_height = sum(row_heights)
        self.current_height -= total_table_height
        table.wrapOn(self, 50, self.current_height)
        table.drawOn(self, 50, self.current_height)

    def product_total(self):
        self.current_height -= 25
        self.setFont("Helvetica", 13)
        self.setFillColor(colors.HexColor(self.h2_font_primary))
        self.drawString(50, self.current_height, "Total")
        self.drawRightString(self.largura - 50, self.current_height, 'R$ 500,00')
        self.current_height = self.current_height - 10
        self.line(50, self.current_height, self.largura - 50, self.current_height)

    def condition_title(self):
        self.current_height -= 35
        self.setFont("Helvetica", 18)
        title = self.context.get("condition", {}).get("title", None)
        if not title:
            return
        self.drawString(50, self.current_height, title)

    def condition_list(self):
        self.current_height -= 10
        conditions = self.context.get("condition", {}).get("conditions", None)
        if not conditions:
            return
        bullet_style = getSampleStyleSheet()["BodyText"]
        bullet_style.alignment = TA_LEFT
        bullet_style.leading = 14
        # max_width = self.largura - 100
        max_width = self.largura - 110
        for condition in conditions:
            self.condition_list_item(condition, max_width, bullet_style)

    def condition_list_item(self, condition, max_width, bullet_style):
        bullet_text = "• " + condition
        paragraph = Paragraph(bullet_text, bullet_style)
        _, h = paragraph.wrap(max_width, self.current_height)
        self.current_height -= h 
        paragraph.drawOn(self, 60, self.current_height)
        self.current_height -= 4 

    def footer(self):
        self.setFillColor(colors.HexColor(self.h2_font_secondary))
        linha_y = 50
        self.line(50, linha_y, self.largura - 50, linha_y)
        self.setFont(self.main_font, 9)
        self.drawString(50, linha_y - 15, self.context['footer']['r1'])
        self.drawString(50, linha_y - 30, self.context['footer']['r2'])
        self.drawString(self.largura - 80, linha_y - 15, f"Página {self.num_page}")
        self.num_page += 1

    def new_page(self):
        self.showPage()
        self.draw()
