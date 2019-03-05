# CNAME Record Setter #

Develop: [![Build Status](https://jenkins.dev.xcnt.io/buildStatus/icon?job=XCNT/cname-record-setter/develop)](https://jenkins.dev.xcnt.io/job/XCNT/cname-record-setter/develop)
Master: [![Build Status](https://jenkins.dev.xcnt.io/buildStatus/icon?job=XCNT/cname-record-setter/develop)](https://jenkins.dev.xcnt.io/job/XCNT/cname-record-setter/master)

This script scans for the DNS resolution of a specific A
the returned IPs to sync with another A record on a google cloud
DNS managed domain.

## Configuration ##

The script is available as a docker file on docker hub.
* `CNAME_RECORD_SETTER_SET_RECORD` - The record which should be set from the ip addresses of the observed record.
* `CNAME_RECORD_SETTER_OBSERVED_RECORD` - The record which is observed to be set.
* `CNAME_RECORD_SETTER_PROJECT_ID` - The project id on google cloud where the provided zone is in which holds the record to be updated.

## Why? ##

We ran into the issue with a webflow site which should be hosted under the root domain.
Whilst it is possible to set a CNAME on a root domain, this would make it not possible to
resolv any sub domains, because the DNS standard states, a CNAME record to be the end of a
DNS resolution. Thus, no sub domains would be checked.

Some DNS provides supply unofficial ANAME records with a similar functionality, providing a transparent proxy of the DNS resolution.
This script implements this functionality by utilizing the Google Cloud DNS API. 

## License ##

This small script is licensed with the [MIT license](LICENSE).

## How to use ##

There is an example configuration file to run the 
[application on Kubernetes](kube/deployment.yaml). The docker image is also publicly available on
[docker hub](https://hub.docker.com/r/xcnt/cname-record-setter).
The `stable` tag refers to the latest build in the master branch. Otherwise all iamges
are published with teh branch and the git commit id if a pin to a specific version is required.
