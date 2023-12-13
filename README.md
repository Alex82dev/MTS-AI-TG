# MTS-AI-TG
Сервис обработки речи в Telegram на основе MTS AI



Скрипт запускает основной цикл, который ожидает команды от Telegram и выполняет соответствующие действия в ответ. Это позволяет скрипту непрерывно работать и обрабатывать входящие сообщения.

Запустите скрипт с помощью команды `python имяфайла.py 

Он предназначен для синтеза речи на основе текстовых сообщений и отправки полученного аудиофайла в Telegram. 

Обратите внимание, что для работы скрипта вам потребуется установить необходимые зависимости, такие как `grpcio`, `googleapis-common-protos`, `python-telegram-bot`, `keycloak`, и другие. Вы можете установить их с помощью `pip install <имя_пакета>`.

Замените `YOUR_BOT_TOKEN` на токен вашего Telegram бота и `chat_id` на идентификатор чата в Telegram, куда вы хотите отправить аудиофайл.

Нужно создать  файл config.ini в папке проекта: 

[API]
server_address = audiogram.mts.ai:443

[Auth]
sso_server_url = https://isso.mts.ru/auth/
realm_name = mts
client_id = <client_id>
client_secret = <client_secret>





Для упаковки в Docker-контейнер вам понадобится создать Dockerfile

# Используем базовый образ с предустановленным Python
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем код в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir grpcio \
    keycloak \
    python-telegram-bot \
    protobuf

# Открываем необходимые порты
# EXPOSE <порт>

# Определяем команду, которая будет запускаться при старте контейнера
CMD ["python", "ваш_скрипт.py"]

Убедитесь, что заменили ваш_скрипт.py на фактическое имя вашего Python-скрипта.

Для сборки Docker-образа перейдите в директорию, содержащую Dockerfile, и выполните следующую команду:

Copy
docker build -t имя_образа .
Эта команда собирает Docker-образ, используя Dockerfile в текущей директории, и помечает его именем имя_образа (вы можете выбрать любое имя).

После того, как образ будет собран, вы можете запустить контейнер на основе этого образа с помощью следующей команды:

Copy
docker run имя_образа
Эта команда запускает контейнер на основе образа имя_образа. Если вашему скрипту требуются аргументы командной строки, вы можете передать их после имени образа:

Copy
docker run имя_образа аргумент1 аргумент2
Замените аргумент1 и аргумент2 на фактические аргументы командной строки, необходимые вашему скрипту.

Обратите внимание, что вам может потребоваться изменить Dockerfile или команду сборки в соответствии с конкретными требованиями вашего приложения
