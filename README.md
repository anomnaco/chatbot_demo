## Quickstart in Gitpod

You can either follow the directions below or [open this in gitpod](https://gitpod.io/#https://github.com/Anant/astra-chatbot-react-python).

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Anant/astra-chatbot-react-python)

## Quick deploy to Vercel

You can clone & deploy it to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Anant/astra-chatbot-react-python)

# Setup

To install backend deps run the following command

```
cd backend
pip install -r requirements.txt

```

To install frontend deps run the following command

```
cd frontend
npm install
```

# Start Servers

To start the backend server, in a terminal tab run the following

```
cd backend
uvicorn main:app --reload
```

To start the frontend in a new terminal run the following

```
cd frontend
npm run dev
```
