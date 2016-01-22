#!/bin/sh
if [ -z "$1" ]; then
        echo "Entry argument not specified"
        exit 1
fi
echo "Checking $1"
allDsas=$(curl http://dxgrid-discovery:2379/v2/keys/dsas 2> /dev/null)
if [ $? -ne 0 ]; then
        echo "Unable to connect to etcd"
        exit 1
fi
sortedDsas=$(echo $allDsas | jq -r '.node.nodes | sort_by(.key | ltrimstr("/dsas/") | tonumber) | .[] | .value+"/"+(.key | ltrimstr("/dsas/"))')
for aDsa in $sortedDsas; do
        dsaIp=$(echo $aDsa | cut -d/ -f2)
        dsaNumber=$(echo $aDsa | cut -d/ -f3)
        echo -n "dsa$dsaNumber [$dsaIp]: "
        curl ldap://$dsaIp:2389/$1 -D /tmp/headers$dsaNumber -o /tmp/entry$dsaNumber > /dev/null 2>&1
        rc=$?
        if [ $rc -eq 39 ]; then
                echo "entry not found"
                exit 1
        fi
        if [ $rc -ne 0 ]; then
                echo "curl error occurred (rc: $rc)"
                exit 1
        fi
        cat /tmp/entry$dsaNumber | sort > /tmp/entry$dsaNumber.sorted
        thisDigest=$(openssl dgst -sha256 /tmp/entry$dsaNumber.sorted | cut -d' ' -f2)
        echo $thisDigest
        if [ -z "$prevDigest" ]; then
                prevDigest=$thisDigest
                continue
        fi
        if [ "$thisDigest" != "$prevDigest" ]; then
                echo "Entry mismatch!"
                exit 1
        fi
done

echo "Entry is consistent in all DSAs"
