from blinker import Namespace

signals = Namespace()

error_signal = signals.signal("error")


def error_signal_handler(sender, **extra):
    print(f"{sender} {extra}")


error_signal.connect(error_signal_handler)
