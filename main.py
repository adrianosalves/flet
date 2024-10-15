import flet as ft
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

def create_event(name, date, time, description):
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': f"Consulta Médica - {name}",
        'description': description,
        'start': {
            'dateTime': f"{date}T{time}:00",
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': f"{date}T{time}:30",
            'timeZone': 'America/Sao_Paulo',
        },
    }
    service.events().insert(calendarId='primary', body=event).execute()

def main(page: ft.Page):
    page.title = "Cadastro de Consulta Médica"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    name_field = ft.TextField(label="Nome do Paciente", width=300)
    date_field = ft.TextField(label="Data da Consulta", hint_text="DD/MM/AAAA", width=300)
    time_field = ft.TextField(label="Horário da Consulta", hint_text="HH:MM", width=300)
    description_field = ft.TextField(label="Descrição do Problema", multiline=True, width=300, height=100)

    def on_submit(e):
        if all([name_field.value, date_field.value, time_field.value, description_field.value]):
            create_event(name_field.value, date_field.value, time_field.value, description_field.value)
            page.add(ft.Text(f"Consulta cadastrada para {name_field.value} em {date_field.value} às {time_field.value}. Problema: {description_field.value}"))
        else:
            page.add(ft.Text("Por favor, preencha todos os campos.", color="red"))

    submit_button = ft.ElevatedButton(text="Cadastrar Consulta", on_click=on_submit)

    page.add(
        ft.Column(
            [
                name_field,
                date_field,
                time_field,
                description_field,
                submit_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(port=80, target=main)