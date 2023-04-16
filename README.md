# ca4024-a2-covid19-abm
This repository contains code relating to assignment 2 for CA4024 abm of covid 19 transmission.

To run simulations excute the following command:

    python3 abm-covid.py

Custom parameters can also be set using the command line. For example to restrict magintude of movement for all agents to 0.02 run the following command:

    python3 abm-covid.py 0.02

To isolate infected agents run the following command:

    python3 abm-covid.py 0.05 isolate

Note program must be executed in same directory as pycxsimulator.py.
