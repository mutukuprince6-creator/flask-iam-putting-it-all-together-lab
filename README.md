# Lab: Putting it All Together - IAM Flask API

## Introduction

This lab is on the longer side, so make sure to set aside some time
for this one. It's set up with a few different checkpoints so that you can build
out the features incrementally. By the end of this lab, you'll have built out
full authentication and authorization flow using sessions and cookies in Flask,
so getting this lab under your belt will give you some good code to reference
when you're building your next project with _auth_. Let's get started!

## Completed Application

This project now includes a Flask REST API and React client for a session-based
recipe application. Users can create accounts, sign in, stay signed in across
page refreshes, sign out, browse recipes, and create recipes belonging to their
account. Passwords are stored as bcrypt hashes and are never serialized in API
responses.

### API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/signup` | Create a user and start a session |
| `GET` | `/check_session` | Return the current session user |
| `POST` | `/login` | Authenticate a user and start a session |
| `DELETE` | `/logout` | End the current session |
| `GET` | `/recipes` | List recipes for authenticated users |
| `POST` | `/recipes` | Create a recipe for the authenticated user |

Authenticated failures return `401`, invalid user or recipe data returns `422`,
and validation errors are returned in an `errors` array for the React forms.

### Verification

Run these commands from `server/`:

```bash
pytest
python seed.py
```

The completed backend currently passes all 19 tests.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-iam-putting-it-all-together-lab)
- [API - Flask: `class flask.session`](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session)
- [User's Guide - Flask RESTful](https://flask-restful.readthedocs.io/en/latest/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/)

## Set Up

As with other labs in this section, there is some starter code in place for a
Flask API backend and a React frontend. To get set up, run:

```bash
pipenv install && pipenv shell
npm install --prefix client
cd server
```

You can work on this lab by running the tests with `pytest`. It will also be
helpful to see what's happening during the request/response cycle by running the
app in the browser. You can run the Flask server with:

```bash
python app.py
```

Note that running `python app.py` will generate an error if you haven't created
your models and run your migrations yet.

And you can run React in another terminal from the project root directory with:

```bash
npm start --prefix client
```

## Instructions

### Task 1: Define the Problem

Our application is currently very bare. We'll need to build out models
and endpoints to allow our frontend Recipe application to log in users,
create recipes, and view recipes.

### Task 2: Determine the Design

#### Models

The `User` model will have the following attributes:

- `id` that is an integer type and a primary key.
- `username` that is a `String` type.
- `_password_hash` that is a `String` type.
- `image_url` that is a `String` type.
- `bio` that is a `String` type.

The `User` model should also:

- incorporate `bcrypt` to create a secure password. Attempts to access the
  `password_hash` should be met with an `AttributeError`.
- constrain the user's username to be **present** and **unique** (no two users
  can have the same username).
- **have many** recipes.

The `Recipe` model will have the following attributes:

- a recipe **belongs to** a user.
- `id` that is an integer type and a primary key.
- `title` that is a `String` type.
- `instructions` that is a `String` type.
- `minutes_to_complete` that is an `Integer` type.

Your `Recipe` model should also:

- constrain the `title` to be present.
- constrain the `instructions` to be present and at least 50 characters long, 
alternately you may use a custom validation.

#### Routes

The `POST /signup` route should:

- Be handled in a `Signup` resource with a `post()` method.
- In the `post()` method, if the user is valid:
  - Save a new user to the database with their username, encrypted password,
    image URL, and bio.
  - Save the user's ID in the session object as `user_id`.
  - Return a JSON response with the user's ID, username, image URL, and bio; and
    an HTTP status code of 201 (Created).
- If the user is not valid:
  - Return a JSON response with the error message, and an HTTP status code of
    422 (Unprocessable Entity).

Handle auto-login by implementing a `GET /check_session` route. It should:

- Be handled in a `CheckSession` resource with a `get()` method.
- In the `get()` method, if the user is logged in (if their `user_id` is in the
  session object):
  - Return a JSON response with the user's ID, username, image URL, and bio; and
    an HTTP status code of 200 (Success).
- If the user is **not** logged in when they make the request:
  - Return a JSON response with an error message, and a status of 401
    (Unauthorized).

Handle login by implementing a `POST /login` route. It should:

- Be handled in a `Login` resource with a `post()` method.
- In the `post()` method, if the user's username and password are authenticated:
  - Save the user's ID in the session object.
  - Return a JSON response with the user's ID, username, image URL, and bio.
- If the user's username and password are not authenticated:
  - Return a JSON response with an error message, and a status of 401
    (Unauthorized).

Handle logout by implementing a `DELETE /logout` route. It should:

- Be handled in a `Logout` resource with a `delete()` method.
- In the `delete()` method, if the user is logged in (if their `user_id` is in
  the session object):
  - Remove the user's ID from the session object.
  - Return an empty response with an HTTP status code of 204 (No Content).
- If the user is **not** logged in when they make the request:
  - Return a JSON response with an error message, and a status of 401
    (Unauthorized).

Handle recipe viewing by implementing a `GET /recipes` route. It should:

- Be handled in a `RecipeIndex` resource with a `get()` method
- In the `get()` method, if the user is logged in (if their `user_id` is in the
  session object):
  - Return a JSON response with an array of all recipes with their title,
    instructions, and minutes to complete data along with a nested user object;
    and an HTTP status code of 200 (Success).
- If the user is **not** logged in when they make the request:
  - Return a JSON response with an error message, and a status of 401
    (Unauthorized).

Handle recipe creation by implementing a `POST /recipes` route. It should:

- Be handled in the `RecipeIndex` resource with a `post()` method.
- In the `post()` method, if the user is logged in (if their `user_id` is in the
  session object):
  - Save a new recipe to the database if it is valid. The recipe should **belong
    to** the logged in user, and should have title, instructions, and minutes to
    complete data provided from the request JSON.
  - Return a JSON response with the title, instructions, and minutes to complete
    data along with a nested user object; and an HTTP status code of 201
    (Created).
- If the user is **not** logged in when they make the request:
  - Return a JSON response with an error message, and a status of 401
    (Unauthorized).
- If the recipe is **not valid**:
  - Return a JSON response with the error messages, and an HTTP status code of
    422 (Unprocessable Entity).

> **Note: Recall that we need to format our error messages in a way that makes
> it easy to display the information in our frontend. For this lab, because we
> are setting up multiple validations on our `User` and `Recipe` models, our
> error responses need to be formatted in a way that accommodates multiple
> errors.**

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Build the Models

Build the User and Recipe models with the required db columns.

#### Step 2: Add Validations and Serialization to Models

Add validations and constraints for both models.

Implement serialization schemas for both models.

#### Step 3: Migrate and Update the Database

Run the migrations after creating your models. You'll need to run
`flask db init` before running `flask db migrate -m "initial migration"` and
`flask db upgrade head`. Be sure to run these commands from the `server/`
directory, not the root directory, so the migrations directory is nested as 
`server/migrations/`.

#### Step 4: Verify your Code and Seed the Database

Ensure that the tests for the models are passing before moving forward. To run
the tests for _only_ the model files, run:

```bash
pytest testing/models_testing/
```

Once your tests are passing, you can seed your database from within the `server`
directory by running:

```bash
python seed.py
```

#### Step 5: Sign Up Feature

After creating the models, the next step is building out a sign up feature.

#### Step 6: Auto-Login Feature

Create the /check_session route.

Make sure the signup and auto-login features work as intended before moving
forward. You can test the `CheckSession` requests with pytest:

```console
$ pytest testing/app_testing/app_test.py::TestCheckSession
```

You should also be able to test this in the React application by signing up via
the sign up form to check the `POST /signup` route; and refreshing the page
after logging in, and seeing that you are still logged in to test the
`GET /check_session` route.

#### Step 7: Login Feature

Build out the /login route.

Make sure this route works as intended by running
`pytest testing/app_testing/app_test.py::TestLogin` before moving forward. You
should also be able to test this in the React application by logging in via the
login form.

#### Step 8: Logout Feature

Build the /logout route.

Make sure the login and logout features work as intended before moving forward.
You can test the `Logout` requests with pytest:

```console
$ pytest testing/app_testing/app_test.py::TestLogout
```

You should also be able to test this in the React application by logging in to
check the `POST /login` route; and logging out with the logout button to test
the `DELETE /logout` route.

#### Step 9: Recipe List Feature

Build out the GET /recipes route.

#### Step 10: Recipe Creation Feature

Build out the POST /recipes route.

#### Step 11: Verify and Refine your Code

After finishing the `RecipeIndex` resource, you're done! Make sure to check your
work. You should be able to run the full test suite now with `pytest`.

You should also be able to test this in the React application by creating a new
recipe with the recipe form, and viewing a list of recipes.

#### Step 12: Commit and Push Git History

* Commit and push your code:

```bash
git add .
git commit -m "final solution"
git push
```

* If you created a separate feature branch, remember to open a PR on main and merge.

### Task 4: Document and Maintain

Optional Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Submit your solution

CodeGrade will use the same test suite as the test suite included.

Once all tests are passing, commit and push your work using `git` to submit to CodeGrade through Canvas.
