from monolith.views import follows
import unittest
 
class TestFollow(unittest.TestCase):

    def test_follow_user(self):
    	# push in the users_table 3 users
    	# create correct_answers
    	# login as user_1

    	# call /follow/user_id_2
    	# assert OK

    	# call /follow/user_id_2
    	# assert EXC

    	# call /follow/user_id_3
    	# assert OK

    	# call /follow/user_id_2
    	# assert EXC

    	# call /follow/user_id_1 (himslef)
    	# assert EXC

    	# call /follow/user_not_exist
    	# assert EXC
    	
    	# delete users and followers

    def test_unfollow_user(self):
		# push in the user_table 3 users
		# push follows in follow_table (1-2, 1-3, 2-3)
		# create correct_answers
		# login as user_1

		# call /unfollow/user_1
		# assert EXC

		# call /unfollow/user_2
		# assert OK

		# call unfollow/user_2
		# assert EXC

		# call unfollow/user_not_exist
		# assert EXC


    
 
 
if __name__ == '__main__':
    unittest.main()