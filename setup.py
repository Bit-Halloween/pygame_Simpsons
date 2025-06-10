from cx_Freeze import setup, Executable
import os

executaveis = [
    Executable(
        script="main_simpsons_com_verduras_py.py",
        icon="recursos/assets/icone_simpsons.ico"
    )
]

setup(
    name="Paygame Simpsons",
    version="1.0",
    description="Jogo criado com Pygame",
    options={
        "build_exe": {
            "packages": ["pygame", "tkinter", "json", "random"],
            "include_files": [
                ("recursos/assets", "recursos/assets"),
                ("funcoes.py", "recursos/funcoes.py"),
                "base.atitus"
            ]
        }
    },
    executables=executaveis
)
# Este script é usado para empacotar o jogo usando cx_Freeze.
# Certifique-se de que cx_Freeze está instalado no seu ambiente Python.
# Você pode instalar cx_Freeze usando o comando: pip install cx_Freeze
# Para construir o executável, execute o seguinte comando no terminal:
# python setup.py build