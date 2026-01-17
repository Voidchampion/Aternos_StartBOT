    from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        print("Installing Chromium for Replit...")
        p.chromium.install()

if __name__ == "__main__":
    main()
