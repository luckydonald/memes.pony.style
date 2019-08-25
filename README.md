# memes.pony.style
memes.pony.style is a simple image sharing web-application. It contains a 
backend with rest api interface and a javascript frontend. Developed for fun
and learning. Revived for ponies and memes.

Used to power https://mylittlefacewhen.com/, will now power https://memes.pony.style

## Technologies
List of most important packages that are used.

- django
- django-tastypie
- pystache
- PIL

- backbone.js
- mustache.js
- jQuery
- CoffeeScript
- sass

- Much digital duct-tape

## Requirements

### Backend
See [requirements.txt](requirements.txt)

### Frontend

- CoffeeScript - http://coffeescript.org/
- sass - http://sass-lang.com/

## Contents

/scripts/
            Contains some script that have been used during development or
            for maintanence. Some aren't too relevant but are stored as a
            reference if their functionality is needed in the future.

/static/    
            Contains frontend stuff. JS, CSS, some images, JS-templates and so on.

/viewer/    
            Main application. REST API interface.

/templates/ 
            Django templates.

/resizor/   
            Generates thumbnails. Can be used as a standalone service with
            small modifications.
