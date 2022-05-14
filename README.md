### Проект YAMBD — REST API для сервиса YAMBD — базы отзывов о фильмах, книгах и музыке.
```
Сами произведения в YAMBD не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Арт»). Новые жанры может создавать только администратор.
```
### Проект YAMBD собирает отзывы (Review) пользователей на произведения (Title).
```
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию)
Техническое описание проекта YaMDb
К Django-проекту по адресу /redoc подключена документация API YaMDb. В ней описаны шаблоны запросов к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.
```
### URL for superuser:
http://127.0.0.1:8000/admin/

### Пользовательские роли
```
Аноним — может просматривать описания произведений, читать отзывы и комментарии.
Аутентифицированный пользователь (user)— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.
Администратор (admin) — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
Администратор Django — те же права, что и у роли Администратор.
Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос с параметром email на /api/v1/auth/email/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email .
Пользователь отправляет POST-запрос с параметрами email и confirmation_code на /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).
Если пользователя создаёт администратор (например, через POST-запрос api/v1/users/...) — письмо с кодом отправлять не нужно.
Тесты не будут проверять отправку писем.
```
### Ресурсы API YaMDb
```
Ресурс AUTH: аутентификация.
Ресурс USERS: пользователи.
Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.
Каждый ресурс описан в документации: указаны эндпойнты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.
Связанные данные и каскадное удаление
При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
При удалении объекта категории Category не удалять связанные с этой категорией произведения (Title).
При удалении объекта жанра Genre не удалять связанные с этим жанром произведения (Title).
При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
База данных
В репозитории в директории /data подготовлены несколько файлов .csv с контентом для Users, Titles, Categories, Genres, Review и Comments.
```
### Технологии API YaMDb
```
Python 3.10
Django 2.2.19
Django REST Framework 3.12.4
Pillow 8.3.1
certifi 2021.10.8
cryptography 36.0.1
```
### Как запустить проект:
```
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/sat0304/api_yamdb.git
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Создать базу данных из CSV файлов, находящихся в папке STATIC
при помощи команды:
```
python3 manage.py csv_to_sqlite
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
