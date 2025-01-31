from dtr_utils.tree_processing import (
    prune_to_max_depth,
    final_tree_generate_dual,
    find_parent_of_lowest_score,
    get_max_depth,
    min_depth,
    get_path_from_best_node,
    count_color_in_paths,
)

import graphviz
from anytree import Node, AnyNode, RenderTree
import pickle
import sys
import dill
from tqdm import tqdm
import string
from nltk.corpus import stopwords
from dtr_utils.ecd_score import (
    alignment_score,
    preprocess_batch,
    get_common_entity_kldiv,
    get_global_vocab,
)
import numpy as np

from dtr_utils import nlp_stanza, model, stop_words


# sys.setrecursionlimit(10000)  # Adjust the value as needed
# from anytree import AnyNode


def get_max_depth(node, depth=0):
    """
    Calculates the maximum depth of a tree.

    Args:
        node (Node): The root node of the tree or subtree.
        depth (int): The current depth in the traversal.

    Returns:
        int: The maximum depth of the tree.
    """
    if not node.children:
        return depth  # Return current depth if the node has no children
    return max(get_max_depth(child, depth + 1) for child in node.children)


def prune_to_max_depth(node, current_depth=0, max_depth=None):
    """
    Prunes the tree to keep only the nodes at the maximum depth.

    Args:
        node (Node): The current node of the tree.
        current_depth (int): The current depth in the tree traversal.
        max_depth (int): The maximum depth of the tree. If None, it will be calculated.

    Returns:
        bool: True if the node should be kept, False otherwise.
    """
    if max_depth is None:
        # Calculate max depth of the tree
        # max_depth = max((len(ancestor_path) for ancestor_path in node.iter_path()))
        max_depth = get_max_depth(node, depth=0)

    # Base case: Leaf nodes
    if not node.children:
        return current_depth == max_depth

    # Recursively check children and prune them if not at max depth
    to_keep = []
    for child in node.children:
        if prune_to_max_depth(child, current_depth + 1, max_depth):
            to_keep.append(child)

    # Replace children with the filtered list
    node.children = to_keep
    return current_depth == max_depth or bool(to_keep)


def find_parent_of_lowest_score(root):
    # Collect all leaf nodes
    leaf_nodes = root.leaves

    if not leaf_nodes:
        print("No leaf nodes found.")
        return None

    # Find the leaf node with the lowest score (assuming name is numeric)
    min_score_node = min(leaf_nodes, key=lambda n: float(n.name))

    return min_score_node


def sanitize_word(word):
    # Create a translation table for characters to be replaced
    translation_table = str.maketrans(
        {
            "<": "lesser than",
            ">": "greater than",
            "\n": " ",
            "\t": " ",
            "\\": "",
            "\r": "",
        }
    )
    return word.translate(translation_table)


def get_max_depth(node, depth=0):
    """
    Calculates the maximum depth of a tree.

    Args:
        node (Node): The root node of the tree or subtree.
        depth (int): The current depth in the traversal.

    Returns:
        int: The maximum depth of the tree.
    """
    if not node.children:
        return depth  # Return current depth if the node has no children
    return max(get_max_depth(child, depth + 1) for child in node.children)


def min_depth(root):
    """
    Recursively finds the minimum depth of the tree rooted at `root`.

    Args:
        root (AnyNode): The root node of the tree.

    Returns:
        int: The minimum depth of the tree.
    """
    # Base case: if a node is a leaf (no children), the depth is 1
    if not root.children:
        return 1

    # Recursively find the minimum depth among all children
    depths = [min_depth(child) for child in root.children]

    # Return the minimum depth + 1 (for the current node)
    return min(depths) + 1


def count_color_in_paths(node, n_color="blue", color_count=0):
    # Increment the color count if the current node's color matches n_color
    try:
        if node.n_color == n_color:
            color_count += 1
    except:
        pass
    # If the node is a leaf (no children), return the current color count for this path
    if not node.children:
        return [color_count]

    # Otherwise, traverse the children and collect color counts for each path
    color_path_counts = []
    for child in node.children:
        color_path_counts.extend(count_color_in_paths(child, n_color, color_count))

    return color_path_counts


def get_path_from_best_node(best_node):
    """
    Backtrack from the best_node to the root and return the path.

    Args:
        best_node (Node): The best node in the tree.

    Returns:
        list: The path from the root to the best_node (inclusive).
    """
    path = []

    # Backtrack from best_node to the root (including the best_node itself)
    current_node = best_node
    while current_node:
        path.append(current_node)
        current_node = current_node.parent

    # Reverse the list to get the path from root to best_node
    path.reverse()

    return path


# ---------------------Tree ECD score--------------------------------------


class Get_ECD_entities:
    def __init__(self, web_text):
        """
        Initializes the Get_ECD_entities class.

        Args:
            web_text (str): The input text from the web.
            leaf_node_text (str): The text for the leaf nodes.
        """
        self.nlp_stanza = nlp_stanza
        self.web_text = web_text
        self.stop_words = stop_words
        # self.stop_words = set(stopwords.words("english"))

        self.data = {"t1": {}, "t2": {}}
        self.data, self.filtered_web_text = self.process_one_text(
            self.web_text, "t1", self.data, task="initialization"
        )

    def process_one_text(self, text, key, data=None, task=None):
        """
        Processes a given text, filters out stopwords and punctuation,
        and extracts entities with their sentence indices.

        Args:
            text (str): The text to be processed.
            key (str): The key for storing data in the dictionary.
            data (dict): The existing data dictionary (optional).

        Returns:
            tuple: A tuple containing the updated data dictionary and filtered text.
        """
        # Initialize data dictionary if not provided

        # if data is None:
        #     data = {}

        if self.data:
            data = self.data

        # Create a sub-dictionary for the provided key
        data[key] = {}

        # Process the entire text with the global Stanza NLP pipeline
        doc_stanza = self.nlp_stanza(text)  # `nlp_stanza` is assumed to be global

        # Get sentences and entities from the processed document
        sentences = doc_stanza.sentences
        stop_words = self.stop_words  # Define the stop words list

        # Initialize an empty list to collect filtered tokens
        filtered_text = []

        for i, sentence in enumerate(sentences):
            filtered_tokens = []

            # Filter tokens in the sentence
            for word in sentence.words:
                if (
                    word.text.lower() not in stop_words
                    and word.text not in string.punctuation
                ):
                    filtered_tokens.append(word.text.lower())

            # Join tokens to reconstruct the filtered sentence
            filtered_text.append(" ".join(filtered_tokens))

            # Extract entities and update the data dictionary
            entities = [ent.text.lower() for ent in sentence.ents]
            for entity in entities:
                if entity not in data[key]:
                    data[key][entity] = {i}
                else:
                    data[key][entity].add(i)

        if task == "initialization":
            return data, filtered_text
        else:
            return data, filtered_text, self.filtered_web_text


class TreeGenerator:
    def __init__(self, input_root, true_context):
        """
        Initializes the TreeGenerator class.

        Args:
            input_root (AnyNode): The root node of the input tree (prebuilt using AnyNode).
            true_context (str): The true context to compute alignment scores.
        """
        self.input_root = input_root
        self.true_context = true_context
        self.root_plain = None
        self.node_counter = 1
        self.tree_ecd = Get_ECD_entities(true_context)

    def generate_tree(self):
        """
        Generates a plain tree by copying nodes from the input tree and computing alignment scores.

        Returns:
            AnyNode: The root node of the plain tree with additional attributes.
        """
        initial_context = (
            self.input_root.name
        )  # Initial context is the name of the input root
        self.root_plain = AnyNode(name=f"ROOT_PLAIN = {initial_context}")

        total_nodes = len(
            self.input_root.leaves
        )  # Count the total number of leaf nodes
        with tqdm(total=total_nodes) as progress_bar:
            self._traverse_and_copy(
                self.input_root, self.root_plain, [], 0, total_nodes, progress_bar
            )

        return self.root_plain

    def _traverse_and_copy(
        self, node, parent_plain, path_plain, level, total_nodes, progress_bar
    ):
        """
        Recursively traverses the input tree and copies nodes to the plain tree.

        Args:
            node (AnyNode): Current node in the input tree.
            parent_plain (AnyNode): Current parent node in the plain tree.
            path_plain (list): Accumulated plain text path.
            level (int): The current level of recursion.
            total_nodes (int): Total number of nodes in the tree for tqdm progress bar.
            progress_bar (tqdm): Progress bar instance.
        """
        # Extract relevant information from the node
        sanitized_word = node.name  # Name of the node
        n_color = getattr(node, "n_color", None)
        score = getattr(node, "score", None)
        ngram_tokens = getattr(node, "ngram_tokens", None)
        ngram_scores = getattr(node, "ngram_scores", None)
        llm_tokens = getattr(node, "llm_tokens", None)
        llm_scores = getattr(node, "llm_scores", None)

        # Create a new node in the plain tree
        new_node = AnyNode(
            id=self.node_counter,
            name=sanitized_word,
            parent=parent_plain,
            n_color=n_color,
            score=score,
            ngram_tokens=ngram_tokens,
            ngram_scores=ngram_scores,
            llm_tokens=llm_tokens,
            llm_scores=llm_scores,
        )

        # Increment the node counter
        self.node_counter += 1

        # Traverse children
        for child in node.children:
            self._traverse_and_copy(
                child,
                new_node,
                path_plain + [sanitized_word],
                level + 1,
                total_nodes,
                progress_bar,
            )

        # Handle leaf nodes
        if not node.children:
            complete_text_plain = "".join(path_plain)
            final_plain_node = AnyNode(name=f"{complete_text_plain}", parent=new_node)

            # Compute alignment score
            data, filtered_leaf_node_text, filtered_web_text = (
                self.tree_ecd.process_one_text(complete_text_plain, "t2")
            )

            # print("\nData,_traverse_and_copy\n",data,"\n\n")
            alignment_score_value, common_entity, missing_entity, extra_entity = (
                self._compute_alignment_score(
                    data, filtered_leaf_node_text, filtered_web_text
                )
            )
            leaf = AnyNode(
                name=[
                    alignment_score_value,
                    common_entity,
                    missing_entity,
                    extra_entity,
                ],
                parent=final_plain_node,
            )
            # print(alignment_score_value,leaf)
            # Update the progress bar
            progress_bar.update(1)

    @staticmethod
    def process_two_texts(t1, t2, data):

        # global_vocab = get_global_vocab(t1, t2)
        common_ent = set(data["t1"].keys()).intersection(set(data["t2"].keys()))
        missing_ent = set(data["t1"].keys()).difference(set(data["t2"].keys()))
        extra_ent = set(data["t2"].keys()).difference(set(data["t1"].keys()))
        # return data, global_vocab, common_ent, extra_ent, missing_ent, t1, t2
        return data, common_ent, extra_ent, missing_ent, t1, t2

    @staticmethod
    def _compute_alignment_score(data, filtered_leaf_node_text, filtered_web_text):
        (
            data,
            global_vocab,
            common_entity,
            extra_entity,
            missing_entity,
            text1,
            text2,
        ) = process_two_texts(filtered_web_text, filtered_leaf_node_text, data)
        # print("\nData,_compute_alignment_score\n",data,"\n\n")

        if len(common_entity) == 0:
            kl_div = [1]
        else:
            kl_div = get_common_entity_kldiv(
                text1, text2, data, global_vocab, common_entity
            )

        # return sum(kl_div) / len(kl_div), common_entity, missing_entity, extra_entity
        return (
            sum(kl_div) / len(kl_div),
            len(common_entity),
            len(missing_entity),
            len(extra_entity),
        )


class TreeLeafStats:
    def __init__(self, root):
        self.root = root
        self.leaf_nodes = self.get_leaf_nodes()
        self.missing_entity_list = [node.name[2] for node in self.leaf_nodes]
        self.extra_entity_list = [node.name[3] for node in self.leaf_nodes]
        print(self.missing_entity_list)
        print(self.extra_entity_list)
        self.sd_miss = np.std(self.missing_entity_list)
        self.sd_extra = np.std(self.extra_entity_list)
        self.avg_kl_div = np.mean(
            [node.name[0] for node in self.leaf_nodes if node.name[0] != -1]
        )
        self.ecd_scores = [self.get_score(node.name) for node in self.leaf_nodes]
        self.extend_leaf_nodes()

        # Return the modified root after initialization
        # return self.root

    def get_leaf_nodes(self):
        return self.root.leaves
        # return [node for node in self.root.descendants if node.is_leaf]

    def get_score(self, node):
        kl_div = node[0] if node[0] != -1 else self.avg_kl_div
        missing = node[2]
        extra = node[3]
        common = node[1]
        return (
            kl_div
            + self.sd_miss * ((missing * (missing + 1)) / (2 * common))
            + self.sd_extra * ((extra * (extra + 1)) / (2 * common))
        )

    def extend_leaf_nodes(self):
        for node, ecd_score in zip(self.leaf_nodes, self.ecd_scores):
            # AnyNode(parent=node, name=f"ECD Score: {ecd_score}")
            AnyNode(parent=node, name=ecd_score)

    def get_stats(self):
        return {
            "missing_entity_sd": self.sd_miss,
            "extra_entity_sd": self.sd_extra,
            "ecd_scores": self.ecd_scores,
        }

    def get_root(self):
        return self.root
