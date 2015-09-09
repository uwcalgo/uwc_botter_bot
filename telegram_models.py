#!/usr/bin/env python

import json

class JsonSerialisable(object):
  fields = ()
  required_fields = ()
  sub_objects = {}

  def __init__(self, *args, **kw_args):
      if len(kw_args) != 0:
        # ok we're creating a non-blank object
        self.init_object(*args, **kw_args)


  def get_sub_object(self, key, value):
      return(self.__class__.sub_objects[key].from_json(value))


  def init_object(self, *args, **kw_args):
      for field in self.__class__.required_fields:
         if field not in kw_args:
	   raise TypeError('Missing parameter for required attribute {}'.format(field))

      for field in self.__class__.fields:
        setattr(self, field, None)

      for key in kw_args: 
	if key not in self.__class__.fields:
	  raise TypeError('{} has no attribute {}'.format(self.__class__.__name__, key))
	if key in self.__class__.sub_objects:
	  new_object = self.get_sub_object(key, kw_args[key])
	  setattr(self, key, new_object)
	else:
          setattr(self, key, kw_args[key])


  @classmethod
  def from_json(cls, json_str):
      new_object = cls()
      dict_repr = json.loads(json_str)
      new_object.init_object(**dict_repr)
      return(new_object)


  def to_dict(self):
      dict_repr = dict()
      for field in self.__class__.fields:
        value = getattr(self, field)
	if value is not None:
	  dict_repr[field] = value
      return(dict_repr)

      
  def __str__(self):
      return json.dumps(self.to_dict())


  def __repr__(self):
      return(str(self))


class User(JsonSerialisable):
  fields = ('id', 'first_name', 'last_name', 'username')
  required_fields = ('id', 'first_name') 


class Update(JsonSerialisable):
  fields = ('update_id', 'message')
  required_fields = ('update_id')
  sub_objects = dict(message=Message)


class Audio(JsonSerialisable):
  pass
 
class Document(JsonSerialisable):
  pass

class Sticker(JsonSerialisable):
  pass

class Video(JsonSerialisable):
  pass

class Voice(JsonSerialisable):
  pass

class Contact(JsonSerialisable):
  pass

class Location(JsonSerialisable):
  pass

class PhotoSize(JsonSerialisable):
  pass

class Message(JsonSerialisable):
  fields = ('message_id', 'from', 'date', 'chat', 'forward_from',
            'forward_date', 'reply_to_message', 'text', 'audio',
	    'document', 'photo', 'sticker', 'video', 'voice',
	    'caption', 'contact', 'location', 'new_chat_participant',
	    'left_chat_participant', 'new_chat_title', 'new_chat_photo',
	    'delete_chat_photo', 'group_chat_created')
  required_fields = ('message_id', 'from', 'date', 'chat')
  sub_objects = dict(from=User, chat=object, forward_from=User, reply_to_message=Message,
                     audio=Audio, document=Document, photo=list, sticker=Sticker,
		     video=Video, voice=Voice, contact=Contact, location=Location,
		     new_chat_participant=User, left_chat_participant=User, 
		     new_chat_photo=list)


  def get_sub_object(self, key, value):
     if key == 'chat':
       dict_repr = json.loads(value)
       if 'first_name' in dict_repr:
         # this is a user
	 new_object = User.from_json(value)
       else:
         new_object = GroupChat.from_json(value)
     elif key == 'photo' or key == 'new_chat_photo':
         new_object = [ Photo.from_json(element) for element in json.loads(value) ]
     else:
         new_object = super(self.__class__, self).get_sub_object(key, value)
     return(new_object)

class GroupChat(JsonSerialisable):
  fields = ('id', 'title')
  required_fields = fields
