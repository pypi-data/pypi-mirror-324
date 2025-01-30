from cyclarity_in_vehicle_sdk.configuration_manager.configuration_manager import ConfigurationManager
from cyclarity_sdk.expert_builder import Runnable, BaseResultsModel

class Results(BaseResultsModel):
    pass


class ConfigurationManagerRunnable(Runnable[Results]):
    cm: ConfigurationManager

    def setup(self):
        self.cm.setup()

    def run(self) -> Results:
        return Results()

    def teardown(self, exception_type, exception_value, traceback):
        self.cm.teardown()

if __name__ == "__main__":
    from cyclarity_sdk.expert_builder import run_from_cli
    run_from_cli(ConfigurationManagerRunnable)