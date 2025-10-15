import customtkinter as ctk
from app import OrcamentoApp

def main():
    root = ctk.CTk()  # Mudança: Use CTk em vez de tk.Tk
    app = OrcamentoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()