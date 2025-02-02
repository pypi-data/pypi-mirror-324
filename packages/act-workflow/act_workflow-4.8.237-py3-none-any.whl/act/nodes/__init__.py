from .chatmodels_node import ChatModelsNode
from .slack_node import SlackNode
from .openai_node import OpenAINode
from .data_transformation_node import DataTransformationNode
from .aggregate_node import AggregateNode
from .if_node import IfNode
from .delay_node import DelayNode
from .retry_node import RetryNode
from .parallel_node import ParallelNode
from .filter_node import FilterNode
from .sort_node import SortNode
from .join_node import JoinNode
from .split_node import SplitNode
from .request_node import RequestNode
from .start_node import StartNode
from .base_node_prod import BaseNode
from .openai_node import OpenAINode
from .github_node import GitHubNode

# You can also include a registry for all nodes if needed
NODES = {
    "ChatModels": ChatModelsNode,
    "Slack": SlackNode,
    "OpenAINode": OpenAINode,
    "DataTransformation": DataTransformationNode,
    "Aggregate": AggregateNode,
    "If": IfNode,
    "Delay": DelayNode,
    "Retry": RetryNode,
    "Parallel": ParallelNode,
    "Filter": FilterNode,
    "Sort": SortNode,
    "Join": JoinNode,
    "Split": SplitNode,
    "Request": RequestNode,
    "Start": StartNode,
    "GitHubNode": GitHubNode, 
    "BaseNode": BaseNode,
    "OpenAINode": OpenAINode,
    "base_node_prod": BaseNode
}