import os
import pwd
import xmlrpclib

class HomeCleaner:
	
	# MINUTES
	CRON_TIME=60

	if os.path.exists("/etc/n4d/conf.d/golem"):
	
		predepends=["Golem"]	

	def __init__(self):
		
		self.home="/home/"
		self.controlled=False
		if os.path.exists("/etc/n4d/controlled-startups.d/HomeCleaner"):
			self.controlled=True
		
	#def init
	
	def startup(self,options):
		return 
		if options["boot"]:
			if options["controlled"]:
				self.delete_orphan_homes()
				
	#def startup
	
	def delete_orphan_homes(self):
		
		n4d=xmlrpclib.ServerProxy("https://server:9779")
		
		try:
			user_list=[]
			ret=n4d.get_user_list("","Golem","*")

			for user in ret:
				user_list.append(user["uid"])

			for user in pwd.getpwall():
				u=user.pw_name
				if u not in user_list:
					user_list.append(u)
					
					
			rm_list=[]
			for item in os.listdir(self.home):
				if os.path.isdir(self.home+item):
					if item not in user_list:
						rm_list.append(item)

			for user in rm_list:
			
				os.system("rm -rf %s/%s"%(self.home,user))
			
			return [True,""]
			
		except Exception as e:
			return [False,str(e)]
		
	#def delete_orphan_homes
	
	
	def n4d_cron(self,minutes):
		
		if minutes%HomeCleaner.CRON_TIME==0:
			if self.controlled:
				self.delete_orphan_homes()
				
	#def n4d_cron
