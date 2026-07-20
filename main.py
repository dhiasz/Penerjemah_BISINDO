from gui.main_window import MainWindow

class MainApp:
    def __init__(self):
        self.main_window = MainWindow()

    def run(self):
        self.main_window.run()

if __name__ == "__main__":
    app = MainApp()
    app.run()