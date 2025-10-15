# ui/initial_screen.py (Removido o toggle de dark mode daqui; movido para main_interface)
import customtkinter as ctk

def criar_tela_inicial(root, callback_novo_orcamento):
    """Cria a tela inicial com botão para novo orçamento (estilo glassmorphism)"""
    root.configure(fg_color=("#f8f9fa", "#2b2b2b"))  # Light/dark bg
    
    # Frame central com rounded e sombra simulada
    initial_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="transparent")
    initial_frame.pack(expand=True, fill="both", padx=100, pady=50)
    
    # Título principal (fonte Apple-like, grande e bold)
    title_label = ctk.CTkLabel(initial_frame, text="Bem-vindo ao", 
                               font=ctk.CTkFont(family="SF Pro Display", size=20, weight="bold"),
                               text_color=("#2c3e50", "#ecf0f1"))
    title_label.pack(pady=(0, 10))
    
    subtitle_label = ctk.CTkLabel(initial_frame, text="Sistema de Orçamentos", 
                                  font=ctk.CTkFont(family="SF Pro Display", size=36, weight="bold"),
                                  text_color=("#2c3e50", "#ecf0f1"))
    subtitle_label.pack(pady=(0, 20))
    
    company_label = ctk.CTkLabel(initial_frame, text="Programa Desenvolvido por Manauara Design", 
                                 font=ctk.CTkFont(family="SF Pro Text", size=18),
                                 text_color=("#7f8c8d", "#bdc3c7"))
    company_label.pack(pady=(0, 50))
    
    # Botão principal com rounded, gradient e hover scale
    btn_frame = ctk.CTkFrame(initial_frame, fg_color="transparent")
    btn_frame.pack()
    
    novo_btn = ctk.CTkButton(btn_frame, text="Gerar Novo Orçamento", 
                             command=callback_novo_orcamento,
                             font=ctk.CTkFont(size=16, weight="bold"),
                             fg_color=("#007AFF", "#0a84ff"),  # Azul Apple
                             hover_color=("#0056b3", "#007AFF"),
                             text_color=("white", "white"),
                             corner_radius=12,
                             height=50,
                             width=250)
    novo_btn.pack(pady=20)