import torch
from tqdm import tqdm
import copy

def prune_low_magnitude_unstructured(model: torch.nn.Module, sparsity: float) -> torch.nn.Module:
    """
    Prune model object (should be inherit torch.nn.Module class) by zeroing its individual weight based on threshold calculated.

    Args:
        model (torch.nn.Module): The model to prune.
        sparsity (float): The fraction of weights to prune. Must be between 0 and 1.

    Returns:
        torch.nn.Module: The modified model with pruned weights.
        
    Example:
        >>> model = SimpleNN()  # Assume this is a model with fc1, fc2, fc3, fc4, fc5 layers
        >>> pruned_model = prune_low_magnitude_unstructured(model, sparsity=0.2)
    """
    print("[OBOR] START OF PRUNING USING LOW_MAGNITUDE_UNSTRUCTURED METHOD")
    
    # Copy model to avoid editing the original object
    model_copy = copy.deepcopy(model)
    
    # Iterate over all parameters in the model
    for name, param in tqdm(model_copy.named_parameters(), desc='Pruning', leave=True):
        # Only prune the weights (ignore biases and embedding layers)
        if 'weight' in name and 'embedding' not in name:
            # Clone the weight matrix
            weights = param.data.clone()
            
            # Flatten the weight matrix and calculate the number of weights to prune
            flat_weights = torch.abs(weights.view(-1))  # Flatten and take absolute values
            k = int(sparsity * flat_weights.numel())  # Number of weights to prune
            
            # Find the threshold for pruning (k-th smallest magnitude)
            if k > 0:
                threshold = torch.topk(flat_weights, k, largest=False).values[-1]
                
                # Create a binary mask for pruning
                mask = torch.abs(weights) > threshold
                
                # Apply the mask to prune the weights
                weights *= mask.float()
            
            # Update the parameter with the pruned weights
            param.data = weights
    
    print("[OBOR] END OF PRUNING")
    return model_copy