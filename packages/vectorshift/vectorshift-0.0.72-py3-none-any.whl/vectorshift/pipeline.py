# functionality to stitch together nodes into pipelines
from collections import defaultdict
import json
import mimetypes
import requests
from networkx import MultiDiGraph, topological_generations

import vectorshift
from vectorshift.node import *
from vectorshift.consts import *

# Helpers for converting to/from JSON.
# Figure out what node class a JSON represents, and convert it into an object
# of that class using the class's from_json_rep method.
node_type_to_node_class: dict[str, NodeTemplate] = {
    'customInput': InputNode,
    'customOutput': OutputNode,
    'text': TextNode,
    'file': FileNode,
    'pipeline': PipelineNode,
    'integration': IntegrationNode,
    'transformation': TransformationNode,
    'fileSave': FileSaveNode,
    'stickyNote': StickyNoteNode,
    'llmOpenAI': OpenAILLMNode,
    'llmOpenAIVision': OpenAIVisionNode,
    'llmGoogleVision': GoogleVisionNode,
    'llmAnthropic': AnthropicLLMNode,
    'llmOpenSource': OpenSourceLLMNode,
    'llmCohere': CohereLLMNode,
    'llmAWS': AWSLLMNode,
    'llmGoogle': GoogleLLMNode,
    'llmLlama': MetaLLMNode,
    'imageGen': ImageGenNode,
    'speechToText': SpeechToTextNode,
    'vectorDBLoader': VectorDBLoaderNode,
    'vectorDBReader': VectorDBReaderNode,
    'vectorQuery': SemanticSearchNode,
    'vectorStore': KnowledgeBaseNode,
    'condition': LogicConditionNode,
    'merge': LogicMergeNode,
    'splitText': SplitTextNode,
    'timeNode': TimeNode,
    'chatMemory': ChatMemoryNode,
    'dataCollector': DataCollectorNode,
    'agent': AgentNode,
}

dataloader_node_type_to_node_class: dict[str, NodeTemplate] = {
    'Api': ApiLoaderNode,
    'File': FileLoaderNode,
    'CSV Query': CSVQueryLoaderNode,
    'URL': URLLoaderNode,
    'Wikipedia': WikipediaLoaderNode,
    'YouTube': YouTubeLoaderNode,
    'Arxiv': ArXivLoaderNode,
    'SerpAPI': SerpAPILoaderNode,
    'Git': GitLoaderNode,
    'YOU_DOT_COM': YouDotComLoaderNode,
    'YOU_DOT_COM_NEWS': YouDotComLoaderNode,
    'EXA_AI_SEARCH': ExaAILoaderNode,
    'EXA_AI_SEARCH_COMPANIES': ExaAILoaderNode,
    'EXA_AI_SEARCH_RESEARCH_PAPERS': ExaAILoaderNode,
    'Notion': NotionLoaderNode,  # DEPRECATED
    'Confluence': ConfluenceLoaderNode,  # DEPRECATED
}


def node_from_json_data(node_json_data) -> NodeTemplate:
    if node_json_data['type'] in node_type_to_node_class:
        return node_type_to_node_class[node_json_data['type']].from_json_rep(
            node_json_data
        )
    elif node_json_data['type'] == 'dataLoader':
        if node_json_data['data']['loaderType'] in dataloader_node_type_to_node_class:
            return dataloader_node_type_to_node_class[
                node_json_data['data']['loaderType']
            ].from_json_rep(node_json_data)
        raise ValueError(
            f"Node: Unrecognized type for Data Loader node {node_json_data['data']['loaderType']}."
        )
    raise ValueError(f"Node: Unrecognized node type {node_json_data['type']}.")


def top_sort_nodes(node_ids: list[str], edges: list[dict]) -> list:
    edges = [
        (
            edge['source'],
            edge['target'],
            {
                'sourceHandle': edge['sourceHandle'].replace(
                    f"{edge['source']}-", '', 1
                ),
                'targetHandle': edge['targetHandle'].replace(
                    f"{edge['target']}-", '', 1
                ),
            },
        )
        for edge in edges
    ]
    G = MultiDiGraph()
    G.add_nodes_from(node_ids)
    G.add_edges_from(edges)
    # Sort the nodes into topological generations
    return topological_generations(G)


# Assign a position (x,y) to a node. Right now this function is
# rudimentary, arranging all nodes in a straight line.
def assign_node_positions(
    node_ids: list[str], edges: list[dict]
) -> dict[str, dict[str, int]]:
    # Generate a graph with just the relevant data from the nodes and edges
    top_gen = top_sort_nodes(node_ids, edges)

    # Assign positions to each node, aligning the nodes within each generation
    # vertically and centered about the x-axis
    positions = {}
    for i, generation in enumerate(top_gen):
        for j, node_id in enumerate(generation):
            positions[node_id] = {
                'x': i * 500,
                'y': (j - len(generation) // 2) * 450 + random.choice([-50, 0, 50]),
            }
    return positions


# Create a pipeline by passing nodes and params in.
class Pipeline:
    def __init__(
        self,
        name: str,
        description: str,
        nodes: list[NodeTemplate],
        id: str = None,
        branch_id: str = None,
        **kwargs,
    ):
        """Create a pipeline by passing nodes and metadata in. Each of the nodes should be a Node object as found in the vectorshift.node module. Links (graph edges) representing data flow between the nodes should already have been created by passing NodeOutputs from earlier Node objects into the constructors of later Node objects. Some basic checks are done to ensure the well-formedness of these links. Refer to the documentation for examples.

        This does not actually save or run the Pipeline, but rather just creates a object representing the Pipeline. The Pipeline.save method should be called to actually save the Pipeline to the VectorShift platform. The Pipeline.run method should be called to actually run the Pipeline.

        Parameters:
            name (str): The name of the pipeline.
            description (str): The description of the pipeline.
            nodes (list[NodeTemplate]): The nodes of the pipeline, which should already have been instantiated and linked via NodeOutputs.
            id (str): The ID of the existing pipeline, if the Pipeline object is meant to represent or replace an existing pipeline.
            branch_id (str): The ID of the existing pipeline branch, if the Pipeline object is meant to represent or replace an existing pipeline branch.

        Returns:
            Pipeline: The Pipeline object.

        NB: Node IDs as assigned through the SDK are given by the Node's specific type and a numerical counter suffix, as opposited to a random string suffix in the no-code editor.
        """
        self.id = id
        self.branch_id = branch_id
        self.name = name
        self.description = description
        # should only be called when fetching a shared pipeline
        self.share_status = PipelineShareStatus.OWNED
        if 'share_status' in kwargs:
            self.share_status = PipelineShareStatus(kwargs['share_status'])
        # Map node IDs to the objects
        self.nodes: dict[str, NodeTemplate] = {}
        # Assign node IDs and gather ID (node type) counts; also record the
        # inputs and outputs
        # NB: in a node's JSON representation, id, type, data.id, and
        # data.nodeType are essentially the same
        self.node_type_counts = defaultdict(int)
        # The OVERALL pipeline input and output nodes, keyed by node IDs
        # (analogous to Mongo)
        self.inputs, self.outputs = {}, {}
        # assign each node an ID and increment self.node_type_counts - before
        # adding edges, all nodes must have IDs first
        for node in nodes:
            self._add_node(node)

        # Create edges: An edge is a dict following the JSON structure. All
        # edges in the computation graph defined by the nodes terminate at some
        # node, i.e. are in the node's _inputs. So it should suffice to parse
        # through every node's _inputs and create an edge for each one.
        self.edges: list[dict[str, str]] = []
        for n in self.nodes.values():
            # n.inputs() is a dictionary of input field names to NodeOutputs
            # from ancestor nodes filling those fields
            target_node_id = n._id
            for input_name, outputs in n._inputs.items():
                if outputs == []:
                    print(
                        f'WARNING: {n.__class__.__name__} node did not receive any inputs for input field {input_name}'
                    )
                # an input could have aggregated several NodeOutputs
                for output in outputs:
                    # Edges are specifically defined by source/target handles,
                    # derived from the node ids
                    source_node_id = output.source._id
                    output_field = output.output_field
                    source_handle = f'{source_node_id}-{output_field}'
                    target_handle = f'{target_node_id}-{input_name}'
                    # Create an edge id following ReactFlow's formatting
                    id = f'reactflow__edge-{source_node_id}{source_handle}-{target_node_id}{target_handle}'
                    self.edges.append(
                        {
                            'source': source_node_id,
                            'sourceHandle': source_handle,
                            'target': target_node_id,
                            'targetHandle': target_handle,
                            'type': 'defaultEdge',
                            'id': id,
                        }
                    )

    def __repr__(self):
        if self.share_status == PipelineShareStatus.RUN:
            # there's only limited info we can access
            rep = {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'inputs': self.inputs,
                'outputs': self.outputs,
                'shared_status': self.share_status.value,
            }
            return f'<Run-only pipeline with JSON representation\n\
                {json.dumps(rep)}\n>'
        return f'<Pipeline with JSON representation\n\
            {json.dumps(self.to_json_rep())}\n>'

    def __str__(self):
        if self.share_status == PipelineShareStatus.RUN:
            # display only the inputs and outputs in lieu of nodes if the
            # pipeline is run-only
            return f"(pipeline id {self.id})=Pipeline(\n\
    id={self.id},\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    inputs={self.inputs},\n\
    outputs={self.outputs},\n\
    share_status={self.share_status.value}\n\
)"
        nodes_strs = [
            '\t' + n.__str__().replace('\n', '\n\t') for n in self.nodes.values()
        ]
        nodes_str = ',\n'.join(nodes_strs)
        id = self.id if self.id is not None else '<no pipeline id>'
        id_str = f"'{self.id}'" if self.id is not None else None
        return f"(pipeline id {id})=Pipeline(\n\
    id={id_str},\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    nodes=[\n{nodes_str}\n\t]\n\
)"

    # Analogous to __str__, but prints the output in a way that aims to
    # be copy-pastable Python code. Nodes are initialized in a top-sorted
    # order before being inserted into the Pipeline constructor.
    def construction_str(self, indicate_id: bool = True):
        """Returns a string that represents how the Pipeline may be constructed using the Python SDK. Some specific details, such as API keys and user data, are omitted if present in the Pipeline's constitutent Nodes. Executing the Python code returned by this method will create an equivalent Pipeline.

        Parameters:
            indicate_id (bool): Whether to include the pipeline ID in the returned string. Defaults to True.

        Returns:
            str: A string that, when executed, will create an equivalent Pipeline.
        """
        if self.share_status == PipelineShareStatus.RUN:
            # run-only pipelines could only have been created through a fetch
            return f"Pipeline.fetch(\n\
    pipeline_id='{self.id}',\n\
    pipeline_name='{self.name}',\n\
) # run-only pipeline"
        construct_node_strs = []
        construct_node_ids = []
        top_gen = top_sort_nodes(list(self.nodes.keys()), self.edges)
        for generation in top_gen:
            for node_id in generation:
                node_var_name, node_constructor_str = self.nodes[
                    node_id
                ].construction_strs()
                construct_node_strs.append(f'{node_var_name}={node_constructor_str}')
                construct_node_ids.append(node_var_name)
        pipeline_construct_str = f"pipeline=Pipeline(\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    nodes=[\n\t{', '.join(construct_node_ids)}\n],\n\
    id={nullable_str(self.id) if indicate_id else None}\n\
)"
        return '\n'.join(construct_node_strs) + '\n' + pipeline_construct_str

    # The generic flag indicates whether or not to return a "generic" version
    # of JSONs for user-created objects, e.g. IntegrationNodes. See notes in
    # node_utils.py.
    def to_json_rep(self, generic: bool = False) -> dict:
        """Convert a Pipeline into a JSON representation, in the format compatible with the VectorShift API. The opposite of from_json_rep.

        Parameters:
            generic (bool): Whether or not to return a "generic" version of particular parts of the Pipeline, e.g. IntegrationNodes, that excludes specific user information.

        Returns:
            dict: A JSON representation of the Pipeline.
        """
        if self.share_status == PipelineShareStatus.RUN:
            return {
                'name': self.name,
                'description': self.description,
                'nodes': None,
                'edges': None,
                'inputs': self.inputs,
                'outputs': self.outputs,
                'nodeIDs': dict(self.node_type_counts),
                # TODO: should this always be False?
                'zipOutputs': False,
            }
        nodes = list(self.nodes.values())
        try:
            node_positions = assign_node_positions(list(self.nodes.keys()), self.edges)
        except Exception as e:
            raise ValueError(
                f'Error when converting to JSON: {e}. This has likely happened because of improper instantation of nodes. Each node should be assigned to its own variable and should not be constructed within other node constructors.'
            )
        node_jsons = []
        for i, node in enumerate(nodes):
            # we currently fix the position and absolute position to be the same
            # width and height values are automatically added when opened in
            # the no-code editor
            node_display_params = {
                'position': node_positions[node._id],
                'positionAbsolute': node_positions[node._id],
                'selected': False,
                'dragging': False,
            }
            node_json = nodes[i].to_json_rep(generic=generic)
            node_jsons.append({**node_json, **node_display_params})
        pipeline_obj = {
            # The overall (top-level) _id field for the JSON is gen'd by Mongo.
            'name': self.name,
            'description': self.description,
            'nodes': node_jsons,
            'edges': self.edges,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'nodeIDs': dict(self.node_type_counts),
            # TODO: should this always be False?
            'zipOutputs': False,
            'share_status': self.share_status.value,
        }
        if self.id:
            pipeline_obj['id'] = self.id
        if self.branch_id:
            pipeline_obj['branch_id'] = self.branch_id
        return pipeline_obj

    def to_json(self) -> str:
        """Convert a Pipeline into a JSON string, in the format compatible with the VectorShift API.

        Parameters:
            generic (bool): Whether or not to return a "generic" version of particular parts of the Pipeline, e.g. IntegrationNodes, that excludes specific user information.

        Returns:
            dict: A JSON representation of the Pipeline.
        """
        return json.dumps(self.to_json_rep(), indent=4)

    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'Pipeline':
        """Converts a JSON representation of a Pipeline as used with the VectorShift API into a Pipeline object. The opposite of to_json_rep.

        Parameters:
            json_data (dict[str, any]): A JSON representation of a Pipeline.

        Returns:
            Pipeline: A Pipeline object.
        """
        share_status = json_data.get('share_status', PipelineShareStatus.OWNED.value)
        share_status = PipelineShareStatus(share_status)
        # If the pipeline is run-only, we only get limited access to the data.
        # Really the only thing we can do is run it.
        if share_status == PipelineShareStatus.RUN:
            p = Pipeline(
                name=json_data['name'],
                description=json_data['description'],
                nodes=[],
                id=json_data.get('id'),
                share_status=share_status,
            )
            p.inputs = json_data.get('inputs', [])
            p.outputs = json_data.get('outputs', [])
            return p
        # # build all nodes first
        # node_ids_to_nodes: dict[str, NodeTemplate] = {}
        # for node_json_data in json_data.get('nodes', []):
        #     n = node_from_json_data(node_json_data)
        #     node_ids_to_nodes[node_json_data['id']] = n
        # # add edges
        # for edge in json_data.get('edges', []):
        #     # find the specific source and target edges
        #     source_id, target_id = edge['source'], edge['target']
        #     source_output_field = edge['sourceHandle'].replace(f'{source_id}-', '', 1)
        #     target_input_name = edge['targetHandle'].replace(f'{target_id}-', '', 1)
        #     source_node = node_ids_to_nodes[source_id]
        #     target_node = node_ids_to_nodes[target_id]
        #     # make sure the input/output fields as stored in the edge exist
        #     if target_input_name not in target_node._inputs.keys():
        #         # each node's _inputs starts out empty if converting from JSON,
        #         # we populate the fields for applicable input edges as
        #         # we process the edges
        #         target_node._inputs[target_input_name] = []
        #     source_node_outputs = source_node.outputs()
        #     if source_output_field not in source_node_outputs.keys():
        #         raise ValueError(
        #             f'Pipeline: Edge source output field {source_output_field} not found.'
        #         )
        #     # link up the source's NodeOutput to the target's _inputs
        #     target_node._inputs[target_input_name].append(
        #         source_node_outputs[source_output_field]
        #     )

        # TODO: save additional metadata like createdDate, userID, cost, etc.,
        # as well as node-specific data like their positions...
        # this necessitates making new member vars in the Pipeline class.
        # Note: Make sure Mongo's ObjectId has been cast to a string already.
        pipeline_id = json_data.get('id')
        # get an arbitrary branch ID for now
        branch_ids = json_data.get('branch_ids', [''])
        branch_id = branch_ids[0] if branch_ids else None
        return Pipeline(
            name=json_data.get('name', 'Untitled Pipeline'),
            description=json_data.get('description', ''),
            nodes=[],
            id=pipeline_id,
            branch_id=branch_id,
        )

    @staticmethod
    def from_json(json_str: str) -> 'Pipeline':
        """Converts a JSON string of a Pipeline as used with the VectorShift API into a Pipeline object. The opposite of to_json.

        Parameters:
            json_str (str): A JSON string representing a Pipeline.

        Returns:
            Pipeline: A Pipeline object.
        """
        json_data = json.loads(json_str)
        return Pipeline.from_json_rep(json_data)

    @staticmethod
    def fetch_json(
        pipeline_id: str = None,
        pipeline_name: str = None,
        username: str = None,
        org_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Fetches a Pipeline's JSON representation from the VectorShift platform. The Pipeline is converted into a Python SDK-compatible object that can be interacted with. Errors may be raised if the Pipeline contains features that are not yet supported by the SDK. The JSON representation has a few additional metadata fields omitted in the Pipeline class.

        Parameters:
            pipeline_name: The name of the Pipeline to fetch.
            pipeline_id: The ID of the Pipeline to fetch.
            username: The username of the user who owns the Pipeline.
            org_name: The name of the organization who owns the Pipeline.
            api_key: The API key of the user who owns the Pipeline.
            public_key: The public key of the user who owns the Pipeline, if applicable.
            private_key: The private key of the user who owns the Pipeline, if applicable.

        Returns:
            dict: A JSON object representing the fetched Pipeline.
        """
        if pipeline_id is None and pipeline_name is None:
            raise ValueError(
                'Pipeline: Must specify either pipeline_id or pipeline_name.'
            )
        if pipeline_name is not None and username is None and org_name is not None:
            raise ValueError('Pipeline: Must specify username if org_name is specified.')
        params = {}
        if pipeline_id is not None:
            params['pipeline_id'] = pipeline_id
        if pipeline_name is not None:
            params['pipeline_name'] = pipeline_name
        if username is not None:
            params['username'] = username
        if org_name is not None:
            params['org_name'] = org_name
        response = requests.get(
            API_PIPELINE_FETCH_ENDPOINT,
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
        pipeline_id: str = None,
        pipeline_name: str = None,
        username: str = None,
        org_name: str = None,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> 'Pipeline':
        """Fetches a Pipeline from the VectorShift platform. The Pipeline is converted into a Python SDK-compatible object that can be interacted with. Errors may be raised if the Pipeline contains features that are not yet supported by the SDK.

        Parameters:
            pipeline_name: The name of the Pipeline to fetch.
            pipeline_id: The ID of the Pipeline to fetch.
            username: The username of the user who owns the Pipeline.
            org_name: The name of the organization who owns the Pipeline.
            api_key: The API key of the user who owns the Pipeline.
            public_key: The public key of the user who owns the Pipeline, if applicable.
            private_key: The private key of the user who owns the Pipeline, if applicable.

        Returns:
            Pipeline: A Pipeline object representing the fetched Pipeline.
        """
        response = Pipeline.fetch_json(
            pipeline_id=pipeline_id,
            pipeline_name=pipeline_name,
            username=username,
            org_name=org_name,
            api_key=api_key,
            public_key=public_key,
            private_key=private_key,
        )
        return Pipeline.from_json_rep(response)

    @staticmethod
    def from_pipeline_node(n: PipelineNode):
        if not n.pipeline_id:
            raise ValueError('PipelineNode: No pipeline_id given.')
        return Pipeline.fetch(pipeline_id=n.pipeline_id)

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id

    def get_branch_id(self) -> str:
        return self.branch_id

    def set_branch_id(self, branch_id: str):
        self.branch_id = branch_id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str):
        self.description = description

    def get_inputs_api(
        self,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> list:
        """Fetches the pipeline's inputs from the VectorShift platform through an API call.

        Parameters:
            api_key (str): The API key to use for authentication.
            public_key (str): The public key to use for authentication if applicable.
            private_key (str): The private key to use for authentication if applicable.

        Returns:
            list: A list of JSON representations of the pipeline's inputs.
        """
        # TODO if the pipeline is run-only do we need this
        # in general, can't we just return self.inputs?
        if self.id is None:
            raise ValueError('Pipeline: No pipeline_id given.')

        response = requests.get(
            f'{API_PIPELINE_GET_INPUTS_ENDPOINT}/{self.id}',
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def get_inputs(self) -> dict:
        """Fetches the pipeline's inputs from the VectorShift platform, a dictionary of input names to their types.

        Returns:
            dict: A dictionary of input names to their types.
        """
        return self.inputs

    def get_outputs(self) -> dict:
        """Fetches the pipeline's outputs from the VectorShift platform, a dictionary of output names to their types.

        Returns:
            dict: A dictionary of output names to their types.
        """
        return self.outputs

    def get_nodes(self) -> dict[str, NodeTemplate]:
        """Get the constitutent Node objects in the Pipeline.

        Returns:
            dict[str, NodeTemplate]: A dictionary of Nodes (NodeTemplate objects), keyed by the string IDs they are referenced by in the Pipeline.
        """
        if self.share_status == PipelineShareStatus.RUN:
            raise ValueError('Pipeline: run-only pipeline contains no node data.')
        return self.nodes

    def get_node_ids(self) -> list[str]:
        """Get the string IDs of the constitutent Node objects in the Pipeline.

        Returns:
            list[str]: A list of the assigned string IDs of the Nodes in the Pipeline.
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, node_id: str) -> NodeTemplate:
        """Get the constitutent Node object in the Pipeline by its string ID.

        Parameters:
            node_id (str): The string ID of the Node to fetch.

        Returns:
            NodeTemplate: The NodeTemplate object representing the Node in the Pipeline.
        """
        return self.nodes.get(node_id, None)

    # Helper function to add a node and assign it an ID; does not add the
    # input edges to the node
    def _add_node(self, node: NodeTemplate):
        # assign a fresh new ID to the node
        t = node.node_type
        type_counter = self.node_type_counts[t] + 1
        node_id = f'{t}-{type_counter}'
        node._id = node_id
        self.node_type_counts[t] = type_counter
        if type(node) == InputNode:
            self.inputs[node_id] = {
                'name': node.name,
                'type': node.input_type.capitalize(),
            }
        elif type(node) == OutputNode:
            self.outputs[node_id] = {
                'name': node.name,
                'type': node.output_type.capitalize(),
            }
        self.nodes[node_id] = node

    def add_node(self, node: NodeTemplate) -> None:
        """Add a Node to the Pipeline. It is your responsibility to accordingly change and connect NodeOutputs to and from the new Node with other constitutent Nodes in the Pipeline before calling this method so that the overall Pipeline still has the correct functionality. Often, it may be easier to create a new Pipeline from scratch using the construction_str method as a guide.

        Parameters:
            node (NodeTemplate): The Node to add to the Pipeline.
        """
        if self.share_status == PipelineShareStatus.RUN:
            raise ValueError('Pipeline: cannot add nodes to a run-only pipeline.')
        # logic for adding node and input edges is analogous to __init__
        self._add_node(node)
        # add edges for the node's inputs
        for input_name, outputs in node._inputs.items():
            if outputs == []:
                print(
                    f'WARNING: {node.__class__.__name__} node did not receive any inputs for input field {input_name}'
                )
            # an input could have aggregated several NodeOutputs
            for output in outputs:
                # Edges are specifically defined by source/target handles,
                # derived from the node ids
                source_node_id = output.source._id
                output_field = output.output_field
                source_handle = f'{source_node_id}-{output_field}'
                target_handle = f'{node._id}-{input_name}'
                # Create an edge id following ReactFlow's formatting
                id = f'reactflow__edge-{source_node_id}{source_handle}-{node._id}{target_handle}'
                self.edges.append(
                    {
                        'source': source_node_id,
                        'sourceHandle': source_handle,
                        'target': node._id,
                        'targetHandle': target_handle,
                        'id': id,
                    }
                )
            return

    # Replace one node with another. Nodes should be of the same exact type.
    # Any inputs and outputs to the replaced node are kept as inputs and
    # outputs of the new node.
    # If the replacement node is of a different type, users should provide
    # input and output maps from old I/O names to new I/O names.
    def replace_node(
        self,
        node_id: str,
        replacement_node: NodeTemplate,
        input_map: dict[str, str] = None,
        output_map: dict[str, str] = None,
    ) -> None:
        """Replace one node with another. The replacement Node should already have been instantiated. Nodes should be of the same exact type. Any inputs and outputs to the replaced node are kept as inputs and outputs of the new node. If the replacement node is of a different type, users should provide input and output maps from old I/O names to new I/O names. Warnings are printed if the replaced node and the replacement node are of different types.

        Parameters:
            node_id (str): The string ID of the node to replace.
            replacement_node (NodeTemplate): The node to replace with.
            input_map (dict[str, str]): A mapping from old input names to new input names. E.g. if the old node had inputs "input_1" and "input_2" and the new node had inputs "input_3" and "input_4", then the input_map could be {"input_1": "input_3", "input_2": "input_4"}.
            output_map (dict[str, str]): A mapping from old output names to new output names.
        """
        if self.share_status == PipelineShareStatus.RUN:
            raise ValueError('Pipeline: cannot replace nodes in a run-only pipeline.')
        if node_id not in self.nodes.keys():
            raise ValueError(f'Pipeline: Node id {node_id} not found.')
        existing_node = self.nodes[node_id]
        if not (type(existing_node) == type(replacement_node)):
            print(
                f'WARNING: Replacement node type ({type(replacement_node)}) does not equal the type of the existing node ({type(existing_node)}), which may cause functionality issues.'
            )
        # if an input_map is given, the map keys should be a subset of the
        # existing node's _inputs keys
        if input_map:
            if not set(input_map.keys()).issubset(set(existing_node._inputs.keys())):
                raise ValueError(
                    'Pipeline: Input map\'s keys do not constitute a subset of the existing node\'s input names.'
                )
            mapped_inputs = {}
            for name, mapped_name in input_map.items():
                mapped_inputs[mapped_name] = existing_node._inputs[name]
            replacement_node._inputs = mapped_inputs
        else:
            replacement_node._inputs = existing_node._inputs
        # the out-edge IDs stay mostly the same as the replacement node takes
        # the existing node's ID; if the output field names are changed (e.g.
        # via an output_map), then we can modify the edges' handle attribute
        if output_map:
            for e in self.edges:
                if e['source'] == node_id:
                    old_output_field = e['sourceHandle'].split('-')[-1]
                    if old_output_field not in output_map.keys():
                        raise ValueError(
                            f'Pipeline: Output map does not contain existing node\'s output {old_output_field}.'
                        )
                    e['sourceHandle'] = f'{node_id}-{output_map[old_output_field]}'
        replacement_node._id = node_id
        self.nodes[node_id] = replacement_node
        return

    def delete_node(self, node_id: str) -> None:
        """Delete a Node from the pipeline. Any NodeOutputs going into or out of the Node (grpah edges) will also be removed.

        Params:
            node_id (str): The string ID of the node to delete.
        """
        if self.share_status == PipelineShareStatus.RUN:
            raise ValueError('Pipeline: cannot delete nodes from a run-only pipeline.')
        if node_id not in self.nodes.keys():
            raise ValueError(f'Pipeline: node id {node_id} not found.')
        del self.nodes[node_id]
        updated_edges = []
        # delete all the out-edges of the node
        for e in self.edges:
            if e['source'] == node_id:
                print(
                    f"WARNING: Removing edge from deleted node {node_id} to node {e['target']}"
                )
                # assume that output field names don't contain hyphens
                target_node_input_name = e['targetHandle'].split('-')[-1]
                target_node = self.nodes[e['target']]
                target_node._inputs[target_node_input_name] = None
            else:
                updated_edges.append(e)
        self.edges = updated_edges
        return

    def save(
        self,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
        update_existing: bool = False,
    ) -> dict:
        """Save the Pipeline to the VectorShift platform.

        Parameters:
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.
            update_existing: If True, update an existing Pipeline using the ID in the object (the Pipeline should have a non-None ID). If False, save as a new Pipeline.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if self.share_status == PipelineShareStatus.RUN:
            raise ValueError('Pipeline: cannot save or update a run-only pipeline.')
        if update_existing and not self.id:
            raise ValueError(
                'Pipeline: Error updating, pipeline object does not have an existing ID. It must be saved as a new pipeline.'
            )
        # if update_existing is False, save as a new pipeline
        if not update_existing:
            self.id = None

        # API_PIPELINE_SAVE_ENDPOINT differentiates between saving and updating
        # pipelines depending on whether or not the JSON has an id
        # (logic in api repo)
        response = requests.post(
            API_PIPELINE_SAVE_ENDPOINT,
            data=({'pipeline': self.to_json()}),
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )

        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        if 'pipeline' in response:
            self.id = response['pipeline'].get('id')
        elif 'id' in response:
            self.id = response['id']
        if 'branch' in response:
            self.branch_id = response['branch'].get('id')
        print(f'Successfully saved pipeline with ID {self.id}.')
        return response

    def update(
        self, api_key: str = None, public_key: str = None, private_key: str = None
    ):
        """Update an existing Pipeline in the VectorShift platform.

        Parameters:
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        self.save(api_key, public_key, private_key, update_existing=True)

    # Sharing structure: list of {user_id, org_id, permissions}
    def share(
        self,
        shared_users: list[dict[str, str]],
        append: bool = False,
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ):
        """Share a Pipeline with other users on the VectorShift platform. The Pipeline must already exist on the VectorShift platform. Permissions must be one of "Run" or "Edit".

        Parameters:
            shared_users (list[dict[str, str]]): A list of users and their permissions to share the Pipeline with. Each user should contain keys "user_id", "org_id", corresponding to their user and organization IDs, and "permissions".
            append (bool): If True, appends the shared users to the existing list of shared users. If False, replaces the existing list of shared users.
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Error sharing: Pipeline does not have an existing ID. It must be saved in order to be shared'
            )
        for u in shared_users:
            if 'user_id' not in u or 'org_id' not in u or 'permissions' not in u:
                raise ValueError(
                    'Error sharing: Each shared user should contain keys "user_id", "org_id", and "permissions"'
                )
            if u['permissions'] not in PIPELINE_SHARE_PERMISSIONS:
                raise ValueError(
                    f'Error sharing: Invalid permissions value {u["permissions"]}. Permissions should be one of {PIPELINE_SHARE_PERMISSIONS}'
                )
        response = requests.post(
            API_PIPELINE_SHARE_ENDPOINT,
            data={
                'pipeline_id': self.id,
                'shared_users': json.dumps(shared_users),
                'append': append,
            },
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error sharing Pipeline: {response.text}')
        response = response.json()
        return response

    def share_with_permissions(
        self, shared_users: list[dict[str, str]], permissions: str = 'Edit', append=False
    ):
        """Share a Pipeline with other users (all with the same permissions) on the VectorShift platform. The Pipeline must already exist on the VectorShift platform. The permissions must be one of "Run" or "Edit".

        Parameters:
            shared_users: A list of users and their permissions to share the Pipeline with. Each user should contain keys "user_id" and "org_id", corresponding to their user and organization IDs.
            permissions: The permissions to share the Pipeline with. Must be one of "Run" or "Edit".
            append: If True, appends the shared users to the existing list of shared users. If False, replaces the existing list of shared users.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        for u in shared_users:
            u['permissions'] = permissions
        return self.share(shared_users, append)

    def get_shared_users(
        self, api_key: str = None, public_key: str = None, private_key: str = None
    ) -> dict:
        """Get the list of shared users for a Pipeline on the VectorShift platform. The Pipeline must already exist on the VectorShift platform.

        Parameters:
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform including a list of shared users.
        """
        if not self.id:
            raise ValueError(
                'Error: Pipeline does not have an existing ID. It must be saved in order to retrieve shared users'
            )
        response = requests.get(
            API_PIPELINE_SHARED_USERS_ENDPOINT,
            params={'pipeline_id': self.id},
            headers={
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        if response.status_code != 200:
            raise Exception(f'Error getting shared users: {response.text}')
        response = response.json()
        return response

    def _setup_run_inputs(
        self,
        inputs: dict[str, str | File | list[File]],
        temporary_file_inputs: dict[str, str | list[str]],
    ):
        run_inputs = {}
        for k, v in inputs.items():
            if isinstance(v, str):
                if k in temporary_file_inputs:
                    raise ValueError(
                        'Cannot run Pipeline with both strings and Files used for the same input.'
                    )
                run_inputs[k] = v
            elif isinstance(v, File):
                run_inputs[k] = v.to_json_rep()
            elif isinstance(v, list):
                if not all(isinstance(f, File) for f in v):
                    raise ValueError(
                        'Cannot run Pipeline with an input list that contains non-File objects.'
                    )
                run_inputs[k] = [f.to_json_rep() for f in v]
            else:
                raise ValueError(
                    f'Error running Pipeline: Invalid input type {type(v)} for input {k}.'
                )
        file_inputs = {}
        for k, v in temporary_file_inputs.items():
            if isinstance(v, str):
                v = [v]
            if not isinstance(v, list) or not (all(isinstance(el, str) for el in v)):
                raise ValueError(f'Invalid input type for temporary_file_inputs key {k}')
            append_counter = 1
            for file_path in v:
                if not os.path.exists(file_path):
                    raise ValueError(f'File with path {file_path} does not exist.')
                if os.path.getsize(file_path) > MAX_FILE_UPLOAD_SIZE:
                    raise ValueError(
                        f'File with path {file_path} is too large to upload.'
                    )
                filetype = mimetypes.guess_type(file_path)[0]
                file_inputs[f'{k}-{append_counter}'] = (
                    file_path,
                    open(file_path, 'rb'),
                    filetype,
                )
        return run_inputs, file_inputs

    def run(
        self,
        inputs: dict[str, str | File | list[File]] = {},
        temporary_file_inputs: dict[str, str | list[str]] = {},
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Run a Pipeline on the VectorShift platform. The Pipeline must already exist on the VectorShift platform. Inputs can be a string or one or more files. inputs should map the Pipeline's input names to strings or Files referencing files which already exist on the VectorShift platform. temporary_file_inputs should map input names to paths to files meant to be uploaded temporarily when running the Pipeline.

        Parameters:
            inputs: A dictionary of inputs to pass to the Pipeline. The keys should correspond to the names of the Pipeline's defined inputs and the values should correspond to the defined data types for the inputs. String inputs should be passed as strings, and file (and audio) inputs should be passed as File objects.
            temporary_file_inputs: If the Pipeline has defined file inputs and you want to run the Pipeline with new uploaded files for those inputs, this dictionary should contain a mapping of the file input names to local file paths. When the Pipeline is run, these files will be uploaded temporarily to the VectorShift platform to be used in the Pipeline run and will not be saved to your storage.
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform including the results of the run.
        """
        if not self.id:
            raise ValueError(
                'Pipeline: Pipeline object must be saved before it can be run.'
            )

        run_inputs, file_inputs = self._setup_run_inputs(inputs, temporary_file_inputs)

        if file_inputs == {}:
            response = requests.post(
                API_PIPELINE_RUN_ENDPOINT,
                data=(
                    {
                        'pipeline_id': self.id,
                        'inputs': json.dumps(run_inputs),
                    }
                ),
                headers={
                    'Api-Key': api_key or vectorshift.api_key,
                    'Public-Key': public_key or vectorshift.public_key,
                    'Private-Key': private_key or vectorshift.private_key,
                },
            )
        else:
            response = requests.post(
                API_PIPELINE_RUN_ENDPOINT,
                files=file_inputs,
                data={
                    'pipeline_id': self.id,
                    'inputs': json.dumps(run_inputs),
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

    async def run_async(
        self,
        inputs: dict[str, str | File | list[File]] = {},
        temporary_file_inputs: dict[str, str | list[str]] = {},
        api_key: str = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        """Run a Pipeline on the VectorShift platform asynchronously. The Pipeline must already exist on the VectorShift platform. Also see Pipeline.run().

        Parameters:
            inputs: A dictionary of inputs to pass to the Pipeline. The keys should correspond to the names of the Pipeline's defined inputs and the values should correspond to the defined data types for the inputs. String inputs should be passed as strings, and file (and audio) inputs should be passed as File objects.
            temporary_file_inputs: If the Pipeline has defined file inputs and you want to run the Pipeline with new uploaded files for those inputs, this dictionary should contain a mapping of the file input names to local file paths. When the Pipeline is run, these files will be uploaded temporarily to the VectorShift platform to be used in the Pipeline run and will not be saved to your storage.
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform including the results of the run.
        """
        try:
            import aiohttp
        except ImportError:
            raise Exception(
                'Pipeline: aiohttp must be installed to run pipelines asynchronously.'
            )
        if not self.id:
            raise ValueError(
                'Pipeline: Pipeline object must be saved before it can be run.'
            )
        run_inputs, file_inputs = self._setup_run_inputs(inputs, temporary_file_inputs)
        async with aiohttp.ClientSession() as session:
            if file_inputs == {}:
                response = await session.post(
                    API_PIPELINE_RUN_ENDPOINT,
                    data=(
                        {
                            'pipeline_id': self.id,
                            'inputs': json.dumps(inputs),
                        }
                    ),
                    headers={
                        'Api-Key': api_key or vectorshift.api_key,
                        'Public-Key': public_key or vectorshift.public_key,
                        'Private-Key': private_key or vectorshift.private_key,
                    },
                )
            else:
                response = await session.post(
                    API_PIPELINE_RUN_ENDPOINT,
                    files=file_inputs,
                    data={
                        'pipeline_id': self.id,
                        'inputs': json.dumps(run_inputs),
                    },
                    headers={
                        'Api-Key': api_key or vectorshift.api_key,
                        'Public-Key': public_key or vectorshift.public_key,
                        'Private-Key': private_key or vectorshift.private_key,
                    },
                )
            if response.status != 200:
                raise Exception(await response.text())
            response = await response.json()
            return response

    # NB probably nicer to call using deploy.py
    def delete(
        self, api_key: str = None, public_key: str = None, private_key: str = None
    ) -> dict:
        """Delete the Pipeline on the VectorShift platform. The Pipeline must already exist on the VectorShift platform. The Config object in the vectorshift.deploy module can be alternatively used. This method clears the ID associated with the Pipeline object.

        Parameters:
            api_key: The API key to use for authentication.
            public_key: The public key to use for authentication, if applicable.
            private_key: The private key to use for authentication, if applicable.

        Returns:
            dict: The JSON response from the VectorShift platform.
        """
        if not self.id:
            raise ValueError(
                'Pipeline: Pipeline object has no ID and so does not correspond to a Pipeline on the VectorShift platform.'
            )
        headers = (
            {
                'Api-Key': api_key or vectorshift.api_key,
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            },
        )
        response = requests.delete(
            API_PIPELINE_DELETE_ENDPOINT,
            data={'pipeline_ids': [self.id]},
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        # reset the ID
        self.id = None
        print('Successfully deleted Pipeline.')
        return response
