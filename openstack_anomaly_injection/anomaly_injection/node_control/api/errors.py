class ContainerException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class NodeException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class DeploymentException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class NetworkException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class DriverException(BaseException):
    def __init__(self, msg):
        super().__init__(msg)
