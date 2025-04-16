from pyfacebook import GraphAPI
api = GraphAPI(app_id="501275456342166", app_secret="98ae7917c68337d30f9c4c6234b29bdb", oauth_flow=True)
print(api.get_token_info())