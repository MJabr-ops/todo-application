/api/register/POST,returns a json of registered user information
/api/login/POST,returns a json of user information and tokens
/api/refresh_token/POST ,returns an access token from cookies refresh token
/api/basket/GET , returns collections of user created todo's
/api/basket/POST , returns registered todo collection
/api/basket/<number>/GET ,returns a specific collection
/api/basket/<number>/PUT ,updates and returns a specific collection
/api/basket/<number>/DELETE ,returns deleted collection
/api/basket/<int:basket>/todo/GET,returns a list of todo's
/api/basket/<int:basket>/todo/POST,returns added todo
/api/basket/<int:basket>/todo/<int:todo>/GET , returns a todo
/api/basket/<int:basket>/todo/<int:todo>/PUT,updates a todo
/api/basket/<int:basket>/todo/<int:todo>/DELETE,deletes a todo