import sys

from crawl import get_html

def main():
    argv_len = len(sys.argv)
    if  argv_len < 2:
        print("no website provided")
        return sys.exit(1)
    if argv_len > 2:
        print("too many arguments provided")
        return sys.exit(1)
    base_url = sys.argv[1]
    print(f"starting crawl of {base_url}")
    html = get_html(base_url)
    print("html", html)
    return sys.exit(0)


if __name__ == "__main__":
    main()
