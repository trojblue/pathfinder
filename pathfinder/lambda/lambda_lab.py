import requests
import time
import unibox as ub
from tqdm.auto import tqdm

instance_mapping = {
    "8xh100": ["gpu_8x_h100_sxm5"],
    "1xh100": ["gpu_1x_h100_pcie"],
    "1xa100": ["gpu_1x_a100", "gpu_1x_a100_sxm4"],
}


"""
"gpu_8x_h100_sxm5"
"gpu_1x_rtx6000"
"gpu_1x_a100"
"gpu_1x_a100_sxm4"
"gpu_2x_a100"
"gpu_4x_a100"
"gpu_8x_a100"
"gpu_1x_a6000"
"gpu_2x_a6000"
"gpu_4x_a6000"
"gpu_8x_v100"
"""

class LambdaInstanceLauncher():
    """
    api_key_file: path to the api key file in txt, with a single line of the api key
    """

    API_BASE_URL = "https://cloud.lambdalabs.com/api/v1"
    REQUEST_TIMEOUT_SLEEP_TIME = 20

    def __init__(self, ssh_key_names: list, api_key_file: str):
        self.logger = ub.UniLogger()
        self.ssh_key_names = ssh_key_names
        self.api_key = ub.loads(api_key_file)[0]

    def _send_request(self, method, endpoint, **kwargs):
        """
        Send a request to the Lambda Labs API with error handling.
        """
        url = f"{self.API_BASE_URL}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Request error: {e}")
            return None
        except requests.exceptions.JSONDecodeError:
            self.logger.error(f"Response JSON decode error, sleeping {self.REQUEST_TIMEOUT_SLEEP_TIME} seconds")
            time.sleep(self.REQUEST_TIMEOUT_SLEEP_TIME)

    def get_instance_types(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.API_BASE_URL}/instance-types", headers=headers)
        return response.json().get('data', {})

    def launch_instance(self, region_name, instance_type_name, ssh_key_names, quantity, node_name):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "region_name": region_name,
            "instance_type_name": instance_type_name,
            "ssh_key_names": ssh_key_names,
            "quantity": quantity,
            "name": node_name
        }
        response = requests.post(f"{self.API_BASE_URL}/instance-operations/launch", headers=headers, json=payload)
        return response.json()

    def _snipe_instances(self, instance_types_list):
        instances = self.get_instance_types()

        for instance_type in instance_types_list:
            curr_meta = instances[instance_type]
            curr_available_regions = curr_meta["regions_with_capacity_available"]

            if curr_available_regions:
                launch_region_name = curr_available_regions[0]["name"]
                launch_response = self.launch_instance(launch_region_name, instance_type,
                                                       self.ssh_key_names, quantity=1, node_name="auto_launched_node")
                self.logger.info(f"launch_response: {launch_response}")
                exit(0)

    def snipe_instances(self, instance_types_list, sleep_time = 1):
        self.logger.info(f"sniping instances from {instance_types_list}")
        pbar = tqdm(desc=f"sniping instances")
        while True:
            self._snipe_instances(instance_types_list)
            pbar.update(1)
            time.sleep(sleep_time)

def launch_instance():
    launcher = LambdaInstanceLauncher(ssh_key_names=["yada"], api_key_file="yada-api-key2.txt")
    snipe_list = ["gpu_1x_h100_pcie", "gpu_1x_a100", "gpu_1x_a100_sxm4"]
    launcher.snipe_instances(snipe_list)


if __name__ == '__main__':
    launch_instance()
