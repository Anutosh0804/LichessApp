GET_TOP_PLAYERS = """
SELECT 
    username as username, 
    current_rating as current_rating, 
    oldest_rating as oldest_rating, 
    rating_history as rating_history
FROM 
    public.user_details;
"""

GET_PLAYER_HISTORY = """
SELECT 
    username as username, 
    current_rating as current_rating, 
    oldest_rating as oldest_rating, 
    rating_history as rating_history
FROM 
    public.user_details
WHERE
    username = '%s';
"""

GET_USERNAME = """
SELECT
    username as username,
    password as password
FROM
    public.users
WHERE
    username = '%s';
"""

INSERT_USER_DETAILS = """
INSERT INTO 
    public.users (username, password)
VALUES
    ('%s', '%s');
"""
