Pygame_Simpsons jogo inspirado na temática "Os Simpsons", desenvolvido na Atitus educação

Desenvolvedor: Eduardo Barreda Mello

RA:1138704

📖 História do Jogo:
Tudo começou numa manhã comum em Springfield...
Homer Simpson acordou sonhando com uma chuva de rosquinhas. Ao abrir os olhos,
viu algo ainda mais incrível: as rosquinhas estavam realmente caindo do céu!
Mas nem tudo era doce. Lisa, preocupada com a saúde do pai, havia convencido
o Professor Frink a construir um canhão... de vegetais! Agora, enquanto o céu
despejava deliciosas rosquinhas, vegetais também
desciam em alta velocidade, tentando sabotar a comilança de Homer.

# 🍩 Pygame_Simpsons

Um jogo desenvolvido com Python e Pygame onde você controla o Homer e deve coletar rosquinhas enquanto evita os vegetais! Use comandos de voz, veja seu desempenho em tempo real e acompanhe o ranking dos maiores pontuadores.

---

## 🕹️ Como Jogar

- Use as **setas esquerda/direita** para mover o Homer.
- Pressione **espaço** para pausar o jogo.
- Evite brócolis e pegue o máximo de rosquinhas!
- O jogo só inicia após você dizer "rosquinhas "no microfone.

---

## 🚀 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/pygame_simpsons.git
cd pygame_simpsons
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

> Ou instale manualmente as principais bibliotecas listadas abaixo.

3. Execute o jogo:

```bash
python main.py
```

---

## 📦 Bibliotecas e Módulos Utilizados

### 🎮 `pygame`

Biblioteca principal usada para criação do jogo. Responsável por renderizar gráficos, capturar eventos do teclado e mouse, reproduzir sons e gerenciar a lógica da janela e do jogo.

```bash
pip install pygame
```

### 🎤 `speech_recognition`

Captura e interpreta comandos de voz do jogador ("eu amo rosquinhas").

```bash
pip install SpeechRecognition
```

### 🎤 `pyaudio`

Permite acesso ao microfone para captura de voz em tempo real.

```bash
pip install pyaudio
```

### 📆 `datetime`

Registra data e hora das partidas.

### 📂 `json`

Armazena e lê pontuações em arquivos estruturados (`log.dat`, `base.atitus`).

### 🕒 `time`, 📄 `os`

Utilizados para pausar o jogo e interagir com arquivos/sistema.

### 📦 `cx_Freeze` (opcional)

Para empacotar o jogo em executável `.exe` no Windows:

```bash
pip install cx_Freeze
```

---

## 🏆 Recursos Extras

- Tela de boas-vindas com nome personalizado
- Comando de voz para iniciar
- Registro automático de logs em `log.dat`
- Tela de morte com ranking dos 5 maiores
- Destaque visual para o campeão e jogador atual

---

## 📁 Estrutura de Pastas

```
pygame_simpsons/
├── main.py
├── recursos/
│   ├── funcoes.py
│   ├── assets/
│   │   ├── homer.png
│   │   ├── brocolis.png
│   │   ├── donut.png
│   │   ├── fundoStart.jpg
│   │   ├── fundoJogo.jpg
│   │   ├── doh_sound.mp3
│   │   └── simpsons_theme.mp3
├── base.atitus
├── log.dat
```

---

## 🙌 Créditos

- 👾 Desenvolvido por Eduardo Barreda
-     Inspirado nos personagens de *Os Simpsons* (uso não comercial)

- 👾 Testador do jogo: Diego Meira, RA: 1109435

---
