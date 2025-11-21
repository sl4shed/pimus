class Services:
    config = None
    screen = None
    controller = None
    logger = None
    server = None
    bluetooth = None
    player = None
    app = None

    @classmethod
    def init(cls, **services):
        for name, service in services.items():
            setattr(cls, name, service)
