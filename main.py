import pygame
import random
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados # Assuming funcoes.py is in a subfolder 'recursos'
import json
import sys
import speech_recognition as sr

def aguardar_comando_voz_visual():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        reconhecido = False
        pygame.display.set_caption("Fale para Iniciar")

        while not reconhecido:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tela.fill((255, 255, 255))  # fundo branco

            msg1 = fonteMenu.render("Diga: 'eu amo rosquinhas'", True, (0, 0, 0))
            msg2 = fonteMenu.render("Usando microfone...", True, (100, 100, 100))
            msg1_rect = msg1.get_rect(center=(largura_tela // 2, altura_tela // 2 - 30))
            msg2_rect = msg2.get_rect(center=(largura_tela // 2, altura_tela // 2 + 10))
            tela.blit(msg1, msg1_rect)
            tela.blit(msg2, msg2_rect)

            pygame.display.update()

            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=4)
                    frase = recognizer.recognize_google(audio, language="pt-BR")
                    print(f"Você disse: {frase}")
                    if frase.lower().strip() == "eu amo rosquinhas":
                        reconhecido = True
                    else:
                        print("Frase incorreta.")
            except sr.UnknownValueError:
                print("Não entendi. Tente de novo.")
            except sr.WaitTimeoutError:
                print("Nada detectado.")

pygame.init()
inicializarBancoDeDados()

# --- Configurações da Tela ---
largura_tela = 1000
altura_tela = 700

tamanho_tela = (largura_tela, altura_tela)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("PyGame Simpsons")

# --- Cores ---
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo_simpsons = (255, 217, 15)
vermelho_perigo = (200, 0, 0)
cor_sol = (255, 255, 0)

# --- Carregar Assets  ---
try:
    icone_simpsons = pygame.image.load("recursos/assets/icone_simpsons.jpg")
    pygame.display.set_icon(icone_simpsons)
    homer_img_original = pygame.image.load("recursos/assets/homer.png")
    donut_img_original = pygame.image.load("recursos/assets/donut.png")
    brocolis_img_original = pygame.image.load("recursos/assets/brocolis.png")
    fundoStart_img = pygame.image.load("recursos/assets/fundoStart_simpsons.jpg")
    fundoJogo_img = pygame.image.load("recursos/assets/fundoJogo_simpsons.jpg")
    fundoPerdeu_img = pygame.image.load("recursos/assets/fundoPerdeu_simpsons.png")
    eat_sound = pygame.mixer.Sound("recursos/assets/comer.mp3")
    game_over_sound = pygame.mixer.Sound("recursos/assets/doh_sound.mp3")
    yuck_sound = pygame.mixer.Sound("recursos/assets/no.mp3")
    pygame.mixer.music.load("recursos/assets/simpsons_theme.mp3")
except pygame.error as e:
    print(f"Erro ao carregar recursos/assets: {e}")
    print("Certifique-se que todos os ficheiros de imagem e som estão na pasta 'recursos/assets'")
    pygame.quit()
    sys.exit()

# --- Fontes ---
fonteMenu = pygame.font.SysFont("comicsansms", 25)
fontePontos = pygame.font.SysFont("comicsansms", 30)
fonteGameOver = pygame.font.SysFont("comicsansms", 70)
fonteNick = pygame.font.SysFont("comicsansms", 18)
fonteMensagemPerdeu = pygame.font.SysFont("comicsansms", 35)
fontePausa = pygame.font.SysFont("comicsansms", 60)
fonteInstrucaoPausa = pygame.font.SysFont("comicsansms", 20)

# --- Escalar Imagens ---
def escalar_imagem(imagem, largura_desejada):
    original_largura = imagem.get_width()
    original_altura = imagem.get_height()
    if original_largura == 0: return imagem
    escala = largura_desejada / original_largura
    altura_desejada = int(original_altura * escala)
    return pygame.transform.scale(imagem, (largura_desejada, altura_desejada))

homer_largura_desejada = 120
homer_img = escalar_imagem(homer_img_original, homer_largura_desejada)
larguraHomer = homer_img.get_width()
alturaHomer = homer_img.get_height()
item_largura_desejada = 50
donut_img = escalar_imagem(donut_img_original, item_largura_desejada)
brocolis_img = escalar_imagem(brocolis_img_original, item_largura_desejada)
larguraItem = item_largura_desejada
alturaItem = item_largura_desejada

# --- Inicializar Relógio ---

relogio = pygame.time.Clock()
nome_jogador_global = ""
mensagem_game_over_especifica = ""

# Inicializar Bart
bart_img = pygame.image.load("recursos/assets/bart.png")
bart_img = pygame.transform.scale(bart_img, (100, 100))
bart_x = -100  # Começa fora da tela
bart_y = 100  # Altura onde ele aparece
bart_speed = 3

# --- Itens Disponíveis ---
ITEM_DONUT = 'donut'
ITEM_BROCOLIS = 'brocolis'
itens_disponiveis = [(donut_img, ITEM_DONUT), (brocolis_img, ITEM_BROCOLIS)]

def obter_nome_jogador():
    global nome_jogador_global
    root_tk = tk.Tk()
    root_tk.withdraw()
    largura_janela_tk = 300
    altura_janela_tk = 100
    pos_x_tk = (root_tk.winfo_screenwidth() - largura_janela_tk) // 2
    pos_y_tk = (root_tk.winfo_screenheight() - altura_janela_tk) // 2
    dialog = tk.Toplevel(root_tk)
    dialog.geometry(f"{largura_janela_tk}x{altura_janela_tk}+{pos_x_tk}+{pos_y_tk}")
    dialog.title("Nickname")
    dialog.attributes("-topmost", True)
    tk.Label(dialog, text="Digite o seu nome:", font=("Comic Sans MS", 12)).pack(pady=5)
    entry_nome = tk.Entry(dialog, font=("Comic Sans MS", 12))
    entry_nome.pack(pady=5)
    entry_nome.focus_set()
    def on_submit():
        global nome_jogador_global
        nome_jogador_global = entry_nome.get().strip()
        if not nome_jogador_global:
            messagebox.showwarning("Aviso", "Por favor, digite o seu nome!", parent=dialog)
        else:
            dialog.destroy()
            root_tk.quit()
    def on_closing():
        global nome_jogador_global
        if not entry_nome.get().strip():
             nome_jogador_global = "JogadorAnónimo"
        dialog.destroy()
        root_tk.quit()
    dialog.protocol("WM_DELETE_WINDOW", on_closing)
    botao_submit = tk.Button(dialog, text="Jogar!", command=on_submit, font=("Comic Sans MS", 12))
    botao_submit.pack(pady=10)
    entry_nome.bind("<Return>", lambda event: on_submit())
    dialog.grab_set()  # Para forzar foco exclusivo
    root_tk.wait_window(dialog)  # Esperar solo esa ventana, no toda la GUI
    root_tk.destroy()  # Destruir después para liberar recursos

def criar_novo_item_caindo():
    escolha = random.choices(itens_disponiveis, weights=[0.7, 0.3], k=1)[0]
    img, tipo = escolha
    largura = img.get_width()
    altura = img.get_height()

    # Posição inicial
    pos_x = random.randint(0, largura_tela - largura)
    pos_y = -altura

    # Hitbox normal (donut) ou reduzida (brocolis)
    if tipo == ITEM_BROCOLIS:
        hitbox_largura = int(largura * 0.2)
        hitbox_altura = int(altura * 0.2)
        offset_x = (largura - hitbox_largura) // 2
        offset_y = (altura - hitbox_altura) // 2
        hitbox = pygame.Rect(pos_x + offset_x, pos_y + offset_y, hitbox_largura, hitbox_altura)
    else:
        hitbox = pygame.Rect(pos_x, pos_y, largura, altura)

    return {
        'image': img,
        'rect': hitbox,
        'draw_pos': (pos_x, pos_y),  # onde desenhar a imagem
        'type': tipo,
        'speed': random.uniform(2.5, 4.5)
    }
def jogar():
    global nome_jogador_global, mensagem_game_over_especifica
    print("DEBUG: Entrou em jogar()")  # DEBUG
    if not nome_jogador_global:
        obter_nome_jogador()
        if not nome_jogador_global:
            print("DEBUG: Nome não fornecido em jogar(), voltando para start_screen()")  # DEBUG
            start_screen()
            return

    posicaoXHomer = largura_tela // 2 - larguraHomer // 2
    posicaoYHomer = altura_tela - alturaHomer - 10
    movimentoXHomer = 0
    pontos = 0
    falling_items = [criar_novo_item_caindo()]
    max_falling_items = 3
    jogo_pausado = False

    # Inicializar relógio
    relogio = pygame.time.Clock()

    # Inicializar Bart (movimento aleatório)
    bart_img = pygame.image.load("recursos/assets/bart.png")
    bart_img = pygame.transform.scale(bart_img, (100, 100))

    bart_x = random.randint(0, largura_tela - bart_img.get_width())
    bart_y = random.randint(0, altura_tela - bart_img.get_height())
    bart_alvo_x = random.randint(0, largura_tela - bart_img.get_width())
    bart_alvo_y = random.randint(0, altura_tela - bart_img.get_height())
    bart_velocidade = 2


    # Animação do sol
    raio_sol_inicial = 30
    raio_sol_min = 25
    raio_sol_max = 35
    velocidade_pulsacao_sol = 0.1
    raio_sol_atual = raio_sol_inicial
    pulsando_para_aumentar = True
    pos_sol_x = largura_tela - 50
    pos_sol_y = 50

    pygame.mixer.music.play(-1)
    rodando_jogo = True
    while rodando_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogo_pausado = not jogo_pausado
                    if jogo_pausado: pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()
                if not jogo_pausado:
                    if evento.key == pygame.K_LEFT: movimentoXHomer = -15
                    if evento.key == pygame.K_RIGHT: movimentoXHomer = 15
            if evento.type == pygame.KEYUP:
                if not jogo_pausado:
                    if (evento.key == pygame.K_LEFT and movimentoXHomer < 0) or \
                       (evento.key == pygame.K_RIGHT and movimentoXHomer > 0):
                        movimentoXHomer = 0       

        if not jogo_pausado:
            posicaoXHomer += movimentoXHomer
            if posicaoXHomer < 0: posicaoXHomer = 0
            elif posicaoXHomer > largura_tela - larguraHomer: posicaoXHomer = largura_tela - larguraHomer

            if len(falling_items) < max_falling_items and random.randint(1, 100) < 4:
                falling_items.append(criar_novo_item_caindo())

            itens_para_remover = []
            rectHomer = pygame.Rect(posicaoXHomer, posicaoYHomer, larguraHomer, alturaHomer)
            for item_jogo in falling_items:
                item_jogo['rect'].y += item_jogo['speed']
                if rectHomer.colliderect(item_jogo['rect']):
                    if item_jogo['type'] == ITEM_DONUT:
                        pontos += 1
                        pygame.mixer.Sound.play(eat_sound)
                        itens_para_remover.append(item_jogo)
                    elif item_jogo['type'] == ITEM_BROCOLIS:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(yuck_sound)
                        pygame.mixer.Sound.play(game_over_sound)
                        escreverDados(nome_jogador_global, pontos)
                        mensagem_game_over_especifica = "Você comeu VEGETAL! D'oh!"
                        dead_screen(pontos)
                        rodando_jogo = False
                        break
                elif item_jogo['rect'].top > altura_tela:
                    if item_jogo['type'] == ITEM_DONUT:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(game_over_sound)
                        escreverDados(nome_jogador_global, pontos)
                        mensagem_game_over_especifica = "Deixou uma rosquinha cair! D'oh!"
                        dead_screen(pontos)
                        rodando_jogo = False
                        break
                    else:
                        itens_para_remover.append(item_jogo)

            if not rodando_jogo:
                break

            for item_removido in itens_para_remover:
                if item_removido in falling_items:
                    falling_items.remove(item_removido)
            if not falling_items:
                falling_items.append(criar_novo_item_caindo())

        # Desenho do fundo
        tela.blit(fundoJogo_img, (0, 0))

                # Atualizar posição do Bart de forma aleatória
        dx = bart_alvo_x - bart_x
        dy = bart_alvo_y - bart_y
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia < 5:
            # Sorteia novo destino
            bart_alvo_x = random.randint(0, largura_tela - bart_img.get_width())
            bart_alvo_y = random.randint(0, altura_tela - bart_img.get_height())
        else:
            # Move em direção ao alvo
            bart_x += bart_velocidade * dx / distancia
            bart_y += bart_velocidade * dy / distancia
        # Desenhar Bart# Desenha o Bart
        tela.blit(bart_img, (int(bart_x), int(bart_y)))

        # Animação do sol
        if pulsando_para_aumentar:
            raio_sol_atual += velocidade_pulsacao_sol
            if raio_sol_atual >= raio_sol_max:
                raio_sol_atual = raio_sol_max
                pulsando_para_aumentar = False
        else:
            raio_sol_atual -= velocidade_pulsacao_sol
            if raio_sol_atual <= raio_sol_min:
                raio_sol_atual = raio_sol_min
                pulsando_para_aumentar = True
        pygame.draw.circle(tela, cor_sol, (pos_sol_x, pos_sol_y), int(raio_sol_atual))

        current_rectHomer = pygame.Rect(posicaoXHomer, posicaoYHomer, larguraHomer, alturaHomer)
        tela.blit(homer_img, current_rectHomer.topleft)
        for item_desenho in falling_items:
            tela.blit(item_desenho['image'], item_desenho['rect'].topleft)

        texto_pontos_render = fontePontos.render("Rosquinhas: " + str(pontos), True, amarelo_simpsons)
        tela.blit(texto_pontos_render, (10, 10))
        texto_instrucao_pausa_render = fonteInstrucaoPausa.render("ESPAÇO para Pausar", True, preto)
        pos_texto_instrucao_x = largura_tela - texto_instrucao_pausa_render.get_width() - 10
        pos_texto_instrucao_y = pos_sol_y + raio_sol_max + 5
        tela.blit(texto_instrucao_pausa_render, (pos_texto_instrucao_x, pos_texto_instrucao_y))

        if jogo_pausado:
            overlay = pygame.Surface(tamanho_tela, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            tela.blit(overlay, (0,0))
            texto_pausa_render = fontePausa.render("Pausado", True, amarelo_simpsons)
            texto_pausa_rect = texto_pausa_render.get_rect(center=(largura_tela / 2, altura_tela / 2))
            tela.blit(texto_pausa_render, texto_pausa_rect)

        pygame.display.update()
        relogio.tick(60)

    return

def start_screen():
    global nome_jogador_global, mensagem_game_over_especifica
    print("DEBUG: Entrou em start_screen()") # DEBUG
    nome_jogador_global = ""
    mensagem_game_over_especifica = ""
    larguraButton = 220
    alturaButton  = 55
    cor_botao = amarelo_simpsons
    cor_texto_botao = preto
    pos_x_botao = largura_tela/5 - larguraButton/5
    pos_y_botao_iniciar = altura_tela/5 - alturaButton
    pos_y_botao_sair = altura_tela/5 + alturaButton/5 + 10

    rodando_start = True
    while rodando_start:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundoStart_img, (0, 0))
        startButtonRect = pygame.Rect(pos_x_botao, pos_y_botao_iniciar, larguraButton, alturaButton)
        pygame.draw.rect(tela, cor_botao, startButtonRect, border_radius=15)
        texto_iniciar = fonteMenu.render("Iniciar Jogo", True, cor_texto_botao)
        texto_iniciar_rect = texto_iniciar.get_rect(center=startButtonRect.center)
        tela.blit(texto_iniciar, texto_iniciar_rect)
        quitButtonRect = pygame.Rect(pos_x_botao, pos_y_botao_sair, larguraButton, alturaButton)
        pygame.draw.rect(tela, cor_botao, quitButtonRect, border_radius=15)
        texto_sair = fonteMenu.render("Sair", True, cor_texto_botao)
        texto_sair_rect = texto_sair.get_rect(center=quitButtonRect.center)
        tela.blit(texto_sair, texto_sair_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if startButtonRect.collidepoint(mouse_pos):
                        obter_nome_jogador()
                        if nome_jogador_global:
                            aguardar_comando_voz_visual()
                            jogar()
                            print("DEBUG: Aguardar comando de voz visual retornou. Chamando jogar()") # DEBUG
                            jogar()
                            print("DEBUG: jogar() retornou para start_screen. Definindo rodando_start = False.") # DEBUG
                            rodando_start = False # CORREÇÃO PRINCIPAL AQUI
                    if quitButtonRect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
        relogio.tick(60)
    print(f"DEBUG: Fim do loop principal de start_screen. rodando_start = {rodando_start}. Retornando de start_screen().") # DEBUG
    return # Adicionado retorno explícito

def dead_screen(pontos_finais):
    global nome_jogador_global, mensagem_game_over_especifica
    print(f"DEBUG: Entrou em dead_screen com pontos: {pontos_finais}") # DEBUG
    larguraButton = 250
    alturaButton  = 60
    cor_botao = amarelo_simpsons
    cor_texto_botao = preto
    pos_x_botao = largura_tela/2 - larguraButton/2
    pos_y_botao_jogar_novamente = altura_tela * 0.60
    pos_y_botao_menu = altura_tela * 0.60 + alturaButton + 30

    def mostrar_log_pontuacoes_tk():
        log_root = tk.Tk()
        log_root.title("Histórico de Pontuações")
        # ... (código da janela de log mantido como antes) ...
        largura_janela_log = 450
        altura_janela_log = 350
        pos_x_log = (log_root.winfo_screenwidth() - largura_janela_log) // 2
        pos_y_log = (log_root.winfo_screenheight() - altura_janela_log) // 2
        log_root.geometry(f"{largura_janela_log}x{altura_janela_log}+{pos_x_log}+{pos_y_log}")
        log_root.attributes("-topmost", True)
        tk.Label(log_root, text="Placar dos Campeões (de Rosquinhas):", font=("Comic Sans MS", 16)).pack(pady=10)
        frame_lista = tk.Frame(log_root)
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical")
        listbox = tk.Listbox(frame_lista, width=60, height=10, font=("Comic Sans MS", 10), yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)
        try:
            with open("base.atitus", "r") as banco_log:
                dados_log_str = banco_log.read()
            if dados_log_str:
                log_partidas = json.loads(dados_log_str)
                sorted_log = sorted(log_partidas.items(), key=lambda item: (item[1][0], item[0]), reverse=True)
                for i, (nome_log, (pts_log, data_log)) in enumerate(sorted_log):
                    listbox.insert(tk.END, f"{i+1}. {nome_log}: {pts_log} rosquinhas em {data_log}")
            else: listbox.insert(tk.END, "Ninguém jogou ainda? D'oh!")
        except FileNotFoundError: listbox.insert(tk.END, "Ficheiro de pontuações sumiu! Foi o Bart?")
        except json.JSONDecodeError: listbox.insert(tk.END, "Ficheiro de pontuações está estranho... Flanders mexeu aqui?")
        except Exception as e: listbox.insert(tk.END, f"Erro ao ler pontuações: {e}")
        tk.Button(log_root, text="Fechar", command=log_root.destroy, font=("Comic Sans MS", 12)).pack(pady=10)
        log_root.mainloop()

    mostrar_log_pontuacoes_tk()
    rodando_dead = True
    while rodando_dead:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundoPerdeu_img, (0, 0))
        texto_game_over_titulo = fonteGameOver.render("VOCE PERDEU!", True, vermelho_perigo)
        texto_game_over_titulo_rect = texto_game_over_titulo.get_rect(center=(largura_tela / 2, altura_tela / 5))
        tela.blit(texto_game_over_titulo, texto_game_over_titulo_rect)
        if mensagem_game_over_especifica:
            texto_razao_perdeu = fonteMensagemPerdeu.render(mensagem_game_over_especifica, True, preto)
            texto_razao_perdeu_rect = texto_razao_perdeu.get_rect(center=(largura_tela / 2, altura_tela / 5 + 80))
            tela.blit(texto_razao_perdeu, texto_razao_perdeu_rect)
        texto_sua_pontuacao = fontePontos.render(f"{nome_jogador_global} fez: {pontos_finais} rosquinhas", True, preto)
        texto_sua_pontuacao_rect = texto_sua_pontuacao.get_rect(center=(largura_tela / 2, altura_tela / 5 + 140))
        tela.blit(texto_sua_pontuacao, texto_sua_pontuacao_rect)
        jogarNovamenteButtonRect = pygame.Rect(pos_x_botao, pos_y_botao_jogar_novamente, larguraButton, alturaButton)
        pygame.draw.rect(tela, cor_botao, jogarNovamenteButtonRect, border_radius=15)
        texto_jogar_novamente = fonteMenu.render("Jogar Novamente", True, cor_texto_botao)
        texto_jogar_novamente_rect = texto_jogar_novamente.get_rect(center=jogarNovamenteButtonRect.center)
        tela.blit(texto_jogar_novamente, texto_jogar_novamente_rect)
        menuButtonRect = pygame.Rect(pos_x_botao, pos_y_botao_menu, larguraButton, alturaButton)
        pygame.draw.rect(tela, cor_botao, menuButtonRect, border_radius=15)
        texto_menu = fonteMenu.render("Menu Principal", True, cor_texto_botao)
        texto_menu_rect = texto_menu.get_rect(center=menuButtonRect.center)
        tela.blit(texto_menu, texto_menu_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if jogarNovamenteButtonRect.collidepoint(mouse_pos):
                        print("DEBUG: dead_screen chamando jogar()") # DEBUG
                        jogar()
                        print("DEBUG: jogar() retornou para dead_screen. Definindo rodando_dead = False.") # DEBUG
                        rodando_dead = False
                    if menuButtonRect.collidepoint(mouse_pos):
                        print("DEBUG: dead_screen chamando start_screen()") # DEBUG
                        start_screen()
                        print("DEBUG: start_screen() retornou para dead_screen. Definindo rodando_dead = False.") # DEBUG
                        rodando_dead = False
        pygame.display.update()
        relogio.tick(60)
    print(f"DEBUG: Fim do loop principal de dead_screen. rodando_dead = {rodando_dead}. Retornando de dead_screen().") # DEBUG
    return # Adicionado retorno explícito

if __name__ == '__main__':
    print("DEBUG: Iniciando o jogo, chamando start_screen() em __main__") # DEBUG
    start_screen()
    print("DEBUG: start_screen() retornou para __main__.") # DEBUG
    pygame.quit()
    print("DEBUG: pygame.quit() chamado em __main__.") # DEBUG
    sys.exit()

