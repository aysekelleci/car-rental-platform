# CAR RENTAL API

### How to run
1. clone repository
2. go to the project folder and run docker:
```bash
docker compose up --build
```
`Note:` change port:5002 if it is already used port 

3. check postman collection link for api requests:
[postman](https://www.postman.com/orange-meadow-393529/workspace/team-workspace/collection/21645071-962efa7c-03d8-4763-84e8-b4d84f0cf252?action=share&source=copy-link&creator=21645071)
- register users (both merchant and users)
- create/update/delete car as a merchant
- rent/return cars as a user
- check rental history for users


### Rent Price logic:
- Each car has its own daily price, with a default value of $50. The total fee is calculated by multiplying the rental duration (days) by the car’s daily price. 
* A special discount is applied for first-time renters to encourage new users (10%). 
+ Additional loyalty discounts are applied for every 5th and 10th rental, rewarding frequent customers.

### Car filter logic:
Users can filter cars based on following criteria:
- Brand and Model
* Minimum and Maximum Year
+ Minimum and Maximum Daily Price
+ Color
- Merchant Username
* Availability Status


### Tech Stack:
- Flask • SQLAlchemy • PostgreSQL • Docker • REST API
