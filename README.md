# Real-time-Taxi-app-with-Django-Channels

##### Features:
1. Real time ride sharing application
2. Messaging between rider and driver using Django channels
3. JWT token based authentication

###### In this application below packages are used:
1. Python
2. Django
3. Django Channels
4. Django Rest Framework
5. PostgresSQL

###### More features to add

1. The rider cancels his request after a driver accepts it.
2. The server alerts all other drivers in the driver pool that someone has accepted a request.
3. The driver periodically broadcasts his location to the rider during a trip.
4. The server only allows a rider to request one trip at a time.
5. The rider can share his trip with another rider, who can join the trip and receive updates.
6. The server only shares a trip request to drivers in a specific geographic location.
7. If no drivers accept the request within a certain timespan, the server cancels the request and returns a message to the rider.
