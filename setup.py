from cx_Freeze import setup, Executable
import os

# Garante que arquivos de recurso sejam incluídos
incluir_arquivos = [
    ("recursos", "recursos"),
    "base.atitus",
    "log.dat"
]

# Configurações do executável
executables = [
    Executable(
        script="main.py",
        icon="recursos/assets/icone.ico",
        base=None,
        target_name="HomerDonuts.exe"
    )
]

# Configuração final do setup
setup(
    name="Pygame_Simpsons",
    version="1.0",
    description="Jogo do Homer em Pygame com comandos de voz",
    options={
        "build_exe": {
            "packages": ["pygame", "speech_recognition", "pyaudio", "json", "datetime"],
            "include_files": incluir_arquivos,
            "include_msvcr": True
        }
    },
    executables=executables
)
