# functionality to deploy and run pipelines
import functools
import requests
from typing import Callable

import vectorshift
from vectorshift.file import File
from vectorshift.integration import *
from vectorshift.pipeline import Pipeline
from vectorshift.transformation import *
from vectorshift.consts import *


class Config:
    # For now, the config is just a wrapper for the API key
    def __init__(self, api_key=None, public_key=None, private_key=None):
        """Create a Config object, which can be used to perform various tasks related to interacting with the VectorShift platform. Given an API key in the constructor, various other class methods can be used to interact with the API using the key.

        Parameters:
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication if applicable.
            private_key (str): The private key to use for authentication if applicable.

        Returns:
            Config: The Config object.
        """
        self.api_key = api_key or vectorshift.api_key
        self.public_key = public_key or vectorshift.public_key
        self.private_key = private_key or vectorshift.private_key

    def fetch_user_details(self) -> dict:
        """Fetch user details, including the user ID, organization ID, and username, from the VectorShift platform. The details will be for the user with which the API key passed into the Config object is associated.

        Returns:
            dict: A JSON representation of the fetched user details.
        """
        response = requests.get(
            API_USER_DETAILS_ENDPOINT,
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def fetch_all_pipelines(self) -> dict:
        """Fetch all the user's accessible pipelines from the VectorShift platform.

        Returns:
            dict: A JSON representation of the fetched pipelines.
        """
        response = requests.get(
            API_PIPELINE_FETCH_ALL_ENDPOINT,
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def fetch_all_pipeline_ids(self) -> list[str]:
        """Fetch all the user's accessible pipeline IDs from the VectorShift platform.

        Returns:
            list[str]: The fetched pipeline IDs.
        """
        ps = self.fetch_all_pipelines()
        ids = [p.get('id') for p in ps]
        return [id for id in ids if id is not None]

    # Save the pipeline as a new pipeline to the VS platform.
    def save_new_pipeline(self, pipeline: Pipeline) -> dict:
        # already implemented in the Pipeline class
        # save method will itself raise an exception if 200 isn't returned
        """Save a new pipeline to the VectorShift platform. This is equivalent to using the Pipeline.save method.

        Parameters:
            pipeline (Pipeline): The pipeline to save.

        Returns:
            dict: The JSON response from the VectorShift platform, including the representation of the saved pipeline.
        """
        response = pipeline.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
            update_existing=False,
        )
        return response

    def fetch_shared_pipelines(self) -> dict:
        """Fetch all the user's shared pipelines from the VectorShift platform.

        Returns:
            dict: The JSON representations of the fetched shared pipelines.
        """
        response = requests.get(
            API_PIPELINE_SHARED_ENDPOINT,
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    # Update the pipeline, assuming it already exists in the VS platform.
    # Raises if the pipeline ID doesn't exist, or isn't in the VS platform.
    def update_pipeline(self, pipeline: Pipeline) -> dict:
        response = pipeline.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
            update_existing=True,
        )
        """Update an existing pipeline in the VectorShift platform. This is equivalent to using the Pipeline.save method with update_existing set to True.

        Parameters:
            pipeline (Pipeline): The pipeline to update.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        response = pipeline.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
            update_existing=True,
        )

        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def run_pipeline(
        self,
        pipeline: Pipeline = None,
        pipeline_id: str = None,
        pipeline_name: str = None,
        username: str = None,
        org_name: str = None,
        inputs: dict[str, str | File | list[File]] = {},
        temporary_file_inputs: dict[str, str | list[str]] = {},
        run_async: bool = False,
    ) -> dict:
        """Run a pipeline in the VectorShift platform. See Pipeline.run for more details."""
        p: Pipeline = pipeline
        if not p:
            if not pipeline_id and not pipeline_name:
                raise ValueError(
                    'Insufficient information: pipeline_id or pipeline_name must be provided.'
                )
            p = Pipeline.fetch(
                pipeline_id=pipeline_id,
                pipeline_name=pipeline_name,
                username=username,
                org_name=org_name,
                api_key=self.api_key,
                public_key=self.public_key,
                private_key=self.private_key,
            )
        if run_async:
            return pipeline.run_async(
                inputs=inputs,
                temporary_file_inputs=temporary_file_inputs,
                api_key=self.api_key,
                public_key=self.public_key,
                private_key=self.private_key,
            )
        return pipeline.run(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
            inputs=inputs,
            temporary_file_inputs=temporary_file_inputs,
        )

    def delete_pipelines(self, pipeline_ids: list[str]) -> dict:
        """Delete pipelines from the VectorShift platform according to their pipeline IDs.

        Parameters:
            pipeline_ids (list[str]): The pipeline IDs to delete.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if pipeline_ids == []:
            return
        response = requests.delete(
            API_PIPELINE_DELETE_ENDPOINT,
            data={'pipeline_ids': pipeline_ids},
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def fetch_all_files(self) -> list[File]:
        """Fetch all user files from the VectorShift platform.

        Returns:
            list[File]: The fetched files.
        """
        return File.fetch_all(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def fetch_files_by_ids(self, file_ids: list[str]) -> list[File]:
        """Fetch user files from the VectorShift platform based on their file IDs.

        Parameters:
            file_ids: The file IDs to fetch.

        Returns:
            list[File]: The fetched files.
        """
        return File.fetch_by_ids(
            file_ids=file_ids,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def fetch_files_by_names(self, file_names: list[str]) -> list[File]:
        """Fetch user files from the VectorShift platform based on their file names.

        Parameters:
            file_names: The file names to fetch.

        Returns:
            list[dict]: The fetched files.
        """
        return File.fetch_by_names(
            file_names=file_names,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def upload_file(
        self,
        file: str,
        folder_id: str = None,
        filetype: str = None,
        return_json: bool = False,
    ) -> dict:
        """Upload a file to the VectorShift platform.

        Parameters:
            file (str): The (local) path to the file to upload. Note that the value of the path will be the name of the file on the VectorShift platform.
            folder_id (str): The ID of the folder to upload the file to. Defaults to None.
            filetype (str): The file type of the file. Defaults to None.
            return_json (bool): Whether or not to return the JSON response from the VectorShift platform. Defaults to False.

        Returns:
            If return_json is True: dict: The JSON response from the VectorShift platform, including the representation of the uploaded file.
            If return_json is False: File: The representation of the uploaded file.
        """
        return File.upload_file(
            file=file,
            folder_id=folder_id,
            filetype=filetype,
            return_json=return_json,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def download_file(
        self, file_id: str, download_url: bool = False, destination_file: str = None
    ):
        """Download a file from the VectorShift platform.

        Parameters:
            file_id (str): The ID of the file to download.
            download_url (bool): Whether or not to return the URL of the file (instead of raw bytes). Defaults to False.
            destination_file (str): A file path, if you wish to write the file to a local file. Ignored if download_url is True. Defaults to None.

        Returns:
            The returned result depends on the parameters.
            If download_url is True: dict: The JSON response from the VectorShift platform, including the URL of the file.
            If download_url is False and destination_file is not None: None (the file is written to the path given by destination_file).
            Else: bytes: The bytes of the downloaded file.
        """
        print(file_id)
        return File.download_file(
            file_id=file_id,
            download_url=download_url,
            destination_file=destination_file,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def delete_files_by_id(self, file_ids: list[str]):
        """Delete user files from the VectorShift platform based on their file IDs.

        Parameters:
            file_ids: The file IDs to delete.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        return File.delete_by_ids(
            file_ids=file_ids,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def delete_files_by_name(self, file_names: list[str]):
        """Delete user files from the VectorShift platform based on their file names.

        Parameters:
            file_names: The file names to delete.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        return File.delete_by_names(
            file_names=file_names,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def fetch_all_knowledge_bases(self) -> list[dict]:
        """Fetch all of a user's Knowledge Bases from the VectorShift platform.

        Returns:
            list[dict]: The JSON representations of the fetched Knowledge Bases.
        """
        response = requests.get(
            API_VECTORSTORE_FETCH_ALL_ENDPOINT,
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    fetch_all_vectorstores = fetch_all_knowledge_bases

    # TODO add methods to delete vectorstores & share objs

    def fetch_all_integrations(self) -> list[dict]:
        """Fetch all of a user's Integrations from the VectorShift platform.

        Returns:
            list[dict]: The JSON representations of the fetched Integrations.
        """
        return Integration.fetch_all(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def fetch_integration(self, integration_id: str) -> dict:
        """Fetch an Integration by its ID from the VectorShift platform.

        Parameters:
            integration_id: The ID of the Integration to fetch.

        Returns:
            dict: The JSON representation of the fetched Integration."""
        return Integration.fetch(
            integration_id,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def fetch_all_transformations(self):
        """Fetch all of a user's Transformations from the VectorShift platform.

        Returns:
            list[dict]: The JSON representations of the fetched Transformations.
        """
        response = requests.get(
            API_TRANSFORMATION_FETCH_ALL_ENDPOINT,
            headers={
                'Api-Key': self.api_key,
                'Public-Key': self.public_key,
                'Private-Key': self.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def fetch_transformation(
        self, transformation_id: str = None, transformation_name: str = None
    ) -> Transformation:
        """Fetch a Transformation from the VectorShift platform. Specify either the ID or the name.

        Parameters:
            transformation_id: The ID of the Transformation to fetch.
            transformation_name: The name of the Transformation to fetch.

        Returns:
            Transformation: The fetched Transformation object."""
        return Transformation.fetch(
            transformation_id=transformation_id,
            transformation_name=transformation_name,
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def save_transformation(
        self,
        transformation: Transformation,
    ) -> dict:
        """Save a Transformation.

        Parameters:
            transformation: The Transformation to save.

        Returns:
            dict: The JSON response from the server, including the representation of the saved transformation.
        """
        return transformation.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def save_transformation_function(
        self,
        transformation_func: Callable[..., dict[str, any]],
        outputs: dict[str, any],
        name: str = '',
        description: str = '',
        inputs: dict[str, any] = {},
        update_id: str = None,
    ) -> dict:
        """Save a Transformation to the VectorShift platform from a Python function. Akin to calling the Transformation constructor and then the Transformation.save() method. See the Transformation class for more details.

        Parameters:
            transformation_func: The function to save as a transformation.
            outputs: A dict of output names to output types of the function.
            name: The name of the transformation.
            description: The description of the transformation. If empty, the function docstring if not None is used.
            inputs: A dict of input names to input types of the function.
            update_id: The ID of the Transformation to update, if this function is meant to update an existing Transformation on the platform.

        Returns:
            dict: The JSON response from the server, including the representation of the saved Transformation.

        Example:
        vs = Config(...)

        def foo(aaa: str, bbb: list[str]) -> dict:
            return {
                'prepended': [aaa] + bbb,
                'joined': aaa.join(bbb)
            }

        vs.save_transformation(
            transformation_func=foo,
            name='my_transformation',
            description='my description',
            inputs={
                'aaa': 'Text',
                'bbb': 'List'
            },
            outputs={
                'prepended': 'List',
                'joined': 'Text'
            },
        )
        """

        t = Transformation(
            id=update_id,
            transformation_func=transformation_func,
            name=name,
            description=description,
            inputs=inputs,
            outputs=outputs,
        )

        return t.save(
            api_key=self.api_key,
            public_key=self.public_key,
            private_key=self.private_key,
        )

    def delete_transformations(self, transformation_ids: list[str]):
        """Delete Transformations from the VectorShift platform by their IDs.

        Parameters:
            transformation_ids (list[str]): The IDs of the Transformations to delete.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        headers = {
            'Api-Key': self.api_key,
            'Public-Key': self.public_key,
            'Private-Key': self.private_key,
        }
        response = requests.delete(
            API_TRANSFORMATION_DELETE_ENDPOINT,
            data={'transformation_ids': transformation_ids},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        print('Successfully deleted transformation(s).')
        return response.json()


VectorShift = Config


def transformation(
    outputs: dict[str, any],
    vs: Config = None,
    api_key: str = None,
    name: str = '',
    description: str = '',
    inputs: dict = {},
    update_id: str = None,
    print_response: bool = True,
):
    """A decorator to save a Python function to the VectorShift platform as a Transformation. The inputs and outputs provided should be dicts of input/output names to the expected types. The function parameters must have names corresponding to the keys of inputs. The function must return a dict of outputs whose keys should match the keys in the outputs argument provided. The function must be a callable object and should be annotated as returning a dict. If the function arguments are annotated with types, the input types may be inferred and do not need to be provided. See the documentation for Config.save_transformation for more details.

    The decorator modifies the function such that once it runs, it returns both its outputs (as a dict) and the JSON response corresponding to the saved transformation as a tuple.

    Parameters:
        outputs: A dict of output names to output types of the function.
        name: The name of the transformation.
        config: The Config object to use. If not provided, api_key must be provided. If provided, api_key is ignored.
        api_key: The API key to use for authentication. If not provided, config must be provided.
        name: The name of the transformation. If empty, the function name is used.
        description: The description of the transformation. If empty, the function docstring if not None is used.
        inputs: A dict of input names to input types of the function.
        update_id: The ID of the transformation to update.
    """
    api_key = api_key or vectorshift.api_key
    if vs is None:
        if not api_key:
            raise ValueError('Either a Config object or api_key must be provided.')
        vs = Config(api_key=api_key)

    def decorator(transformation_func):
        response = vs.save_transformation_function(
            transformation_func=transformation_func,
            outputs=outputs,
            name=name,
            description=description,
            inputs=inputs,
            update_id=update_id,
        )

        if print_response:
            print(response)

        @functools.wraps(transformation_func)
        def wrapper(*args, **kwargs):
            return transformation_func(*args, **kwargs)

        return wrapper

    return decorator
