import torch
from tqdm import tqdm
import copy

def prune_low_magnitude_structured(model: torch.nn.Module, pruning_rate: float) -> torch.nn.Module:
    """
    Prune model object (should be inherit torch.nn.Module class) by changing its structure based on sum absolute weight of each neurons.

    Args:
        model (torch.nn.Module): Model to prune. Model should have layers 'fc1', 'fc2', 'fc3' and so on, on top of each other.
        pruning_rate (float): The fraction of neurons to prune in each layer. Must be between 0 and 1.

    Returns:
        torch.nn.Module: The modified model with pruned neurons.

    Example:
        >>> model = SimpleNN()  # Assume this is a model with fc1, fc2, fc3, fc4, fc5 layers
        >>> pruned_model = prune_low_magnitude_structured(model, pruning_rate=0.2)
    """
    print("[OBOR] START OF PRUNING USING LOW_MAGNITUDE_STRUCTURED METHOD")
    
    # Copy model to avoid editing the original object
    model_copy = copy.deepcopy(model)
    
    # Calculate how many fc layer inside the model
    num_fc_layers = sum(1 for name, _ in model_copy.named_children() if name.startswith("fc"))

    with torch.no_grad():
        for layer in tqdm(range(1, num_fc_layers + 1), desc='Pruning', leave=True):
            weight = getattr(model_copy, f'fc{layer}').weight.detach().clone()
            bias = getattr(model_copy, f'fc{layer}').bias.detach().clone()

            # Calculate sum absolute weights on each neurons
            sum_abs_weights = torch.sum(torch.abs(weight), dim=1)

            # Calculate how many neurons to prune base on pruning rate parameter
            num_neurons_to_prune = int(pruning_rate * weight.size(0))

            # Find the neuron that need to be pruned
            _, prune_indices = torch.topk(-sum_abs_weights, num_neurons_to_prune)

            # Create mask, the nouron that need to be prune will have False value in the mask
            mask = torch.ones(weight.size(0), dtype=torch.bool)
            mask[prune_indices] = False

            # Prune the weight and bias
            pruned_weight = weight[mask]
            pruned_bias = bias[mask]

            # Copy it back to copied model
            getattr(model_copy, f'fc{layer}').weight.data = pruned_weight
            getattr(model_copy, f'fc{layer}').bias.data = pruned_bias

            # Prune the input dimension for the next fc layer
            if layer < num_fc_layers:
                next_weight = getattr(model_copy, f'fc{layer+1}').weight.detach().clone()

                pruned_next_weight = next_weight[:, mask]

                getattr(model_copy, f'fc{layer+1}').weight.data = pruned_next_weight

    print("[OBOR] END OF PRUNING")
    return model_copy