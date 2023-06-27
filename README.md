# Vacancy-parser
Помогает анализировать зарплаты прогрраммистов на разных языках программирования.  
Результат будет выглядеть, как на скрине ниже:  

![](https://sun9-70.userapi.com/impg/YmQcI0OEA4OCzw8ixiRzkHSApSYxUhK_OLrlZQ/G4MFY-tnuBI.jpg?size=977x458&quality=96&sign=128d545e5641e4fce998df87bfa24562&type=album)  


## Установка
Python 3 уже должен быть установлен
1. Зайдите на сайт [api.superjob](https://api.superjob.ru/), зарегистрируйте ваше приложение и получите **Secret key**:  
   Выглядит он так: **v3.r.437641244.422959df1e8dc688bfefc5d288acee7ae0b291b1.f1568c454cebf7ec3ddf4014ebee1e2d9928cb32**
    
2. Клонируйте репозиторий с github - для этого выполните в консоли:  
`git clone https://github.com/oZerro/vacancy-parser.git`

3. Создайте виртуальное окружение.  
Для создания виртуального окружения:  
- Перейдите в директорию своего проекта.  
`cd vacancy-parser` 
- Выполните:  
`python -m venv venv`

4. Активируйте виртуальное окружение.  
Для активации виртуального окружения выполните:  
- `venv\Scripts\activate.bat` - для Windows;
- `source venv/bin/activate` - для Linux и MacOS.

5. Установите зависимости:  
 `pip install -r requirements.txt`  

6. Создайте файл **.env** в вашей деректории проекта.  

- `type nul > .env` - для Windows;
- `touch файл.txt` - для Linux и MacOS.

9. Откройте файл **.env** в любом текстовом редакторе и добавьте ваши токены - сохраните.  
Строка будет выглядеть так:  
`SUPERJOB_TOKEN='тут ваш токен SUPERJOB'`  


## Как запустить
Для запуска - из дериктории проекта выполните команду в консоли:  
`python main.py`  
После запуска нужно немного подождать.
