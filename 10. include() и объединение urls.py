Пришло время навести порядок и структурировать наш проект.
Всё, что касается статей, должно храниться и работать в приложении Articles App, 
а всё, что касается аккаунтов — в Accounts App. Так и с templates, и с views, и с URL Mapping.



Такая структура позволяет разрабатывать проекты по частям и повторно использовать готовые приложения: 
копируете директорию приложения в другой проект, подключаете — и оно работает.
В предыдущих уроках мы разместили urls.py в дефолтной директории проекта. 
Это было сделано, чтобы объяснить механизм работы URL Mapping на простом примере.
Но для разделения проекта на приложения нужно создать два разных файла urls.py: один для Articles App, другой — для Accounts App.
Адреса вида articles/... будут обрабатываться в файле articles/urls.py, а адреса вида accounts/... — в accounts/urls.py
В Django есть механизм, который позволяет ссылаться на другие файлы urls.py. 
Именно это будет делать головной файл urls.py нашего проекта.



Список доступных путей в urls.py должен называться urlpatterns — переменную именно с таким названием будет искать 
Django после получения входящего запроса.
Чтобы сослаться на другой urlpatterns, следует вместо имени view-функции в path() указать название того urls.py, 
где содержится функция.
Например, чтобы из головного urls.py сослаться на urlpatterns в файле articles/urls.py, 
вместо имени функции в path() пишут include('articles.urls').
# это код головного urls.py
from django.urls import path

urlpatterns = [
    path('articles/', include('articles.urls'))  # ссылаемся на articles/urls.py
    # все адреса, начинающиеся с 'articles/' обрабатываются в файле articles/urls.py 
]

Когда мы из головного urls.py ссылаемся на какой-то другой и пишем path('anything/page', include('other.urls')) — Django удаляет из запрошенного адреса часть anything/ и в файле other/urls.py проводит поиск без учёта этой части адреса, то есть просто по адресу page.
Например, запрошен URL articles/dashboard:

Этот URL передаётся в головной urls.py. 
Django видит в адресе строку articles/ и перенаправляет запрос в articles/urls.py, по дороге отрезав от URL часть articles/. В articles/urls.py Django ищет только строку dashboard.

# головной urls.py
# сюда передан URL "articles/dashboard"
from django.urls import path

urlpatterns = [
    path('articles/', include('articles.urls')) 
    # Django идёт искать подходящий шаблон в файл articles/urls.py 
    # но искать там будет без учёта части адреса 'articles/'
]

# urls.py в директории articles
# сюда передан "обрезанный" URL: 'dashboard'
from . import views
from django.urls import path

urlpatterns = [
    path('<int:id>', views.article_by_id),
    path('tag/<str:tag>', views.articles_by_tag),
    path('dashboard', views.dashboard)  # ура, нашёлся!    
]

А если пользователь запросил URL /articles/73374954, то в файле articles/urls.py будет проведён поиск строки '73374954'.
