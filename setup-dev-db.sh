#!/bin/bash

psql postgres -h localhost -U postgres -a -f schema.txt
 
psql postgres -h localhost -U postgres -a -f dev-schema.txt

