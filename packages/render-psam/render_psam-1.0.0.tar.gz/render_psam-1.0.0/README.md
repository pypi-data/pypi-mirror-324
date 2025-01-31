
# Run batched

This is a very basic module that allows you to run a pytorch model on numpy arrays in batches. It handles
the batching for you, so you can just pass in a numpy array and get a numpy array back. It also works when the
input or return value is a dict of numpy arrays.