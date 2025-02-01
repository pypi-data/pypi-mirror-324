# functionality for defining and working with Vector Store objects
import requests
import json

import vectorshift
from vectorshift.pipeline import Pipeline
from vectorshift.consts import (
    API_CHATBOT_FETCH_ENDPOINT,
    API_CHATBOT_RUN_ENDPOINT,
)


# TODO: Potentially change to inherit from Pydantic BaseModel
class Chatbot:
    def __init__(
        self,
        name: str,
        description: str = '',
        pipeline: Pipeline = None,
        input: str = None,
        output: str = None,
        id: str = None,
    ):
        """Create a new Chatbot object.

        Parameters:
            name (str): The name of the Chatbot.
            description (str): The description of the Chatbot.
            pipeline (Pipeline): The Pipeline object the Chatbot uses.
            input (str): The input the Chatbot expects.
            output (str): The output the Chatbot expects.
            id (str): The ID of the Chatbot to replace (if replacing an existing Chatbot).

        Returns:
            Chatbot: A new Chatbot object.
        """
        self.name = name
        self.description = description
        self.pipeline = pipeline
        self.input = input
        self.output = output
        self.id = id

    # converts Chatbot object to JSON representation
    def to_json_rep(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'pipeline': self.pipeline.to_json_rep() if self.pipeline else None,
            'input': self.input,
            'output': self.output,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_json_rep())

    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'Chatbot':
        return Chatbot(
            name=json_data.get('name'),
            description=json_data.get('description'),
            pipeline=json_data.get('pipeline'),
            input=json_data.get('input'),
            output=json_data.get('output'),
            id=json_data.get('id'),
        )

    @staticmethod
    def from_json(json_str: str) -> 'Chatbot':
        json_data = json.loads(json_str)
        return Chatbot.from_json_rep(json_data)

    def __repr__(self):
        # TODO: format this reprerentation to be more readable
        return f'Chatbot({", ".join(f"{k}={v}" for k, v in self.to_json_rep().items())})'

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        self.description = description

    # TODO: Add validation for chatbot_id and pipeline_id (in pipeline.py)
    # to prevent 5XX errors
    @staticmethod
    def fetch_json(
        chatbot_id: str = None,
        chatbot_name: str = None,
        username: str = None,
        org_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Fetches the JSON representation of an existing Chatbot from the VectorShift platform. Specify the chatbot_id or chatbot_name. The JSON representation has a few additional metadata fields omitted in the Chatbot class.

        Parameters:
            chatbot_id (str): The ID of the Chatbot to fetch.
            chatbot_name (str): The name of the Chatbot to fetch.
            username (str): The username of the user who owns the Chatbot.
            org_name (str): The name of the organization who owns the Chatbot.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication.
            private_key (str): The private key to use for authentication.

        Returns:
            dict: The JSON representation of the fetched Chatbot.
        """
        if chatbot_id is None and chatbot_name is None:
            raise ValueError('Must specify either chatbot_id or chatbot_name.')
        if chatbot_name is not None and username is None and org_name is not None:
            raise ValueError('Must specify username if org_name is specified.')

        params = {}
        if chatbot_id:
            params['chatbot_id'] = chatbot_id
        if chatbot_name:
            params['chatbot_name'] = chatbot_name

        response = requests.get(
            API_CHATBOT_FETCH_ENDPOINT,
            params=params,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching chatbot object: {response.text}')
        return response.json()

    @staticmethod
    def fetch(
        chatbot_name: str = None,
        chatbot_id: str = None,
        username: str = None,
        org_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> 'Chatbot':
        """Fetch an existing Chatbot from the VectorShift platform. Specify the chatbot_id or chatbot_name.

        Parameters:
            chatbot_id (str): The ID of the Chatbot to fetch.
            chatbot_name (str): The name of the Chatbot to fetch.
            username (str): The username of the user who owns the Chatbot.
            org_name (str): The name of the organization who owns the Chatbot.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication.
            private_key (str): The private key to use for authentication.

        Returns:
            Chatbot: The fetched Chatbot object.
        """
        response = Chatbot.fetch_json(
            chatbot_id=chatbot_id,
            chatbot_name=chatbot_name,
            username=username,
            org_name=org_name,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        response['pipeline'] = Pipeline.fetch(
            pipeline_id=response.get('pipeline', {}).get('id')
        )

        return Chatbot.from_json_rep(response)

    # TODO: Build functionality alongside FastAPI endpoint
    def save(
        self,
        update_existing: bool = False,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Save a Chatbot to the VectorShift platform.

        Parameters:
            update_existing (bool): Whether to update an existing Chatbot or create a new one.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication if applicable.
            private_key (str): The private key to use for authentication if applicable.

        Returns:
            dict: The JSON response including the saved Chatbot object.
        """
        raise NotImplementedError('Chatbot.save() is not yet implemented.')

    def run(
        self,
        input: str,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Run a Chatbot on the VectorShift platform.

        Parameters:
            input (str): The input to send to the Chatbot.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication if applicable.
            private_key (str): The private key to use for authentication if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError('Chatbot must be saved before it can be run.')
        response = requests.post(
            API_CHATBOT_RUN_ENDPOINT,
            data=(
                {
                    'chatbot_id': self.id,
                    'input': input,
                }
            ),
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
