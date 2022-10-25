import cv2                # Biblioteca para abrir a camera
import mediapipe as mp    # Biblioteca para a detecção de pontos de referência
from math import hypot              # Vai medir a distância entre os pontos


video = cv2.VideoCapture(0) # Variável que armazena a função de captura de video,
#no caso, como passamos como parâmetro o índice zero, em vez de um caminho de video,
#irá fazer o video capture da webcam de índice 0 do nosso computador(no caso, a integrada)

# O mediapipe contém, uma espécie de rede neural própria
# chamando a biblioteca com o mp. o atributo solutions conecta ela a uma api do google
# dentro dessa api, podemos retirar as informações distribuídas por eles
# o atributo pose, é um tracking do corpo humano(Aquelas ligações e bolinhas la)
pose = mp.solutions.pose

# essa variável está armazeando a pose, passando como parâmetro
# o mínimo de semelhança entre os modelos previamente carregados
# e o video que será processado pela webcam.
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5, )


# A variável armazena o método que usamos para desenhar as linhas e pontos
# que vão fazer parte da composição do corpos identificados pelo noss
draw = mp.solutions.drawing_utils

# Contador para identificar quatos polichinelos foram feitos

# Essa variável só serve pra impedir o contador não contar mais de um polichinelo por vez
# Um video, não passa de um aglomerado de imagens sendo exibidas de forma rápida uma
# Atrás da outra, nós precisamos de uma variável que recebe True ou False, pois
# O laço de verificação do movimento, reconhecerá a mesma pose em diversas imagens
# E acrescentará um ao contador diversas vezes
# Após detectar que o movimento está certo uma vez, definos o valor de Check para False
# Desta maneira, como visto daqui a pouco, só fara a contagem uma vez



def polichinelos():
    contador = 0

    check = False
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        novaimg = cv2.resize(img, (800, 600))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape

        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos

            cabeca = int(points.landmark[pose.PoseLandmark.NOSE].y*h)

            peDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_ANKLE].y*h)

            peDireitoX = int(points.landmark[pose.PoseLandmark.RIGHT_ANKLE].x*w)

            peEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_ANKLE].y*h)

            peEsquerdoX = int(points.landmark[pose.PoseLandmark.LEFT_ANKLE].x*w)

            distanciaPes = hypot(peDireitoX - peEsquerdoX , peDireitoY, peEsquerdoY)

            maoDireitaY = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].y*h)

            maoDireitaX = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].x*w)

            maoEsquerdaY = int(points.landmark[pose.PoseLandmark.LEFT_WRIST].y*h)

            maoEsquerdaX = int(points.landmark[pose.PoseLandmark.LEFT_WRIST].x*w)

            quadrilEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_HIP].y*h)

            quadrilEsquerdoX = int(points.landmark[pose.PoseLandmark.LEFT_HIP].x*w)

            quadrilDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].y*h)

            quadrilDireitoX = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].x*w)

            peDY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h)

            peDX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

            peEY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)

            peEX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)

            moDY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h)

            moDX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x*w)

            moEY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)

            moEX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x*w)

            print(f'quadril: {quadrilDireitoY}')
            # maos <=150 pes >=150

            distMO = hypot(moDX-moEX,moDY-moEY) 
            distPE = hypot(peDX-peEX,peDY-peEY)

            # Condicionais para verificar as distâncias descrevidas acima
            # E verificar se os polichinelos foram executados com base
            # Na posição das mãos e dos pés
            if check == True and distMO <=150 and distPE >=150 and (moDY and moEY) < cabeca:
                contador +=1
                check = False # Alterando a variável check para falsa para não contar
                # Mais de um polichinelo

            if distMO >150 and distPE <150:
                check = True # Quando o ultimo movimento é feito altera a variável para true
            # Para permitir que outro polichinelo seja finalizado e computado



            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'

            if quadrilDireitoY >= 600:
                texto = f'Se afaste'


            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(novaimg,(100,450),(700,550),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(120,525),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            

        cv2.imshow('Resultado',novaimg)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break
         
def agachamento():

    contador = 0
    check = False
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        novaimg = cv2.resize(img, (800, 600))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos

            maoDireitaY = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].y*h)

            maoDireitaX = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].x*w)

            posicaoMaoDireita = (maoDireitaX, maoDireitaY)

            maoEsquerdaY = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].y*h)

            maoEsquerdaX = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].x*w)

            posicaoMaoEsquerda = (maoEsquerdaX, maoEsquerdaY)

            ombroDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y*h)

            ombroDireitoX = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].x*w)

            posicaoOmbroDireito = (ombroDireitoX, ombroDireitoY)

            ombroEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].y*h)

            ombroEsquerdoX = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].x*w)

            posicaoOmbroEsquerdo = (ombroEsquerdoX, ombroEsquerdoY)

            peDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_ANKLE].y*h)

            peDireitoX = int(points.landmark[pose.PoseLandmark.RIGHT_ANKLE].x*w)

            peEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_ANKLE].y*h)

            peEsquerdoX = int(points.landmark[pose.PoseLandmark.LEFT_ANKLE].x*w)

            joelhoEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_KNEE].y*h)

            joelhoDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_KNEE].y*h)
            
            quadrilEsquerdoY = int(points.landmark[pose.PoseLandmark.LEFT_HIP].y*h)

            quadrilDireitoY = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].y*h)
            
            


            # Função utilizada para extrair as cordenadas finais dos pés e mãos 
            distPE = hypot(peDireitoX- peEsquerdoX, peDireitoY-peEsquerdoY)

            print(f'quadril: {quadrilDireitoY}, pés {distPE}')
            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés


            if check == True and quadrilEsquerdoY > joelhoEsquerdoY-50 and quadrilDireitoY > joelhoDireitoY-50:
                contador +=1
                check = False # Alterando a variável check para falsa para não contar
                              # Mais de um polichinelo

            if quadrilEsquerdoY <= joelhoEsquerdoY-50 and quadrilDireitoY <= joelhoDireitoY-50:
                check = True # Quando o ultimo movimento é feito altera a variável para true
                             # Para permitir que outro polichinelo seja finalizado e computado


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video'
            cv2.rectangle(novaimg,(100,450),(700,550),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(120,525),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',novaimg)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

def rosca_direta():
    contador = 0
    check = False
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        novaimg = cv2.resize(img, (800, 600))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos
            
            ombroDY = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y*h)
        
            ombroDX = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].x*w)

            ombroEY = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].y*h)

            ombroEX = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].x*w)

            maoDY = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].y*h)

            maoDX = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].x*w)

            maoEY = int(points.landmark[pose.PoseLandmark.LEFT_WRIST].y*h)
            
            maoEX = int(points.landmark[pose.PoseLandmark.LEFT_WRIST].x*w)

            quadrilDY = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].x*w)

            quadrilEY = int(points.landmark[pose.PoseLandmark.LEFT_HIP].y*h)

            # Função utilizada para extrair as cordenadas finais dos pés e mãos 

            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés
            if check == True and (ombroDY-50) < maoDY < ombroDY and (ombroEY-50) < maoEY <= ombroEY and (ombroDX-30) < maoDX < (ombroDX+30) and (ombroEX-30) < maoEX < (ombroEX+30):
                contador += 1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo
                print(False)

            if maoDY >= quadrilDY-200 and maoEY >= quadrilEY-200:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado
                print(True)


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(novaimg,(100,450),(700,550),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(120,525),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',novaimg)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

def elevação_lateral():
    contador = 0
    check = False
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        novaimg = cv2.resize(img, (800, 600))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos
            
            ombroDY = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y*h)
        
            ombroDX = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].x*w)

            ombroEY = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].y*h)

            ombroEX = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].x*w)

            maoDY = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].y*h)

            maoDX = int(points.landmark[pose.PoseLandmark.RIGHT_WRIST].x*w)

            maoEY = int(points.landmark[pose.PoseLandmark.LEFT_WRIST].y*h)
            
            maoEX = int(points.landmark[pose.PoseLandmark.LEFT_WRIST].x*w)

            quadrilDY = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].x*w)


            # Função utilizada para extrair as cordenadas finais dos pés e mãos 

            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés
            if check == True and ombroDY-30 <= maoDY <= ombroDY+30 and ombroEY-30 <= maoEY <= ombroEY+30 and maoDX <= ombroDX-100 and maoEX >= ombroEX+100:
                contador += 1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo
                print(False)

            if maoDY >= quadrilDY-100 and maoEY >= quadrilDY-100:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado
                print(True)


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(novaimg,(100,450),(700,550),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(120,525),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',novaimg)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

