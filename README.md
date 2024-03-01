
# Introduction

**minDB** is a hobby project for various use cases including a database for keeping a record of our chat messages across discord channels.

It is a simple key-value store, which can be called via [FastAPI](https://fastapi.tiangolo.com/).

The functionalities:

1. Create a database
2. List databases
3. Delete a database
4. Populate a database
5. Retrieve database contents

## How to use

For now, simply go to the root of the directory and run the following command:

```bash
python -m uvicorn minDB.main:app --reload
```

Then go to localhost:8000/docs to see the API documentation.
