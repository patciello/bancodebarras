import flet as ft
import requests

# Função para buscar textos no backend
def fetch_texts():
    response = requests.get('http://localhost:5000/texts')
    if response.status_code == 200:
        return response.json()
    return []

def main(page: ft.Page):
    page.title = "Micro SaaS"
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    search_box = ft.TextField(
        hint_text="Buscar ou cadastrar texto...",
        width=500,
        bgcolor=ft.colors.WHITE,
        color=ft.colors.BLACK,
        border_radius=15,
    )

    result_text = ft.Text(value="")

    def add_text(e):
        text = search_box.value
        if text.strip() == "":
            result_text.value = "Por favor, insira um texto!"
            page.update()
            return
        
        response = requests.post('http://localhost:5000/texts', json={'text': text})
        if response.status_code == 201:
            result_text.value = "Texto adicionado com sucesso!"
        elif response.status_code == 400:
            result_text.value = "Texto já existente!"
        else:
            result_text.value = "Erro ao adicionar texto!"
        
        update_text_list()
        page.update()

    # Atualizar a lista de textos
    def update_text_list():
        texts = fetch_texts()
        text_list.controls.clear()
        for text in texts:
            text_list.controls.append(ft.Text(text['text'], color=ft.colors.WHITE))

    # Botão de adicionar texto
    submit_button = ft.ElevatedButton("Adicionar", on_click=add_text)

    # Lista de textos
    text_list = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.AUTO
    )

    # Carregar a lista inicial de textos
    update_text_list()

    # Adiciona os elementos à página
    page.add(
        ft.Column(
            [
                search_box,
                submit_button,
                result_text,
                text_list
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

# Executar o aplicativo Flet
ft.app(target=main)
