from .anomaly import PumbaAnomaly


class CpuStressAnomaly(PumbaAnomaly):
    def __init__(self, config, name=""):
        self.pumba_command = "stress"
        super().__init__(config, name)

    def _construct_exec_string(self):
        self.exec_string = " ".join(["pumba",
                                     self.config["global_options"],
                                     self.pumba_command,
                                     "--stress-image  alexeiled/stress-ng:latest-ubuntu",
                                     self.config["command_options"],
                                     self.config["containers"]])
        print(self.exec_string)
