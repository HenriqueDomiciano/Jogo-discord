import random 
import requests
import discord
import numpy as np
import os
import time
TOKEN = os.environ['TOKEN']
client = discord.Client()
#start the tic tac toe part
def arruma(bo,pos,lance):
    x_und = 'X'
    O_und = 'O'
    if lance:
        bo = bo[:(pos-1)*2] + x_und + bo[(pos-1)*2 + 1:]
    else:
        bo = bo[:(pos-1)*2] + O_und + bo[(pos-1)*2 + 1:]
    return bo
def can_be_tie(x):
    return x.count(0)<2 and sum(x)<2
def win_or_tie(b):
    tie = []
    for i in range(len(b)):
        soma =b[i]
        tie.append(can_be_tie(soma))
        if sum(soma)==3:
            return False,"X ganhou",
        elif sum(soma)==-3:
            return False,"O ganhou"
    c=[ list(e) for e in zip(*b)] #transposing the matriz wich represents the game to check columns 
    for j in range(len(c[0])):
        soma = c[j]
        tie.append(can_be_tie(soma))
        if sum(soma) ==3:
            return False,"X ganhou"
        elif sum(soma) == -3:
            return False,"O ganhou"
    soma = []
    for i in range(len(b)):
        soma.append(b[i][i])
    if sum(soma) == 3:
        return False,"X ganhou"
    elif sum(soma) == -3:
        return False,"O ganhou"
    tie.append(can_be_tie(soma))
    soma = []
    for i in range(len(b)):
        soma.append(b[i][len(b[i])-1-i])
    if sum(soma) == 3:
        return False,"X ganhou"
    elif sum(soma) == -3:
        return False,"O ganhou"
    tie.append(can_be_tie(soma))
    if all(tie):
        return False,"Empate"
    return True,'_'
#end tic tac toe part
"""This is the connect Four part"""
def fall_chip(board,pos,player):
    try:
        if board[0][pos-1] !=0 :
            return False
        j = 0 
        while j<6:
            if board[j+1][pos-1] == 0 :
                j+=1
            else:
                break 
        board[j][pos-1] = player
        return board
    except:
        return False

def find_diagonais(board):
    diagonais = []
    parcial,parcial1 = [],[]
    for i in range(len(board[0])-1,-1,-1):
        for j in range(len(board)):
            if (i+j)<len(board[0]):
                parcial.append(board[j][i])
            else:
                break
        if len(parcial)>=4:
            diagonais.append(parcial)
        parcial = []
    for i in range(1,len(board)):
        for j,k in zip(range(i,len(board[0])),range(0,len(board))):
            parcial.append(board[j][k])
        if len(parcial)>=4:
            diagonais.append(parcial)
        parcial = []
    for i in range(len(board[0])):
        parcial.append(board[i][i])

    diagonais.append(parcial)

    return diagonais
def check_win_or_tie(board):
    
    board = list(board)
    somas = []
    d = find_diagonais(board)
    for i in range(len(board)):
        colunas = [row[i] for row in board]
        linhas  = board[i]
        for k in range(len(linhas)-3):
            parc = colunas[k:k+4]
            parl = linhas[k:k+4]
            somas.append(sum(parc))
            somas.append(sum(parl))
            if parc.count(-1)==4 or parl.count(-1)==4:
                return True,'O ganhou'
            elif parc.count(1)==4 or parl.count(1)==4:
                return True,'X ganhou'
    for i in range(len(d)):
        for j in range(len(d[i])-3):
            parc1  = d[i][j:j+4]
            somas.append(sum(parc1))
            if parc1.count(-1)==4 :
                return True,"O ganhou"
            elif parc1.count(1)==4:
                return True,'X ganhou'
    if (np.array(board) == 0).sum() < 3 and (somas.count(3)==0 or somas.count(-3)==0):
        return True,'Empate'
    return False,'_'
"""End connect four part"""
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    

    if message.content.startswith('!ajuda'):
        await message.channel.send('''Este é um bot que joga alguns jogos como o jogo da velha e forca para jogar forca digite $forca 
        para jogar o jogo da velha digite $velha''')

    if message.content.startswith('$dados'):
        
        global score_parc_player1 
        global score_parc_player2  
        global score_total_player1  
        global score_total_player2 
        score_parc_player1 = 0 
        score_parc_player2 =0 
        score_total_player1 = 0
        score_total_player2 = 0


        await message.channel.send('''O jogo funciona assim ganha quem chegar em 100 pontos primeiro . É jogado um dado, se vc tirar qualquer valor diferente de um ele e somado ao seus pontos parciais caso vc tire um 
        vc perde os pontos parciais e é a vez do computador, Cada rodada o jogador pode escolher parar ou continuar se o jogador decidir parar os pontos parciais se tornam pontos normais, use os 
        comandos $parar (para parar) $jogar (para lançar os dados) vc irá jogar contra o computador''')
    
    if message.content.startswith('$jogar'):
        jogada = random.randint(1,6)
        if jogada!=1:
            score_parc_player1+=jogada
            await message.channel.send(f'Vc tirou {jogada}\n\n Seu score_parcial é {score_parc_player1}\n\n Seu score geral é {score_total_player1} ')
        else:
            score_parc_player1=0
            await message.channel.send(f'Vc tirou 1 é a vez do computador')
            for i in range(3):
                jogada = random.randint(1,6)
                await message.channel.send(f'O computador tirou : {jogada} ')
                if jogada!=1:
                    score_parc_player2+=jogada
                    if score_parc_player2+score_total_player2>=100:
                        await message.channel.send(f'O computador decidiu parar com um score geral de {score_total_player2+score_parc_player2} \n\n O Computador ganhou!!!')
                        score_parc_player1 = 0
                        score_parc_player2 = 0 
                        score_total_player1 = 0 
                        score_total_player2 = 0
                        break
                else:
                    score_parc_player2 = 0 
                    break
                time.sleep(0.5)
            score_total_player2+=score_parc_player2
            await message.channel.send(f'O computador tirou um score parcial de {score_parc_player2} o score geral é de {score_total_player2}')
            score_parc_player2 = 0 
        
    if message.content.startswith('$parar'):
        score_total_player1+=score_parc_player1
        score_parc_player1 =0 
        await message.channel.send(f'Seu score geral agora é {score_total_player1}')
        if score_total_player1>=100:
            score_parc_player1 = 0
            score_parc_player2 = 0 
            score_total_player1 = 0 
            score_total_player2 = 0
            await message.channel.send('Vc ganhou !!!!!!!!!')
        else:
            for i in range(3):
                jogada = random.randint(1,6)
                await message.channel.send(f'O computador tirou : {jogada} ')
                if jogada!=1:
                    score_parc_player2+=jogada
                    if score_parc_player2+score_total_player2>=100:
                        await message.channel.send(f'O computador decidiu parar com um score geral de {score_total_player2+score_parc_player2} \n\n O Computador ganhou!!!')
                        score_parc_player1 = 0
                        score_parc_player2 = 0 
                        score_total_player1 = 0 
                        score_total_player2 = 0
                        break
                else:
                    score_parc_player2 = 0 
                    break
                time.sleep(0.5)
            score_total_player2+=score_parc_player2
            await message.channel.send(f'O computador tirou um score parcial de {score_parc_player2} o score geral é de {score_total_player2}')
            score_parc_player2 = 0 

    if message.content.startswith('$forca'):
        global word
        global attempt
        global letras
        global palavra 
        word =  requests.get('https://api.dicionario-aberto.net/random').json()['word'].upper()
        attempt = 0
        letras = []
        palavra = len(word)*['*']
        await message.channel.send(f' Vc ainda tem {10-attempt} tentativas \n {" ".join(palavra)} \n Digite $letra "Letra" para testar a letra')
    
    if message.content.startswith("$letra"):
        try:
            letra = message.content.replace('$letra','').strip().upper()
            if len(letra)>1:
                await message.channel.send('Caractere não valido')
            elif (letra in letras):
                await message.channel.send('A letra já foi enviada')
            else:
                found = False
                letras.append(letra)
                
                for l in range(len(word)):
                    if word[l] == letra:
                        palavra[l] = letra
                        found = True
                
                if found ==False:
                    attempt+=1

                if ''.join(palavra)==word:
                    await message.channel.send(f'Vc Ganhou !!!!! \n\n A palavra era :{word}\n\n Para reiniciar o jogo digite $forca ')
                    word =  requests.get('https://api.dicionario-aberto.net/random').json()['word'].upper()
                    attempt = 0
                    letras = []
                    palavra = len(word)*['*']
                                    
                
                elif attempt==10:
                    await message.channel.send(f' Vc perdeu \n\n A palavra era {word}')
                    word =  requests.get('https://api.dicionario-aberto.net/random').json()['word'].upper()
                    attempt = 0
                    letras = []
                    palavra = len(word)*['*']
                
                await message.channel.send(f'Vc ainda tem {10-attempt} tentativas \n\n {" ".join(palavra)} \n\n Letras já tentadas {" ".join(letras)} \n\n Digite $letra " A Letra que vc quer" para testar a letra')
        
        except Exception as e:
            await message.channel.send(f'Vc deve criar um jogo primeiro digite $Forca')
    
    if message.content.startswith('$velha'):
        global player
        global player1 
        global player1_nome
        global player2
        global player2_nome
        global board
        global start
        global board2
        global ganhador
        board = """-|-|-\n-|-|-\n-|-|-"""
        b_inicial = """1|2|3\n4|5|6\n7|8|9"""
        board2 = [3*[0],3*[0],3*[0]]
        player1 = str(message.author.id)
        player1_nome = str(message.author.name)
        player2 = '' 
        player = True
        start = True
        await message.channel.send(f'As posições são\n {b_inicial} \n\n Digite $posi e o número que vc deseja em seguida')
            
    if message.content.startswith('$posi'):
        if str(message.author.id)==player1 and player and start:
            try:
                posx = int(message.content.replace('$posi','').strip())
                i = (posx-1)//3
                j = (posx%3)-1
                if board2[i][j]==0:
                    board2[i][j]=1
                    board = arruma(board,posx,player)
                    player = False
                    await message.channel.send(f'\n{board}')
                    start,ganhador = win_or_tie(board2)
                    if not(start):
                        board = """-|-|-\n-|-|-\n-|-|-"""
                        b_inicial = """1|2|3\n4|5|6\n7|8|9"""
                        board2 = [3*[0],3*[0],3*[0]]
                        player1 = str(message.author.id)
                        player1_nome = str(message.author.name)
                        player2 = '' 
                        player = True
                        start = True
                        if ganhador == 'X ganhou':
                            await message.channel.send(f'O ganhador é {player1_nome}')
                        elif ganhador =='O ganhou':
                            await message.channel.send(f'O ganhador é {player2_nome}')
                        else:
                            await message.channel.send(f'Empatou')
                else:
                    await message.channel.send('Posição invalida digite outra')
            except:
                await message.channel.send('Envie um valor valido para o seu jogo')
        elif (not(player) and start and message.author.id==player2) or player2=='':
            if player2=='':
                player2_nome = message.author.name
                player2 = message.author.id
                await message.channel.send(f'Vc {player2_nome} esta jogando contra {player1_nome}')
            try:
                posx = int(message.content.replace('$posi','').strip())
                i = (posx-1)//3
                j = (posx%3)-1
                if board2[i][j]==0:
                    board2[i][j]=-1
                    board = arruma(board,posx,player)
                    player = True
                    start,ganhador = win_or_tie(board2)  
                    await message.channel.send(f'\n{board}')
                    if not(start):
                        board = """-|-|-\n-|-|-\n-|-|-"""
                        b_inicial = """1|2|3\n4|5|6\n7|8|9"""
                        board2 = [3*[0],3*[0],3*[0]]
                        player1 = str(message.author.id)
                        player1_nome = str(message.author.name)
                        player2 = '' 
                        player = True
                        start = True
                        if ganhador == 'X ganhou':
                            await message.channel.send(f'O ganhador é {player1_nome}')
                        elif ganhador =='O ganhou':
                            await message.channel.send(f'O ganhador é {player2_nome}')
                        else:
                            await message.channel.send(f'Empatou')
                else:
                    await message.channel.send('Posição invalida digite outra')
            except:
                await message.channel.send('Envie um valor valido para o seu jogo')
        elif start:
            await message.channel.send('Vc não está no jogo ou não é sua vez se quiser jogar espere ate o final e comece outro com $velha')
    if message.content.startswith('$cn4'):
        global boardcn4
        global boardcn4_res
        boardcn4 = [7*[0],7*[0],7*[0],7*[0],7*[0],7*[0],7*[0]]
        global string   
        string= ''
        global player1cn4
        player1cn4 = str(message.author.id)
        global player1cn4_name
        player1cn4_name = str(message.author.name)
        global player2cn4
        player2cn4 = ''
        global player2cn4_name
        player2cn4_name = ''
        global playercn4
        playercn4 = True
        global is_over
        is_over = False
        await message.channel.send('O jogo foi inicializado para digitar a posição escolha um digito de 1 a 7 e coloque nesta forma "$poscn4 1"')
    if message.content.startswith('$poscn4'):
        if playercn4 and (not(is_over)) and str(message.author.id)==player1cn4  :
            try:
                posA = int(message.content.replace('$poscn4','').strip())
                boardcn4_res = boardcn4
                boardcn4 = fall_chip(boardcn4,posA,-1)
                if boardcn4==False:
                    boardcn4 = boardcn4_res
                    await message.channel.send('Jogada invalida')
                    playercn4 = True
                else:
                    string = ''
                    for i in range(len(boardcn4)):
                        for j in range(len(boardcn4[0])):
                            if boardcn4[i][j]==1:
                                string = string + ' X '
                            elif boardcn4[i][j]==-1:
                                string = string+ ' O '
                            else:
                                string = string +' E '
                        string = string + '\n'
                    playercn4 = False 
                    await message.channel.send(string)
                    is_over,ganhador = check_win_or_tie(boardcn4)
                    if (is_over):
                        boardcn4 = [7*[0],7*[0],7*[0],7*[0],7*[0],7*[0],7*[0]]
                        string= ''
                        if ganhador == 'X ganhou' :
                            await message.channel.send(f'{player1cn4_name} Ganhou')
                        elif ganhador == 'O ganhou':
                            await message.channel.send(f'{player2cn4_name} Ganhou')
                        else:
                            await message.channel.send(f'Empatou')
                        message.channel.send('Digite $cn4 para jogar novamente')
            except Exception as e:
                print(e)
                await message.channel.send('Envie um valor valido')
        
        elif (player2cn4==str(message.author.id) and (not(is_over)) and not(playercn4) ) or player2cn4=='':
            if player2cn4=='':
                player2cn4_name = str(message.author.name)
                player2cn4 = str(message.author.id)
                await message.channel.send(f'Vc {player2cn4_name} esta jogando contra {player1cn4_name} jogue novamente sua jogada')
            try:
                posA = int(message.content.replace('$poscn4','').strip())
                boardcn4_res = boardcn4
                boardcn4 = fall_chip(boardcn4,posA,1)
                if boardcn4==False:
                    boardcn4 = boardcn4_res
                    await message.channel.send('Jogada invalida')
                    playercn4 = False
                else:
                    string = ''
                    for i in range(len(boardcn4)):
                        for j in range(len(boardcn4[0])):
                            if boardcn4[i][j]==1:
                                string = string + ' X '
                            elif boardcn4[i][j]==-1:
                                string = string+ ' O '
                            else:
                                string = string +' E '
                        string = string + '\n'
                    playercn4 = True 
                    await message.channel.send(string)
                    is_over,ganhador = check_win_or_tie(boardcn4)
                    if (is_over):
                        boardcn4 = [7*[0],7*[0],7*[0],7*[0],7*[0],7*[0],7*[0]]
                        string= ''
                        if ganhador == 'X ganhou' :
                            await message.channel.send(f'{player1cn4_name} Ganhou')
                        elif ganhador == 'O ganhou':
                            await message.channel.send(f'{player2cn4_name} Ganhou')
                        else:
                            await message.channel.send(f'Empatou')
                        message.channel.send('Digite $cn4 para jogar novamente')
            except Exception as e:
                print(e)
                await message.channel.send('Envie um valor valido')
        else:
            print(player2cn4_name)
            await message.channel.send('Não é sua vez')
client.run(TOKEN)




