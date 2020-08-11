import telebot
from os import linesep
from calendario.calendar import Calendario

TOKEN = "1356839149:AAEBxwSv82WxBRNTMrlIFEtKMwtH_2v0fr0"
LISTA_COMANDOS = f'/compromisso_hoje - Exibe os compromissos de hoje{linesep}/compromisso_semana - Exibe os compromissos da semana{linesep}/criar_compromisso - Permite que você crie um compromisso'
bot = telebot.TeleBot(TOKEN)
calendario = Calendario()
calendario.login()

def separaData(data):
    data = data.split('-')
    data.reverse()
    nova_data = ""
    for d in data:
        nova_data += d + "/"
    return nova_data[:-1]

def separa_Data_Hora(data):
    data = data[:-9]
    data = data.replace("T", " ")
    hora = data[11:]
    data = data[:10]
    data = separaData(data)
    return data, hora

def ajeitaEvento(lista_eventos):
    mensagem = ""
    for evento in lista_eventos:
        data_inicio, hora_inicio = separa_Data_Hora(lista_eventos[evento]["inicio"])
        data_termino, hora_termino = separa_Data_Hora(lista_eventos[evento]["final"])
        separador = '---------------------------------------------'
        mensagem += f'Nome: {lista_eventos[evento]["Nome"]}{linesep}    De: {data_inicio} as {hora_inicio}{linesep}    Até:  {data_termino} as {hora_termino}{linesep}{separador}{linesep}'
    return mensagem
    

@bot.message_handler(commands=["start"])
def boas_vindas(session):
    bot.send_message(session.chat.id, f'Olá! eu sou o #Botinho, fui desenvolvido para te ajudar a se lembrar dos seus *compromissos*.{linesep}Que tal dar uma olhadinha nos meus comandos?{linesep}{linesep}{LISTA_COMANDOS}{linesep}{linesep}Além de ver seus compromissos quando você quiser eu ainda vou te mandar o que você tem que fazer na semana todo domingo e o que você vai fazer no dia seguinte automaticamente.{linesep}Se você esquecer os comandos pode reve-los em /ajuda')

@bot.message_handler(commands=['ajuda'])
def ajuda(session):
    bot.send_message(session.chat.id, f'Aqui esá a lista de comandos:{linesep}{linesep}{LISTA_COMANDOS}')

@bot.message_handler(commands=['compromisso_hoje'])
def compromisso_hoje(session):
    eventos = calendario.PegaEventos()
    evento = ajeitaEvento(eventos)
    bot.send_message(session.chat.id, f'Seus #Compromissos_de_hoje:{linesep}{linesep}{evento}')

@bot.message_handler(commands=['compromisso_semana'])
def compromisso_semana(session):
    eventos = calendario.PegaEventos(7)
    evento = ajeitaEvento(eventos)
    bot.send_message(session.chat.id, f'Seus #Compromissos_da_semana:{linesep}{linesep}{evento}')

@bot.message_handler(commands=['criar_compromisso'])
def criar_compromisso(session):
    bot.send_message(session.chat.id, 'Cria um compromisso')

bot.polling()