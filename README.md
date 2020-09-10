# Unu - API

**unu-api** is a REST Full API to manage the backend operations 
for Unu app (A web application to create events, work collaboratively 
with your team and expose your event to the whole world through the 
app's auto-generated landig page).

> You can see the demo here: [https://unu.vercel.app](https://unu.vercel.app)

## Documentation
Also, you can see the API Documentation here:
(This version actually run in a test server. Then the ip adress si raw and it doesn't have a configured domain)

- Swagger docs: http://34.68.103.23/docs
- OpenApi docs: http://34.68.103.23/redoc


# Installation
Clone this repository:

```bash
git clone https://github.com/emanuelosva/unu-api.git
```

## Setup workspace
If you want to use this project as a base of your project, first you can make some configurations
to work correctly and according with our style code guide.

#### Create a virtual enviroment and install all dependencies
Run in the root directory:

```bash
python3 -m venv .env
source .env/bin/activate
pip3 install -r app/requirements.txt
pip3 install -r app/requirements.dev.txt
```

This step enable the correct function of the linter and preconfigured style code guides.

#### Set the enviroment variables
Go to the file named `app/.env.example` and rename it to `app/.env`
After that fill all required env variables.
This step is totally needed.


#### Run the application
If you want to initialize the uvicorn server for development run in the root directory:

```bash
source scripts/dev.sh
```

If you made any change in the Dockerfile or in the requirements you must rebuild the image to install all packages in the container and then:

```bash
source scripts/dev.sh
```

If you add test in the dorectory app/test, you can run your test and generate a coverage output with:

```bash
source scripts/test.sh
```

To deploy in a production server run:

```bash
sudo source scripts/start.sh
```


## Contributors

- [Emanuel Osorio](https://github.com/emanuelosva)

- [Mario barbosa](https://github.com/mariobarbosa777)