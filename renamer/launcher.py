from ui.main_window import RenamerMainWindow


WINDOW_INSTANCE = None


def show():
    global WINDOW_INSTANCE

    try:
        if WINDOW_INSTANCE:
            WINDOW_INSTANCE.close()
            WINDOW_INSTANCE.deleteLater()
    except:
        pass

    WINDOW_INSTANCE = RenamerMainWindow()
    WINDOW_INSTANCE.show()