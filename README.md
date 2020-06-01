# FMC-route-copy
Copy Routes from one FTD Sensor to another managed by the same FMC

## Step 1
Edit the env_lab file with your host, username and password etc.

## Step 2
$ pip3 install -r requirements.txt

## Step 3
$ python3 ./FMC-route-copy -d

This should show you the different containerUUID's (FTD sensors) and associated routes for those containers.

## Step 4
$ python3 ./FMC-route-copy -dtf

Dumps the routes to a file where the script ran ('fmc-route-output.txt'). You can manipulate it by removing some routes, etc.

## Step 5
$ python3 ./FMC-route-copy -l containerUUID

This will load the routes into the new FTD sensor (containerUUID). If you see errors it could be that the particular route already exists. It will continue down your list. (It will read from the file output from the -dtf option).
