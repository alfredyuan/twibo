import weibo
import twitter

class twibo:
	tw_consumer_key = "gGlhtxpw1nW5gDwbPJnU4w"
	tw_consumer_secret = "jWmeFahHQzi6pOjBsjkBY0cEmK7GpolpPYta06FS0i4"

	tw_access_token = "16324190-IgS3RBr7YAWEYrMgwOI1MAjLVKFe1EwPdGNg8P5Dh"
	tw_access_token_secret = "D3XrT4ZedLc852IH2M1sJl0onuKMDJqF79iRO8I"

	@staticmethod
	def verifyTwitterAccount(tw_name):
		api = twitter.Api(consumer_key=twibo.tw_consumer_key,consumer_secret=twibo.tw_consumer_secret,access_token_key=twibo.tw_access_token, access_token_secret=twibo.tw_access_token_secret)

		try:
			u = api.GetUser(tw_name)
		except twitter.TwitterError:
			return None

		return u.profile_image_url