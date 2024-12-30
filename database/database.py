


import time
import pymongo, os
import motor, asyncio
from config import DB_URL, DB_NAME
from bot import Bot
import motor.motor_asyncio  # Import the correct module



dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]


default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }



class Rohit:

    def __init__(self, DB_URL, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
        self.database = self.dbclient[DB_NAME]

        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.user_data = self.database['users']
        self.banned_user_data = self.database['banned_user']
        self.autho_user_data = self.database['autho_user']

        self.auto_delete_data = self.database['auto_delete']
        self.hide_caption_data = self.database['hide_caption']
        self.protect_content_data = self.database['protect_content']
        self.channel_button_data = self.database['channel_button']

        self.del_timer_data = self.database['del_timer']
        self.channel_button_link_data = self.database['channelButton_link']

        self.rqst_fsub_data = self.database['request_forcesub']
        self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']
        self.store_reqLink_data = self.database['store_reqLink']



    # USER MANAGEMENT
    async def present_user(self, user_id: int):
        found = await self.user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_user(self, user_id: int):
        await self.user_data.insert_one({'_id': user_id})
        return

    async def full_userbase(self):
        user_docs = await self.user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in user_docs]
        return user_ids

    async def del_user(self, user_id: int):
        await self.user_data.delete_one({'_id': user_id})
        return

    # VERIFICATION MANAGEMENT
    async def db_verify_status(self, user_id):
        user = await self.user_data.find_one({'_id': user_id})
        if user:
            return user.get('verify_status', default_verify)
        return default_verify

    async def db_update_verify_status(self, user_id, verify):
        await self.user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

    async def get_verify_status(self, user_id):
        verify = await self.db_verify_status(user_id)
        return verify

    async def update_verify_status(self, user_id, verify_token="", is_verified=False, verified_time=0, link=""):
        current = await self.db_verify_status(user_id)
        current['verify_token'] = verify_token
        current['is_verified'] = is_verified
        current['verified_time'] = verified_time
        current['link'] = link
        await self.db_update_verify_status(user_id, current)

    # CHANNEL BUTTON SETTINGS
    async def set_channel_button_link(self, button_name: str, button_link: str):
        await self.channel_button_link_data.delete_many({})  # Remove all existing documents
        await self.channel_button_link_data.insert_one({'button_name': button_name, 'button_link': button_link}) # Insert the new document

    async def get_channel_button_link(self):
        data = await self.channel_button_link_data.find_one({})
        if data:
            return data.get('button_name'), data.get('button_link')
        return ' Channel', 'https://t.me/Javpostr'


    # DELETE TIMER SETTINGS
    async def set_del_timer(self, value: int):        
        existing = await self.del_timer_data.find_one({})
        if existing:
            await self.del_timer_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.del_timer_data.insert_one({'value': value})

    async def get_del_timer(self):
        data = await self.del_timer_data.find_one({})
        if data:
            return data.get('value', 600)
        return 600

    # SET BOOLEAN VALUES FOR DIFFERENT SETTINGS

    async def set_auto_delete(self, value: bool):
        existing = await self.auto_delete_data.find_one({})
        if existing:
            await self.auto_delete_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.auto_delete_data.insert_one({'value': value})

    async def set_hide_caption(self, value: bool):
        existing = await self.hide_caption_data.find_one({})
        if existing:
            await self.hide_caption_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.hide_caption_data.insert_one({'value': value})

    async def set_protect_content(self, value: bool):
        existing = await self.protect_content_data.find_one({})
        if existing:
            await self.protect_content_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.protect_content_data.insert_one({'value': value})

    async def set_channel_button(self, value: bool):
        existing = await self.channel_button_data.find_one({})
        if existing:
            await self.channel_button_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.channel_button_data.insert_one({'value': value})

    async def set_request_forcesub(self, value: bool):
        existing = await self.rqst_fsub_data.find_one({})
        if existing:
            await self.rqst_fsub_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.rqst_fsub_data.insert_one({'value': value})


    # GET BOOLEAN VALUES FOR DIFFERENT SETTINGS        

    async def get_auto_delete(self):
        data = await self.auto_delete_data.find_one({})
        if data:
            return data.get('value', False)
        return False

    async def get_hide_caption(self):
        data = await self.hide_caption_data.find_one({})
        if data:
            return data.get('value', False)
        return False

    async def get_protect_content(self):
        data = await self.protect_content_data.find_one({})
        if data:
            return data.get('value', False)
        return False

    async def get_channel_button(self):
        data = await self.channel_button_data.find_one({})
        if data:
            return data.get('value', False)
        return False

    async def get_request_forcesub(self):
        data = await self.rqst_fsub_data.find_one({})
        if data:
            return data.get('value', False)
        return False

    # CHANNEL MANAGEMENT
    async def channel_exist(self, channel_id: int):
        found = await self.channel_data.find_one({'_id': channel_id})
        return bool(found)

    async def add_channel(self, channel_id: int):
        if not await self.channel_exist(channel_id):
            await self.channel_data.insert_one({'_id': channel_id})
            return

    async def del_channel(self, channel_id: int):
        if await self.channel_exist(channel_id):
            await self.channel_data.delete_one({'_id': channel_id})
            return

    async def get_all_channels(self):
        channel_docs = await self.channel_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    # ADMIN USER MANAGEMENT
    async def admin_exist(self, admin_id: int):
        found = await self.admins_data.find_one({'_id': admin_id})
        return bool(found)

    async def add_admin(self, admin_id: int):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({'_id': admin_id})
            return

    async def del_admin(self, admin_id: int):
        if await self.admin_exist(admin_id):
            await self.admins_data.delete_one({'_id': admin_id})
            return

    async def get_all_admins(self):
        users_docs = await self.admins_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids


    # BAN USER MANAGEMENT
    async def ban_user_exist(self, user_id: int):
        found = await self.banned_user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_ban_user(self, user_id: int):
        if not await self.ban_user_exist(user_id):
            await self.banned_user_data.insert_one({'_id': user_id})
            return

    async def del_ban_user(self, user_id: int):
        if await self.ban_user_exist(user_id):
            await self.banned_user_data.delete_one({'_id': user_id})
            return

    async def get_ban_users(self):
        users_docs = await self.banned_user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids


    # REQUEST FORCE-SUB MANAGEMENT

    # Initialize a channel with an empty user_ids array (acting as a set)
    async def add_reqChannel(self, channel_id: int):
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$setOnInsert': {'user_ids': []}},  # Start with an empty array to represent the set
            upsert=True  # Insert the document if it doesn't exist
        )

    # Set the request_forcesub mode for a specific channel
    async def set_request_forcesub_channel(self, channel_id: int, fsub_mode: bool):
        await self.rqst_fsub_Channel_data.update_one(
        {'_id': channel_id},
        {'$set': {'fsub_mode': fsub_mode}},
        upsert=True
    )

    # Method 1: Add user to the channel set
    async def reqSent_user(self, channel_id: int, user_id: int):
        # Add the user to the set of users for a specific channel
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$addToSet': {'user_ids': user_id}}, 
            upsert=True
        )

    # Method 2: Remove a user from the channel set
    async def del_reqSent_user(self, channel_id: int, user_id: int):
        # Remove the user from the set of users for the channel
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': channel_id}, 
            {'$pull': {'user_ids': user_id}}
        )

    # Clear the user set (user_ids array) for a specific channel
    async def clear_reqSent_user(self, channel_id: int):
        if await self.reqChannel_exist(channel_id):
            await self.rqst_fsub_Channel_data.update_one(
                {'_id': channel_id}, 
                {'$set': {'user_ids': []}}  # Reset user_ids to an empty array
            )

    # Method 3: Check if a user exists in the channel set
    async def reqSent_user_exist(self, channel_id: int, user_id: int):
        # Check if the user exists in the set of the channel's users
        found = await self.rqst_fsub_Channel_data.find_one(
            {'_id': channel_id, 'user_ids': user_id}
        )
        return bool(found)

    # Method 4: Remove a channel and its set of users
    async def del_reqChannel(self, channel_id: int):
        # Delete the entire channel's user set
        await self.rqst_fsub_Channel_data.delete_one({'_id': channel_id})

    # Method 5: Check if a channel exists
    async def reqChannel_exist(self, channel_id: int):
        # Check if the channel exists
        found = await self.rqst_fsub_Channel_data.find_one({'_id': channel_id})
        return bool(found)

    # Method 6: Get all users from a channel's set
    async def get_reqSent_user(self, channel_id: int):
        # Retrieve the list of users for a specific channel
        data = await self.rqst_fsub_Channel_data.find_one({'_id': channel_id})
        if data:
            return data.get('user_ids', [])
        return []

    # Method 7: Get all available channel IDs
    async def get_reqChannel(self):
        # Retrieve all channel IDs
        channel_docs = await self.rqst_fsub_Channel_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids


    # Get all available channel IDs in store_reqLink_data
    async def get_reqLink_channels(self):
        # Retrieve all documents from store_reqLink_data
        channel_docs = await self.store_reqLink_data.find().to_list(length=None)
        # Extract the channel IDs from the documents
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    # Get the stored link for a specific channel
    async def get_stored_reqLink(self, channel_id: int):
        # Retrieve the stored link for a specific channel_id from store_reqLink_data
        data = await self.store_reqLink_data.find_one({'_id': channel_id})
        if data:
            return data.get('link')
        return None

    # Set (or update) the stored link for a specific channel
    async def store_reqLink(self, channel_id: int, link: str):
        # Insert or update the link for the channel_id in store_reqLink_data
        await self.store_reqLink_data.update_one(
            {'_id': channel_id}, 
            {'$set': {'link': link}}, 
            upsert=True
        )

    # Delete the stored link and the channel from store_reqLink_data
    async def del_stored_reqLink(self, channel_id: int):
        # Delete the document with the channel_id in store_reqLink_data
        await self.store_reqLink_data.delete_one({'_id': channel_id})


db = Rohit(DB_URL, DB_NAME)
