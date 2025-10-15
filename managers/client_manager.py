import json
import os
import customtkinter as ctk
from tkinter import messagebox

class ClientManager:
    def __init__(self):
        self.clientes_file = "clientes.json"
        self.clientes = self.carregar_clientes()
    
    def carregar_clientes(self):
        try:
            if os.path.exists(self.clientes_file):
                with open(self.clientes_file, 'r', encoding='utf-8') as f:
                    self.clientes = json.load(f)
            else:
                self.clientes = []
                self.salvar_clientes()
            return self.clientes
        except Exception as e:
            print(f"Erro ao carregar clientes: {e}")
            self.clientes = []
            return []
    
    def salvar_clientes(self):
        try:
            with open(self.clientes_file, 'w', encoding='utf-8') as f:
                json.dump(self.clientes, f, ensure_ascii=False, indent=2)
            print("Clientes salvos no JSON!")  # Debug: Confirme salvamento
        except Exception as e:
            print(f"Erro ao salvar clientes: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar clientes: {e}")
    
    def atualizar_lista_clientes(self, combo):
        nomes_clientes = [cliente['nome'] for cliente in self.clientes]
        combo.configure(values=nomes_clientes)  # Correção: .configure para CTkComboBox
    
    def cadastrar_cliente(self, root, cliente_var, cliente_combo):
        janela = ctk.CTkToplevel(root)  # Use CTkToplevel
        janela.title("Cadastrar Novo Cliente")
        janela.geometry("400x300")
        janela.transient(root)
        janela.grab_set()
        
        # Correção: Lift e focus para ficar na frente
        janela.lift()  # Traz para frente
        janela.attributes('-topmost', True)  # Fica acima do main window
        janela.attributes('-topmost', False)  # Remove topmost após focar
        janela.focus_force()  # Força foco
        
        # Centralização para 1920x1080
        janela.update_idletasks()
        screen_width = janela.winfo_screenwidth()  # 1920
        screen_height = janela.winfo_screenheight()  # 1080
        popup_width = 400
        popup_height = 300
        x = (screen_width // 2) - (popup_width // 2)  # ~760
        y = (screen_height // 2) - (popup_height // 2)  # ~390
        janela.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        main_frame = ctk.CTkFrame(janela, corner_radius=15, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Nome:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", pady=5)
        nome_var = ctk.StringVar()
        nome_entry = ctk.CTkEntry(main_frame, textvariable=nome_var, width=300, corner_radius=8)
        nome_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        ctk.CTkLabel(main_frame, text="Telefone:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, sticky="w", pady=5)
        telefone_var = ctk.StringVar()
        telefone_entry = ctk.CTkEntry(main_frame, textvariable=telefone_var, width=300, corner_radius=8)
        telefone_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        ctk.CTkLabel(main_frame, text="Endereço:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, sticky="w", pady=5)
        endereco_var = ctk.StringVar()
        endereco_entry = ctk.CTkEntry(main_frame, textvariable=endereco_var, width=300, corner_radius=8)
        endereco_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def salvar():
            if nome_var.get().strip():
                novo_cliente = {
                    "nome": nome_var.get().strip(),
                    "telefone": telefone_var.get().strip(),
                    "endereco": endereco_var.get().strip()
                }
                self.clientes.append(novo_cliente)
                self.salvar_clientes()  # Garante salvamento no JSON
                self.atualizar_lista_clientes(cliente_combo)
                cliente_var.set(novo_cliente['nome'])
                janela.destroy()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nome do cliente é obrigatório.")
        
        ctk.CTkButton(button_frame, text="Salvar", command=salvar, 
                      fg_color=("#4caf50", "#27ae60"), text_color="white").pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Cancelar", command=janela.destroy, 
                      fg_color=("#f44336", "#e74c3c"), text_color="white").pack(side="left")
        
        main_frame.columnconfigure(1, weight=1)
    
    def editar_cliente(self, root, cliente_var, cliente_combo):
        cliente_selecionado = cliente_var.get()
        if not cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return
        
        cliente = next((c for c in self.clientes if c['nome'] == cliente_selecionado), None)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return
        
        janela = ctk.CTkToplevel(root)
        janela.title("Editar Cliente")
        janela.geometry("400x300")
        janela.transient(root)
        janela.grab_set()
        
        # Correção: Lift e focus para ficar na frente
        janela.lift()  # Traz para frente
        janela.attributes('-topmost', True)  # Fica acima do main window
        janela.attributes('-topmost', False)  # Remove topmost após focar
        janela.focus_force()  # Força foco
        
        # Centralização para 1920x1080
        janela.update_idletasks()
        screen_width = janela.winfo_screenwidth()  # 1920
        screen_height = janela.winfo_screenheight()  # 1080
        popup_width = 400
        popup_height = 300
        x = (screen_width // 2) - (popup_width // 2)  # ~760
        y = (screen_height // 2) - (popup_height // 2)  # ~390
        janela.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        main_frame = ctk.CTkFrame(janela, corner_radius=15, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Nome:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", pady=5)
        nome_var = ctk.StringVar(value=cliente['nome'])
        nome_entry = ctk.CTkEntry(main_frame, textvariable=nome_var, width=300, corner_radius=8)
        nome_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        ctk.CTkLabel(main_frame, text="Telefone:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=1, column=0, sticky="w", pady=5)
        telefone_var = ctk.StringVar(value=cliente['telefone'])
        telefone_entry = ctk.CTkEntry(main_frame, textvariable=telefone_var, width=300, corner_radius=8)
        telefone_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        ctk.CTkLabel(main_frame, text="Endereço:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, sticky="w", pady=5)
        endereco_var = ctk.StringVar(value=cliente['endereco'])
        endereco_entry = ctk.CTkEntry(main_frame, textvariable=endereco_var, width=300, corner_radius=8)
        endereco_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def salvar():
            if nome_var.get().strip():
                cliente['nome'] = nome_var.get().strip()
                cliente['telefone'] = telefone_var.get().strip()
                cliente['endereco'] = endereco_var.get().strip()
                self.salvar_clientes()  # Garante salvamento no JSON
                self.atualizar_lista_clientes(cliente_combo)
                cliente_var.set(cliente['nome'])
                janela.destroy()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nome do cliente é obrigatório.")
        
        ctk.CTkButton(button_frame, text="Salvar", command=salvar, 
                      fg_color=("#4caf50", "#27ae60"), text_color="white").pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Cancelar", command=janela.destroy, 
                      fg_color=("#f44336", "#e74c3c"), text_color="white").pack(side="left")
        
        main_frame.columnconfigure(1, weight=1)
    
    def apagar_cliente(self, cliente_var, cliente_combo):
        cliente_selecionado = cliente_var.get()
        if not cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para apagar.")
            return
        
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente apagar o cliente '{cliente_selecionado}'?")
        if resposta:
            self.clientes = [c for c in self.clientes if c['nome'] != cliente_selecionado]
            self.salvar_clientes()  # Garante salvamento no JSON após remoção
            self.atualizar_lista_clientes(cliente_combo)
            cliente_var.set("")
            messagebox.showinfo("Sucesso", "Cliente apagado com sucesso!")