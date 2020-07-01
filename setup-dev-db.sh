#!/bin/bash

psql postgres -h localhost -U postgres -f schema.txt
 
psql postgres -h localhost -U postgres -f dev-schema.txt

