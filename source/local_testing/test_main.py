#fastapi tem um modulo chamado testclient uma dessas classes é o testclient onde podemos testar de modo simples nossa api
from fastapi.testclient import TestClient

#importando o arquivo da outra pasta (pasta source/query/main)
from source.query.main import app

#importando classe testclient do proprio fastapi e colocamos como parametro nossa aplicação
client = TestClient(app)

#cada funcao que quero que seja um teste inicia com 'test_.....'
# a unit test that tests the status code and response of the defined path
def test_get_path():
    #a partir de client faz a requisição get que tem essa rota items/42
    #chama o get que esta na outra pasta, ele roda essa função 
    r = client.get("/items/42")
    #retorna um objeto de retorno dessa função
    assert r.status_code == 200
    #retorna um json
    assert r.json() == {"fetch": "Fetched 1 of 42"}
    #se passar nas duas validações o teste ta ok

# a unit test that tests the status code and response of the defined query
def test_get_path_query():
    #verifica o mesmo codigo
    r = client.get("/items/42?count=5")
    assert r.status_code == 200
    assert r.json() == {"fetch": "Fetched 5 of 42"}

# a unit test that tests the status code
def test_get_malformed():
    #teste pra verificar se vai da erro
    r = client.get("/items")
    assert r.status_code != 200