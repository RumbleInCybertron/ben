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

      *  **POST** `/user/login`
      
      Authenticate an existing user.
      
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
        "message": "Login successful"
      }
      ```

      *  **GET** `/user/users`
      
      Retrieve all users (admin functionality).

      **Response**:
      ```json
      [
        {
          "id": 1,
          "user_name": "string"
        }
      ]
      ```

      *  **GET** `/user/{id}`
      
      Retrieve a user by ID.

      **Response**:
      ```json
      {
        "id": 1,
        "user_name": "string"
      }
      ```

      *  **PUT** `/user/{id}/reward`
      
      Update user rewards.
      
      **Request Body**:
      ```json
      {
        "gold": 100,
        "diamond": 25
      }
      ```
      **Response**:
      ```json
      {
        "message": "User rewards updated successfully"
      }
      ```

  2.  Quest Catalog Service
      *  **POST** `/catalog/quests`  
      Create a new quest.
      
      **Request Body**:
      ```json
      [
        {
          "quest_id": 1,
          "name": "Daily Login",
          "description": "Log in daily to earn rewards",
          "reward_id": 1,
          "streak": 1,
          "duplication": 0
        }
      ]
      ```

      **Response**:
      ```json
      {
        "message": "Quest created successfully"
      }
      ```

      *  **GET** `/catalog/quests`  
      Retrieve a list of available quests.
      
      **Response**:
      ```json
      [
        {
          "quest_id": 1,
          "name": "Daily Login",
          "description": "Log in daily to earn rewards",
          "reward_id": 1,
          "streak": 1,
          "duplication": 0
        }
      ]
      ```

      *  **GET** `/catalog/quests/{id}`  
      Retrieve quest details by ID.
      
      **Response**:
      ```json
      {
        "quest_id": 1,
        "name": "Daily Login",
        "description": "Log in daily to earn rewards",
        "reward_id": 1,
        "streak": 1,
        "duplication": 0
      }
      ```

      *  **PUT** `/catalog/quests/{id}`  
      Update quest details.

      **Request Body**:
      ```json
      {
        "name": "New Quest Name",
        "description": "Updated description",
        "streak": 3,
        "duplication": 1
      }      
      ```

      **Response**:
      ```json
      {
        "message": "Quest updated successfully"
      }
      ```

      * **DELETE** `/catalog/quests/{id}
      Delete a quest by ID.
      
      **Response**:
      ```json
      {
        "message": "Quest deleted successfully"
      }
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

      *  **POST** `/user-quests/sign-in-three-times`
      Process the "Sign In Three Times" quest.
      **Request Body**:
      ```json
        {
          "user_id": 1
        }
      ```
        **Response**:
        ```json
        {
          "message": "Quest completed successfully"
        }
        ```

      *  **POST** `/user-quests/`
      Create a new user quest.
      **Request Body**:
      ```json
      {
        "user_id": 1,
        "quest_id": 2
      }
      ```
      **Response**:
      ```json
      {
        "message": "User quest created successfully"
      }
      ```

      * **PUT** `/user-quests/
      Update progress for a user quest.
      **Request Body**:
      ```json
      {
        "user_id": 1,
        "quest_id": 1,
        "progress": 100
      }
      ```
      **Response**:
      ```json
      {
        "message": "Quest progress updated successfully"
      }
      ```
