from .models import (
	DBSession,
	Customer,
	TwiboEngineLog,
	Tweet,
	Weibo,
	)

import transaction

from sqlalchemy import desc

class LogController:
	@staticmethod
	def log_list():
		return DBSession.query(TwiboEngineLog).order_by(desc(TwiboEngineLog.log_time)).all()

class CustomerController:

	@staticmethod
	def new_customer(params, profile_pic=None):
		c = DBSession.query(Customer).filter_by(tw_name=params['tw_name']).all()

		if c:
			return False

		with transaction.manager:
			c = Customer(params['tw_name'])
			c.wi_account_name = params['wi_name']
			c.wi_account_pwd = params['wi_pwd']
			c.auto_sync = bool(params['auto_sync'])
			c.profile_pic = profile_pic
			DBSession.add(c)

		return True

	@staticmethod
	def customer_list():
		return DBSession.query(Customer).all()