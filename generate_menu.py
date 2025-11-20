#!/usr/bin/env python3
"""
Generate a professional multi-page PDF menu for East @ West Restaurant
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Circle, Polygon, Path
from reportlab.graphics import renderPDF
from PIL import Image as PILImage
import os
from io import BytesIO

class MenuPDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.3*inch,
            leftMargin=0.3*inch,
            topMargin=0.3*inch,
            bottomMargin=0.3*inch
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        # Use the uploaded icons
        self.vegan_icon_path = r'C:\Users\mbike\Downloads\vegan-sigle.jpg'
        self.vegetarian_icon_path = r'C:\Users\mbike\Downloads\vegetarian-sigle.jpg'
        
    def _setup_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#1a5d3f'),
            spaceAfter=3,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#d4af37'),
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=12,
            textColor=colors.white,
            spaceAfter=2,
            spaceBefore=2,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            backColor=colors.HexColor('#1a5d3f'),
            borderPadding=3
        )
        
        # Item name style
        self.item_name_style = ParagraphStyle(
            'ItemName',
            parent=self.styles['Normal'],
            fontSize=8.5,
            textColor=colors.HexColor('#1a5d3f'),
            fontName='Helvetica-Bold',
            spaceAfter=0.5
        )
        
        # Item description style
        self.item_desc_style = ParagraphStyle(
            'ItemDesc',
            parent=self.styles['Normal'],
            fontSize=7,
            textColor=colors.HexColor('#4b5563'),
            fontName='Helvetica',
            leading=8
        )
        
        # Price style
        self.price_style = ParagraphStyle(
            'Price',
            parent=self.styles['Normal'],
            fontSize=9.5,
            textColor=colors.HexColor('#d4af37'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        )
        
        # Info box style
        self.info_style = ParagraphStyle(
            'InfoBox',
            parent=self.styles['Normal'],
            fontSize=7,
            textColor=colors.HexColor('#1a5d3f'),
            fontName='Helvetica-Oblique',
            alignment=TA_CENTER,
            spaceAfter=2,
            backColor=colors.HexColor('#f0f9f4'),
            borderColor=colors.HexColor('#1a5d3f'),
            borderWidth=0.8,
            borderPadding=3
        )
        
        # Footer style
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica',
            alignment=TA_CENTER
        )
    
    def add_cover_page(self, logo_path):
        """Create a very compact cover page with logo"""
        # Add decorative top border
        top_border = Table([['']], colWidths=[7.2*inch])
        top_border.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1a5d3f')),
        ]))
        self.story.append(Spacer(1, 0.08*inch))
        self.story.append(top_border)

        self.story.append(Spacer(1, 0.15*inch))

        # Add logo - smaller
        if logo_path and os.path.exists(logo_path):
            logo = Image(logo_path, width=1.8*inch, height=1.8*inch)
            logo.hAlign = 'CENTER'
            self.story.append(logo)
            self.story.append(Spacer(1, 0.12*inch))
        
        # Description with decorative box
        desc_style = ParagraphStyle(
            'Description',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1a5d3f'),
            alignment=TA_CENTER,
            leading=13,
            fontName='Helvetica-Bold'
        )
        desc = Paragraph("✦ Authentic Lebanese & Syrian Cuisine ✦", desc_style)
        
        desc_table = Table([[desc]], colWidths=[4.8*inch])
        desc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9f4')),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#d4af37')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        desc_table.hAlign = 'CENTER'
        self.story.append(desc_table)
        
        self.story.append(Spacer(1, 0.08*inch))
        
        # Location and year combined
        location_style = ParagraphStyle(
            'Location',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#4b5563'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        location = Paragraph("Brussels, Belgium • 2025", location_style)
        self.story.append(location)
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Add decorative bottom border
        bottom_border = Table([['']], colWidths=[7.2*inch])
        bottom_border.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1a5d3f')),
        ]))
        self.story.append(bottom_border)
        
        self.story.append(PageBreak())
    
    def add_menu_item(self, name, description, price, is_vegan=False, is_vegetarian=False):
        """Add a single menu item with very compact styling"""
        # Create dietary indicator with uploaded icons - very small
        if is_vegan and self.vegan_icon_path and os.path.exists(self.vegan_icon_path):
            dietary_img = Image(self.vegan_icon_path, width=10, height=10)
            dietary_content = Table(
                [[dietary_img, Paragraph(f"<b>{name}</b>", self.item_name_style)]],
                colWidths=[12, 5.9*inch]
            )
            dietary_content.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
        elif is_vegetarian and self.vegetarian_icon_path and os.path.exists(self.vegetarian_icon_path):
            dietary_img = Image(self.vegetarian_icon_path, width=10, height=10)
            dietary_content = Table(
                [[dietary_img, Paragraph(f"<b>{name}</b>", self.item_name_style)]],
                colWidths=[12, 5.9*inch]
            )
            dietary_content.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
        else:
            dietary_content = Paragraph(f"<b>{name}</b>", self.item_name_style)
        
        # Create the item content
        item_data = [
            [dietary_content, Paragraph(f"<b>{price}</b>", self.price_style)],
            [Paragraph(description, self.item_desc_style), ""]
        ]
        
        item_table = Table(item_data, colWidths=[5.9*inch, 1.3*inch])
        item_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 1.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafafa')),
            ('BOX', (0, 0), (-1, -1), 0.2, colors.HexColor('#d4af37')),
            ('LINEBELOW', (0, 0), (-1, 0), 0.3, colors.HexColor('#e5e7eb')),
        ]))
        
        self.story.append(item_table)
        self.story.append(Spacer(1, 0.01*inch))
    
    def add_section(self, title, items):
        """Add a menu section with very compact styling"""
        # Add decorative top border
        top_border = Table([['']], colWidths=[7.2*inch])
        top_border.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#d4af37')),
        ]))
        self.story.append(top_border)
        
        # Section header with background
        header_table = Table([[Paragraph(title.upper(), self.section_style)]], colWidths=[7.2*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a5d3f')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d4af37')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        self.story.append(header_table)
        
        # Add decorative bottom border
        bottom_border = Table([['']], colWidths=[7.2*inch])
        bottom_border.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#d4af37')),
        ]))
        self.story.append(bottom_border)
        self.story.append(Spacer(1, 0.02*inch))
        
        # Add items
        for item in items:
            self.add_menu_item(
                item['name'],
                item['description'],
                item['price'],
                item.get('is_vegan', False),
                item.get('is_vegetarian', False)
            )
        
        self.story.append(Spacer(1, 0.03*inch))
    
    def add_info_box(self, text):
        """Add a very compact information box"""
        info_content = Paragraph(f"<i>✦ {text} ✦</i>", self.info_style)
        
        # Create a table for the info box with border
        info_table = Table([[info_content]], colWidths=[7.2*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9f4')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#1a5d3f')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.story.append(info_table)
        self.story.append(Spacer(1, 0.03*inch))
    
    def add_contact_page(self, logo_path):
        """Add a compact contact information page with logo footer"""
        self.story.append(PageBreak())
        
        self.story.append(Spacer(1, 0.3*inch))
        
        # Contact title with decorative border
        contact_title_style = ParagraphStyle(
            'ContactTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.white,
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        contact_title = Paragraph("Visit Us", contact_title_style)
        title_table = Table([[contact_title]], colWidths=[7.2*inch])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a5d3f')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#d4af37')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        self.story.append(title_table)
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Contact details in a styled box
        contact_style = ParagraphStyle(
            'ContactDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_CENTER,
            leading=14,
            fontName='Helvetica'
        )
        
        contact_info = """
        <b><font size="13" color="#1a5d3f">East @ West Restaurant</font></b><br/>
        <br/>
        <font size="9">Bld de l'Empereur 26 • 1000 Brussels • Belgium</font><br/>
        <br/>
        <b><font color="#1a5d3f">☎</font></b> <font size="9">+32 465 20 60 24</font> • 
        <b><font color="#1a5d3f">✉</font></b> <font size="9">contact@eastatwest.com</font>
        """
        
        contact = Paragraph(contact_info, contact_style)
        
        contact_table = Table([[contact]], colWidths=[6.2*inch])
        contact_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9f4')),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1a5d3f')),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        contact_table.hAlign = 'CENTER'
        self.story.append(contact_table)
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Book a table button
        button_style = ParagraphStyle(
            'Button',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        button = Paragraph("BOOK A TABLE", button_style)
        
        button_table = Table([[button]], colWidths=[2.5*inch])
        button_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d4af37')),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1a5d3f')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        button_table.hAlign = 'CENTER'
        self.story.append(button_table)
        
        self.story.append(Spacer(1, 0.12*inch))
        
        # Footer message
        footer_msg_style = ParagraphStyle(
            'FooterMsg',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#4b5563'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        footer_msg = Paragraph("<i>We look forward to serving you!</i>", footer_msg_style)
        self.story.append(footer_msg)
        
        # Add logo in footer
        self.story.append(Spacer(1, 0.2*inch))

        if logo_path and os.path.exists(logo_path):
            footer_logo = Image(logo_path, width=0.9*inch, height=0.9*inch)
            footer_logo.hAlign = 'CENTER'
            self.story.append(footer_logo)
        
    def build(self):
        """Build the PDF document"""
        self.doc.build(self.story)

def main():
    # Initialize the PDF generator
    pdf = MenuPDFGenerator("east_west_menu.pdf")

    # Use the restaurant logo
    logo_path = r'C:\Users\mbike\.claude\projects\menu-project\logo.png'
    
    # Add cover page with logo
    pdf.add_cover_page(logo_path)
    
    # PAGE 1: COLD MEZZES
    cold_mezzes = [
        {"name": "Zahra", "description": "Cooked cauliflower, marinated in a homemade sauce (tomato, garlic and lemon), topped with lemon tahini sauce", "price": "7,50€", "is_vegetarian": True},
        {"name": "Muhammara", "description": "Grilled red pepper dip, pomegranate molasses and walnuts", "price": "8€", "is_vegan": True},
        {"name": "Makdous", "description": "Baby eggplants stuffed with walnuts and peppers marinated in olive oil", "price": "8€", "is_vegan": True},
        {"name": "Itch", "description": "Bulgur cooked in tomato sauce with peppers, onion, parsley and pomegranate molasses", "price": "7,50€", "is_vegan": True},
        {"name": "Hummus", "description": "Chickpea puree with tahini (sesame paste)", "price": "7,50€", "is_vegan": True},
        {"name": "Moutabal", "description": "Grilled eggplant caviar with tahini (sesame paste)", "price": "8€", "is_vegan": True},
        {"name": "Warak Enab", "description": "Vine leaves stuffed with rice, herbs, marinated in olive oil, mint and pomegranate molasses", "price": "7€", "is_vegan": True},
        {"name": "Moussaka", "description": "Eggplant, onion, chickpeas and tomato", "price": "7,50€", "is_vegan": True}
    ]
    
    pdf.add_section("Cold Mezzes", cold_mezzes)
    
    # WARM MEZZES
    warm_mezzes = [
        {"name": "Oriental Eggplant", "description": "Grilled eggplant topped with minced meat cooked with onion, tomato and pepper", "price": "13,50€"},
        {"name": "Chicken Liver", "description": "Chicken liver cooked with onion and special spices. Served with pomegranate sauce", "price": "11,50€"},
        {"name": "Fatteh", "description": "Cooked chickpeas, fried Lebanese bread, garlic and homemade lemon tahini sauce", "price": "7,50€", "is_vegetarian": True},
        {"name": "Falafel (2 pcs)", "description": "Fried chickpea balls served with tahini sauce", "price": "4€", "is_vegan": True},
        {"name": "Grilled Syrian Cheese", "description": "Grilled Syrian cheese", "price": "10€", "is_vegetarian": True},
        {"name": "Kibbeh (2 pcs)", "description": "Fried bulgur croquettes stuffed with minced meat, onion and walnuts", "price": "7€"},
        {"name": "Sujuk", "description": "Oven-baked Lebanese bread stuffed with seasoned minced meat, tomato and pickles", "price": "12,50€"},
        {"name": "Arayes Cheese", "description": "Oven-baked Lebanese bread stuffed with Syrian cheese", "price": "10€", "is_vegetarian": True},
        {"name": "Toshka", "description": "Oven-baked Lebanese bread stuffed with minced meat and Syrian cheese", "price": "12,50€"},
        {"name": "Batata Harra", "description": "Fried potato cubes with red peppers, coriander and garlic", "price": "7,50€", "is_vegan": True},
        {"name": "Foul Moudamas", "description": "Fava beans marinated with lemon juice, tomatoes, cumin, garlic, olive oil and tahini sauce", "price": "8€", "is_vegan": True}
    ]
    
    pdf.add_section("Warm Mezzes", warm_mezzes)
    
    # TASTING MENUS - on same page
    pdf.add_info_box("All tasting menus serve 2 people")
    
    tasting_menus = [
        {"name": "Menu East@West", "description": "Fattoush, Hummus, Moutabal, Zahra, Falafel, 2× Kibbeh, 2× Kabab skewers, 2× Chich taouk, 2× Dessert", "price": "67,50€"},
        {"name": "Menu Vegan", "description": "Fattoush, Hummus, Moutabal, Moussaka, Itch, Zahra, 2× Falafel, Batata Harra, 2× Dessert", "price": "64,50€", "is_vegan": True},
        {"name": "Menu Sahten", "description": "Tabouleh, Hummus, Toshka, Sujuk, Chicken liver, 2× Kibbeh, 2× Skewers, 2× Dessert", "price": "84€"},
        {"name": "Menu Lazeez", "description": "Tabouleh, Hummus, Moutabal, Muhammara, Warak Enab, Moussaka, Foul Moudamas, 2× Falafel, 2× Dessert", "price": "65,50€", "is_vegan": True}
    ]
    
    pdf.add_section("Tasting Menus / 2 People", tasting_menus)
    
    # DISHES
    dishes = [
        {"name": "Foodie Meat", "description": "Hummus, Zahra, Kibbeh, 1× Chich taouk, 1× Kabab, Foul moudamas, Fattouch", "price": "24€"},
        {"name": "Foodie Vegan", "description": "Hummus, Zahra, 2× Warak eneb, 2× Falafel, Batata harra, Foul moudamas, Fattouch", "price": "24€", "is_vegan": True},
        {"name": "Chef's Mezze", "description": "Grilled minced meat with mushrooms, onion, lemon tahini sauce and parsley", "price": "13,50€"}
    ]
    
    pdf.add_section("Dishes", dishes)
    
    # SKEWERS
    pdf.add_info_box("All skewers served with garlic sauce and pickles")
    
    skewers = [
        {"name": "2× Shish Taouk", "description": "Chicken skewers", "price": "10€"},
        {"name": "2× Kebab", "description": "Beef skewers", "price": "10€"}
    ]
    
    pdf.add_section("Skewers", skewers)
    
    # LUNCH DISHES - removed page break
    pdf.add_info_box("All dishes are served with Lebanese bread")
    
    lunch_dishes = [
        {"name": "Chef's Dish", "description": "1 kebab, 1 chich taouk, warak eneb, kibbeh, cauliflower, muhammara, fattouch", "price": "23,50€"},
        {"name": "Sujuk", "description": "Lebanese bread stuffed with minced meat, tomato, pickles + hummus, moutabal, Fattoush", "price": "20,80€"},
        {"name": "Toshka", "description": "Lebanese bread stuffed with minced meat and Syrian cheese + hummus, moutabal, Fattoush", "price": "20,80€"},
        {"name": "Chich Taouk", "description": "2 chicken skewers + hummus, itch (bulgur), fattoush, pickles, garlic sauce", "price": "19€"},
        {"name": "Mix Grill", "description": "1 kebab and 1 chich taouk + hummus, itch (bulgur), fattoush", "price": "19€"},
        {"name": "Kebab", "description": "2 seasoned minced meat skewers + hummus, fattoush", "price": "19€"},
        {"name": "Mix Break", "description": "Hummus, itch (bulgur), kabab/chich taouk, cauliflower, fattouch", "price": "16,50€"},
        {"name": "Falafel", "description": "4 pieces falafel + hummus, moutabal, Fattoush, tahini sauce, pickles", "price": "18€", "is_vegan": True},
        {"name": "Mix Break Vegan", "description": "Hummus, warak eneb, itch (bulgur), cauliflower, fattouch", "price": "14,50€", "is_vegan": True}
    ]
    
    pdf.add_section("Lunch Dishes", lunch_dishes)
    
    # SANDWICH FORMULAS
    sandwiches = [
        {"name": "Falafel Sandwich + Fattoush Salad", "description": "Falafel, tomato, tahini, pickles, lettuce", "price": "12,50€", "is_vegan": True},
        {"name": "Chich Taouk + Fattoush Salad", "description": "Grilled chicken, lettuce, tomato, garlic sauce", "price": "12,50€"},
        {"name": "Kabab + Fattoush Salad", "description": "Minced meat, hummus, tomato, lettuce, onion", "price": "12,50€"}
    ]
    
    pdf.add_section("Sandwich + Salad Formulas", sandwiches)
    
    # SALADS - removed page break
    salads = [
        {"name": "Original Tabouleh", "description": "Parsley, tomato, onion, lemon, bulgur, mint", "price": "8€", "is_vegan": True},
        {"name": "Fattoush", "description": "Tomato, lettuce, red cabbage, radish, cucumber, onion", "price": "8€", "is_vegan": True},
        {"name": "Falafel Salad", "description": "Falafel, lettuce, cucumber, tomato, pickles, tahini", "price": "13,50€", "is_vegan": True}
    ]
    
    pdf.add_section("Salads", salads)
    
    # Add contact page with logo in footer
    pdf.add_contact_page(logo_path)
    
    # Build the PDF
    pdf.build()
    print("PDF menu generated successfully!")
    print(f"Saved to: east_west_menu.pdf")

if __name__ == "__main__":
    main()
