import json
import requests
from vectorshift.consts import (
    API_AUTOMATION_DELETE_ENDPOINT,
    API_AUTOMATION_DEPLOY_ENDPOINT,
    API_AUTOMATION_FETCH_ENDPOINT,
    API_AUTOMATION_GET_APPS_ENDPOINT,
    API_AUTOMATION_GET_PAYLOADS_ENDPOINT,
    API_AUTOMATION_GET_TRIGGERS_ENDPOINT,
    API_AUTOMATION_LIST_ENDPOINT,
    API_AUTOMATION_PROCESS_PAYLOADS_ENDPOINT,
    API_AUTOMATIONS_GET_EVENTS_ENDPOINT,
)
import vectorshift


class Automation:
    def __init__(
        self,
        name: str,
        description: str,
        app: dict,
        event: str,
        trigger: dict,
        pipeline: dict,
        mappings: list,
        id: str = None,
    ):
        """NOTE: Creating automations via the SDK is currently not supported."""
        self.id = id
        self.name = name
        self.description = description
        self.app = app
        self.event = event
        self.trigger = trigger
        self.pipeline = pipeline
        self.mappings = mappings

    def to_json_rep(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'app': self.app,
            'event': self.event,
            'trigger': self.trigger,
            'pipeline': self.pipeline,
            'mappings': self.mappings,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_json_rep(), indent=4)

    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'Automation':
        pipeline = json_data.get('pipeline', {})
        if pipeline is not None:
            pipeline = (pipeline.get('id'),)
        trigger = json_data.get('trigger', {})
        if trigger is not None:
            trigger = trigger.get('name')
        return Automation(
            id=json_data.get('id'),
            name=json_data.get('name'),
            description=json_data.get('description'),
            app=json_data.get('app'),
            event=json_data.get('event'),
            trigger=trigger,
            pipeline=pipeline,
            mappings=json_data.get('mappings'),
        )

    @staticmethod
    def from_json(json_str: str) -> 'Automation':
        json_data = json.loads(json_str)
        return Automation.from_json_rep(json_data)

    def __repr__(self) -> str:
        return str(self.to_json_rep())

    @staticmethod
    def fetch_all(
        api_key=None,
        public_key=None,
        private_key=None,
    ) -> list['Automation']:
        response = requests.get(
            API_AUTOMATION_LIST_ENDPOINT,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)

        automations = []
        for automation in response.json():
            print(automation)
            automations.append(Automation.from_json_rep(automation))
        return automations

    @staticmethod
    def fetch_json(
        automation_id: str = None,
        automation_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Fetches the JSON representation of an Automation from the VectorShift platform. Specify either the ID or the name. The JSON representation has a few additional metadata fields omitted in the Automation class.

        Parameters:
            automation_id: The ID of the Automation to fetch.
            automation_name: The name of the Automation to fetch.

        Returns:
            dict: The JSON representation of the fetched Automation.
        """
        if automation_id is None and automation_name is None:
            raise ValueError('Must specify either automation_id or automation_name.')

        params = {}
        if automation_id:
            params['automation_id'] = automation_id
        if automation_name:
            params['automation_name'] = automation_name

        response = requests.get(
            API_AUTOMATION_FETCH_ENDPOINT,
            params=params,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    @staticmethod
    def fetch(
        automation_id: str = None,
        automation_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> 'Automation':
        """Fetch an Automation from the VectorShift platform. Specify either the ID or the name.

        Parameters:
            automation_id: The ID of the Automation to fetch.
            automation_name: The name of the Automation to fetch.

        Returns:
            Automation: The fetched Automation object.
        """
        response = Automation.fetch_json(
            automation_id=automation_id,
            automation_name=automation_name,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return Automation.from_json_rep(response)

    def delete(self, api_key=None, public_key=None, private_key=None) -> str:
        print(self.id)
        response = requests.delete(
            f'{API_AUTOMATION_DELETE_ENDPOINT}/{self.id}',
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    @staticmethod
    def get_apps(
        api_key=None,
        public_key=None,
        private_key=None,
    ) -> list:
        response = requests.get(
            API_AUTOMATION_GET_APPS_ENDPOINT,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    @staticmethod
    def get_events(app_id: str, api_key=None, public_key=None, private_key=None) -> list:
        response = requests.get(
            f'{API_AUTOMATIONS_GET_EVENTS_ENDPOINT}/{app_id}',
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    @staticmethod
    def get_triggers(
        app_id: str, event: str, api_key=None, public_key=None, private_key=None
    ) -> list:
        response = requests.get(
            API_AUTOMATION_GET_TRIGGERS_ENDPOINT,
            params={
                'app_id': app_id,
                'event': event,
            },
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    def get_payloads(self, api_key=None, public_key=None, private_key=None) -> list:
        response = requests.get(
            f'{API_AUTOMATION_GET_PAYLOADS_ENDPOINT}/{self.id}',
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    def deploy(
        self, active: bool, api_key=None, public_key=None, private_key=None
    ) -> bool:
        response = requests.post(
            f'{API_AUTOMATION_DEPLOY_ENDPOINT}/{self.id}',
            data={'active': active},
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response

    def process_payloads(
        self,
        api_key=None,
        public_key=None,
        private_key=None,
    ):
        response = requests.post(
            API_AUTOMATION_PROCESS_PAYLOADS_ENDPOINT,
            data={
                'automation_id': self.id,
            },
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response
