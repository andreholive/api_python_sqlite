from models import Pessoas, db_session

def insere_pessoa():
    pessoa = Pessoas(nome='Daniela', idade='41')
    pessoa.save()

def consulta():
    resultado = Pessoas.query.all()
    for p in resultado:
        print(p)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Daniela').first()
    pessoa.idade = 21
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Andre').first()
    pessoa.delete()

if __name__ == '__main__':
    #insere_pessoa()
    #exclui_pessoa()
    consulta()