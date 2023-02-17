import httpx, sys
from colorama import Fore, Style
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--dL', '--domain-list', dest = 'file', metavar = "FILE")
parser.add_option('-u', '--url', dest = 'url', type = 'string')
parser.add_option('--no-error', dest = 'noerror', action='store_true')
(options, args) = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

def get_status_code(response):
    if response.status_code == 200:
        return f"{Fore.GREEN}{response.status_code}{Style.RESET_ALL}"
    elif response.status_code in [301, 302, 303, 307, 308, 300, 304]:
        return f"{Fore.BLUE}{response.status_code}{Style.RESET_ALL}"
    elif response.status_code in [401, 402, 407, 418, 419, 420, 422, 423, 424, 425, 426, 428, 429, 431, 440, 444, 449, 450, 451, 494, 495, 496, 497, 499]:
        return f"{Fore.YELLOW}{response.status_code}{Style.RESET_ALL}"
    elif response.status_code in [403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 421, 426, 428, 429, 431, 444, 449, 450, 451, 494, 495, 496, 497, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527]:
        return f"{Fore.RED}{response.status_code}{Style.RESET_ALL}"
    else:
        return f"{Fore.YELLOW}{response.status_code}{Style.RESET_ALL}"


def check_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    elif url.startswith("www."):
        url = "https://" + url
    return url
     
def domain_list(url_list):
    with open(url_list, 'r') as file:
        for line in file:
            domain = line.strip()
            url = check_http(domain)
            try:
                response = httpx.get(url, follow_redirects=True, verify=False)
                status = get_status_code(response)
                print(f"{response.url} - {status}")
            except httpx.HTTPError as exc:
                if options.noerror:
                    continue
                else:
                    print(f"Erro ao tentar acessar a URL {url}: {exc}")

def domain(domain):
    url = check_http(domain)
    try:
        response = httpx.get(url, follow_redirects=True, verify=False)
        status = get_status_code(response)
        print(f"{response.url} - {status}")
    except httpx.HTTPError as exc:
        print(f"Erro ao tentar acessar a URL {url}: {exc}")

try:
    if(options.url):
        domain(options.url)
    elif(options.file):
        domain_list(options.file)
except KeyboardInterrupt:
    print(f"{Fore.YELLOW}[!] The program was interrupted by the user.{Style.RESET_ALL}")
    sys.exit(1)
except EOFError:
    print(f"{Fore.YELLOW}[!] No input was received.{Style.RESET_ALL}")
    sys.exit(1)
except FileNotFoundError:
    print(f"{Fore.YELLOW}[!] The file or directory could not be found.{Style.RESET_ALL}")
    sys.exit(1)
except OSError:
    print(f"{Fore.YELLOW}[!] An operating system error occurred. The file or directory may not be accessible.{Style.RESET_ALL}")
    sys.exit(1)
except Exception:
    print(f"{Fore.YELLOW}[!] An unexpected error occurred. Please try again later.{Style.RESET_ALL}")
    sys.exit(1)

