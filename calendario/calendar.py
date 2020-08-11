from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Calendario():
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.service = None
        
    def login(self):
        self.credenciais = None
        if os.path.exists('./calendario/token.pickle'):
            with open('./calendario/token.pickle', 'rb') as self.token:
                self.credenciais = pickle.load(self.token)
        if not self.credenciais or not self.credenciais.valid:
            if self.credenciais and self.credenciais.expired and self.credenciais.refresh_token:
                self.credenciais.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file('./calendario/credentials.json', self.SCOPES)
                self.credenciais = self.flow.run_local_server(port=0)
            with open('./calendario/token.pickle', 'wb') as self.token:
                pickle.dump(self.credenciais, self.token)
        self.service = build('calendar', 'v3', credentials=self.credenciais)
    
    def PegaEventos(self, dias=1):
        self.agora = datetime.datetime.utcnow().isoformat() + 'Z'
        self.limite = (datetime.datetime.utcnow() + datetime.timedelta(days=dias)).isoformat() + 'Z' 
        
        self.eventos = self.service.events().list(calendarId='primary', timeMin=self.agora,
                                                    timeMax=self.limite, maxResults=10,
                                                    singleEvents=True, orderBy='startTime').execute()
        resultados = self.eventos["items"]
        lista_eventos = {}
        for resultado in resultados:
            lista_eventos[resultado["id"]] = {"Nome" : resultado["summary"], "inicio": resultado["start"]["dateTime"], "final" : resultado["end"]["dateTime"]}
            
        return lista_eventos