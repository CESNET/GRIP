GRIP
====

Database of suspicious GRoups of IP addresses

GENERAL INFORMATION
-------------------

GRIP (Group of IPs) system is

GRIP allows to register network addresses suspicious of harmful activities in groups. These groups are created based on the similarity of multiple security incident reports. Groups are stored locally and regularly updated. In practice, these groups could be botnets.

System is implemented in Python. All used services are open source.


MOTIVATION
----------

The motivation for creating such a system was to connect information about whether the suspected network address is with some other addresses in the group, that is, if it is in the worst possible case it is part of a botnet. 

Using such a system would play a role in cleaning network traffc, in Scrubbing Center. If the network address would have really bad reputable score on the NERD system, or the traffc from the address would be disabled, then blocking other addresses from the same group can be considered. Also it will create a database of network addresses that may not have a record on NERD system, so it extend its database, because the GRIP system will extract security incident information from multiple sources. 

The goal is to find some patterns of botnets behavior and make rules to find all members of botnets.

The main problem is to verify that the found group is really botnet.


NOTICE
------

Information in Wiki pages are about system solution in production state. Information about testing solution are in page [https://github.com/CESNET/GRIP/wiki/Testing](Testing).

