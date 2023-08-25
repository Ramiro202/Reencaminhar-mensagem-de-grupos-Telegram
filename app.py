
from os import system
from time import sleep
from dotenv import dotenv_values
from pyfiglet import figlet_format
from telethon.sync import TelegramClient, events
from telethon.tl.types import Channel

system("clear || cls")
env = dotenv_values(".env")
api_id = env["API_ID"]
api_hash = env["API_HASH"]
phone = env["PHONE"]


try:
    # Criar uma instância do cliente
    client = TelegramClient("session_name", api_id, api_hash)
    # Iniciar o cliente
    client.connect()

except ConnectionError:
    print("=="*20)
    print("\033[1;31mERRO | Falha na conexão a internet\033[m")
    exit()

def banner():
    user = client.get_me()
    print("\033[1;34mby: https://t.me/ramirosegunda\033[m")
    print("??"*25)
    text = figlet_format("Telegram CopMsg", width=50, justify="center")
    print("\033[1;34m", text, "\033[m")
    print("=="*25)
    print(f"\033[1;32m{'O programa irá se incarregar de pegar Todas '.center(50)}")
    print(f"\033[1;32m{'as mensagens do Grupo/Canal que selecionares e'.center(50)}")
    print(f"{'irá mandar onde tu desejar!'.center(50)}\033[m")
    print("--"*25)
    print(f"\033[1;34mUsuário: {user.first_name} {f'({user.username})'.rjust(32)}")
    print("~~"*25)

def find_groups():
    lista = list()
    # Obter a lista de conversas
    dialogs = client.get_dialogs()

    # Pegar apenas os grupos
    for dialog in dialogs:
        if isinstance(dialog.entity, Channel):
            group = dialog.entity
            lista.append({"name_group": group.title, "chat_id": group.id})
    return lista

def target_group(chat_id):
    # Onde as mensagens serão copiadas
    target = chat_id
    group_msg = client.get_messages(target, limit=200)

def copy_and_send(source_chat_id, target_chat_id):
    @client.on(events.NewMessage(chats=source_chat_id))
    async def event_handler(event):
        if event.message.text:
            await client.send_message(target_chat_id, event.message.text)
        elif event.message.media:
            media = None
            if event.message.photo:
                media = event.message.photo
            elif event.message.video:
                media = event.message.video
            elif event.message.document:
                media = event.message.document

            if media:
                await client.send_file(target_chat_id, media)
    
    # Iniciar o cliente para receber e enviar as mensagens
    client.start()
    client.run_until_disconnected()

def group_send_msg(chat_id, message):
    target = chat_id
    client.send_message(target, message)

def forward_messages(source_chat_id, target_chat_id):
    messages = client.get_messages(source_chat_id, limit=200)

    for message in messages:
        client.send_message(target_chat_id, message)

def reconectar(phone):
    # Se não estiver conectado, vai receber
    # O código de confirmação pelo telegram
    client.send_code_request(phone)
    client.sign_in(phone, input('Digite o codigo enviado: '))

# Se não estiver conectado, vai enviar o código para telegram
if not client.is_user_authorized():
    reconectar(phone)


banner()

groups = find_groups()
for num, group in enumerate(groups):
    print(f"{num} - {group['name_group']}")

print("--" * 25)
source_group = int(input("Grupo de onde deseja copiar as mensagens: "))
if 0 <= source_group < len(groups):
    source_chat_id = groups[source_group]['chat_id']
    target_group(source_chat_id)

    target_send_group = int(input("Grupo para onde deseja enviar as mensagens copiadas: "))
    if 0 <= target_send_group < len(groups):
        target_chat_id = groups[target_send_group]['chat_id']

else:
    print("Escolha inválida para copiar mensagens.")
    exit()

print("--" * 25)
print(f"Selecionado para copiar: {groups[source_group]['name_group']}")
print(f"Selecionado para receber: {groups[source_group]['name_group']}")
print("--" * 25)

copy_and_send(source_chat_id, target_chat_id)

