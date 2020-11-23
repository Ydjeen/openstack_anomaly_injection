class Container:

    def __init__(self, id, host, image, command, created, status, ports, name, container_driver, network_driver,
                 *args, **kwargs):
        self.id = id
        self.host = host
        self.image = image
        self.command = command
        self.created = created
        self.status = status
        self.ports = ports
        self.name = name
        self.container_driver = container_driver
        self.network_driver = network_driver

    def start(self):
        self._check_driver(self.container_driver)
        self.container_driver.start(self.name, self.host)

    def stop(self):
        self._check_driver(self.container_driver)
        self.container_driver.stop(self.name, self.host)

    def terminate(self):
        self._check_driver(self.container_driver)
        self.container_driver.terminate(self.name, self.host)

    def restart(self):
        self._check_driver(self.container_driver)
        self.container_driver.restart(self.name, self.host)

    @staticmethod
    def _check_driver(driver):
        if driver is None:
            raise Exception("Driver must be provided in order to use this function")

    def __repr__(self):
        return self.id
