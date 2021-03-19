# Full Stack Trivia API

## Getting Started

- Base URL: The backend is hosted at the default, ```http://localhost:5000/```. And the front end at port 3000.
- Authentication: No authentication needed.

### Installing Dependencies (backend)

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup (optional)
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

### Installing Dependencies (frontend)

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```
npm install
```

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```.

## Error Handling

Errors are returned as JSON objects in the following format

```
{
	'success': False,
	'error': 400,
	'message': "bad request"
}
```

The api will return two error types when requests fail:

- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

## Endpoints

### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
```
{
	'1' : "Science",
	'2' : "Art",
	'3' : "Geography",
	'4' : "History",
	'5' : "Entertainment",
	'6' : "Sports"
}
```

### GET '/questions'

- Fetches a list of ten questions objects (json), according to the number of the desired page.
- Request Arguments: The number of the page (NOT mandatory)
- Returns: An object with four keys (questions, total_questions, current_category, categories).
```
{
	'questions': [
			{'id': 1, 'question': "What...", ....},
			{'id': 2, 'question': "What...", ....},
			...
		],
	'total_questions': 123, // total number of questions in the database
	'current_category': None,
	'categories': {'1': 'Science', '2': "Art", ...}
}
```

### DELETE '/questions/1'

- Deletes the question, that has id 1, from the database.
- Request Arguments: None
- Returns: An object with two keys (success & message).
```
{
	'success': True,
	'message': f"Question {question_id} has been deleted."
}
```

### POST '/questions'

- Inserts new question into the database.
- Request Arguments: Question and Answer texts, category id and difficulty level.
- Returns: An object with two keys (success & message)
```
{
	'success': True,
	'message': 'A new question has been added.'
}
```

### POST '/questions/search'

- Fetches all question that contains the searchTerm, in its text.
- Request Arguments: searchTerm value.
- Returns: An object with three keys (questions, total_questions and current_category)
```
{
	'questions': [
			{'id': 1, 'question': "What...", ....},
			{'id': 2, 'question': "What...", ....},
			...
		],
	'total_questions': 123, // total number of questions in the database
	'current_category': None,
}
```

### GET '/categories/1/questions'

- Fetches all question, that belongs to a specific category which has id 1.
- Request Arguments: None
- Returns: An object with three keys (questions, total_questions and current_category)
```
{
	'questions': [
			{'id': 1, 'question': "What...", ....},
			{'id': 2, 'question': "What...", ....},
			...
		],
	'total_questions': 123, // total number of questions in the database
	'current_category': {'id': 1, 'type': "Science"}
}
```

### POST '/quizzes'

- Fetches a random question from the database, within a specific category or not.
- Request Arguments: An category object with two keys (id & type), 
					 and list of the previous question.
- Returns: An object with a single key, question, that maps to an object the question info.
```
{
	'question': {
		'id': 1, 
		'question': "...", 
		'answer': "...", 
		'category': 1, 
		'difficulty': 1
	}
}
```

