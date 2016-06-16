#!/bin/bash
# ------------------------------------------------------------------
# [Miguel Angel Alvarez Cabrerizo (@n40lab)]  
# Add or Remove VM name and IP address to/from PowerDNS
# ------------------------------------------------------------------

VERSION=0.1.0
USAGE="Usage: pdns_hook -hv OP[DELETE|REPLACE] VM_NAME VM_IPADDR"

# --- Options processing -------------------------------------------
if [ $# == 0 ] ; then
    echo $USAGE
    exit 1;
fi

while getopts ":i:vh" optname
  do
    case "$optname" in
      "v")
        echo "Version $VERSION"
        exit 0;
        ;;
      "h")
        echo $USAGE
        exit 0;
        ;;
      "?")
        echo "Unknown option $OPTARG"
        exit 0;
        ;;
      ":")
        echo "No argument value for option $OPTARG"
        exit 0;
        ;;
      *)
        echo "Unknown error while processing options"
        exit 0;
        ;;
    esac
  done

shift $(($OPTIND - 1))

XPATH=/var/lib/one/remotes/datastore/xpath.rb
OP=$1
T64=$2

VM_NAME=`$XPATH -b $T64 UNAME`
VM_IP_ADDR=`$XPATH -b $T64 NIC/IP`

# --- Body --------------------------------------------------------

curl -X PATCH --data '{"rrsets": [ {"name": "'$VM_NAME'.artemit.mgmt.", "type": "A", "ttl": 86400, "changetype": "'$OP'", "records": [ {"content": "'$VM_IP_ADDR'", "disabled": false } ] } ] }' -H 'X-API-Key: eeetZYu3FtGG3bJc' http://jano.artemit.mgmt:8081/api/v1/servers/localhost/zones/artemit.mgmt.

# -----------------------------------------------------------------


