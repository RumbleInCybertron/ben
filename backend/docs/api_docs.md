### API Documentation
## Base URL

Replace `<external-ip>` with the Ingress external IP:

  *  API Gateway: `http://<external-ip>/`

## Endpoints

  1.  User Authentication Service
      *  **POST** `/user/signup`
      
      Register a new user.
      
      **Request Body**:
      ```json
      {
        "user_name": "string",
        "password": "string"
      }
      ```
      **Response**:
      ```json
      {
        "message": "User created successfully"
      }
      ```

  2.  Quest Catalog Service
      *  **GET** `/catalog/quests`  
        Retrieve a list of available quests.
        
        **Response**:
        ```json
        [
          {
            "quest_id": 1,
            "name": "Daily Login",
            "description": "Log in daily",
            "reward_id": 1,
            "streak": 1,
            "duplication": 0
          }
        ]
        ```
    
  3.  Quest Processing Service
    *  **POST** `/user-quests/daily-login`
     Process the Daily Login quest for a user.
     **Request Body**:
     ```json
      {
        "user_id": 1
      }
     ```
      **Response**:
      ```json
      {
        "message": "Daily Login Quest processed successfully"
      }
      ```