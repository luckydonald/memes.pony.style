# create user
`memes_pony_style`

```postgresql
DROP USER IF EXISTS memes_pony_style;
CREATE USER memes_pony_style WITH PASSWORD '<password>';
CREATE DATABASE memes_pony_style;
GRANT ALL ON DATABASE memes_pony_style TO memes_pony_style;
```

# create migration files
```bash
python manage.py makemigrations
python manage.py makemigrations viewer
```

# apply migration files
```bash
python manage.py migrate
```
