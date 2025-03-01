# django-stripe
Бэкенд для создания платежных форм на Django + Stripe API. Позволяет получить страницу товара/списка товаров и, по нажатию кнопки Checkout, перейти на страницу оплаты.

### Шаблон наполнения env-файла:

``` SECRET_KEY='' # секретный ключ Django ```

``` STRIPE_PUBLIC_KEY='' # публичный ключ STRIPE API ``` 

``` STRIPE_SECRET_KEY='' # секретный ключ STRIPE API ``` 


### Стек технологий:
  Python==3.12, django==5.1.6, python-dotenv==1.0.1, stripe==11.6.0

### Установка:
* Клонируйте репозиторий:

  ``` git@github.com:Glaser1/Stripe_API_Backend.git ```
* Установите docker согласно официальной инструкции (в зависимости от вашей операционной системы):
    https://docs.docker.com/engine/install/    

* Создайте в корневой директории проекта файл .env - в нем укажите переменные среды согласно шаблону выше;

* Создайте Docker образ:
  ``` docker build -t django-stripe <путь до Dockerfile> ```

* Запустите приложение в фоновом режиме в контейнере: 
  ``` docker run --name <имя контейнера> -it -p 8000:8000 django-stripe ```
* Зайдите в контейнер:
  ``` docker exec it <id контейнера> bash ```
  
* Выполните миграцию в контейнерах: 

  ``` python3 manage.py makemigrations ```
  
  ``` python3 manage.py migrate ```

* Создайте суперпользователя Django:

  ``` python3 manage.py createsuperuser ```

* Заполните базу данных базу данных:
  ``` python3 manage.py loaddata fixtures.json ```
  
## Примеры запросов:
 - Перейти на страницу товара (GET-запрос):
   ``` /item/{item_id}/ ```
 - Перейти на страницу оплаты выбранного товара (GET-запрос):
   ``` /buy/{item_id}/ ```
 - Получить список товаров в заказе (GET-запрос):
   ``` /order/{order_id}/ ```
 - Перейти на страницу оплаты выбранного заказа (GET-запрос):
  ``` /order/pay/{order_id}/ ```
  
  
### Проект будет доступен по локальному IP: localhost:8000


