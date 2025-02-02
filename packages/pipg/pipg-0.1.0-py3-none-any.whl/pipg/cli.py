import os
import subprocess
import sys


def colored_text(text, color):
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m",
    }
    return f"{colors[color]}{text}{colors['reset']}"


def is_package_installed(package_name):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def update_requirements(package_name, version):
    package_entry = f"{package_name}=={version}"
    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", "w") as f:
            f.write(package_entry + "\n")
        print(
            colored_text(
                f"PACOTE: {package_entry} registrado no requirements.txt", "green"
            )
        )
        return

    with open("requirements.txt", "r") as f:
        lines = f.readlines()

    updated = False
    with open("requirements.txt", "w") as f:
        for line in lines:
            if line.startswith(f"{package_name}=="):
                f.write(package_entry + "\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(package_entry + "\n")
            print(
                colored_text(
                    f"PACOTE: {package_entry} registrado no requirements.txt", "green"
                )
            )
        else:
            print(
                colored_text(
                    f"PACOTE: {package_entry} atualizado no requirements.txt", "yellow"
                )
            )


def install_package(package_name):
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name], check=True
        )
        print(colored_text(f"PACOTE: {package_name} instalado com sucesso!", "green"))
    except subprocess.CalledProcessError:
        print(colored_text(f"Erro ao instalar {package_name}", "red"))
        return

    package_name = package_name.split("==")[0]
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        print(
            colored_text(f"Erro ao obter informações do pacote {package_name}", "red")
        )
        return

    version = None
    for line in result.stdout.splitlines():
        if line.startswith("Version:"):
            version = line.split()[1]
            break

    if version:
        update_requirements(package_name, version)
    else:
        print(colored_text(f"Erro ao obter a versão do {package_name}", "red"))


def uninstall_package(package_name):
    package_name = package_name.split("==")[0]
    if not is_package_installed(package_name):
        print(colored_text(f"{package_name} não está instalado.", "yellow"))
        return

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", package_name], check=True
        )
        print(
            colored_text(f"PACOTE: {package_name} desinstalado com sucesso!", "green")
        )
    except subprocess.CalledProcessError:
        print(colored_text(f"Erro ao desinstalar {package_name}", "red"))
        return

    if os.path.exists("requirements.txt"):
        try:
            with open("requirements.txt", "r") as f:
                lines = f.readlines()

            with open("requirements.txt", "w") as f:
                for line in lines:
                    if not line.startswith(f"{package_name}=="):
                        f.write(line)
            print(
                colored_text(
                    f"PACOTE: {package_name} removido do requirements.txt", "green"
                )
            )
        except IOError:
            print(colored_text("Erro ao acessar o arquivo requirements.txt", "red"))
    else:
        print(colored_text("Nenhum requirements.txt encontrado.", "red"))


def main():
    if len(sys.argv) < 3:
        print(colored_text("Uso: pipg <install|uninstall> <pacote>", "red"))
        sys.exit(1)

    command, package_name = sys.argv[1], sys.argv[2]

    if command == "install":
        install_package(package_name)
    elif command == "uninstall":
        uninstall_package(package_name)
    else:
        print(
            colored_text(
                "Comando não reconhecido. Apenas 'install' e 'uninstall' são suportados.",
                "red",
            )
        )


if __name__ == "__main__":
    main()
