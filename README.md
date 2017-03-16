#LilLink

LilLink is a simple URL shortener that is powered by Flask for the backend and Redis for the URL data store.

This URL shortener serves mostly for pedagogical purposes and as such, this project has a minimalistic backbone.

## Set up

For the Redis database that is used, we use a global key-value pair as a counter, `('siteCounter', 0)`.
The 'siteCounter' key acts as a global counter for the number of URLs indexed.

Upon initializing LilLink, we immediately check to see whether `siteCounter` exists or not.

If not, we create it through Redis's SETNX command and give it the value of 0.


