# vapp-config-forwardinc-mw

===================================

Config for the scalable forwardinc solution

How this config works:

Each POD runs a single DSA instance. The DSA name follows the format dsa[DSA number]. The DSA
number is an integer from 0..n, where n is the number of replicas. This DSA number is assigned
by the dxgrid-discovery sidecar, and can be queried from etcd.

dxgrid-discovery

Monitor service that watches for dxgrid pods created/killed by kubernetes, and updates
etcd. All the other dxgrid pods watch etcd for changes and configure.

An etcd entry for a dxgrid POD with hostname "dxgrid-data-rc-ylgiq" and IP "10.244.85.6"
looks like this:
   
```
{
	"key": "/dsas/0",
	"value": "dxgrid-data-rc-ylgiq/10.244.85.6",
	"modifiedIndex": 40,
	"createdIndex": 40
}
```

dxgrid-dsa

This config is run by dxgrid container. It waits for this POD's entry to exist in etcd under the /dsas subtree.
It looks for an entry under /dsas with value matching this POD's Hostname/IP.

Once a matching entry is found, then the DSA name is established by using the information from the entry.
The entry's subkey ("0" in the example above) is the DSA_number.
In this example the DSA instance that runs in this POD will be named "dsa0".

Queries etcd for all other DSA's and write out a single /knowledge/dsas.dxc.
dxagent is also configured in this step. This DSA's certificate and private are also used by dxagent
that runs in this POD.

Attempt to get an onlinebackup from one of the other running dsas if possible, and use it as its own db.
If an onlibebackup cannot be obtained from other dsas, then load from LDIF as last resort.

Finally, keep watching etcd for changes and reconfigure.