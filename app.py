from flask import Flask
from flask_restful import Resource, Api, request
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@auth.verify_password
def check(login, passwd):
    if not (login, passwd):
        return False
    return Usuarios.query.filter_by(login=login, senha=passwd).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não encontrado'
            }
        return response

    @auth.login_required
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {'status': 'sucesso', 'mensagem': 'Pessoa {} foi alterado!'.format(pessoa.nome)}
        return response

    @auth.login_required
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        return {'status': 'sucesso', 'mensagem': 'Pessoa Deletado!'}

class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade':i.idade} for i in pessoas]
        return response
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        return {'id': pessoa.id, 'nome': pessoa.nome, 'idade': pessoa.idade}

class Atividade(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        print(pessoa)
        atividades = Atividades.query.filter_by(pessoa_id=pessoa['id'])
        print(atividades)
class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'pessoa': a.pessoa.nome, 'nome':a.nome, 'id': a.id} for a in atividades]
        return response
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.status = 'Pendente'
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id': atividade.id
        }
        return response

api.add_resource(Pessoa, '/pessoa/<nome>')
api.add_resource(ListaPessoas, '/pessoas')
api.add_resource(Atividade, '/atividades/<nome>')
api.add_resource(ListaAtividades, '/atividades')

if __name__ == '__main__':
    app.run(debug=True)