from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from tkinter import filedialog, messagebox
from datetime import datetime

import os

class PDFGenerator:
    def __init__(self, app):
        self.app = app
        self.setup_styles()
   
    def setup_styles(self):
        self.styles = getSampleStyleSheet()
       
        self.id_style = ParagraphStyle(
            'IDStyle', parent=self.styles['Normal'], fontSize=14.271, spaceAfter=12,
            alignment=TA_LEFT, fontName='Helvetica-Bold'
        )
       
        self.cliente_style = ParagraphStyle(
            'ClienteStyle', parent=self.styles['Normal'], fontSize=13, spaceAfter=12,
            alignment=TA_LEFT, fontName='Helvetica'
        )
       
        self.intro_style = ParagraphStyle(
            'IntroStyle', parent=self.styles['Normal'], fontSize=14, spaceAfter=15,
            alignment=TA_CENTER, fontName='Helvetica-Bold'
        )
       
        self.mao_obra_style = ParagraphStyle(
            'MaoObraStyle', parent=self.styles['Normal'], fontSize=12, spaceAfter=6,
            alignment=TA_RIGHT, fontName='Helvetica'
        )
       
        self.total_style = ParagraphStyle(
            'TotalStyle', parent=self.styles['Normal'], fontSize=12, spaceAfter=6,
            alignment=TA_RIGHT, fontName='Helvetica-Bold'
        )
       
        self.assinatura_style = ParagraphStyle(
            'AssinaturaStyle', parent=self.styles['Normal'], fontSize=12, spaceAfter=6,
            alignment=TA_LEFT, fontName='Helvetica'
        )
       
        self.data_style = ParagraphStyle(
            'DataStyle', parent=self.styles['Normal'], fontSize=12, spaceAfter=6,
            alignment=TA_RIGHT, fontName='Helvetica'
        )
   
    def gerar_pdf(self):
        if not self.app.item_manager.itens:
            messagebox.showwarning("Aviso", "Adicione pelo menos um item ao orçamento.")
            return
       
        if not self.app.cliente_var.get().strip():
            messagebox.showwarning("Aviso", "Informe o nome do cliente.")
            return
       
        nome_arquivo = f"orcamento-{self.app.orcamento_id}-{self.app.cliente_var.get().replace(' ', '_')}.pdf"
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=nome_arquivo
        )
       
        if not arquivo:
            return
       
        try:
            doc = SimpleDocTemplate(arquivo, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                                    topMargin=20*mm, bottomMargin=20*mm)
           
            elementos = []
           
            # Logo
            if os.path.exists(self.app.logo_path):
                try:
                    logo = Image(self.app.logo_path, width=88.71*mm, height=22.56*mm)
                    elementos.append(Spacer(1, 10*mm))
                    elementos.append(logo)
                    elementos.append(Spacer(1, 12*mm))
                except Exception as e:
                    print(f"Erro ao carregar logo: {e}")
                    elementos.append(Spacer(1, 40*mm))
           
            # ID
            id_text = f"ORÇAMENTO Nº {self.app.orcamento_id}"
            elementos.append(Paragraph(id_text, self.id_style))
            elementos.append(Spacer(1, 10*mm))
           
            # Cliente
            cliente_text = f"<b>Cliente:</b> {self.app.cliente_var.get()}"
            elementos.append(Paragraph(cliente_text, self.cliente_style))
            elementos.append(Spacer(1, 12*mm))
           
            # Intro
            intro_text = "<b>Prezado cliente, esta é nossa proposta orçamentária,<br/><br/>conto com sua avaliação.</b>"
            elementos.append(Paragraph(intro_text, self.intro_style))
            elementos.append(Spacer(1, 10*mm))
           
            # Tabela de itens
            dados_tabela = [['ITEM', 'DESCRIÇÃO', 'QUANT.', 'VALOR', 'TOTAL']]

            # Estilo para descrições (auto-wrap na largura da coluna)
            desc_style = ParagraphStyle(
                'DescStyle',
                parent=self.styles['Normal'],
                fontSize=10,  # Tamanho da fonte para cálculo preciso do wrap
                alignment=TA_LEFT,
                leftIndent=6,  # Padding interno
                rightIndent=6,
                spaceAfter=0,
                spaceBefore=0
            )

            for item in self.app.item_manager.itens:
                # Formatar valores
                valor_str = f"R$ {item['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                total_str = f"R$ {item['total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
                # Determinar quantidade para exibição
                if item['tipo'] == 'numero':
                    quant_display = f"{item['quantidade']:.0f}"
                elif item['tipo'] == 'm2':
                    quant_display = item['medida']  # Já está no formato "largura x altura"
                else:
                    quant_display = item['medida']
            
                # Usar Paragraph para auto-quebra na largura de 80mm (7.8cm)
                descricao_para = Paragraph(item['descricao'], desc_style)
            
                dados_tabela.append([
                    item['id'],
                    descricao_para,  # Auto-wrap baseado na largura da coluna
                    quant_display,
                    valor_str,
                    total_str
                ])

            # Criar tabela (ajustado para suportar Paragraph na coluna 1)
            tabela = Table(dados_tabela, colWidths=[20*mm, 80*mm, 25*mm, 30*mm, 30*mm])
            tabela.setStyle(TableStyle([
                # Cabeçalho em negrito e centralizado
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                # Alinhamento das colunas
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Item
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Descrição (Paragraph cuida do wrap)
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Quantidade
                ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Valor
                ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # Total
                # Grid simples
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # Padding interno (ajustado para Paragraph)
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                # Específico para Paragraph na coluna de descrição
                ('VALIGN', (1, 1), (1, -1), 'TOP'),  # Alinhamento vertical no topo para texto longo
            ]))

            elementos.append(tabela)
            elementos.append(Spacer(1, 18*mm))
           
            # Mão de obra
            mao_obra_text = "VALOR DA MÃO DE OBRA COM MATERIAL" if self.app.mao_obra_var.get() == "com_material" else "VALOR SOMENTE DA MÃO DE OBRA"
            elementos.append(Paragraph(mao_obra_text, self.mao_obra_style))
            elementos.append(Spacer(1, 5*mm))
           
            # Total
            total = sum(item['total'] for item in self.app.item_manager.itens)
            total_str = f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            elementos.append(Paragraph(f"<b>TOTAL: {total_str}</b>", self.total_style))
           
            # Prazo
            if self.app.prazo_var.get() and self.app.prazo_entry.get().strip() and self.app.prazo_entry.get() != "Ex: 15 dias úteis":
                prazo_text = f"<b>PRAZO DE ENTREGA: {self.app.prazo_entry.get()}</b> DIAS"
                elementos.append(Spacer(1, 5*mm))
                elementos.append(Paragraph(prazo_text, self.mao_obra_style))
           
            # Assinatura
            elementos_assinatura = []
            elementos_assinatura.append(Spacer(1, 15*mm))
            elementos_assinatura.append(Paragraph("_" * 31, self.assinatura_style))
            elementos_assinatura.append(Paragraph("<b>Francisco de Jesus Nascimento</b>", self.assinatura_style))
            elementos_assinatura.append(Spacer(1, 5*mm))
            data_atual = datetime.now().strftime("%d/%m/%Y")
            elementos_assinatura.append(Paragraph(data_atual, self.data_style))
           
            elementos.append(KeepTogether(elementos_assinatura))
           
            doc.build(elementos)
           
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\nArquivo: {arquivo}")
           
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")
            import traceback
            traceback.print_exc()