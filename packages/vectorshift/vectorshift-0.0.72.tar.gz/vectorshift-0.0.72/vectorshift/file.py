import json
import mimetypes
import requests

import vectorshift
from vectorshift.consts import *
from vectorshift.node_utils import *


class File:
    def __init__(
        self,
        id: str = None,
        name: str = '',
        file_key: str = '',
        filetype: str = '',
        user_id: str = None,
        org_id: str = 'Personal',
        upload_date: str = None,
    ):
        """Reference an existing file on the VectorShift platform. A File object serves purely as a reference to an existing file and does not contain the contents of the file itself, nor does it represent a file object on your computer. To fetch the details of a file from the platform, use the File.fetch() method. To save a file to the platform, use the File.upload() method. To download a file from the platform, use the File.download() method."""
        self.id = id
        self.name = name
        self.file_key = file_key
        self.filetype = filetype
        self.user_id = user_id
        self.org_id = org_id
        self.upload_date = upload_date

    def __repr__(self):
        return f'<File with JSON representation: {json.dumps(self.to_json_rep())}>'

    def __str__(self):
        return f"(file id {self.id})=File(\n\
    id={self.id},\n\
    name='{self.name}',\n\
    file_key='{self.file_key}',\n\
    filetype='{self.filetype}',\n\
    user_id={self.user_id},\n\
    org_id={self.org_id},\n\
    upload_date={self.upload_date},\n\
)"

    def construction_str(self, indicate_id: bool = True) -> str:
        return f"file=File(\n\
    id={self.id if indicate_id else None},\n\
    name='{self.name}',\n\
    file_key='{self.file_key}',\n\
    filetype='{self.filetype}',\n\
    user_id={self.user_id if indicate_id else None},\n\
    org_id={self.org_id if indicate_id else None},\n\
    upload_date={self.upload_date if indicate_id else None},\n\
)"

    def to_json_rep(self) -> dict[str, any]:
        return {
            'id': self.id,
            'name': self.name,
            'fileKey': self.file_key,
            'type': self.filetype,
            'userID': self.user_id,
            'orgID': self.org_id,
            'uploadDate': self.upload_date,
            'category': 'File',
        }

    def to_json(self) -> str:
        return json.dumps(self.to_json_rep())

    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'File':
        """Converts a JSON representation of a file on the VectorShift platform into a File object. The opposite of to_json_rep.

        Parameters:
            json_data (dict[str, any]): A JSON representation of a file.

        Returns:
            File: A File object.
        """
        id = json_data.get('id')
        if not id and '_id' in json_data:
            id = str(json_data.get('_id'))
        return File(
            id=id,
            name=json_data.get('name'),
            file_key=json_data.get('fileKey'),
            filetype=json_data.get('type'),
            user_id=json_data.get('userID'),
            org_id=json_data.get('orgID'),
            upload_date=json_data.get('uploadDate'),
        )

    @staticmethod
    def from_json(json_str: str) -> 'File':
        """Converts a JSON string of a file on the VectorShift platform into a File object. The opposite of to_json.

        Parameters:
            json_str (str): A JSON string representing a file.

        Returns:
            File: A File object.
        """
        json_data = json.loads(json_str)
        return File.from_json_rep(json_data)

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_file_key(self) -> str:
        return self.file_key

    def get_filetype(self) -> str:
        return self.filetype

    def get_user_id(self) -> str:
        return self.user_id

    def get_org_id(self) -> str:
        return self.org_id

    def get_upload_date(self) -> str:
        return self.upload_date

    @staticmethod
    def fetch_json(
        file_id: str = None,
        file_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Fetches the JSON representation of a file from the VectorShift platform. Specify either the ID or the name.

        Parameters:
            file_id: The ID of the file to fetch.
            file_name: The name of the file to fetch.

        Returns:
            dict: The JSON representation of the fetched file.
        """
        if file_id is None and file_name is None:
            raise ValueError('At least one of the file ID or name must be specified.')
        params = {}
        if file_id is not None:
            params = [('file_ids', file_id)]
            response = requests.get(
                API_FILE_FETCH_BY_ID_ENDPOINT,
                params=params,
                headers={
                    'Api-Key': api_key or vectorshift.api_key,
                    'Public-Key': public_key or vectorshift.public_key,
                    'Private-Key': private_key or vectorshift.private_key,
                },
            )
            if response.status_code != 200:
                raise Exception(response.text)
            response_json = response.json()
            return response_json[0]
        else:
            params = [('file_names', file_name)]
            response = requests.get(
                API_FILE_FETCH_ENDPOINT,
                params=params,
                headers={
                    'Api-Key': api_key or vectorshift.api_key,
                    'Public-Key': public_key or vectorshift.public_key,
                    'Private-Key': private_key or vectorshift.private_key,
                },
            )
            if response.status_code != 200:
                raise Exception(response.text)
            response_json = response.json()
            return response_json[0]

    @staticmethod
    def fetch(
        file_id: str = None,
        file_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> 'File':
        """Fetch a file from the VectorShift platform. Specify either the ID or the name.

        Parameters:
            file_id: The ID of the file to fetch.
            file_name: The name of the file to fetch.

        Returns:
            File: The fetched file object.
        """
        response = File.fetch_json(
            file_id=file_id,
            file_name=file_name,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return File.from_json_rep(response)

    @staticmethod
    def fetch_all_json(
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list[dict]:
        """Fetch all user files from the VectorShift platform.

        Returns:
            list[File]: The JSON representation of the fetched files.
        """
        response = requests.get(
            API_FILE_FETCH_ALL_ENDPOINT,
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
    def fetch_all(
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list['File']:
        """Fetch all user files from the VectorShift platform.

        Returns:
            list[File]: The fetched files.
        """
        response = File.fetch_all_json(
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return [File.from_json_rep(file) for file in response]

    @staticmethod
    def fetch_by_ids_json(
        file_ids: list[str],
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list[dict]:
        """Fetch user files from the VectorShift platform based on their file IDs.

        Parameters:
            file_ids: The file IDs to fetch.

        Returns:
            list[File]: The JSON representation of the fetched files.
        """
        params = []
        for f_id in file_ids:
            params.append(('file_ids', f_id))
        response = requests.get(
            API_FILE_FETCH_BY_ID_ENDPOINT,
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
    def fetch_by_ids(
        file_ids: list[str],
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list['File']:
        """Fetch user files from the VectorShift platform based on their file IDs.

        Parameters:
            file_ids: The file IDs to fetch.

        Returns:
            list[File]: The fetched files.
        """
        response = File.fetch_by_ids_json(
            file_ids=file_ids,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return [File.from_json_rep(file) for file in response]

    @staticmethod
    def fetch_by_names_json(
        file_names: list[str],
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list[dict]:
        """Fetch user files from the VectorShift platform based on their file names.

        Parameters:
            file_names: The file names to fetch.

        Returns:
            list[dict]: The JSON representations of the fetched files.
        """
        params = []
        for f_name in file_names:
            params.append(('file_names', f_name))
        response = requests.get(
            API_FILE_FETCH_ENDPOINT,
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
    def fetch_by_names(
        file_names: list[str],
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list['File']:
        """Fetch user files from the VectorShift platform based on their file names.

        Parameters:
            file_names: The file names to fetch.

        Returns:
            list[dict]: The fetched files.
        """
        response = File.fetch_by_names_json(
            file_names=file_names,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return [File.from_json_rep(file) for file in response]

    @staticmethod
    def upload_file(
        file: str,
        folder_id: str = None,
        filetype: str = None,
        return_json: bool = False,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ):
        """Upload a file to the VectorShift platform.

        Parameters:
            file (str): The (local) path to the file to upload. Note that the value of the path will be the name of the file on the VectorShift platform.
            folder_id (str): The ID of the folder to upload the file to. Defaults to None.
            filetype (str): The file type of the file. Defaults to None.
            return_json (bool): Whether or not to return the JSON response from the VectorShift platform. Defaults to False.
            api_key (str): The API key to use. Defaults to None.
            public_key (str): The public key to use. Defaults to None.
            private_key (str): The private key to use. Defaults to None.

        Returns:
            If return_json is True: dict: The JSON response from the VectorShift platform, including the representation of the uploaded file.
            If return_json is False: File: The representation of the uploaded file.
        """
        try:
            headers = {
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
            # infer the file type
            if filetype is None:
                filetype = mimetypes.guess_type(file)[0]
            if filetype is None:
                raise ValueError(
                    f'Could not determine file type of {file}. Please ensure the file name has an appropriate suffix.'
                )

            if not os.path.exists(file):
                raise ValueError(f'File with path {file} does not exist.')
            if os.path.getsize(file) > MAX_FILE_UPLOAD_SIZE:
                raise ValueError(f'File with path {file} is too large to upload.')
            with open(file, 'rb') as f:
                files = {'file': (file, f, filetype)}
                response = requests.post(
                    API_FILE_UPLOAD_ENDPOINT,
                    data={'folderId': folder_id},
                    headers=headers,
                    files=files,
                )
        except Exception as e:
            raise ValueError(f'Problem uploading file: {e}')
        response_json = response.json()
        # API currently returns a singleton list
        response_json = response_json[0]
        uploaded_filename = next(iter(response_json.get('uploaded_files', [])), {}).get(
            'name'
        )
        if uploaded_filename:
            print(f'Successfully uploaded file as {uploaded_filename}.')
        if return_json:
            return response_json
        if 'content' not in response_json:
            raise ValueError(
                f'Problem retrieving uploaded file. JSON response: {response_json}'
            )
        return File.from_json_rep(response_json['content'])

    @staticmethod
    def download_file(
        file_id: str,
        download_url: bool = False,
        destination_file: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ):
        """Download a file from the VectorShift platform.

        Parameters:
            file_id (str): The ID of the file to download.
            download_url (bool): Whether or not to return the URL of the file (instead of raw bytes). Defaults to False.
            destination_file (str): A file path, if you wish to write the file to a local file. Ignored if download_url is True. Defaults to None.
            api_key (str): The API key to use. Defaults to None.
            public_key (str): The public key to use. Defaults to None.
            private_key (str): The private key to use. Defaults to None.

        Returns:
            The returned result depends on the parameters.
            If download_url is True: dict: The JSON response from the VectorShift platform, including the URL of the file.
            If download_url is False and destination_file is not None: None (the file is written to the path given by destination_file).
            Else: bytes: The bytes of the downloaded file.
        """
        response = requests.get(
            API_FILE_DOWNLOAD_ENDPOINT + f'/{file_id}',
            params={'download_url': download_url},
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        if download_url:
            return response.json()
        if destination_file:
            with open(destination_file, 'wb') as f:
                f.write(response.content)
            return None
        return response.content

    def download(self, download_url: bool = False, destination_file: str = None):
        '''Download a file from the VectorShift platform. Analogous to the File.download_file method.'''
        return File.download_file(
            file_id=self.id, download_url=download_url, destination_file=destination_file
        )

    # NB probably nicer to call using deploy.py
    def delete(
        self, api_key: str = None, public_key: str = None, private_key: str = None
    ) -> dict:
        """Delete a file on the VectorShift platform. The Config object in the vectorshift.deploy module can be alternatively used. This method clears information associated with the object.

        Parameters:
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'File object does not have an ID and so does not correspond to a file on the VectorShift platform.'
            )
        headers = {
            'Api-Key': api_key or vectorshift.api_key,
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }
        response = requests.delete(
            API_FILE_DELETE_ENDPOINT,
            data={'file_ids': [self.id]},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        # reset variables
        self.id = (None,)
        self.name = ('',)
        self.file_key = ''
        self.filetype = ''
        self.user_id = (None,)
        self.org_id = 'Personal'
        self.upload_date = None
        print('Successfully deleted file.')
        return response.json()

    @staticmethod
    def delete_by_ids(
        file_ids: list,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ):
        """Delete user files from the VectorShift platform based on their file IDs.

        Parameters:
            file_ids: The file IDs to delete.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        headers = {
            'Api-Key': api_key or vectorshift.api_key,
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }
        response = requests.delete(
            API_FILE_DELETE_ENDPOINT,
            data={'file_ids': file_ids},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        print('Successfully deleted file(s).')
        return response.json()

    @staticmethod
    def delete_by_names(
        file_names: list,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ):
        """Delete user files from the VectorShift platform based on their file names.

        Parameters:
            file_names: The file names to delete.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        headers = {
            'Api-Key': api_key or vectorshift.api_key,
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }
        response = requests.delete(
            API_FILE_DELETE_BY_NAMES_ENDPOINT,
            data={'file_names': file_names},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        print('Successfully deleted file(s).')
        return response.json()
