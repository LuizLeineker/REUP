import tkinter as tk
from tkinter import messagebox
import mysql.connector

# CONEXÃO COM O BANCO ===================================================================================================
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # ou 'usuario_reup' se você criou
        password="positivo",  # sua senha do mysql
        database="reup_db"
    )


# CRUD =================================================================================================================

# Função para mostrar os frames
def mostrar_frame(frame):
    frame.tkraise()

# Função para inserir produto
def inserir_produto():
    id_val = id_produto.get()
    modelo_val = modelo.get()
    tamanho_val = tamanho.get()
    marca_val = marca.get()

    if id_val == "" or modelo_val == "Selecione uma opção" or tamanho_val == "Selecione um tamanho" or marca_val == "":
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "INSERT INTO produtos (id, modelo, tamanho, marca) VALUES (%s, %s, %s, %s)"
        valores = (id_val, modelo_val, tamanho_val, marca_val)

        cursor.execute(sql, valores)
        conexao.commit()

        messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")

        id_produto.delete(0, tk.END)
        marca.delete(0, tk.END)
        modelo.set("Selecione uma opção")
        tamanho.set("Selecione um tamanho")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao inserir: {erro}")

    finally:
        cursor.close()
        conexao.close()


# Função para buscar produto pelo ID
def buscar_produto():
    id_val = entrada_id_excluir.get()
    if id_val == "":
        messagebox.showerror("Erro", "Informe o ID para buscar!")
        return

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "SELECT * FROM produtos WHERE id = %s"
        cursor.execute(sql, (id_val,))
        resultado = cursor.fetchone()

        if resultado:
            messagebox.showinfo("Produto encontrado",
                                f"ID: {resultado[0]}\nModelo: {resultado[1]}\nTamanho: {resultado[2]}\nMarca: {resultado[3]}")
        else:
            messagebox.showinfo("Não encontrado", "Produto não encontrado!")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro na busca: {erro}")

    finally:
        cursor.close()
        conexao.close()


# INTERFACE ============================================================================================================
# Criar janela
janela = tk.Tk()
janela.title("ReUp")
janela.geometry("1200x600")

janela.rowconfigure(0, weight=1)
janela.columnconfigure(0, weight=1)

# Frames
frame_principal = tk.Frame(janela)
frame_principal.grid(row=0, column=0, sticky='nsew')

frame_Inserir = tk.Frame(janela)
frame_Inserir.grid(row=0, column=0, sticky='nsew')

frame_Excluir = tk.Frame(janela)
frame_Excluir.grid(row=0, column=0, sticky='nsew')


# Frame principal
label = tk.Label(frame_principal, text="ReUp", font=("Arial", 24))
label.pack(pady=50)

botaoInserir = tk.Button(frame_principal, text="Inserir Produto", command=lambda: mostrar_frame(frame_Inserir))
botaoInserir.pack(pady=10)

botaoExcluir = tk.Button(frame_principal, text="Buscar Produto", command=lambda: mostrar_frame(frame_Excluir))
botaoExcluir.pack(pady=25)

# Frame Inserir Produto
label_inserir = tk.Label(frame_Inserir, text="Inserir Produto", font=("Arial", 24))
label_inserir.pack(pady=50)

tk.Label(frame_Inserir, text="Insira o ID:", font=("Arial", 12)).pack(pady=8)
id_produto = tk.Entry(frame_Inserir)
id_produto.pack(pady=10)

tk.Label(frame_Inserir, text="Selecione o modelo:", font=("Arial", 12)).pack(pady=15)
modelo = tk.StringVar(frame_Inserir)
modelo.set("Selecione uma opção")
opcoes = ["Camisa", "Camiseta", "Polo", "Jaqueta", "Moletom", "Calça Jeans", "Calça Moletom"]
menu = tk.OptionMenu(frame_Inserir, modelo, *opcoes)
menu.pack(pady=17)

tk.Label(frame_Inserir, text="Selecione o tamanho:", font=("Arial", 12)).pack(pady=20)
tamanho = tk.StringVar(frame_Inserir)
tamanho.set("Selecione um tamanho")
opcoesTamanho = ["GG", "G", "M", "P", "PP"]
menuTamanho = tk.OptionMenu(frame_Inserir, tamanho, *opcoesTamanho)
menuTamanho.pack(pady=22)

tk.Label(frame_Inserir, text="Marca:", font=("Arial", 12)).pack(pady=15)
marca = tk.Entry(frame_Inserir)
marca.pack(pady=10)

botaoSalvar = tk.Button(frame_Inserir, text="Salvar Produto", command=inserir_produto)
botaoSalvar.pack(pady=20)

botaoVoltarInserir = tk.Button(frame_Inserir, text="Voltar", command=lambda: mostrar_frame(frame_principal))
botaoVoltarInserir.pack(pady=10)

# Frame Buscar Produto
label_excluir = tk.Label(frame_Excluir, text="Buscar Produto", font=("Arial", 24))
label_excluir.pack(pady=50)

tk.Label(frame_Excluir, text="Insira o ID:", font=("Arial", 12)).pack(pady=19)
entrada_id_excluir = tk.Entry(frame_Excluir)
entrada_id_excluir.pack(pady=20)

botaoBuscar = tk.Button(frame_Excluir, text="Buscar", command=buscar_produto)
botaoBuscar.pack(pady=10)

botaoVoltarExcluir = tk.Button(frame_Excluir, text="Voltar", command=lambda: mostrar_frame(frame_principal))
botaoVoltarExcluir.pack(pady=10)


# Mostrar inicialmente o frame principal
mostrar_frame(frame_principal)

janela.mainloop()
