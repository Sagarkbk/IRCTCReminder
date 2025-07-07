# @usersRouter.get("/getUser/{google_id}")
# async def getUser(request: Request, response: Response):
#     try:
#         user = request.state.user
#         response.status_code = status.HTTP_200_OK
#         return {"User Details" : user}
#     except Exception as e:
#         print(f"Exception when hitting /getUser: {e}")
#         raise

# @usersRouter.post("/signup", dependencies=[]) #I dont need user verification for this endpoint, so made dependencies as empty. This is my comment, not AI generated.    
# async def addUser(body: User, response: Response):
#     try:
#         await db.connect()
#         get_user_with_googleid_query = """
#                 SELECT * FROM users WHERE google_id = $1
#                 """
#         existingUserWithId = await db.fetchone(get_user_with_googleid_query, body.google_id)
#         if existingUserWithId:
#             response.status_code = status.HTTP_400_BAD_REQUEST
#             return "User already exists with provided Google ID"
#         get_user_with_email_query = """
#                 SELECT * FROM users WHERE email = $1
#                 """
#         existingUserWithEmail = await db.fetchone(get_user_with_email_query, body.email)
#         if existingUserWithEmail:
#             response.status_code = status.HTTP_400_BAD_REQUEST
#             return "User already exists with provided Email"
#         insert_user_query = """
#                 INSERT INTO users (google_id, email, username, reminder_days, calendar_enabled, last_updated_at) VALUES ($1, $2, $3, $4, $5, $6)
#                 """
#         await db.execute(insert_user_query, body.google_id, body.email, body.username, body.reminder_days, body.calendar_enabled, datetime.now(timezone.utc))
#         get_user_query = """
#                 SELECT * FROM users WHERE google_id = $1
#                 """
#         newUser = await db.fetchone(get_user_query, body.google_id)
#         response.status_code = status.HTTP_201_CREATED
#         return {"newUser" : newUser}
#     except Exception as e:
#         print(f"Exception when hitting /addUser: {e}")
#         raise

# @usersRouter.post("/generateToken/{google_id}")
# async def generateToken(google_id, response: Response, request: Request):
#     try:
#         user = request.state.user
#         if user['telegram_id']:
#             response.status_code = status.HTTP_204_NO_CONTENT
#             return "User has already linked his google and telegram acccounts"
#         await db.connect()
#         check_if_token_exists_query = """
#                 SELECT * FROM google_telegram_link WHERE user_id = $1
#                 """
#         unusedToken = await db.fetchone(check_if_token_exists_query, user['id'])
#         current_time = datetime.now(timezone.utc)
#         expires_at = current_time + timedelta(minutes=30)
#         if unusedToken and (not unusedToken['is_used']) and (unusedToken['expires_at'] > current_time):
#             response.status_code = status.HTTP_200_OK
#             return {"Unused/Non-Expired Token" : unusedToken['token']}
        
#         # Deleting existing token if its expired or used and creating new one
#         if unusedToken and (unusedToken['is_used'] or (unusedToken['expires_at'] < current_time)):
#             delete_expired_or_used_token_query = """
#                 DELETE FROM google_telegram_link WHERE user_id = $1
#                 """
#             await db.execute(delete_expired_or_used_token_query, user['id'])

#         # For now creating token by combining google_id and user id
#         token = f"{google_id}#{user['id']}"
#         insert_token_query = """
#                 INSERT INTO google_telegram_link (user_id, token, expires_at) VALUES ($1, $2, $3)
#                 """
#         await db.execute(insert_token_query, user['id'], token, expires_at)
#         response.status_code = status.HTTP_201_CREATED
#         return {"Token" : token}

#     except Exception as e:
#         print(f"Exception when hitting /generateToken: {e}")
#         raise

# @usersRouter.post("/linkAccounts")
# async def linkAccounts(body: LinkAccounts, response: Response, request: Request):
#     try:
#         user = request.state.user
#         if user['telegram_id']:
#             response.status_code = status.HTTP_204_NO_CONTENT
#             return "User has already linked his google and telegram acccounts"
        
#         if not body.token:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return "Please come to telegram through the link from website so that we can link your google and telegram accounts"
        
#         await db.connect()
#         get_token_details_query = """
#                 SELECT * from google_telegram_link WHERE token = $1
#                 """
#         token_details = await db.fetchone(get_token_details_query, body.token)
#         if token_details['is_used']:
#             response.status_code = status.HTTP_400_BAD_REQUEST
#             return "Your token has been used. Please check if accounts have been linked already"
        
#         current_time = datetime.now(timezone.utc)
#         if token_details['expires_at'] < current_time:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return "Your session token has expired. Please come to telegram through the link from website so that we can link your google and telegram accounts"
        
#         link_accounts_query = """
#                 UPDATE users SET telegram_id = $1, telegram_username = $2,
#                 telegram_linked_at = $3, last_updated_at = $4 WHERE id = $5
#                 """
#         await db.execute(link_accounts_query, body.telegram_id, body.telegram_username, current_time, current_time, user['id'])
#         delete_session_query = """
#                 UPDATE google_telegram_link SET is_used = $1 WHERE
#                 token = $2
#                 """
#         await db.execute(delete_session_query, True, body.token)
#         response.status_code = status.HTTP_201_CREATED
#         return "Added telegram details/Linked google and telegram accounts"
#     except Exception as e:
#         print(f"Exception when hitting /linkAccounts: {e}")
#         raise


# @usersRouter.post("/addHolidays")
# async def addHolidays(body: Holidays, response:Response, request: Request):
#     try:
#         user = request.state.user
#         if not (len(body.holiday_name) == len(body.holiday_date) == len(body.category)):
#             response.status_code = status.HTTP_400_BAD_REQUEST
#             return "Number of names, dates, categories are not matching"
        
#         await db.connect()
#         add_holidays_query = """
#                 INSERT INTO selected_holidays (user_id, holiday_name, holiday_date, category, 
#                 day_before_sent, release_day_sent, last_updated_at) VALUES ($1, $2, $3, $4, $5, $6, $7)
#                 """
#         updated_at = datetime.now(timezone.utc)
#         for holiday_name, holiday_date, category in zip(body.holiday_name, body.holiday_date, body.category):
#             await db.execute(add_holidays_query, user['id'], holiday_name, holiday_date, category, body.day_before_sent, body.release_day_sent, updated_at)
#         response.status_code = status.HTTP_201_CREATED
#         return "Holidays added into your list"
#     except Exception as e:
#         print(f"Exception when hitting /addHolidays: {e}")
#         raise

# # Sample working body for /addHolidays
# # {
# #     "user_id": 1,
# #     "holiday_name": ["Sankranthi", "Deepavali"],
# #     "holiday_date": ["2026-01-14", "2025-10-20"],
# #     "category": ["AP Regional", "National"]
# # }

# @usersRouter.put("/updateHolidays")
# async def updateHolidays(body: Holidays, response:Response, request: Request):
#     try:
#         user = request.state.user
#         if not (len(body.holiday_name) == len(body.holiday_date) == len(body.category)):
#             response.status_code = status.HTTP_400_BAD_REQUEST
#             return "Number of names, dates, categories are not matching"
        
#         num_holidays = len(body.holiday_date)
#         day_before_sent = body.day_before_sent or [False] * num_holidays
#         release_day_sent = body.release_day_sent or [True] * num_holidays

#         # Need to put this inside transaction.
#         await db.connect()
#         delete_existing_holidays = """
#             DELETE FROM selected_holidays WHERE user_id = $1
#             """
#         await db.execute(delete_existing_holidays, user['id'])
#         add_holiday_query = """
#                 INSERT INTO selected_holidays (user_id, holiday_name, holiday_date, category, 
#                 day_before_sent, release_day_sent, last_updated_at) VALUES ($1, $2, $3, $4, $5, $6, $7)
#                 """
#         updated_at = datetime.now(timezone.utc)
#         for ind in range(len(body.holiday_date)):
#             await db.execute(add_holiday_query, user['id'], body.holiday_name[ind], body.holiday_date[ind], body.category[ind], day_before_sent[ind], release_day_sent[ind], updated_at)
#         response.status_code = status.HTTP_200_OK
#         return "Holidays updated"
#     except Exception as e:
#         print(f"Exception when hitting /addHolidays: {e}")
#         raise

# Todo: 
# Need to make all db calls inside transactions