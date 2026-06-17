print("Начало загрузки...")

from .tui import TUI
print("TUI импортирован")

def main():
    print("Запуск main()")
    app = TUI()
    app.run()

if __name__ == "__main__":
    print("Условие name сработало")
    main()