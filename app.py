# app.py (Versão final com WhatsApp integrado; logo bundlada; pronto para compilar)
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from ui.initial_screen import criar_tela_inicial
from ui.main_interface import criar_interface_principal
from managers.client_manager import ClientManager
from managers.item_manager import ItemManager
from pdf.generator import PDFGenerator
from utils.helpers import gerar_id

class OrcamentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Orçamentos - Manauara Design")
        self.root.geometry("1400x1200")
        # Centralizar janela principal
        self.root.update_idletasks()  # Atualiza geometria
        screen_width = self.root.winfo_screenwidth()  # 1920
        screen_height = self.root.winfo_screenheight()  # 1080
        window_width = 1100
        window_height = 900
        x = (screen_width // 2) - (window_width // 2)  # Centraliza horizontal: ~460
        y = (screen_height // 2) - (window_height // 2)  # Centraliza vertical: ~190
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configurações CTk (temas aero 2025)
        ctk.set_appearance_mode("light")  # Light por default
        ctk.set_default_color_theme("blue")  # Azul Apple-like
        
        # Variáveis principais
        self.orcamento_id = gerar_id()
        # Path da logo (funciona em dev e .exe bundlado)
        if getattr(sys, 'frozen', False):
            # Rodando como .exe: usa temp dir
            base_path = sys._MEIPASS
        else:
            # Dev: usa pasta atual
            base_path = os.path.abspath(".")
        self.logo_path = os.path.join(base_path, "logo", "Logomain.jpg")
        self.numero_whatsapp = "+5511999999999"  # MUDE AQUI pro número específico (formato internacional)
        self.client_manager = ClientManager()
        self.item_manager = ItemManager()
        self.item_manager.app = self  # Permite acessar app no manager  
        self.pdf_generator = PDFGenerator(self)
        
        # Configurar salvamento ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)
        
        # Mostrar tela inicial
        self.criar_tela_inicial()
    
    def criar_tela_inicial(self):
        """Cria a tela inicial com botão para novo orçamento"""
        self.root.configure(fg_color=("#f8f9fa", "#2b2b2b"))
        criar_tela_inicial(self.root, self.iniciar_novo_orcamento)
    
    def iniciar_novo_orcamento(self):
        """Inicia um novo orçamento: limpa dados e mostra interface principal"""
        # Limpar dados anteriores
        self.item_manager.itens = []
        self.orcamento_id = gerar_id()
        
        # Destruir tela inicial
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Criar e mostrar interface principal
        self.criar_interface()
    
    def novo_orcamento_mantendo_cliente(self):
        """Gera novo orçamento mantendo o cliente selecionado"""
        self.item_manager.itens = []
        self.orcamento_id = gerar_id()
        self.id_label.configure(text=self.orcamento_id)  # Correção: .configure
        
        # Limpar tabela via item_manager
        for item in self.item_manager.tree.get_children():
            self.item_manager.tree.delete(item)
        
        # Resetar total via item_manager
        self.item_manager.atualizar_total(self.total_label)
        
        # Manter cliente selecionado (self.cliente_var permanece)
        messagebox.showinfo("Novo Orçamento", f"Novo orçamento gerado! ID: {self.orcamento_id}\nCliente mantido: {self.cliente_var.get() or 'Nenhum'}")
    
    def criar_interface(self):
        """Cria a interface principal"""
        criar_interface_principal(self.root, self)
        # Inicializar tabela e total vazios após criar interface
        self.item_manager.atualizar_tabela()
        self.item_manager.atualizar_total(self.total_label)
    
    def ao_fechar(self):
        """Função chamada ao fechar o programa"""
        try:
            # Salvar clientes antes de fechar
            self.client_manager.salvar_clientes()
            print("Clientes salvos com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar ao fechar: {e}")
        finally:
            # Fechar o programa
            self.root.destroy()