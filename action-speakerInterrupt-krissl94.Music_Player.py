#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined. 
      To access global parameters use conf['global']['parameterName']. For end-user parameters use conf['secret']['parameterName'] 
     
    Refer to the documentation for further details. 
    """ 
    
    import sys
    import spotipy
    token = 'AQDEGnI0JkHBgkcTvJD3sjP_lFhhCBhzwTx_G5ZwP9zG-gNOzQYSMD8_FwmNBRYrU3JkNM4AlRetdLL1Asoa8VDqhz24ZO-IzIz7P8bGMheuKAFrgf9vqwBhyw_NGqAcMBZTUH3hG-Wc3KHgm9ZemimLiaWGdU7fjzfV-fksE3Yy7rTA2ehpoqqdvbWRbzjvrx41js8KUhMzXFsGClXubF3iCWdYdV6M9O8BnHFT1ceiELGJiiZ82DGbgEo',
    spotify = spotipy.Spotify(token)
    import spotipy.util as util

    scope = 'user-library-read, user-modify-playback-state'

    if len(conf['secret']) > 1:
        username = conf['secret']['sp_username']
    else:
        hermes.publish_end_session(current_session_id, "Usage: %s username" % (sys.argv[0],))
        sys.exit()


#util.prompt_for_user_token(username, scope, '690df81ba6104b089ffe0e49b469ccfc', 'f82cf0651d11453aad0e546dd75f7c79', '192.168.178.61')

    spotify.pause_playback('')
    result_sentence = conf['secret']['sp_username'] 
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
   


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("speakerInterrupt", subscribe_intent_callback) \
         .start()
