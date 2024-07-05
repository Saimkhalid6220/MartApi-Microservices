from fastapi import FastAPI

app = FastAPI()

@app.post('/user/create')
def create_user(username:str , password: str):
    return {'message': 'User created successfully'}