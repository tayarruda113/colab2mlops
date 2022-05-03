"""
Creator: Ivanovitch Silva
Date: 17 April 2022
Create API
"""
# from typing import Union
from pydantic import BaseModel #validar tipos de dados
from fastapi.responses import HTMLResponse #acessar o endereço da api e mostrar msg em html
from fastapi import FastAPI
import pandas as pd
import joblib 
import os
import wandb
import sys
#tem que trazer (importar) as classes do pipeline que geraram coisas personalizadas
from source.api.pipeline import FeatureSelector, CategoricalTransformer, NumericalTransformer

# global variables
#alem de importar tem que indicar de maneira estatica que todas essa classes sao modulos se não, não consegue executar
setattr(sys.modules["__main__"], "FeatureSelector", FeatureSelector)
setattr(sys.modules["__main__"], "CategoricalTransformer", CategoricalTransformer)
setattr(sys.modules["__main__"], "NumericalTransformer", NumericalTransformer)

# name of the model artifact
#acessando o modelo do wandb
#LEMBRAR DE FAZER O LOGIN NO TERMINAL
artifact_model_name = "decision_tree/model_export:latest"


# initiate the wandb project
#indicar de onde vem o modelo e executa (run) o experimento 
run = wandb.init(project="decision_tree",job_type="api")

# create the api
app = FastAPI()

#especificar o objeto para fazer as predições
# declare request example data using pydantic
# a person in our dataset has the following attributes
class Person(BaseModel):
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str

    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "workclass": 'Self-emp-inc',
                "fnlwgt": 473748,
                "education": 'Some-college',
                "education_num": 10,
                "marital_status": 'Married-civ-spouse',
                "occupation": 'Exec-managerial',
                "relationship": 'Husband',
                "race": 'White',
                "sex": 'Male',
                "capital_gain": 0,
                "capital_loss": 0,
                "hours_per_week": 25,
                "native_country": 'United-States'
            }
        }


#nossa API terá duas funções, um GET e um POST
        
# give a greeting using GET
#no GET iremos ter apenas uma mensagem
#sera exibida no path /
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <p><span style="font-size:28px"><strong>Hello World</strong></span></p>"""\
    """<p><span style="font-size:20px">In this project, we will apply the skills """\
        """acquired in the Deploying a Scalable ML Pipeline in Production course to develop """\
        """a classification model on publicly available"""\
        """<a href="http://archive.ics.uci.edu/ml/datasets/Adult"> Census Bureau data</a>.</span></p>"""

#predict é a função mais importante
#vamos passar uma pessoa com algumas configurações e vamos fazer a predição de quanto ela ganha
# run the model inference and use a Person data structure via POST to the API.
@app.post("/predict")
async def get_inference(person: Person):
    
    # Download inference artifact
    model_export_path = run.use_artifact(artifact_model_name).file()
    #fazendo o load do artefato do wandb
    pipe = joblib.load(model_export_path)
    
    # Create a dataframe from the input feature
    # note that we could use pd.DataFrame.from_dict
    # but due be only one instance, it would be necessary to
    # pass the Index.
    #chama a pessoa que passamos e criamos um dataframe com apenas uma linha que é a pessoa que queremos saber a predição
    #o pipeline ira fazer toda a transformação dos dados
    df = pd.DataFrame([person.dict()])

    # Predict test data
    #arvore de decisao ira fazer o predict
    #df ja tratado pelo pipeline
    predict = pipe.predict(df)

    return "low income <=50K" if predict[0] <= 0.5 else "high income >50K"