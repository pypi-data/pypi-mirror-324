# functionality for defining and working with Knowledge Base (Vector Store) objects
import os
from typing import Optional
import requests
import json

import vectorshift
from vectorshift.consts import *


class KnowledgeBase:
    # initializes a new Knowledge Base
    # TODO: add support for alpha here (and the corresponding node method from_knowledge_base_obj)
    def __init__(
        self,
        name: str,
        description: str = '',
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        is_hybrid: bool = False,
        id: str = None,
    ):
        """Create a new Knowledge Base.

        Parameters:
            name (str): The name of the Knowledge Base.
            description (str): The description of the Knowledge Base.
            chunk_size (int): The chunk size of the Knowledge Base (the default size, in bytes, of each unit of information uploaded).
            chunk_overlap (int): The chunk overlap of the Knowledge Base (the default number of bytes of overlap between each unit of information uploaded).
            is_hybrid (bool): Whether the Knowledge Base is supports hybrid search.
            id (str): The ID of the Knowledge Base to replace (if replacing an existing Knowledge Base).

        Returns:
            KnowledgeBase: A new Knowledge Base object.
        """
        self.name = name
        self.description = description
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.is_hybrid = is_hybrid
        self.id = id

    # converts Knowledge Base object to JSON representation
    def to_json_rep(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'chunkSize': self.chunk_size,
            'chunkOverlap': self.chunk_overlap,
            'isHybrid': self.is_hybrid,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_json_rep())

    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'KnowledgeBase':
        return KnowledgeBase(
            name=json_data.get('name'),
            description=json_data.get('description'),
            chunk_size=json_data.get('chunkSize', DEFAULT_CHUNK_SIZE),
            chunk_overlap=json_data.get('chunkOverlap', DEFAULT_CHUNK_OVERLAP),
            is_hybrid=json_data.get('isHybrid', False),
            id=json_data.get('id'),
        )

    @staticmethod
    def from_json(json_str: str) -> 'KnowledgeBase':
        json_data = json.loads(json_str)
        return KnowledgeBase.from_json_rep(json_data)

    def __repr__(self):
        return f'KnowledgeBase({", ".join(f"{k}={v}" for k, v in self.to_json_rep().items())})'

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str):
        self.description = description

    def get_chunk_size(self) -> int:
        return self.chunk_size

    def set_chunk_size(self, chunk_size: int):
        self.chunk_size = chunk_size

    def get_chunk_overlap(self) -> int:
        return self.chunk_overlap

    def set_chunk_overlap(self, chunk_overlap: int):
        self.chunk_overlap = chunk_overlap

    # TODO: Add validation for base_id and pipeline_id (in pipeline.py)
    # to prevent 5XX errors
    @staticmethod
    def fetch_json(
        base_id: str = None,
        base_name: str = None,
        username: str = None,
        org_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Fetches the JSON representation of a Knowledge Base from the Vectorshift API. The JSON representation has a few additional metadata fields omitted in the KnowledgeBase class.

        Parameters:
            base_id (str): The ID of the Knowledge Base to fetch.
            base_name (str): The name of the Knowledge Base to fetch.
            username (str): The username of the user who owns the Knowledge Base.
            org_name (str): The organization name of the user who owns the Knowledge Base.
            api_key (str): The API key of the user who owns the Knowledge Base.

        Returns:
            dict: The JSON representation of the fetched Knowledge Base.
        """
        if base_id is None and base_name is None:
            raise ValueError('Must specify either base_id or base_name.')
        if base_name is not None and username is None and org_name is not None:
            raise ValueError('Must specify username if org_name is specified.')

        params = {}
        if base_id is not None:
            params['vectorstore_id'] = base_id
        if base_name is not None:
            params['vectorstore_name'] = base_name
        if username is not None:
            params['username'] = username
        if org_name is not None:
            params['org_name'] = org_name

        response = requests.get(
            API_VECTORSTORE_FETCH_ENDPOINT,
            params=params,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching Knowledge Base object: {response.text}')
        return response.json()

    @staticmethod
    def fetch(
        base_id: str = None,
        base_name: str = None,
        username: str = None,
        org_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> 'KnowledgeBase':
        """Fetch a Knowledge Base from the Vectorshift API.

        Parameters:
            base_id (str): The ID of the Knowledge Base to fetch.
            base_name (str): The name of the Knowledge Base to fetch.
            username (str): The username of the user who owns the Knowledge Base.
            org_name (str): The organization name of the user who owns the Knowledge Base.
            api_key (str): The API key of the user who owns the Knowledge Base.

        Returns:
            KnowledgeBase: A new Knowledge Base object.
        """
        response = KnowledgeBase.fetch_json(
            base_id=base_id,
            base_name=base_name,
            username=username,
            org_name=org_name,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return KnowledgeBase.from_json_rep(response)

    def save(
        self,
        update_existing: bool = False,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Save a Knowledge Base to the Vectorshift platform.

        Parameters:
            update_existing (bool): Whether to update an existing Knowledge Base or create a new one.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication, if applicable.
            private_key (str): The private key to use for authentication, if applicable.

        Returns:
            dict: The response from the Vectorshift platform.
        """
        if update_existing and not self.id:
            raise ValueError(
                "Error updating: KnowledgeBase object does not have an existing ID. It must be saved as a new Knowledge Base."
            )
        # if update_existing is false, save as a new knowledge base
        if not update_existing:
            self.id = None

        # API_VECTORSTORE_SAVE_ENDPOINT handles saving and updating knowledge bases
        # depending on whether or not the JSON has an id (logic in api repo)
        response = requests.post(
            API_VECTORSTORE_SAVE_ENDPOINT,
            data=({'vectorstore': self.to_json()}),
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )

        if response.status_code != 200:
            raise Exception(f'Error saving Knowledge Base object: {response.text}')
        response = response.json()
        # TODO shouldn't have to use two 'get's here
        self.id = response.get('id').get('id')

        return response

    def update_metadata(
        self,
        list_of_item_ids: list[str],
        list_of_metadata: list[str],
        keep_prev: bool,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        """Update the metadata of a list of items in the Knowledge Base by their IDs.

        Parameters:
            list_of_item_ids (list[str]): A list of item IDs to update.
            list_of_metadata (list[str]): A list of metadata to update the items with.
            keep_prev (bool): Whether to keep the previous metadata of the items.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication, if applicable.
            private_key (str): The private key to use for authentication, if applicable.

        Returns:
            None
        """
        if not self.id:
            raise ValueError(
                "Error updating: Knowledge Base object does not have an existing ID. It must be saved first."
            )

        data = {
            'vectorstore_id': self.id,
            'list_of_item_ids': list_of_item_ids,
            'list_of_metadata': [json.dumps(metadata) for metadata in list_of_metadata],
            'keep_prev': keep_prev,
        }

        response = requests.post(
            API_VECTORSTORE_UPDATE_METADATA_ENDPOINT,
            data=data,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )

        if response.status_code != 200:
            raise Exception(f'Error updating document(s) metadata: {response.text}')
        return

    def update_selected_files(
        self,
        integration_id: str,
        keep_prev: bool,
        selected_items: Optional[list[str]] = None,
        select_all_items_flag: Optional[bool] = True,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        """Update items associated with an Integration in the Knowledge Base, pulling new data from the Integration into the Knowledge Base.

        Parameters:
            integration_id (str): The ID of the integration to update.
            keep_prev (bool): Whether to keep the previous data from the Integration.
            selected_items (list[str], optional): A list of item IDs to update. Defaults to None.
            select_all_items_flag (bool, optional): Whether to select all items in the Integration. Defaults to True.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication, if applicable.
            private_key (str): The private key to use for authentication, if applicable.

        Returns:
            None
        """
        if not self.id:
            raise ValueError(
                "Error updating: Knowledge Base object does not have an existing ID. It must be saved first."
            )

        data = {
            'vectorstore_id': self.id,
            'integration_id': integration_id,
            'selected_items': selected_items,
            'keep_prev': keep_prev,
            'select_all_items_flag': select_all_items_flag,
        }

        response = requests.post(
            API_VECTORSTORE_UPDATE_SELECTED_ITEMS_ENDPOINT,
            data=data,
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )

        if response.status_code != 200:
            raise Exception(f'Error updating items selected: {response.text}')
        return

    # TODO: endpoint does not exist
    '''
    def sync(
        self,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        if not self.id:
            raise ValueError('Error loading documents: Knowledge Base object does not have an existing ID. It must be saved as a new Knowledge Base.')

        response = requests.post(
            API_VECTORSTORE_SYNC_ENDPOINT,
            data={
                'vectorstore_id': self.id,
            },
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)

        response = response.json()
        return
    '''

    def load_documents(
        self,
        document,
        document_name: str = None,
        document_type: str = 'File',
        chunk_size: int = None,
        chunk_overlap: int = None,
        selected_items: list = None,
        select_all_items_flags: list = None,
        metadata: dict = None,
        metadata_by_item: dict = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Load documents into the Knowledge Base. Currently, only local files and URLs are officially supported from the SDK.

        Parameters:
            document (str): The path to the document to load or a URL whose contents are to be loaded.
            document_name (str, optional): The name of the document loaded.
            document_type (str, optional): The type of the document to load. Defaults to 'File'. Can also be "URL" or "Recursive URL".
            chunk_size (int, optional): The size of the chunks to load.
            chunk_overlap (int, optional): The overlap between chunks.
            selected_items (list, optional): A list of item IDs to load.
            select_all_items_flags (list, optional): A list of flags indicating whether to select all items in the document.
            metadata (dict, optional): A dictionary of metadata to associate with the document.
            metadata_by_item (dict, optional): A dictionary of metadata to associate with each item in the document.
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication, if applicable.
            private_key (str): The private key to use for authentication, if applicable.

        Returns:
            dict: The server response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Error loading documents: Knowledge Base object does not have an existing ID. It must be saved as a new Knowledge Base.'
            )

        if document_type not in [
            'File',
            'Integration',
            'URL',
            'Recursive URL',
            'Wikipedia',
            'YouTube',
            'Arxiv',
            'Git',
        ]:
            raise ValueError('Invalid document type.')

        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap

        data = {
            'vectorstore_id': self.id,
            'vectorstore_name': self.name,
            'document_name': document_name,
            'document_type': document_type,
            'chunk_size': chunk_size,
            'chunk_overlap': chunk_overlap,
            'selected_items': json.dumps(selected_items),
            'select_all_items_flags': json.dumps(select_all_items_flags),
            'metadata': json.dumps(metadata),
            'metadata_by_item': json.dumps(metadata_by_item),
        }

        headers = {
            'Api-Key': api_key or vectorshift.api_key,
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }

        if document_type == 'File':
            if isinstance(document, str):
                if not os.path.exists(document):
                    raise ValueError(f'File with path {document} does not exist.')
                if os.path.getsize(document) > MAX_FILE_UPLOAD_SIZE:
                    raise ValueError(
                        f'File with path {document} is too large to upload.'
                    )
                with open(document, 'rb') as f:
                    files = {'document': f}
                    response = requests.post(
                        API_VECTORSTORE_LOAD_ENDPOINT,
                        data=data,
                        headers=headers,
                        files=files,
                    )
            else:
                files = {'document': document}
                response = requests.post(
                    API_VECTORSTORE_LOAD_ENDPOINT,
                    data=data,
                    headers=headers,
                    files=files,
                )
        elif document_type == 'Integration':
            data['document'] = document
            response = requests.post(
                API_VECTORSTORE_LOAD_ENDPOINT,
                data=data,
                headers=headers,
            )
        else:
            data['document'] = document
            response = requests.post(
                API_VECTORSTORE_LOAD_ENDPOINT,
                data=data,
                headers=headers,
            )

        if response.status_code != 200:
            raise Exception(
                f'KnowledgeBase object encountered an error loading documents: {response.text}'
            )
        response = response.json()

        return response

    def query(
        self,
        query: str,
        max_docs: int = 5,
        filter: dict = None,
        rerank: bool = False,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Query the Knowledge Base.

        Parameters:
            query (str): The query to run.
            max_docs (int, optional): The maximum number of documents to return. Defaults to 5.
            filter (dict, optional): A dictionary of filters to apply to the query. Defaults to None.
            rerank (bool, optional): Whether to rerank the results. Defaults to False.
            api_key (str): The API key to use for authentication.

        Returns:
            dict: The JSON representation of the server response to the query from the VectorShift platform.
        """
        filter = filter or {}
        response = requests.post(
            API_VECTORSTORE_QUERY_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'query': query,
                'max_docs': max_docs,
                'filter': filter,
                'rerank': rerank,
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

    def list_documents(self, max_documents: int = 5) -> dict:
        """List the documents in the Knowledge Base.

        Parameters:
            max_documents: The maximum number of documents to return. Defaults to 5.

        Returns:
            dict: The JSON representation of the files in the Knowledge Base.
        """
        if not self.id:
            raise ValueError(
                'Error listing documents: Knowledge Base object does not have an existing ID. It must be saved as a new Knowledge Base.'
            )
        response = requests.post(
            API_VECTORSTORE_LIST_DOCUMENTS_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'max_documents': max_documents,
            },
            headers={
                'Api-Key': vectorshift.api_key,
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error listing documents: {response.text}')
        response = response.json()

        return response

    def delete_documents(self, document_ids: list, filter: dict = None) -> dict:
        """Delete documents in the Knowledge Base by their IDs.

        Parameters:
            document_ids (list): The IDs of the documents to delete.

        Returns:
            dict: The JSON representation of the server response from the VectorShift platform.
        """
        # TODO: Add the ability to delete multiple documents at once or by filter
        if not self.id:
            raise ValueError(
                'Error deleting documents: Knowledge Base object does not have an existing ID. It must be saved as a new Knowledge Base.'
            )

        if not isinstance(document_ids, list):
            document_ids = [document_ids]
        if len(document_ids) == 0:
            raise ValueError(
                'Error deleting documents: document_ids must be a non-empty list of document IDs.'
            )
        elif len(document_ids) > 1:
            raise NotImplementedError(
                'Error deleting documents: deleting multiple documents at once is not yet supported.'
            )
        response = requests.delete(
            API_VECTORSTORE_DELETE_DOCUMENTS_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'document_ids': document_ids,
            },
            headers={
                'Api-Key': vectorshift.api_key,
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error deleting documents: {response.text}')
        response = response.json()

        return response

    def share(self, shared_users: list[str]) -> dict:
        """Share the Knowledge Base with other users.

        Parameters:
            shared_users (list): A list of email addresses to share the Knowledge Base with.

        Returns:
            dict: The JSON representation of the server response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Error sharing: Knowledge Base does not have an existing ID. It must be saved in order to be shared.'
            )

        shared_users_dicts = []
        for user in shared_users:
            shared_users_dicts.append(
                {
                    'email': user,
                    'permissions': 'View',
                }
            )
        response = requests.post(
            API_VECTORSTORE_SHARE_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'shared_users': json.dumps(shared_users_dicts),
            },
            headers={
                'Api-Key': vectorshift.api_key,
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error sharing Knowledge Base: {response.text}')
        response = response.json()

        return response

    def fetch_shared(self) -> dict:
        """Fetch shared Knowledge Base documents.

        Returns:
            dict: The JSON representation of the server response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Error listing documents: Knowledge Base does not have an existing ID. It must be saved.'
            )

        response = requests.get(
            API_VECTORSTORE_FETCH_SHARED_ENDPOINT,
            headers={
                'Api-Key': vectorshift.api_key,
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f'Error fetching shared Knowledge Base documents: {response.text}'
            )
        response = response.json()

        return response

    def remove_share(self, users_to_remove: list[str]) -> dict:
        """Unshare a Knowledge Base with users.

        Parameters:
            users_to_remove (list): A list of email addresses to unshare the Knowledge Base with.

        Returns:
            dict: The JSON representation of the server response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Error listing documents: Knowledge Base object does not have an existing ID. It must be saved in order to be shared.'
            )

        response = requests.delete(
            API_VECTORSTORE_REMOVE_SHARE_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'users_to_remove': users_to_remove,
            },
            headers={
                'Api-Key': vectorshift.api_key,
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error removing shared Knowledge Base: {response.text}')
        response = response.json()

        return response


VectorStore = KnowledgeBase
