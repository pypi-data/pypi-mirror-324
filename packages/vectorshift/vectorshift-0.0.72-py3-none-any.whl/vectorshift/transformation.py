import inspect
import json
import re
import requests
from types import GenericAlias
from typing import Callable

import vectorshift
from vectorshift.consts import *
from vectorshift.node_utils import *


def get_transformation_type_from_anno_type(t):
    if type(t) == type:
        return TRANSFORMATION_TYPE_NAMES.get(t.__name__, 'Any')
    elif isinstance(t, GenericAlias):
        return TRANSFORMATION_TYPE_NAMES.get(t.__origin__.__name__, 'Any')
    return 'Any'


class Transformation:
    def _setup_function(
        self,
        transformation_func: Callable[..., dict[str, any]],
        outputs: dict[str, any],
        inputs: dict[str, any] = {},
    ):
        # validate inputs
        if not callable(transformation_func):
            raise ValueError('Cannot save a non-function object as a transformation')
        if not re.fullmatch(
            TRANSFORMATION_IO_NAME_PATTERN, transformation_func.__name__
        ):
            raise ValueError('Invalid name for function provided to Transformation.')
        f_code = transformation_func.__code__
        n_args = f_code.co_argcount
        if inputs != {} and len(inputs.keys()) != n_args:
            raise ValueError(
                f'Incorrect number of inputs given for function (expected {n_args})'
            )
        f_argnames = f_code.co_varnames[:n_args]
        if inputs != {} and sorted(inputs.keys()) != sorted(f_argnames):
            raise ValueError(
                f'Incorrect input names given for function (expected {f_argnames})'
            )
        # make sure the values of inputs and outputs are transformation type strings
        for k, v in inputs.items():
            if not isinstance(v, str):
                if not isinstance(v, type) or not isinstance(v, GenericAlias):
                    raise ValueError(
                        f'Invalid transformation input type {type(v)}. Expected str or type or GenericAlias.'
                    )
                inputs[k] = get_transformation_type_from_anno_type(v)
        for k, v in outputs.items():
            if not isinstance(v, str):
                if not isinstance(v, type) and not isinstance(v, GenericAlias):
                    raise ValueError(
                        f'Invalid transformation output type {str(v)}. Expected str or type or GenericAlias.'
                    )
                outputs[k] = get_transformation_type_from_anno_type(v)
        supported_transformation_types = TRANSFORMATION_TYPE_NAMES.values()
        for t in inputs.values():
            if t not in supported_transformation_types:
                raise ValueError(f'Invalid transformation input type {t}')
        for t in outputs.values():
            if t not in supported_transformation_types:
                raise ValueError(f'Invalid transformation output type {t}')
        # infer types from annotations if applicable; the function should be annotated to return a dict
        f_type_annos = transformation_func.__annotations__
        if (
            get_transformation_type_from_anno_type(f_type_annos.get('return', None))
            != 'Dict'
        ):
            raise TypeError(
                "Provided function for transformation must have a return type annotation of 'dict'"
            )
        for argname in f_argnames:
            if argname in f_type_annos:
                arg_t = get_transformation_type_from_anno_type(f_type_annos[argname])
                if argname in inputs:
                    input_t = inputs[argname]
                    if input_t != 'Any' and input_t != arg_t:
                        raise ValueError(
                            f'Provided transformation type {input_t} is incompatible with inferred type {arg_t} from type annotations'
                        )
                else:
                    inputs[argname] = arg_t
            else:
                if argname not in inputs:
                    inputs[argname] = 'Any'
        # check input and output names
        for k in inputs.keys():
            if not re.fullmatch(TRANSFORMATION_IO_NAME_PATTERN, k):
                raise ValueError(
                    f'Invalid name for input variable {k} provided to Transformation. Variable names should be alphanumeric and underscores only and between 2 and 48 characters long.'
                )
        for k in outputs.keys():
            if not re.fullmatch(TRANSFORMATION_IO_NAME_PATTERN, k):
                raise ValueError(
                    f'Invalid name for output variable {k} provided to Transformation. Variable names should be alphanumeric and underscores only and between 2 and 48 characters long.'
                )

        # TODO is there some way to check outputs?
        self.transformation_func = transformation_func
        self.inputs = inputs
        self.outputs = outputs

    def __init__(
        self,
        transformation_func: Callable[..., dict[str, any]],
        outputs: dict[str, any],
        id: str = None,
        name: str = '',
        description: str = '',
        inputs: dict[str, any] = {},
    ):
        """Initialize a Transformation to the VectorShift platform from a Python function. The inputs and outputs provided should be dicts of input/output names to the expected types. The function parameters must have names corresponding to the keys of inputs. The function must return a dict of outputs whose keys should match the keys in the outputs argument provided. The function must be a callable object and should be annotated as returning a dict. If the function arguments are annotated with types, the input types may be inferred and do not need to be provided.

        Supported Transformation types are 'Any', 'Text', 'Bool', 'Integer', 'Float', 'List', and 'Dict'. Python types can also be directly passed into the values of the inputs and outputs dicts and the conversion to the type string will be done for you.

        Parameters:
            transformation_func: The function to save as a transformation.
            outputs: A dict of output names to output types of the function.
            name: The name of the transformation.
            description: The description of the transformation. If empty, the function docstring if not None is used.
            inputs: A dict of input names to input types of the function.
            id: The ID of the Transformation, if the Transformation object is meant to correspond to an already-existing Transformation on the platform.

        Returns:
            Transformation: A Python object representing the Transformation.

        Example:
        def foo(aaa: str, bbb: list[str]) -> dict:
            return {
                'prepended': [aaa] + bbb,
                'joined': aaa.join(bbb)
            }

        t = Transformation(
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

        NB: inputs did not need to be explicitly provided, as the types could have been inferred from the function signature type annotations.
        """
        self.id = id

        self._setup_function(transformation_func, outputs, inputs)
        if name == '':
            name = transformation_func.__name__
        if not re.fullmatch(TRANSFORMATION_NAME_PATTERN, name):
            raise ValueError(
                'Transformation name must be between 2 and 80 characters and contain only alphanumeric characters, hyphens, underscores, periods, and spaces.'
            )
        if description == '' and transformation_func.__doc__ is not None:
            description = transformation_func.__doc__
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Transformation with JSON representation: {json.dumps(self.to_json_rep())}>'

    def __str__(self):
        return f"(transformation id {self.id})=Transformation(\n\
    id={self.id},\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    inputs={self.inputs},\n\
    outputs={self.outputs},\n\
    transformation_func={inspect.getsource(self.transformation_func)}\n\
)"

    def construction_str(self, indicate_id: bool = True) -> str:
        function_def = inspect.getsource(self.transformation_func)
        transformation_construct_str = f"transformation=Transformation(\n\
    transformation_func={self.transformation_func.__name__},\n\
    inputs={self.inputs},\n\
    outputs={self.outputs},\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    id={nullable_str(self.id) if indicate_id else None}\n\
)"
        return f'{function_def}\n{transformation_construct_str}'

    def to_json_rep(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'functionName': self.transformation_func.__name__,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'function': inspect.getsource(self.transformation_func),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_json_rep(), indent=4)

    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'Transformation':
        """Converts a JSON representation of a Transformation into a Transformation object. The opposite of to_json_rep. WARNING: this code will execute the function stored. It is your responsibility to ensure the execution of your Transformation function does not have unwanted side effects.

        Parameters:
            json_data (dict[str, any]): A JSON representation of a Transformation.

        Returns:
            Transformation: A Transformation object.
        """
        exec_globals, exec_locals = {}, {}
        exec(json_data['function'], exec_globals, exec_locals)
        transformation_func = exec_locals.get(json_data['name'])
        if not transformation_func:
            raise Exception(
                f'Error loading JSON: Could not find function with name {json_data["name"]}'
            )
        return Transformation(
            id=json_data['id'],
            name=json_data['name'],
            description=json_data['description'],
            transformation_func=transformation_func,
            inputs=json_data['inputs'],
            outputs=json_data['outputs'],
        )

    @staticmethod
    def from_json(json_str: str) -> 'Transformation':
        """Converts a JSON string of a Transformation as used with the VectorShift API into a Transformation object. The opposite of to_json.

        Parameters:
            json_str (str): A JSON string representing a Transformation.

        Returns:
            Transformation: A Transformation object.
        """
        json_data = json.loads(json_str)
        return Transformation.from_json_rep(json_data)

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        if not re.fullmatch(r'^[a-zA-Z0-9\-._\s]{2,80}$', name):
            raise ValueError(
                'Transformation name must be between 2 and 80 characters and contain only alphanumeric characters, hyphens, underscores, periods, and spaces.'
            )
        self.name = name

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str):
        self.description = description

    def get_transformation_func(self) -> Callable:
        return self.transformation_func

    def set_transformation_func(
        self,
        transformation_func: Callable[..., dict[str, any]],
        outputs: dict[str, any],
        inputs: dict[str, any] = {},
    ):
        self._setup_function(transformation_func, outputs, inputs)

    @staticmethod
    def fetch_json(
        transformation_id: str = None,
        transformation_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Fetches the JSON representation of a Transformation from the VectorShift platform. Specify either the ID or the name. The JSON representation has a few additional metadata fields omitted in the Transformation class.

        Parameters:
            transformation_id: The ID of the Transformation to fetch.
            transformation_name: The name of the Transformation to fetch.

        Returns:
            dict: The JSON representation of the fetched Transformation.
        """
        if transformation_id is None and transformation_name is None:
            raise ValueError(
                'At least one of the Transformation ID or name must be specified.'
            )
        params = {}
        if transformation_id is not None:
            params['transformation_id'] = transformation_id
        if transformation_name is not None:
            params['transformation_name'] = transformation_name
        response = requests.get(
            API_TRANSFORMATION_FETCH_ENDPOINT,
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
        transformation_id: str = None,
        transformation_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> 'Transformation':
        """Fetch a Transformation from the VectorShift platform. Specify either the ID or the name.

        Parameters:
            transformation_id: The ID of the Transformation to fetch.
            transformation_name: The name of the Transformation to fetch.

        Returns:
            Transformation: The fetched Transformation object.
        """
        response = Transformation.fetch_json(
            transformation_id=transformation_id,
            transformation_name=transformation_name,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return Transformation.from_json_rep(response)

    def save(
        self,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Save a Transformation.

        Parameters:
            api_key: The API key to use when calling the VectorShift platform.
            public_key: The public key to use when calling the VectorShift platform.
            private_key: The private key to use when calling the VectorShift platform.

        Returns:
            dict: The JSON response from the server, including the representation of the saved transformation.
        """
        transformation_json = self.to_json()
        response = requests.post(
            API_TRANSFORMATION_SAVE_ENDPOINT,
            data={'transformation': transformation_json},
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Server error creating transformation: {response.text}')
        response = response.json()
        self.id = response.get('id')
        print(f'Successfully saved transformation with ID {self.id}.')
        return response

    # NB probably nicer to call using deploy.py
    def delete(
        self, api_key: str = None, public_key: str = None, private_key: str = None
    ) -> dict:
        """Delete the Transformation on the VectorShift platform. The Transformation must already exist on the VectorShift platform. The Config object in the vectorshift.deploy module can be alternatively used. This method clears the ID associated with the Transformation object.

        Parameters:
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Transformation object does not exist and so does not correspond to a Transformation on the VectorShift platform.'
            )
        headers = {
            'Api-Key': api_key or vectorshift.api_key,
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }
        response = requests.delete(
            API_TRANSFORMATION_DELETE_ENDPOINT,
            data={'transformation_ids': [self.id]},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        # reset the ID
        self.id = None
        print('Successfully deleted Transformation.')
        return response.json()
