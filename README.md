#LilLink

LilLink is a simple URL shortener that is powered by Flask for the backend and Redis for the URL data store.

This URL shortener serves mostly for pedagogical purposes and as such, its deployment is kept to a bare minimum, whereupon the web server and the Redis server are both running on a local host.

## Set up

After downloading this repository and grabbing all the necessary dependencies, we must perform a simple setup for this Redis database that will be associated with this app.

In the database that this project references, we must create the following key-value pair:
('siteCounter', 0).

The 'siteCounter' key acts as a global counter for the number of URLs indexed.



