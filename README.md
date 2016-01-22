# vapp-config-forwardinc-mw

===================================

Config for the scalable forwardinc solution

This config needs to work with dxgrid-discovery sidecar (vapp-config-discovery-forwardinc).

How this config works:

Each POD runs a single DSA instance. The DSA name follows the format dsa[DSA number]. The DSA
number is an integer from 0..n, where n is the number of replicas. This DSA number is assigned
by the dxgrid-discovery sidecar, and can be queried from etcd.

Sidecar

1. POD created by kubernetes
2. (01 GetIPs) Wait for this POD's entry to exist in etcd under the /dsas subtree.
   It looks for an entry under /dsas with value matching this POD's Hostname/IP.
   A matching entry for a POD with hostname "dxgrid-data-rc-ylgiq" and IP "10.244.85.6"
   looks like this:
   
   ```
   {
        "key": "/dsas/0",
        "value": "dxgrid-data-rc-ylgiq/10.244.85.6",
        "modifiedIndex": 40,
        "createdIndex": 40
   }
   ```
   This entry in etcd is inserted by the dxgrid-discovery sidecar.
3. Once a matching entry is found, then the DSA name is established by using the information from the entry.
   The entry's subkey ("0" in the example above) is the DSA_number.
   In this example the DSA instance that runs in this POD will be named "dsa0".
4. (02 ProcessConfig) Queries etcd for all other DSA's and write out a single /knowledge/dsas.dxc.
   dxagent is also configured in this step. This DSA's certificate and private are also used by dxagent
   that runs in this POD.
   Writes /solution/.configured.

dxgrid service

1. (01 SymlinkConfigFolder) Creates symlinks for config, data and log folders.
2. (03 WaitForConfig) Waits for /solution/.configured
3. (04 LoadLDIF) If the db file does not exist then attempt to request for an onlinebackup
   from another DSA. See comments in (04 LoadLDIF)
4. DSA starts