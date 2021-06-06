# Description of the project
### Technology stack
- Python, Django, DjangoRestFramework.
- PostgreSQL.
- Nginx, Gunicorn.
---------
# Cloning & Run:
- sudo apt-get update
- sudo apt-get upgrade 
- PACKAGES=“python3.8 python3-pip python3-venv postgresql-12”
- sudo apt-get -y –force-yes install $PACKAGES 

### Get the code
- git clone https://github.com/lsujh/photo_gallery_docker.git

### Docker build
- cd photo_gallery_docker
- docker-compose up -d --build
- Access the web app in browser: http://0.0.0.0:8000/

### Virtualenv modules installation (Unix based systems)
- cd photo_gallery_docker/photo_gallery
- python -m venv venv
- source venv/bin/activate

### Install modules
- pip install -r requirements.txt
- Edit file .env with settings database

### Create tables
- python3 manage.py migrate

### Start the application (development mode)
- python manage.py runserver # default port 8000

### Start the app - custom port
- python manage.py runserver 0.0.0.0:<your_port>

### Access the web app in browser: http://127.0.0.1:8000/
### Admin login
- email admin@admin.com
- password admin

### API
/admin/ - site Admin

/swagger/ - swagger

/api/signup/ - registration 

/api-auth/login/ - login

/api-auth/logout/ - logout

/api/albums/ - list albums, create album 

/api/album/{album_id}/ - one album (view, update, delete)

/api/photos/ - list photos, create photo

/api/photo/{photo_id}/ - one photo (view, update, delete)

/api/user/{user_id}/photos/ - user photos list

/api/user/{user_id}/albums/ - user albums list

/api/user/{user_id}/bookmarks/ - user bookmarks list
   
/api/photo/{photo_id}/comments/ - photo comments (list, create)

/api/photos/comment/delete/{comment_id/ - comment delete

/api/bookmark/{photo_id}/ - bookmark create

/api/bookmarks/ - bookmarks list

/api/bookmark/delete/{bookmark_id/ - bookmark delete

/api/feed/ - list photos by rating

/api/user/me/ - detail for me

/api/user/{user_id}/ - user detail
