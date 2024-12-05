from proton.runner.run import run


class App:

    def greet(self):
        return "Hello"


app = App()

if __name__ == "__main__":
    run(app)
