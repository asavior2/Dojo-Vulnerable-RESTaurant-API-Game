import ast
import subprocess
import time
from os import listdir
from os.path import isfile, join

from colorama import Fore, Style

BASE_PATH = "app"
VULNS_TESTS_DIR = "tests/vulns/"
VULNS_TEST_FILES_PATHS = sorted(
    [
        join(VULNS_TESTS_DIR, f)
        for f in listdir(VULNS_TESTS_DIR)
        if isfile(join(VULNS_TESTS_DIR, f))
    ]
)


def run_tests(test_file_path=None):
    try:
        command = [
            "pytest",
            "--disable-warnings",
            "-qq",
        ]
        if test_file_path:
            command.append(test_file_path)

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        animation = "|/-\\"
        idx = 0
        print("  Ejecutando pruebas... Por favor espere...", end="\r")
        while process.poll() is None:
            print(animation[idx % len(animation)], end="\r")
            idx += 1
            time.sleep(0.1)

        stdout, stderr = process.communicate()

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    class TestsResult:
        def __init__(self, returncode, stdout, stderr):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    return TestsResult(process.returncode, stdout, stderr)


def is_vulnerability_fixed(test_file_path):
    result = run_tests(test_file_path)
    return (
        result.returncode == 1
    )  # Tests were collected and run but some of the tests failed


def get_unit_tests_suite_result():
    return run_tests()


def get_vuln_name(test_file_path):
    level_len = len("tests/vulns/level_")
    title_idx = test_file_path[level_len:].find("_") + 1
    return (
        test_file_path[level_len + title_idx :]
        .replace("_", " ")
        .replace(".py", "")
        .title()
    )


def get_level_number(test_file_path):
    level_len = len("tests/vulns/level_")
    number_idx = test_file_path[level_len:].find("_")
    return test_file_path[level_len : level_len + number_idx]


def get_level_title(test_file_path):
    level_number = get_level_number(test_file_path)
    vuln_name = get_vuln_name(test_file_path)

    return f"Level {level_number} - {vuln_name}"


def print_level_description(test_file_path):
    level_title = get_level_title(test_file_path)
    with open(test_file_path, "r") as source_file:
        source_code = source_file.read()
    tree = ast.parse(source_code)

    level_description = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            level_description = ast.get_docstring(node)

    if not level_description:
        raise Exception("¡No se proporcionan pistas!")

    print(level_title, end="\n\n")
    print(level_description, end="\n\n")

    full_test_file_path = join(BASE_PATH, test_file_path)
    print(
        f"Archivo de prueba que confirma la vulnerabilidad:\n    {full_test_file_path}",
        end="\n\n\n",
    )


def print_welcome_screen():
    print(Fore.GREEN, end="")
    print(
        """
            ¡Bienvenidos al DOJO Vulnerable RESTAurant!

            Iniciativa de ciberseguridad para promover el desarrollo seguro de aplicaciones web.

            Contexto:
            
            ¡Nuestro restaurante fue atacado recientemente por un actor de amenazas desconocido!
            La API y el sistema subyacente del restaurante se vieron comprometidos al explotar varias vulnerabilidades de seguridad.

            El propietario del restaurante, Mysterious Chef, quiere que
            investigue cómo sucedió y solucione las vulnerabilidades.
            El chef sospecha que los atacantes estaban asociados con el restaurante
            recién inaugurado ubicado al otro lado de la calle.

            Los atacantes dejaron pruebas que confirman los exploits que
            utilizaron para obtener acceso al sistema. Puede leer estas pruebas
            para comprender mejor la vulnerabilidad, pero no las modifique.

            Su tarea es solucionar las vulnerabilidades para asegurarse de que esas pruebas maliciosas ya no pasen. En los próximos pasos,
            obtendrá pistas de vulnerabilidad dejadas por los atacantes.
            Use esas pistas para implementar correcciones.
        """,
        end="\n\n",
    )
    print(Style.RESET_ALL, end="")


def print_congrats_screen():
    print(Fore.GREEN, end="")
    print(
        """
            ¡Felicitaciones! ¡Excelente trabajo!

            ¡Pudiste reparar todas las vulnerabilidades explotadas
            durante el ataque!

            Sin embargo, somos conscientes de otras vulnerabilidades en el sistema.
            Además, hay una vulnerabilidad más que permite ejecutar
            comandos en el servidor como usuario root, pero debes encontrarla
            por tu cuenta :)

            Recuerda... estas vulnerabilidades se implementaron y se te proporcionaron
            con fines de aprendizaje, no uses este conocimiento para atacar
            servicios que no son de tu propiedad o para los que no tienes permisos
            para hacerlo.

            Un gran poder conlleva una gran responsabilidad...
        """
    )
    print(Style.RESET_ALL, end="")


def press_key_to_continue(text, color=Fore.YELLOW, end="\n"):
    print(color, end="")
    input(text + end)
    print(Style.RESET_ALL, end="")


def print_color_text(text, color, end="\n"):
    print(color, end="")
    print(text, end=end)
    print(Style.RESET_ALL, end="")


def move_cursor_top(lines=1):
    for line in range(lines):
        print("\033[1A\033[K", end="")


print_welcome_screen()
press_key_to_continue("Haga clic en cualquier tecla para continuar...", end="\n\n")

for i, level_test_file in enumerate(VULNS_TEST_FILES_PATHS, start=1):
    vuln_name = get_vuln_name(level_test_file)
    is_vuln_fixed = is_vulnerability_fixed(level_test_file)
    unit_tests_result = get_unit_tests_suite_result()
    is_working_fine = unit_tests_result.returncode == 0
    first_try = True

    if is_vuln_fixed and is_working_fine:
        print_color_text(
            f'¡Felicitaciones! Has solucionado la vulnerabilidad. "{vuln_name}"',
            color=Fore.GREEN,
            end="\n\n",
        )
    else:
        print_level_description(level_test_file)

    while not is_vuln_fixed or not is_working_fine:
        if is_vuln_fixed and not is_working_fine:
            unit_tests_result_out = unit_tests_result.stdout.replace("\n", "\n\r")
            print_color_text(
                unit_tests_result_out,
                color=Fore.RED,
                end="\n\r\n\r",
            )
            logs_lines_count = unit_tests_result_out.count("\n\r")
            print_color_text(
                f"¡La vulnerabilidad parece estar solucionada! Sin embargo, la función no funciona correctamente. Revise los registros de pruebas unitarias anteriores...",
                color=Fore.RED,
                end="\n\r",
            )
            press_key_to_continue(
                "Solucione el problema y presione cualquier tecla para validar...",
                end="\r\r",
            )
            move_cursor_top(logs_lines_count + 4)
        elif not is_vuln_fixed:
            if first_try:
                press_key_to_continue(
                    "Solucione la vulnerabilidad y presione cualquier tecla para validar la solución...",
                    end="\r\r",
                )
                move_cursor_top()
            else:
                press_key_to_continue(
                    """Lamentablemente la vulnerabilidad aún no se ha solucionado.
Solucione la vulnerabilidad y presione cualquier tecla para validar la solución...""",
                    color=Fore.RED,
                    end="\r\r",
                )
                move_cursor_top(2)

        first_try = False
        is_vuln_fixed = is_vulnerability_fixed(level_test_file)
        unit_tests_result = get_unit_tests_suite_result()
        is_working_fine = unit_tests_result.returncode == 0

        if is_vuln_fixed and is_working_fine:
            print_color_text(
                f'¡Felicitaciones! Has solucionado la vulnerabilidad "{vuln_name}"',
                color=Fore.GREEN,
                end="\n\n",
            )
            press_key_to_continue("Haga clic en cualquier tecla para continuar...", end="\n\n")
            first_try = True

    if i == len(VULNS_TEST_FILES_PATHS):
        print_congrats_screen()
