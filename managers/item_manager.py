# managers/item_manager.py (Correções: Use .configure para CTk; garanta destroy da janela; ajuste toggle_prazo)
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk  # Para compatibilidade com CTkEntry

class ItemManager:
    def __init__(self):
        self.itens = []
        self.tree = None
        self.total_label = None  # Para atualizar total
   
    def criar_tabela_itens(self, parent):
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)  # pack para CTkScrollableFrame
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
       
        columns = ('item', 'descricao', 'quantidade', 'medida', 'unidade', 'valor', 'total')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
       
        self.tree.heading('item', text='ITEM', anchor='center')
        self.tree.heading('descricao', text='DESCRIÇÃO', anchor='w')
        self.tree.heading('quantidade', text='QUANT.', anchor='center')
        self.tree.heading('medida', text='MEDIDA', anchor='center')
        self.tree.heading('unidade', text='UNIDADE', anchor='center')
        self.tree.heading('valor', text='VALOR UNIT.', anchor='e')
        self.tree.heading('total', text='TOTAL', anchor='e')
       
        self.tree.column('item', width=60, minwidth=50, anchor='center')
        self.tree.column('descricao', width=350, minwidth=200, anchor='w')
        self.tree.column('quantidade', width=80, minwidth=60, anchor='center')
        self.tree.column('medida', width=100, minwidth=80, anchor='center')
        self.tree.column('unidade', width=80, minwidth=60, anchor='center')
        self.tree.column('valor', width=120, minwidth=100, anchor='e')
        self.tree.column('total', width=120, minwidth=100, anchor='e')
       
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
       
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
       
        # Binds corrigidos
        self.tree.bind('<Double-1>', self.editar_item)
        self.tree.bind('<Button-3>', self.mostrar_menu_contexto)
       
        self.tree.tag_configure('even', background='#f8f9fa')
        self.tree.tag_configure('odd', background='#ffffff')
   
    def adicionar_item(self, root, total_label):
        """Adiciona um novo item à tabela (recebe root e total_label)"""
        item_num = len(self.itens) + 1
        item_id = f"{item_num:02d}"
        self.editar_item_janela(root, item_id, novo_item=True, total_label=total_label)
   
    def editar_item(self, event):
        """Abre janela de edição para item existente (via bind)"""
        item = self.tree.selection()[0]
        if not item:
            return
        item_id = self.tree.item(item, 'values')[0]
        root = event.widget.winfo_toplevel()
        self.editar_item_janela(root, item_id, novo_item=False)
   
    def editar_item_selecionado(self, root, total_label):
        """Edita item selecionado na tabela"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para editar.")
            return
        item = selection[0]
        item_id = self.tree.item(item, 'values')[0]
        self.editar_item_janela(root, item_id, novo_item=False, total_label=total_label)
   
    def editar_item_janela(self, root, item_id, novo_item=True, total_label=None):
        """Cria janela de edição de item (total_label opcional para atualizar após salvar)"""
        janela = ctk.CTkToplevel(root)  # Mudança: Use CTkToplevel para consistência
        janela.title(f"Editar Item {item_id}")
        janela.geometry("700x500")
        janela.update_idletasks()
        x = (janela.winfo_screenwidth() // 2) - (700 // 2)
        y = (janela.winfo_screenheight() // 2) - (500 // 2)
        janela.geometry(f"700x500+{x}+{y}")
        # managers/item_manager.py (Mesma correção no editar_item_janela, após janela.grab_set()):
        janela.lift()  # Traz para frente
        janela.attributes('-topmost', True)
        janela.attributes('-topmost', False)
        janela.focus_force()  # Força foco
        janela.transient(root)
        janela.grab_set()
       
        main_frame = ctk.CTkFrame(janela, corner_radius=15, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
       
        ctk.CTkLabel(main_frame, text="Descrição:").grid(row=0, column=0, sticky="w", pady=5)
        descricao_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        descricao_frame.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)
        
        # Use CTkTextbox para descrição (suporta multiline)
        descricao_text = ctk.CTkTextbox(descricao_frame, height=100, width=500, corner_radius=8)
        descricao_text.pack(fill="both", expand=True)
        
        char_count_label = ctk.CTkLabel(descricao_frame, text="0 caracteres")
        char_count_label.pack(anchor="e")
        
        def update_char_count(event=None):
            count = len(descricao_text.get("1.0", "end-1c").strip())
            char_count_label.configure(text=f"{count} caracteres")
        
        descricao_text.bind('<KeyRelease>', update_char_count)
        descricao_text.bind('<Button-1>', update_char_count)
        
        ctk.CTkLabel(main_frame, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=5)
        quantidade_var = tk.StringVar(value="1")  # Use tk.StringVar para compatibilidade com Spinbox
        quantidade_spinbox = tk.Spinbox(main_frame, from_=1, to=9999, textvariable=quantidade_var, width=20, font=("Segoe UI", 12))
        quantidade_spinbox.grid(row=1, column=1, sticky="w", pady=5)
        
        ctk.CTkLabel(main_frame, text="Tipo:").grid(row=2, column=0, sticky="w", pady=5)
        tipo_var = ctk.StringVar(value="numero")
        tipo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tipo_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        ctk.CTkRadioButton(tipo_frame, text="Número", variable=tipo_var, value="numero").pack(side="left", padx=(0, 10))
        ctk.CTkRadioButton(tipo_frame, text="M (linear)", variable=tipo_var, value="m").pack(side="left", padx=(0, 10))
        ctk.CTkRadioButton(tipo_frame, text="M² (área)", variable=tipo_var, value="m2").pack(side="left", padx=(0, 10))
        ctk.CTkRadioButton(tipo_frame, text="Unidade livre", variable=tipo_var, value="livre").pack(side="left")
        
        medida_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        medida_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        largura_var = ctk.StringVar()
        altura_var = ctk.StringVar()
        
        ctk.CTkLabel(medida_frame, text="Largura (m):").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
        largura_entry = ctk.CTkEntry(medida_frame, textvariable=largura_var, width=150)
        largura_entry.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 20))
        
        ctk.CTkLabel(medida_frame, text="Altura (m):").grid(row=0, column=2, sticky="w", pady=5, padx=(0, 10))
        altura_entry = ctk.CTkEntry(medida_frame, textvariable=altura_var, width=150)
        altura_entry.grid(row=0, column=3, sticky="w", pady=5)
        
        ctk.CTkLabel(medida_frame, text="Medida (m):").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
        medida_var = ctk.StringVar()
        medida_entry = ctk.CTkEntry(medida_frame, textvariable=medida_var, width=150)
        medida_entry.grid(row=1, column=1, sticky="w", pady=5, padx=(0, 20))
        
        ctk.CTkLabel(medida_frame, text="Unidade:").grid(row=1, column=2, sticky="w", pady=5, padx=(0, 10))
        unidade_var = ctk.StringVar()
        unidade_entry = ctk.CTkEntry(medida_frame, textvariable=unidade_var, width=150)
        unidade_entry.grid(row=1, column=3, sticky="w", pady=5)
        
        ctk.CTkLabel(main_frame, text="Valor Unitário (R$):").grid(row=4, column=0, sticky="w", pady=5)
        valor_var = ctk.StringVar()
        valor_entry = ctk.CTkEntry(main_frame, textvariable=valor_var, width=150, placeholder_text="0,00")
        valor_entry.grid(row=4, column=1, sticky="w", pady=5)
        
        def toggle_measurement_fields():
            tipo = tipo_var.get()
            if tipo == "m2":
                largura_entry.grid()
                altura_entry.grid()
                ctk.CTkLabel(medida_frame, text="Largura (m):").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 10))
                ctk.CTkLabel(medida_frame, text="Altura (m):").grid(row=0, column=2, sticky="w", pady=5, padx=(0, 10))
                medida_entry.grid_remove()
                unidade_entry.grid_remove()
                ctk.CTkLabel(medida_frame, text="Medida (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Unidade:").grid_remove()
            # ... (resto igual, mas use grid_remove/grid para CTk widgets)
            elif tipo == "m":
                medida_entry.grid()
                ctk.CTkLabel(medida_frame, text="Medida (m):").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 10))
                largura_entry.grid_remove()
                altura_entry.grid_remove()
                unidade_entry.grid_remove()
                ctk.CTkLabel(medida_frame, text="Largura (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Altura (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Unidade:").grid_remove()
            elif tipo == "livre":
                unidade_entry.grid()
                ctk.CTkLabel(medida_frame, text="Unidade:").grid(row=1, column=2, sticky="w", pady=5, padx=(0, 10))
                largura_entry.grid_remove()
                altura_entry.grid_remove()
                medida_entry.grid_remove()
                ctk.CTkLabel(medida_frame, text="Largura (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Altura (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Medida (m):").grid_remove()
            else:
                largura_entry.grid_remove()
                altura_entry.grid_remove()
                medida_entry.grid_remove()
                unidade_entry.grid_remove()
                ctk.CTkLabel(medida_frame, text="Largura (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Altura (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Medida (m):").grid_remove()
                ctk.CTkLabel(medida_frame, text="Unidade:").grid_remove()
        
        tipo_var.trace('w', lambda *args: toggle_measurement_fields())
        
        def format_value(event=None):
            try:
                valor = valor_var.get().replace(',', '.').replace('R$', '').strip()
                if valor:
                    if '.' not in valor and ',' not in valor:
                        valor = f"{valor}.00"
                    valor_float = float(valor)
                    valor_var.set(f"{valor_float:.2f}".replace('.', ','))
            except ValueError:
                pass
        
        valor_entry.bind('<FocusOut>', format_value)
        
        # Carregar dados se editando
        if not novo_item:
            for item in self.itens:
                if item['id'] == item_id:
                    descricao_text.insert("1.0", item['descricao'])
                    quantidade_var.set(str(int(item['quantidade'])))
                    tipo_var.set(item['tipo'])
                    if item['tipo'] == 'm2' and 'x' in item['medida']:
                        try:
                            largura, altura = item['medida'].split('x')
                            largura_var.set(largura.strip())
                            altura_var.set(altura.strip())
                        except:
                            pass
                    elif item['tipo'] == 'm':
                        medida_var.set(item['medida'])
                    elif item['tipo'] == 'livre':
                        unidade_var.set(item['unidade'])
                    valor_var.set(f"{item['valor']:.2f}".replace('.', ','))
                    break
        
        toggle_measurement_fields()
        update_char_count()
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        def salvar_item():
            try:
                descricao = descricao_text.get("1.0", "end-1c").strip()
                quantidade = float(quantidade_var.get().replace(',', '.'))
                tipo = tipo_var.get()
                
                if tipo == "m2":
                    largura = largura_var.get().replace(',', '.') if largura_var.get() else "0"
                    altura = altura_var.get().replace(',', '.') if altura_var.get() else "0"
                    medida = f"{largura}x{altura}"
                elif tipo == "m":
                    medida = medida_var.get().replace(',', '.') if medida_var.get() else "0"
                elif tipo == "livre":
                    medida = unidade_var.get().replace(',', '.') if unidade_var.get() else "0"
                else:
                    medida = "0"
                
                unidade = unidade_var.get() if tipo == "livre" else ""
                valor = float(valor_var.get().replace(',', '.'))
                
                if tipo == "numero":
                    total = quantidade * valor
                elif tipo == "m":
                    total = float(medida) * valor
                elif tipo == "m2":
                    largura_val = float(largura_var.get().replace(',', '.')) if largura_var.get() else 0
                    altura_val = float(altura_var.get().replace(',', '.')) if altura_var.get() else 0
                    area = largura_val * altura_val
                    total = area * valor
                else:
                    total = float(medida) * valor
                
                item_data = {
                    'id': item_id,
                    'descricao': descricao,
                    'quantidade': quantidade,
                    'tipo': tipo,
                    'medida': medida,
                    'unidade': unidade,
                    'valor': valor,
                    'total': total
                }
                
                if novo_item:
                    self.itens.append(item_data)
                else:
                    for i, item in enumerate(self.itens):
                        if item['id'] == item_id:
                            self.itens[i] = item_data
                            break
                
                self.atualizar_tabela()
                if total_label:
                    self.atualizar_total(total_label)
                janela.destroy()  # Garantia de destroy após salvar
                messagebox.showinfo("Sucesso", "Item salvo com sucesso!")  # Feedback visual
                
            except ValueError as e:
                messagebox.showerror("Erro", "Erro ao salvar item: Verifique os valores numéricos.")
        
        ctk.CTkButton(button_frame, text="Salvar", command=salvar_item, 
                      fg_color=("#4caf50", "#27ae60"), text_color="white").pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Cancelar", command=janela.destroy, 
                      fg_color=("#f44336", "#e74c3c"), text_color="white").pack(side="left")
        
        main_frame.columnconfigure(1, weight=1)
   
    def atualizar_tabela(self):
        """Atualiza a tabela de itens"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, item in enumerate(self.itens):
            valor_str = f"R$ {item['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            total_str = f"R$ {item['total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            if item['tipo'] == 'numero':
                unidade = 'un'
                medida_display = f"{item['quantidade']:.0f}"
            elif item['tipo'] == 'm':
                unidade = 'm'
                medida_display = item['medida']
            elif item['tipo'] == 'm2':
                unidade = 'm²'
                medida_display = item['medida']
            else:
                unidade = item['unidade'] or 'un'
                medida_display = item['medida']
            
            tag = 'even' if i % 2 == 0 else 'odd'
            
            self.tree.insert('', 'end', values=(
                item['id'],
                item['descricao'],
                medida_display,
                item['medida'] if item['tipo'] != 'numero' else '',
                unidade,
                valor_str,
                total_str
            ), tags=(tag,))
    
    def atualizar_total(self, total_label):
        """Atualiza o total geral"""
        total = sum(item['total'] for item in self.itens)
        total_str = f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        total_label.configure(text=total_str)  # Correção: .configure
    
    def mostrar_menu_contexto(self, event):
        """Mostra menu de contexto para remover item (clique direito)"""
        item = self.tree.selection()[0]
        if item:
            menu = ctk.CTkMenu(self.tree, tearoff=0)  # Use CTkMenu se disponível, ou tk.Menu
            menu.add_command(label="Remover Item", command=lambda: self.remover_item(item))
            menu.post(event.x_root, event.y_root)
    
    def remover_item(self, item):
        """Remove item da tabela"""
        item_id = self.tree.item(item, 'values')[0]
        self.itens = [it for it in self.itens if it['id'] != item_id]
        self.atualizar_tabela()
    
    def toggle_prazo(self, prazo_entry, prazo_var):
        """Ativa/desativa o campo de prazo de entrega"""
        if prazo_var.get():
            prazo_entry.configure(state='normal')  # Correção: .configure
            prazo_entry.delete(0, 'end')
        else:
            prazo_entry.configure(state='disabled')  # Correção: .configure
            prazo_entry.delete(0, 'end')
            prazo_entry.insert(0, "Ex: 15 dias úteis")