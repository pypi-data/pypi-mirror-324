import os
import typing
import warnings

import gguf
import numpy as np
from sklearn.decomposition import PCA
import torch
from transformers import PreTrainedModel, PreTrainedTokenizerBase, AutoTokenizer
from dataclasses import dataclass
import tqdm

from .model import ControlModel, model_layer_list
from .dataset import DatasetEntry


@dataclass
class ControlVector:
    model_type: str
    directions: dict[int, np.ndarray]

    @classmethod
    def train(
        cls,
        model: "PreTrainedModel | ControlModel",
        dataset: list[DatasetEntry],
        **kwargs,
    ) -> "ControlVector":
        """
        Train a ControlVector for a given model and tokenizer using the provided dataset.

        Args:
            model (PreTrainedModel | ControlModel): The model to train against.
            tokenizer (PreTrainedTokenizerBase): The tokenizer to tokenize the dataset.
            dataset (list[DatasetEntry]): The dataset used for training.
            **kwargs: Additional keyword arguments.
                max_batch_size (int, optional): The maximum batch size for training.
                    Defaults to 32. Try reducing this if you're running out of memory.
                method (str, optional): The training method to use. Can be either
                    "pca_diff" or "pca_center". Defaults to "pca_diff".

        Returns:
            ControlVector: The trained vector.
        """
        tokenizer = AutoTokenizer.from_pretrained(model.model_name, token=model.token)
        tokenizer.pad_token_id = 0

        with torch.inference_mode():
            dirs = read_representations(
                model,
                tokenizer,
                dataset,
                **kwargs,
            )
        return cls(model_type=model.config.model_type, directions=dirs)

    def export_gguf(self, path: os.PathLike[str] | str):
        """
        Export a trained ControlVector to a llama.cpp .gguf file.
        Note: This file can't be used with llama.cpp yet. WIP!

        ```python
        vector = ControlVector.train(...)
        vector.export_gguf("path/to/write/vector.gguf")
        ```
        ```
        """

        arch = "controlvector"
        writer = gguf.GGUFWriter(path, arch)
        writer.add_string(f"{arch}.model_hint", self.model_type)
        writer.add_uint32(f"{arch}.layer_count", len(self.directions))
        for layer in self.directions.keys():
            writer.add_tensor(f"direction.{layer}", self.directions[layer])
        writer.write_header_to_file()
        writer.write_kv_data_to_file()
        writer.write_tensors_to_file()
        writer.close()

    @classmethod
    def import_gguf(cls, path: os.PathLike[str] | str) -> "ControlVector":
        reader = gguf.GGUFReader(path)

        archf = reader.get_field("general.architecture")
        if not archf or not len(archf.parts):
            warnings.warn(".gguf file missing architecture field")
        else:
            arch = str(bytes(archf.parts[-1]), encoding="utf-8", errors="replace")
            if arch != "controlvector":
                warnings.warn(
                    f".gguf file with architecture {arch!r} does not appear to be a control vector!"
                )

        modelf = reader.get_field("controlvector.model_hint")
        if not modelf or not len(modelf.parts):
            raise ValueError(".gguf file missing controlvector.model_hint field")
        model_hint = str(bytes(modelf.parts[-1]), encoding="utf-8")

        directions = {}
        for tensor in reader.tensors:
            if not tensor.name.startswith("direction."):
                continue
            try:
                layer = int(tensor.name.split(".")[1])
            except:
                raise ValueError(
                    f".gguf file has invalid direction field name: {tensor.name}"
                )
            directions[layer] = tensor.data

        return cls(model_type=model_hint, directions=directions)

    def _helper_combine(
        self, other: "ControlVector", other_coeff: float
    ) -> "ControlVector":
        if self.model_type != other.model_type:
            warnings.warn(
                "Trying to add vectors with mismatched model_types together, this may produce unexpected results."
            )

        model_type = self.model_type
        directions: dict[int, np.ndarray] = {}
        for layer in self.directions:
            directions[layer] = self.directions[layer]
        for layer in other.directions:
            other_layer = other_coeff * other.directions[layer]
            if layer in directions:
                directions[layer] = directions[layer] + other_layer
            else:
                directions[layer] = other_layer
        return ControlVector(model_type=model_type, directions=directions)

    def __eq__(self, other: "ControlVector") -> bool:
        if self is other:
            return True

        if self.model_type != other.model_type:
            return False
        if self.directions.keys() != other.directions.keys():
            return False
        for k in self.directions.keys():
            if (self.directions[k] != other.directions[k]).any():
                return False
        return True

    def __add__(self, other: "ControlVector") -> "ControlVector":
        if not isinstance(other, ControlVector):
            raise TypeError(
                f"Unsupported operand type(s) for +: 'ControlVector' and '{type(other).__name__}'"
            )
        return self._helper_combine(other, 1)

    def __sub__(self, other: "ControlVector") -> "ControlVector":
        if not isinstance(other, ControlVector):
            raise TypeError(
                f"Unsupported operand type(s) for -: 'ControlVector' and '{type(other).__name__}'"
            )
        return self._helper_combine(other, -1)

    def __neg__(self) -> "ControlVector":
        directions: dict[int, np.ndarray] = {}
        for layer in self.directions:
            directions[layer] = -self.directions[layer]
        return ControlVector(model_type=self.model_type, directions=directions)

    def __mul__(self, other: int | float | np.int_ | np.float64) -> "ControlVector":
        directions: dict[int, np.ndarray] = {}
        for layer in self.directions:
            directions[layer] = other * self.directions[layer]
        return ControlVector(model_type=self.model_type, directions=directions)

    def __rmul__(self, other: int | float | np.int_ | np.float64) -> "ControlVector":
        return self.__mul__(other)

    def __truediv__(self, other: int | float | np.int_ | np.float64) -> "ControlVector":
        return self.__mul__(1 / other)


def read_representations(
    model: "PreTrainedModel | ControlModel",
    tokenizer: PreTrainedTokenizerBase,
    inputs: list[DatasetEntry],
    hidden_layers: typing.Iterable[int] | None = None,
    batch_size: int = 32,
    method: typing.Literal["pca_diff", "pca_center", "umap"] = "pca_diff",
    transform_hiddens: (
        typing.Callable[[dict[int, np.ndarray]], dict[int, np.ndarray]] | None
    ) = None,
) -> dict[int, np.ndarray]:
    """
    Extract the representations based on the contrast dataset.
    """
    if not hidden_layers:
        hidden_layers = range(-1, -model.config.num_hidden_layers, -1)

    # normalize the layer indexes if they're negative
    n_layers = len(model_layer_list(model))
    hidden_layers = [i if i >= 0 else n_layers + i for i in hidden_layers]

    # the order is [positive, negative, positive, negative, ...]
    train_strs = [s for ex in inputs.entries for s in (ex.positive, ex.negative)]

    layer_hiddens = batched_get_hiddens(
        model, tokenizer, train_strs, hidden_layers, batch_size
    )

    if transform_hiddens is not None:
        layer_hiddens = transform_hiddens(layer_hiddens)

    # get directions for each layer using PCA
    directions: dict[int, np.ndarray] = {}
    for layer in tqdm.tqdm(hidden_layers):
        h = layer_hiddens[layer]
        assert h.shape[0] == len(inputs.entries) * 2

        if method == "pca_diff":
            train = h[::2] - h[1::2]
        elif method == "pca_center":
            center = (h[::2] + h[1::2]) / 2
            train = h
            train[::2] -= center
            train[1::2] -= center
        elif method == "umap":
            train = h
        else:
            raise ValueError("unknown method " + method)

        if method != "umap":
            # shape (1, n_features)
            pca_model = PCA(n_components=1, whiten=False).fit(train)
            # shape (n_features,)
            directions[layer] = pca_model.components_.astype(np.float32).squeeze(axis=0)
        else:
            # still experimental so don't want to add this as a real dependency yet
            import umap  # type: ignore

            umap_model = umap.UMAP(n_components=1)
            embedding = umap_model.fit_transform(train).astype(np.float32)
            directions[layer] = np.sum(train * embedding, axis=0) / np.sum(embedding)

        # calculate sign
        projected_hiddens = project_onto_direction(h, directions[layer])

        # order is [positive, negative, positive, negative, ...]
        positive_smaller_mean = np.mean(
            [
                projected_hiddens[i] < projected_hiddens[i + 1]
                for i in range(0, len(inputs.entries) * 2, 2)
            ]
        )
        positive_larger_mean = np.mean(
            [
                projected_hiddens[i] > projected_hiddens[i + 1]
                for i in range(0, len(inputs.entries) * 2, 2)
            ]
        )

        if positive_smaller_mean > positive_larger_mean:  # type: ignore
            directions[layer] *= -1

    return directions


def batched_get_hiddens(
    model,
    tokenizer,
    inputs: list[str],
    hidden_layers: list[int],
    batch_size: int,
) -> dict[int, np.ndarray]:
    """
    Using the given model and tokenizer, pass the inputs through the model and get the hidden
    states for each layer in `hidden_layers` for the last token.

    Returns a dictionary from `hidden_layers` layer id to an numpy array of shape `(n_inputs, hidden_dim)`
    """
    batched_inputs = [
        inputs[p : p + batch_size] for p in range(0, len(inputs), batch_size)
    ]
    hidden_states = {layer: [] for layer in hidden_layers}
    with torch.no_grad():
        for batch in tqdm.tqdm(batched_inputs):
            # get the last token, handling right padding if present
            encoded_batch = tokenizer(batch, padding=True, return_tensors="pt")
            encoded_batch = encoded_batch.to(model.device)
            out = model(**encoded_batch, output_hidden_states=True)
            attention_mask = encoded_batch["attention_mask"]
            for i in range(len(batch)):
                last_non_padding_index = (
                    attention_mask[i].nonzero(as_tuple=True)[0][-1].item()
                )
                for layer in hidden_layers:
                    hidden_idx = layer + 1 if layer >= 0 else layer
                    hidden_state = (
                        out.hidden_states[hidden_idx][i][last_non_padding_index]
                        .cpu()
                        .float()
                        .numpy()
                    )
                    hidden_states[layer].append(hidden_state)
            del out

    return {k: np.vstack(v) for k, v in hidden_states.items()}


def project_onto_direction(H, direction):
    """Project matrix H (n, d_1) onto direction vector (d_2,)"""
    mag = np.linalg.norm(direction)
    assert not np.isinf(mag)
    return (H @ direction) / mag


def merge_vectors(
    vector1: ControlVector,
    vector2: ControlVector,
    method: str = "add",
) -> ControlVector:
    """
    Merge two ControlVector objects according to the specified method.

    Args:
        vector1 (ControlVector): The first vector to merge.
        vector2 (ControlVector): The second vector to merge.
        method (str, optional): The merging strategy. Supported values:
            - "add": Returns vector1 + vector2
            - "mean": Returns (vector1 + vector2) / 2
            - "subtract": Returns vector1 - vector2
            - "concat": Concatenate directions (not always meaningful, but provided as example)

          Defaults to "add".

    Returns:
        ControlVector: A new ControlVector that is the merged result.

    Example:
        >>> merged = merge_vectors(vec1, vec2, method="mean")
    """
    if not isinstance(vector1, ControlVector) or not isinstance(vector2, ControlVector):
        raise TypeError("Both arguments must be instances of ControlVector.")

    if method == "add":
        return vector1 + vector2
    elif method == "mean":
        return (vector1 + vector2) / 2
    elif method == "subtract":
        return vector1 - vector2
    elif method == "concat":
        # For 'concat', we simply stack the directions. This is somewhat unconventional,
        # but can be useful in certain advanced workflows.
        # If the same layer is present in both, we stack them along a new axis.
        directions = {}
        all_layers = set(vector1.directions.keys()).union(vector2.directions.keys())

        for layer in all_layers:
            dir1 = vector1.directions.get(layer)
            dir2 = vector2.directions.get(layer)

            if dir1 is None:
                directions[layer] = dir2
            elif dir2 is None:
                directions[layer] = dir1
            else:
                # Concat along the 0th dimension (new axis at the front).
                directions[layer] = np.stack((dir1, dir2), axis=0)

        # The resulting shape differs from the standard (d,) shape in ControlVector.
        # Post-processing might be required downstream.
        # We'll keep the model_type from vector1 for convenience.
        return ControlVector(model_type=vector1.model_type, directions=directions)
    else:
        raise ValueError(f"Unknown merge method '{method}'.")
