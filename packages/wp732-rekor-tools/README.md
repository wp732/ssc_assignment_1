# A tool for verifying artifacts logged to Rekor  

You can find out more about this tool and the motivation behind it at https://github.com/wp732/ssc_assignment_1  

usage: wp732_rekor_tool [-h] [-d] [-c] [--inclusion INCLUSION] [--artifact ARTIFACT] [--consistency]  
                        [--tree-id TREE_ID] [--tree-size TREE_SIZE] [--root-hash ROOT_HASH] [-e ENTRY]  
  
Rekor Verifier  
  
options:  
  -h, --help            show this help message and exit  
  -d, --debug           Debug mode  
  -c, --checkpoint      Obtain latest checkpoint from Rekor Server public instance. When used with -d  
                        also saves the checkpoint to ~/checkpoint.json  
  --inclusion INCLUSION  
                        Verify inclusion of an entry in the Rekor Transparency Log using log index and  
                        artifact filename. Usage: --inclusion 126574567  
  --artifact ARTIFACT   Artifact filepath for verifying signature  
  --consistency         Verify consistency of a given checkpoint with the latest checkpoint.  
  --tree-id TREE_ID     Tree ID for consistency proof  
  --tree-size TREE_SIZE  
                        Tree size for consistency proof  
  --root-hash ROOT_HASH  
                        Root hash for consistency proof  
  -e ENTRY, --entry ENTRY  
                        Get Rekor log entry by log index Usage: --entry 126574567  
  
# Examples  

wp732_rekor_tool \  
    --checkpoint  
    
wp732_rekor_tool \  
    --inclusion <log index from .rekorBundle.Payload.logIndex of artifact bundle json> \  
    --artifact <file path to artifact that was cosigned>   

wp732_rekor_tool \  
    --consistency \  
    --tree-id <rekor tree id from .treeID of artifact bundle json> \  
    --tree-size <rekor tree size from .treeSize of artifact bundle json> \  
    --root-hash <rekor root hash from .rootHash of artifact bundle json>  
