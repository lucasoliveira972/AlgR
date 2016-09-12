import sqlite3

HELP_TEXT = """
--- SINTAXE ---

--- SELECAO ---
Para realizar uma selecao utilize o operador SIG antes da expressao.
Por exemplo: SIG idade > 10 (Usuarios)
Para efetuar uma selecao com dois ou mais condicoes, utilize o operador AND
entre as condicoes.
Por exemplo: SIG idade > 10 AND nome = "Joao" (Usuarios)

--- PROJECAO ---
Para realizar uma projecao utilize o operador PI antes da expressao.
Por exemplo: PI idade (Usuarios)
Para efetuar uma projecao a partir do resultado de uma selecao, utilize o
operador SIG (Ver acima) como relacao.
OBS: A selecao deve ser efetuada anteriormente.
Exemplo: SIG idade > 10 (Usuarios)
         PI nome (SIG)

--- PRODUTO CARTESIANO ---
Tambem e possivel realizar expressoes com a relacao entre tuplas de duas
ou mais tabelas.
Para efetuar operacoes com produto cartesiano, utilize * entre as tabelas
na relacao.
Exemplo - Produto cartesiano numa projecao:
PI Usuarios.nome, Produtos.nome (Usuarios * Produtos)
Exemplo - Produto cartesiano numa selecao:
SIG Usuarios.idade > 10 AND Produtos.preco < 100 (Usuarios * Produtos)

--- BASE DE DADOS ---
Por padrao o script utiliza a base de dados 'registros.db', caso queira
utilizar outra base de dados, faça uso do comando 'db_set' seguido do 
caminho para a base de dados.
Exemplo: db_set C:\db1.db

AVISO: No momento o script só suporta SQLITE3.
"""


def run_query(query):
	try:
		r = c.execute(query)
		columns = [desc[0] for desc in c.description]
		print(' | '.join(columns))
		print('-----------------------------')
		for row in r:
			print(' | '.join([str(elem) for elem in row]))
			print('-----------------------------')
	except sqlite3.OperationalError as e:
		print('Error: ' + str(e))


def parse_sel(exp):
	global cond_sel
	global rel_sel

	cond_sel = exp[exp.find(' ') + 1 : exp.rfind('(')]
	rel_sel = exp[exp.rfind('(') + 1 : exp.find(')')]
	if (rel_sel.find('*') != -1):
		rel_sel = rel_sel.replace(' ', '').replace('*', ',')
	print('Condicao de selecao: ' + cond_sel)
	print('Relacao: ' + rel_sel)
	query = 'SELECT * FROM {} WHERE {}'.format(rel_sel, cond_sel)
	print('Query SQL: ' + query + '\n')
	run_query(query)


def parse_proj(exp):
	attr = exp[exp.find(' ') + 1 : exp.rfind('(')]
	rel = exp[exp.rfind('(') + 1 : exp.find(')')]

	if (rel.find('*') != -1):
		rel = rel.replace(' ', '').replace('*', ',')
	elif (rel.split(' ')[0] == "SIG"): #TODO - Aceitar e executar expressoes de selecao na relacao
		if ('cond_sel' and 'rel_sel' in globals()):
			print('Projecao de uma selecao')
			print('Atributos: ' + attr)
			print('Relacao: ' + rel_sel)
			query = 'SELECT {} FROM {} WHERE {}'.format(attr, rel_sel, cond_sel)
			print ('Query SQL: ' + query + '\n')
			run_query(query)
		else:
			print('Nao foi possivel executar a operacao')
		return		
	print('Atributos: ' + attr)
	print('Relacao: ' + rel)
	query = 'SELECT {} FROM {}'.format(attr, rel)
	print('Query SQL: ' + query + '\n')
	run_query(query)


def show_help():
	print(HELP_TEXT)


def set_database(path):
	global c
	global conn
	conn = sqlite3.connect(path)
	c = conn.cursor()


def main():
	set_database('registros.db')

	while True:
		s = input('> ')
		op = s.split(' ')[0]

		if op in ('SIG', 'sig', 'σ'):
			parse_sel(s)
		elif op in ('PI', 'pi', 'π'):
			parse_proj(s)
		elif op in ('h', 'help', 'ajuda'):
			show_help()
		elif op in ('db_set', 'database_set'):
			# Talvez devesse fechar a conexão antiga?
			set_database(s.split(' ')[1])
		else:
			print('Comando nao existente. Digite \'help\' para ver a lista de comandos.')


if __name__ == '__main__':
	main()
