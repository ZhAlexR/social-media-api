# Social Media Network API
Social Media API **easy-to-use** backend solution for building social media applications. 
This repository contains a fully functional RESTful API built using DRF and SQLite, 
providing developers with a scalable and efficient way to manage user authentication, profiles, posts, comments, and more. 
With a comprehensive set of endpoints and robust data modeling, this API is ideal for building social media 
applications that can handle high levels of traffic and user engagement. 

# API features

- User Authentication: The API supports user authentication with JWT (JSON Web Token) authentication, 
which allows for secure access to user data and resources.

- User Profiles: The API allows users to create and manage their profiles, 
including their personal information, profile picture, and bio.

- Posts and Comments: Users can create, edit, and delete posts, 
as well as add comments to posts. 
The API provides endpoints to retrieve, update, and delete posts and comments.
- Follow/Unfollow: Users can follow and unfollow other users on the platform, 
and the API provides endpoints to retrieve a user's followers and followers.
- Search: The API allows users to search for other users and posts using keywords.
- Analytics: The API provides analytics for user activities, such as the number 
of likes and comments on posts, as well as user engagement.

# Installation via GitHub

```shell
git clone git@github.com:ZhAlexR/social-media-api.git
cd Cinema-api
python3 -m venv venv
source venv/bin/activete # for linux or macOS
venv\Scripts\activete # for Windows
```

Perform the next commands to create migrations for your DB:
```shell
python manage.py makemigration
python manage.py migrate
```

Start your server using:
```shell
python manage.py runserver
```

# <p style="text-align: center;">Enjoy your Social Media Network API!</p>

<div align="center">
    <img src="https://media.giphy.com/media/t3sZxY5zS5B0z5zMIz/giphy-downsized-large.gif" alt="">
</div>

