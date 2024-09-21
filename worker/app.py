import faust

app = faust.App(
    id='experiment-worker-python',
    autodiscover=True,
    origin='worker',
)


def main() -> None:
    app.main()
