from sys import argv
from struct import *
import sys
import os
import time
import math

#
def Read_compac(Name, n):

	Arq = open(Name, "rb")
	Dados_cod = []

	#Lê o arquivo
	while True:
		rec = Arq.read(2)

		if len(rec) != 2:
			break

		(Dados, ) = unpack('>H', rec)
		Dados_cod.append(Dados)

	return Dados_cod

#
def Write_compac(Name, Dados, n):

	output_Arq = open(Name, 'wb')

	#Salva o arquivo em modo binário
	for d in Dados:
		output_Arq.write(pack('>H',d))

	output_Arq.close()

#
def Read_bin(Name):

	input_arq = open(Name, 'rb')
	
	Dados = input_arq.read()

	input_arq.close()

	return Dados

#
def Write_arq(Name, Dados, n):

	#Gera o arquivo de saída
	output_Arq = open(Name, 'w')

	#Salva o arquivo
	for d in Dados:
	    output_Arq.write(d)
	    
	#Fecha os arquivos
	output_Arq.close()

#
def Convert_nBits(Dados, n):

	#Escreve os valores em binarios de n bits
	Dados_convert = []
	aux = []

	nBits = "0"+str(n)+"b"

	for Valor in Dados:
		Valor_chr = format(Valor, nBits)
		Dados_convert.append(Valor_chr)

		x = Valor_chr.encode('ascii')
		aux.append(x)

	#Converte os valores em binarios de 8 bits
	Dados_8bit = []
	buffer_ = ""

	range_ = round(((len(Dados_convert)*n)/8)+0.5)

	for i in range(range_):
		if(i < len(Dados_convert)):
			buffer_ = buffer_ + Dados_convert[i]

		#Divide os dados
		d_8 = buffer_[0:8]
		d_n = buffer_[8:len(buffer_)]

		#Converte os 8 primeiros bits e salva
		#d_8_bin = d_8.encode('ascii')				#############
		d_8_bin = d_8
		Dados_8bit.append(d_8_bin)

		#Salva o restante no buffer
		buffer_ = d_n

	#Verifica o ultimo byte
	tam = len(Dados_8bit)
	byte = Dados_8bit[tam-1]
	nBits = "08b"

	Valor_conv = format(int(byte), nBits)

	#Dados_8bit[tam-1] = Valor_conv.encode('ascii')	###############
	Dados_8bit[tam-1] = Valor_conv

	return Dados_8bit

#
def Decodificador(Dados, n):

	#Define o tamanho do dicionario
	Tam_tab = int(math.pow(2,n))

	#Cria as variáveis
	Prox_cod = 256
	Dados_decod = []
	string = ""

	#Inicializa o dicionario
	Tam_dict = 256
	Dicionario = dict((i, chr(i)) for i in range(Tam_dict))

	#Percorre o arquivo
	for code in Dados:

		if not (code in Dicionario):
			Dicionario[code] = string + (string[0])

		Dados_decod += Dicionario[code]

		if not(len(string) == 0):
			Dicionario[Prox_cod] = string + (Dicionario[code][0])
			Prox_cod += 1

		string = Dicionario[code]

		if len(Dicionario) == Tam_tab:
			Tam_dict = 256
			Dicionario.clear()
			Dicionario = dict((i, chr(i)) for i in range(Tam_dict))

	return Dados_decod

#
def Codificador(Dados, n):

	#Verifica o valor do n
	if(n < 9):
		print("Erro: 'n' invalido")
		sys.exit()

	#Define o tamanho maximo do dicionario
	Tam_tab = int(math.pow(2,n)) 

	#Inicializa o dicionario
	Tam_dict = 256
	Dicionario = {chr(i): i for i in range(Tam_dict)}
	string = ""
	Dados_cod = []

	#\n, \r

	#Percorre o arquivo
	for c in Dados:

		novo_c = string + chr(c)

		if novo_c in Dicionario:
			string = novo_c

		else:
			Dados_cod.append(Dicionario[string])

			#Se o dicionario não estiver cheio, insere o novo chr
			if(len(Dicionario) < Tam_tab):
				Dicionario[novo_c] = Tam_dict
				Tam_dict += 1
				string = chr(c)

			#Se o dicionario estiver cheio, reseta
			else:
				Dados_cod.append(Dicionario[string])
				Tam_dict = 256
				Dicionario = {chr(i): i for i in range(Tam_dict)}
				string = ""

	if string:
		Dados_cod.append(Dicionario[string])

	return Dados_cod

#
def main():

	#arq = "corpus16MB.txt"
	#arq = "mapa.mp4"
	n = 9
	out_ = "Dados_codificados.txt"
	Script = open("Com_reset_script.txt", "w")
	Dados = Read_bin(arq)

	################################ Cod

	while(n <= 16):
		print("n= ",n)
		out_ = "Com_reset_codificados_k="+str(n)+".txt"
		inicio = time.time()
		Dados_cod = Codificador(Dados, n)
		fim = time.time()
		Write_compac(out_, Dados_cod, n) #salvar em 2,4 ou 8 bytes
		Script.write("Tempo de codificação para n = "+str(n)+": "+str(fim - inicio)+"\n")
		n = n+1


if __name__ == "__main__":
    main()