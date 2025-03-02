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

* Установите Docker согласно официальной инструкции (в зависимости от вашей операционной системы):
    https://docs.docker.com/engine/install/  

* Установите Docker Compose
    https://docs.docker.com/compose/install/linux/

* Создайте в корневой директории проекта файл .env - в нем укажите переменные среды согласно шаблону выше;

* Запустите приложение в фоновом режиме в контейнере: 
  ``` docker compose up -d --build ```
* Зайдите в контейнер:
  ``` docker exec -it <id контейнера> bash ```
* Выполните миграцию в контейнерах: 

  ``` python3 stripe_payment/manage.py makemigrations ```
  
  ``` python3 stripe_payment/manage.py migrate ```

* Создайте суперпользователя Django:

  ``` python3 manage.py createsuperuser ```
  
## Примеры запросов:
 - Получить список товаров в заказе (GET-запрос):
   ``` /api/order/{order_id}/ ```
 - Перейти на страницу оплаты выбранного заказа (GET-запрос):
  ``` /api/create-payment-intent/{order_id}/ ```

  
### Проект будет доступен по локальному IP: localhost:8000
