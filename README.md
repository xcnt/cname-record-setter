# CNAME Record Setter #

Develop: [![Build Status](https://jenkins.dev.xcnt.io/buildStatus/icon?job=XCNT/cname-record-setter/develop)](https://jenkins.dev.xcnt.io/job/XCNT/job/cname-record-setter/job/develop/)
Master: [![Build Status](https://jenkins.dev.xcnt.io/buildStatus/icon?job=XCNT/cname-record-setter/master)](https://jenkins.dev.xcnt.io/job/XCNT/job/cname-record-setter/job/master/)

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
