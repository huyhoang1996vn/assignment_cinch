## Web+Database Topic 2: Infinite Hierarchical Comments

## Difficulty

Intermediate

## Thoughts

Create a simple website that implements a potentially challenging feature. This project should employ a database and include user registration and login functionality. It should separate frontend and backend implementations, using Python to provide a RESTful API. Candidates should demonstrate their understanding of object-oriented programming and can utilize any popular frontend frameworks.

## Note

This practical exercise is primarily focused on backend development. While a frontend page must be created, its design is less critical as long as it functions properly.


## Exercise Content

Develop a "Tree-shaped Comments" website using Python and a database. The challenge of the "infinite hierarchy" requires experience in database design, ORM/SQL queries, and data display. The candidate should showcase fundamental skills in user registration/login functionality, including password handling, field validation, and browser session/cookie management. The Python backend should provide a RESTful API, and the frontend can use various frameworks (e.g., jQuery, React, Vue, Angular, etc.).

## Functional Requirements

- Users can register on the website
    - Required fields: username, password, email.
    - Username checks: cannot be empty; must consist of letters and numbers; length should be between 5 and 20 characters; must not duplicate existing usernames.
    - Password checks: cannot be empty; length should be between 8 and 20 characters; must contain at least one uppercase letter, one lowercase letter, one number, and one special character.
    - Email checks: cannot be empty; must be in the correct format; must not duplicate existing emails. For simplicity, email confirmation is not required.

- Users can login to the website
    - Login with either username + password or email + password.
    - Provide a “remember me” function, allowing the user to remain logged in for one month.
    - If “remember me” is not selected, revisiting the site after closing the browser will prompt for registration or login.
    - Upon login, the username and email should be displayed at the top of the page.

- Users can post comments after login:
    - Comment length should be between 3 and 200 characters and can support Unicode characters for internationalization.
    - While typing, there should be a dynamic prompt indicating how many more characters can be entered.
    - The time of the comment should be recorded.

- Users can comment on a specific comment:
    - The requirements for replying comment should be the same as comment.
    - Users can comment on any comment, without any limit on nesting level.

- Users can view comments:
    - A single page should display all comments and the nested structure of replies (no lazy loading).
    - Comments should be arranged in reverse chronological order, with the most recent at the top.
    - Next to each comment, the username of the poster and the time of posting should be visible.
    - Viewing comments does not require login.

## Technical Requirements

- Provide a command for website initialization and startup, which opens the homepage automatically in a browser.
- Recommended Python framework: Flask.
- Use a database (either relational or NoSQL), create necessary tables, and utilize SQL/NoSQL/ORM appropriately. SQLite is preferred for ease of review since it requires no installation.
- Passwords must be stored in a non-plaintext form with irreversible encryption.
- Database queries can use either ORM or raw SQL.
- The backend's RESTful API must consider permission checks along with proper HTTP methods and HTTP response codes.
- Performance for deeply nested comments (exceeding 50 levels) should not present noticeable issues, ensuring acceptable response times.
- Appropriate unit testing should be included.

## How to Clone and Submit Code

1. Clone the repository directly using SSH.
    1. Forking is not supported; please clone directly.
    2. Use the `git` protocol for cloning; avoid HTTPS URLs.
    3. Cloning requires SSH keys; username/password authentication is not supported.
2. Create a new branch locally and develop on that branch.
3. Push the branch and create a pull request (PR).



# FastAPI Project

### Create Virtual
```sh
virtualenv -p python3 env
source env/bin/activate
```

### Install requirements
```sh
sudo apt install python3-pip
pip3 install -r requirements.txt 
```

### Migrations
```sh
alembic init alembic
alembic revision --autogenerate -m "Added initial tables"
alembic upgrade head
```

### Run app (DEV)
```sh
uvicorn main:app --reload
fastapi dev main.py
```

### Docs Api
http://localhost:8000/docs
http://localhost:8000/redoc




- Migarte
alembic revision -m "first migrations"
alembic upgrade head
alembic downgrade base
https://arunanshub.hashnode.dev/using-sqlmodel-with-alembic

- Create all tables
- Api
- Users if needed
- Test the application
- Deploy
- Monitor application performance and logs
- Update documentation as necessary
- Push code in git
