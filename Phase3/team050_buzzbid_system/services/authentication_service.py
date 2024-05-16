# services/authentication_service.py
from database.connection import execute_query
from database.connection import execute_search_query

class AuthenticationService:
    @staticmethod
    def check_existing_user(username):
        query = """SELECT * FROM "user" WHERE username = %s;"""
        result = execute_query(query, (username,))
        return bool(result)

    @staticmethod
    def login(username, password):
        query = """SELECT * FROM "user" WHERE username = %s AND password = %s;"""
        result = execute_query(query, (username, password))
        return bool(result)
    
    @staticmethod
    def get_user_details(username):
        query = """
        SELECT u.first_name, u.last_name, u.user_type,a."position", u.username
        FROM "user" u
        left join adminuser a ON a.username = u.username 
        WHERE u.username = %s
        """
        result = execute_query(query, (username,))
        if result:
            print("Result:",result)
            user_details = result[0]
            return {
                "first_name": user_details[0],
                "last_name": user_details[1],
                "user_type" : user_details[2],
                "position" : user_details[3],
                "username" : user_details[4]
            }
        else:
            return {"first_name": "", "last_name": "", "user_type":"", "position":"", "username":""}
    
    @staticmethod
    def add_new_user(username, password, first_name, last_name):
        query = """INSERT INTO "user" (username, password,first_name,last_name,user_type) 
                VALUES (%s, %s, %s, %s, %s)
                """
        result = execute_query(query, (username, password, first_name, last_name,"Regular"))
        if result:
            return True

    @staticmethod
    def list_item(username, name, condition, category, description, starting_price, min_sale_price, get_it_now_price, auction_end, returns_accepted):
        if get_it_now_price != "":
            query = """INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW() + INTERVAL %s DAY, %s, NULL); 
                    """
            result = execute_query(query, (username, name, condition, category, description, starting_price, min_sale_price, get_it_now_price, auction_end, returns_accepted))
        else:
            query = """INSERT INTO "item" (username, name, condition, category_name, description, starting_bid, min_sale_price, get_it_now_price, end_time, is_returnable, cancellation_reason) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NOW() + INTERVAL %s DAY, %s, NULL); 
                    """
            result = execute_query(query, (username, name, condition, category, description, starting_price, min_sale_price, auction_end, returns_accepted))
        return


    @staticmethod    
    def search_item(keyword, category, min_price, max_price, condition):

        #if user did not provide a search criteria, default to these values when querying. Otherwise, keep the existing value
        keyword = keyword.strip() or '%'
        category = category or '%'
        min_price = min_price or 0
        max_price = max_price or 999999999999
        condition = condition or 'Poor'

        query="""
            WITH keyword_search AS(
                SELECT item_id FROM "item"
                WHERE (name LIKE %(keyword)s OR %(keyword)s IS NULL) OR (description LIKE %(keyword)s OR %(keyword)s IS NULL)
                GROUP BY item_id
                )
                , category_search AS(
                SELECT item_id FROM "item"
                WHERE (category_name LIKE %(category)s OR %(category)s IS NULL)
                GROUP BY item_id
                )
                , min_price_search AS (
                SELECT i.item_id FROM "item" i
                LEFT OUTER JOIN "bid" b ON i.item_id = b.item_id
                GROUP BY i.item_id
                HAVING (COALESCE(MAX(b.bid_amount), i.starting_bid) >= %(minPrice)s OR %(minPrice)s IS NULL)
                )
                , max_price_search as (
                SELECT i.item_id 
                FROM "item" i
                LEFT OUTER JOIN "bid" b ON i.item_id = b.item_id
                GROUP BY i.item_id
                HAVING (COALESCE(MAX(b.bid_amount), i.starting_bid) <= %(maxPrice)s OR %(maxPrice)s IS NULL)
                )
                , condition_search AS (
                    SELECT item_id FROM "item"
                    WHERE 
                        CASE 
                            WHEN condition = 'Poor' THEN 1
                            WHEN condition = 'Fair' THEN 2
                            WHEN condition = 'Good' THEN 3
                            WHEN condition = 'Very Good' THEN 4
                            WHEN condition = 'New' THEN 5
                            ELSE NULL
                        END >= 
                        CASE 
                            WHEN %(condition)s = 'Poor' THEN 1
                            WHEN %(condition)s = 'Fair' THEN 2
                            WHEN %(condition)s = 'Good' THEN 3
                            WHEN %(condition)s = 'Very Good' THEN 4
                            WHEN %(condition)s = 'New' THEN 5
                            ELSE 0
                        END
                    GROUP BY item_id
                )
                SELECT
                    i.item_id,
                    i.name,
                    COALESCE(MAX(b.bid_amount)::text, '-') AS current_bid,
                    COALESCE (
                        (SELECT b.username 
                        FROM "bid" b 
                        WHERE b.item_id = i.item_id 
                        ORDER BY b.bid_amount DESC 
                        LIMIT 1
                    ), '-') AS high_bidder,
                    COALESCE(i.get_it_now_price::text, '-') AS get_it_now_price,
                    i.end_time AS auction_ends
                FROM "item" i
                LEFT OUTER JOIN "bid" b ON i.item_id = b.item_id
                INNER JOIN "keyword_search" keyword_search_view ON i.item_id = keyword_search_view.item_id
                INNER JOIN "category_search" category_search_view ON i.item_id = category_search_view.item_id
                INNER JOIN "min_price_search" min_price_search_view ON i.item_id = min_price_search_view.item_id
                INNER JOIN "max_price_search" max_price_search_view ON i.item_id = max_price_search_view.item_id
                INNER JOIN "condition_search" condition_search_view ON i.item_id = condition_search_view.item_id
                WHERE 1=1
                    AND   i.end_time > NOW() 
                    AND   i.cancellation_reason IS NULL
                GROUP BY i.item_id
                ORDER BY i.end_time ASC;
            """        
        #breakpoint()

        params_dict = {
        'keyword': f"%{keyword}%",
        'category': category, 
        'minPrice': float(min_price),
        'maxPrice': float(max_price),
        'condition': condition #condition doesn't have to be formatted because it's a string as part of ENUMS already 
        }

        print("\nUser input these parameters: ", params_dict)
        
        result = execute_search_query(query, params_dict)
        # print(f"RESULT LENGTH: {len(result)} \n RESULTS: {result}")
        return result


    @staticmethod
    def delete_rating(item_id): #if there is a rating service file, this will go into it
        query = """DELETE FROM "rating" \
                    WHERE item_id = %s; \
                """
        result = execute_query(query, (item_id))
        if result:
            return True

    @staticmethod
    def get_current_time():
        query = """SELECT NOW();"""
        return execute_query(query)