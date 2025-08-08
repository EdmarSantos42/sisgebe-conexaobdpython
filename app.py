# app.py

from db_config import conectar
from crud import categoria

def main():
    conexao= conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM livros;")  # Exemplo de consulta simples

            resultados = cursor.fetchall()

            print("\nLivros cadastrados:")
            for linha in resultados:
                print(linha)

        except Exception as e:
            print(f"Erro na execução: {e}")
        finally:
            conexao.close()
            print("\nConexão encerrada.")

if __name__ == "__main__":
    main()

def menu():
    while True:
        print("\n=== MENU SGB ===")
        print("1. Criar Categoria")
        print("2. Listar Categorias")
        print("3. Atualizar Categoria")
        print("4. Deletar Categoria")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da categoria: ")
            descricao = input("Descrição: ")
            categoria.criar_categoria(nome, descricao)
        elif opcao == "2":
            cats = categoria.listar_categorias()
            for c in cats:
                print(f"{c['id']} - {c['nome']} ({c['descricao']})")
        elif opcao == "3":
            id_cat = int(input("ID da categoria: "))
            nome = input("Novo nome: ")
            descricao = input("Nova descrição: ")
            categoria.atualizar_categoria(id_cat, nome, descricao)
        elif opcao == "4":
            id_cat = int(input("ID da categoria: "))
            categoria.deletar_categoria(id_cat)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()