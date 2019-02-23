# d-separation
Repository for implementing algorithm for determining d-separation in a DAG. Partial fulfilment of HW 1 for 601.676.

To run: `./run.sh`

To get d-separation results for different pair of nodes, add in the following format in the file `run.sh`:
```
python3 dsep.py -f <graph-file-name> -s <source-node> -t <target-node> -g <conditioned-nodes>
```
The conditioned nodes argument should be a string of space-separated integers.
