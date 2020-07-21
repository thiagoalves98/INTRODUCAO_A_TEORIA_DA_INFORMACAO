from sys import argv
from struct import *
import sys
import os
import time

#
def Decodificador(input_Arq, n, name_out):

	#Define o tamanho da tabela
	Tam_tab = pow(2,int(n))

	#Abre o aquivo 
	Arq = open(input_Arq, "rb")

	#Cria as variáveis
	Dados_cod = []
	Prox_cod = 256
	Dados_decod = ""
	string = ""

	#Lê o arquivo
	while True:
		rec = Arq.read(2)

		if len(rec) != 2:
			break

		(Dados, ) = unpack('>H', rec)
		Dados_cod.append(Dados)

	#Inicializa o dicionario
	Tam_dict = 256
	Dicionario = dict([(x, chr(x)) for x in range(Tam_dict)])

	print(Dados_cod, type(Dados_cod), Dados_cod[0], type(Dados_cod[0]))

	#Percorre o arquivo
	for code in Dados_cod:

		if not (code in Dicionario):
			Dicionario[code] = string + (string[0])

		Dados_decod += Dicionario[code]

		if not(len(string) == 0):
			Dicionario[Prox_cod] = string + (Dicionario[code][0])
			Prox_cod += 1

		string = Dicionario[code]

	print(Dados_decod, type(Dados_decod), Dados_decod[0], type(Dados_decod[0]))

	#Gera o arquivo de saída
	output_Arq = open(name_out, 'w')

	#Salva o arquivo
	for Dados in Dados_decod:
	    output_Arq.write(Dados)
	    
	#Fecha os arquivos
	output_Arq.close()
	Arq.close()

	return Dados_decod

#Codificador com leitura binaria
def Codificador_bin(input_Arq, n, name_out):

	#Define o tamanho da tabela
	Tam_tab = pow(2,int(n)) 

	#Abre o aquivo     
	Dados = open(input_Arq, 'rb').read()

	#Inicializa o dicionario
	Tam_dict = 256
	Dicionario = {chr(i): i for i in range(Tam_dict)}
	string = ""
	Dados_cod = []

	#Percorre o arquivo
	for c in Dados:

		#Gambiarra!
		if chr(c) == '\r':
			continue
		
		novo_c = string + chr(c)

		if novo_c in Dicionario:
			string = novo_c

		else:
			Dados_cod.append(Dicionario[string])

			if(len(Dicionario) <= Tam_tab):
				Dicionario[novo_c] = Tam_dict
				Tam_dict += 1

			string = chr(c)

	if string in Dicionario:

		Dados_cod.append(Dicionario[string])

	#Gera o arquivo de saída
	output_Arq = open(name_out, "wb")

	#Salva o arquivo em modo binário
	for Dados in Dados_cod:

		output_Arq.write(pack('>H',Dados))

	#Fecha os arquivos
	output_Arq.close()

	return Dados_cod

#Codificador com leitura comum
def Codificador_chr(input_Arq, n, name_out):

	#Define o tamanho da tabela
	Tam_tab = pow(2,int(n)) 

	#Abre o aquivo     
	Arq = open(input_Arq)     
	Dados = Arq.read()

	#Inicializa o dicionario
	Tam_dict = 256
	Dicionario = {chr(i): i for i in range(Tam_dict)}
	string = ""
	Dados_cod = []

	#Percorre o arquivo
	for c in Dados:
		
		novo_c = string + c

		if novo_c in Dicionario:
			string = novo_c

		else:
			Dados_cod.append(Dicionario[string])

			if(len(Dicionario) <= Tam_tab):
				Dicionario[novo_c] = Tam_dict
				Tam_dict += 1

			string = c

	if string in Dicionario:
		Dados_cod.append(Dicionario[string])

	#Gera o arquivo de saída
	output_Arq = open(name_out, "wb")

	#Salva o arquivo em modo binário
	for Dados in Dados_cod:
		output_Arq.write(pack('>H',int(Dados)))

	#Fecha os arquivos
	output_Arq.close()
	Arq.close()

	return Dados_cod

#
def main():

	#arq = "corpus16MB.txt"
	#arq = "Trecho.txt" 
	arq = "mapa.mp4"
	Script = open("script.txt", "w")
	n = 9

	while(n <= 16):
		print("n= ",n)
		out_ = "Sem_reset_codificado_k="+str(n)+".txt"
		inicio = time.time()
		SaidaBin = Codificador_bin(arq, n, out_)
		fim = time.time()
		Script.write("Tempo de codificação para n = "+str(n)+": "+str(fim - inicio)+"\n")

		n = n+1

	#DecodBin = Decodificador("Sem_reset_Codificado.txt", n, "Sem_reset_Decodificado.txt")

	'''
	while(n <= 16):

		print("Iniciando para n =", n)

		inicio = time.time()

		nome_cod = 'CodBin_k='+str(n)+'.txt'

		SaidaBin = Codificador_bin(arq, n, nome_cod)

		fim = time.time()

		print("Tempo de codificação para n = ",n,": ", fim - inicio)

		Script.write("Tempo de codificação para n = "+str(n)+": "+str(fim - inicio))

		print("Decodificando...")	##################

		inicio = time.time()

		nome_decod = 'DecodBin_k='+str(n)+'.txt'

		DecodBin = Decodificador(nome_cod, n, nome_decod)

		fim = time.time()

		print("Tempo de decodificação para n = ",n,": ", fim - inicio)

		Script.write("Tempo de codificação para n = "+str(n)+": "+str(fim - inicio))

		n = n+1

	'''
	#Script.close()

	###Testes
	'''
	################### Compara as codificações das duas leituras

	SaidaBin = Codificador_bin(arq, n, "SaidaBin.txt")
	SaidaChr = Codificador_chr(arq, n, "SaidaChr.txt")

	if SaidaBin == SaidaChr:
		print("Ok!\n")
	else:
		print("As codificações Chr-Bin não bateram\n")
	
	################### Compara as saidas das duas leituras

	DecodBin = Decodificador("SaidaBin.txt", n, "DecodBin.txt")
	DecodChr = Decodificador("SaidaChr.txt", n, "DecodChr.txt")

	if DecodBin == DecodChr:
		print("Ok!\n")
	else:
		print("As decodificações Chr-Bin não bateram\n")

	################### Compara os dados que foram salvos com o arquivo original
 
	Arquivo = open(arq)     
	Dados = Arquivo.read()

	if Dados == DecodBin:
		print("Decodificação binaria ok\n")
	else:
		print("Decodificação binaria não retornou para o arquivo original\n")

	if Dados == DecodChr:
		print("Decodificação chr ok\n")
	else:
		print("Decodificação chr não retornou para o arquivo original\n")

	###################
	'''

if __name__ == "__main__":
    main()