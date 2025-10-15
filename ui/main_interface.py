# ui/main_interface.py (Reordenado layout: itens acima de total/opções; toggle dark mode movido para title_frame; correções em lambdas)
import customtkinter as ctk
from tkinter import messagebox
from functools import partial

def toggle_dark_mode():
    """Função global para toggle dark mode"""
    current_mode = ctk.get_appearance_mode()
    new_mode = "dark" if current_mode == "light" else "light"
    ctk.set_appearance_mode(new_mode)

def criar_interface_principal(root, app):
    """Cria a interface principal completa (estilo aero 2025)"""
    root.configure(fg_color=("#f8f9fa", "#2b2b2b"))

    # Frame principal com padding amplo
    main_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    

    # Título com botão novo orçamento e toggle dark mode (alinhado à direita)
    title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    title_frame.pack(fill="x", pady=(0, 20))

    title_label = ctk.CTkLabel(
        title_frame,
        text="Sistema de Orçamentos",
        font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    )
    title_label.pack(side="left", padx=(0, 20), pady=10)

    # Botão novo orçamento (glass-like)
    novo_orc_btn = ctk.CTkButton(
        title_frame,
        text="📄 Novo Orçamento",
        command=app.novo_orcamento_mantendo_cliente,
        fg_color=("#e3f2fd", "#34495e"),
        hover_color=("#bbdefb", "#2c3e50"),
        text_color=("#1976d2", "#ecf0f1"),
        corner_radius=8,
        width=150
    )
    novo_orc_btn.pack(side="right", pady=10, padx=(0, 10))

    # Toggle dark mode (movido para cá)
    mode_toggle = ctk.CTkSwitch(title_frame, text="Dark Mode", command=toggle_dark_mode)
    mode_toggle.pack(side="right", pady=10)

    subtitle_label = ctk.CTkLabel(
        title_frame,
        text="Manauara Design",
        font=ctk.CTkFont(family="SF Pro Text", size=14),
        text_color=("#7f8c8d", "#bdc3c7")
    )
    subtitle_label.pack(side="left", pady=(0, 10))

    # Informações do orçamento (frame glass)
    info_frame = ctk.CTkFrame(main_frame, corner_radius=12, fg_color=("#f0f8ff", "#34495e"))
    info_frame.pack(fill="x", pady=(0, 15))

    # ID (label bold com cor accent)
    id_label_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    id_label_frame.pack(fill="x", padx=15, pady=10)
    ctk.CTkLabel(
        id_label_frame,
        text="ID do Orçamento:",
        font=ctk.CTkFont(size=12, weight="bold")
    ).pack(side="left")
    app.id_label = ctk.CTkLabel(
        id_label_frame,
        text=app.orcamento_id,
        font=ctk.CTkFont(family="Monaco", size=14, weight="bold"),
        text_color=("#e74c3c", "#e74c3c")
    )
    app.id_label.pack(side="left", padx=10)

    # Cliente (combobox rounded)
    cliente_frame_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
    cliente_frame_inner.pack(fill="x", padx=15, pady=10)
    ctk.CTkLabel(
        cliente_frame_inner,
        text="Cliente:",
        font=ctk.CTkFont(size=12, weight="bold")
    ).pack(side="left")

    app.cliente_var = ctk.StringVar()
    app.cliente_combo = ctk.CTkComboBox(
        cliente_frame_inner,
        variable=app.cliente_var,
        width=300,
        font=ctk.CTkFont(size=12),
        button_color=("#007AFF", "#0a84ff"),
        button_hover_color=("#0056b3", "#007AFF")
    )
    app.cliente_combo.pack(side="left", padx=(10, 10))

    # Botões cliente (pequenos, rounded)
    # Use partial para evitar problemas de binding de lambdas em loop
    btn_defs = [
        ("➕ Novo", partial(app.client_manager.cadastrar_cliente, app.root, app.cliente_var, app.cliente_combo)),
        ("✏️ Editar", partial(app.client_manager.editar_cliente, app.root, app.cliente_var, app.cliente_combo)),
        ("🗑️ Apagar", partial(app.client_manager.apagar_cliente, app.cliente_var, app.cliente_combo)),
    ]

    for text, cmd in btn_defs:
        btn = ctk.CTkButton(
            cliente_frame_inner,
            text=text,
            command=cmd,
            fg_color="transparent",
            hover_color=("#e3f2fd", "#34495e"),
            text_color=("#007AFF", "#ecf0f1"),
            width=60,
            height=25,
            corner_radius=6
        )
        btn.pack(side="left", padx=2)

    # Atualiza a lista de clientes no combobox (assinatura da sua função pode variar)
    # espera-se que atualizar_lista_clientes receba o combobox ou atualize via app.cliente_combo internamente
    try:
        app.client_manager.atualizar_lista_clientes(app.cliente_combo)
    except TypeError:
        # Caso a sua função espere outro formato, chame sem argumentos
        app.client_manager.atualizar_lista_clientes()

    # Itens (frame scrollable com rounded) - MOVIDO PARA ANTES DAS OPÇÕES/TOTAL
    items_frame = ctk.CTkScrollableFrame(main_frame, corner_radius=12, fg_color=("#f0f8ff", "#34495e"))
    items_frame.pack(fill="both", expand=True, pady=(0, 15))

    # Botões itens (barra superior glass)
    button_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
    button_frame.pack(fill="x", padx=15, pady=(10, 5))

    add_btn = ctk.CTkButton(
        button_frame,
        text="➕ Adicionar Item",
        command=lambda: app.item_manager.adicionar_item(app.root, app.total_label),
        fg_color=("#4caf50", "#27ae60"),
        hover_color=("#45a049", "#2ecc71"),
        text_color="white",
        corner_radius=8,
        height=35
    )
    add_btn.pack(side="left", padx=(0, 10))

    edit_btn = ctk.CTkButton(
        button_frame,
        text="✏️ Editar Item",
        command=lambda: app.item_manager.editar_item_selecionado(app.root, app.total_label),
        fg_color=("#ff9800", "#f39c12"),
        hover_color=("#fb8c00", "#e67e22"),
        text_color="white",
        corner_radius=8,
        height=35
    )
    edit_btn.pack(side="left")

    # Tabela itens
    app.item_manager.criar_tabela_itens(items_frame)

    # Opções de mão de obra e total (AGORA APÓS ITENS)
    mao_obra_frame = ctk.CTkFrame(main_frame, corner_radius=12, fg_color=("#f0f8ff", "#34495e"))
    mao_obra_frame.pack(fill="x", pady=(0, 15))

    app.mao_obra_var = ctk.StringVar(value="com_material")

    radio_frame = ctk.CTkFrame(mao_obra_frame, fg_color="transparent")
    radio_frame.pack(padx=15, pady=10, fill="x")

    ctk.CTkRadioButton(
        radio_frame,
        text="Valor da mão de obra com material",
        variable=app.mao_obra_var,
        value="com_material",
        font=ctk.CTkFont(size=12)
    ).pack(anchor="w", pady=5)

    ctk.CTkRadioButton(
        radio_frame,
        text="Valor somente da mão de obra",
        variable=app.mao_obra_var,
        value="somente_mao_obra",
        font=ctk.CTkFont(size=12)
    ).pack(anchor="w", pady=5)

    # Prazo (switch + entry rounded)
    prazo_frame = ctk.CTkFrame(mao_obra_frame, fg_color="transparent")
    prazo_frame.pack(padx=15, pady=10, fill="x")

    app.prazo_var = ctk.BooleanVar()
    ctk.CTkSwitch(
        prazo_frame,
        text="Incluir prazo de entrega",
        variable=app.prazo_var,
        command=lambda: app.item_manager.toggle_prazo(app.prazo_entry, app.prazo_var)
    ).pack(anchor="w")

    app.prazo_entry = ctk.CTkEntry(
        prazo_frame,
        width=200,
        placeholder_text="Ex: 15 dias úteis",
        font=ctk.CTkFont(size=12),
        corner_radius=8
    )
    app.prazo_entry.pack(anchor="w", pady=(5, 0))

    # Total (label bold com cor verde glass)
    total_frame = ctk.CTkFrame(mao_obra_frame, fg_color="transparent")
    total_frame.pack(padx=15, pady=10, fill="x")

    ctk.CTkLabel(
        total_frame,
        text="TOTAL:",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    ).pack(side="left")

    app.total_label = ctk.CTkLabel(
        total_frame,
        text="R$ 0,00",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#27ae60", "#2ecc71")
    )
    app.total_label.pack(side="right")

    # Botão PDF (grande, centralizado, com ícone)
    pdf_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    pdf_frame.pack(pady=20)

    pdf_btn = ctk.CTkButton(
        pdf_frame,
        text="📄 Gerar PDF",
        command=app.pdf_generator.gerar_pdf,
        fg_color=("#ff5722", "#e74c3c"),
        hover_color=("#f4511e", "#c0392b"),
        text_color="white",
        corner_radius=12,
        height=50,
        width=200,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    pdf_btn.pack()

    # Inicializar tabela e total
    app.item_manager.atualizar_tabela()
    app.item_manager.atualizar_total(app.total_label)
