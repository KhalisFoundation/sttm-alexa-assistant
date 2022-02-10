import logging
import ask_sdk_core.utils as ask_utils
from utils import create_presigned_url

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.utils import get_intent_name
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.ui import StandardCard, Image, SimpleCard
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective)
from ask_sdk_model.interfaces import display

import better_translit as bt
import banidb
import random
from datetime import date

audio_data = {
    "card": {
        "title": 'My Hukamnama',
        "text": 'My Hukamnama',
    }
}
card = StandardCard(
    title=audio_data["card"]["title"],
    text=audio_data["card"]["text"],
    
)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "<speak><phoneme alphabet=\"ipa\" ph=\"ʋɑhɪGʊru d͡ʒi kɑ kʰɑlsa, ʋɑhɪGʊru d͡ʒi ki fət̪eh\">Waheguru ji ka Khalsa, Waheguru ji ki Fateh</phoneme></speak>"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Just say Hukamnama"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ShabadRandomIntentHandler(AbstractRequestHandler):
    # Handler for Audioplayer Play Intent
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RandomShabad")(handler_input) #GS .. Keyword to invoke GurbaniAudio
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        random_shabad = banidb.random()
        speech_text = f"Waheguru ji, Here is todays Shabad with ID {bt.better(random_shabad['shabad_id'])} and first line as {bt.better(random_shabad['verses'][0]['verse'])}"
        
        return (
            handler_input.response_builder
                .speak(speech_text)
                .ask(speech_text)
                .response
        )


class AudioPlayIntentHandler(AbstractRequestHandler):
    # Handler for Audioplayer Play Intent
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PlayAudio")(handler_input) #GS .. Keyword to invoke GurbaniAudio
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("in AudioPlayIntent GS")
        speech_text = "Waheguru ji, Here is todays Hukamnama"
        audio_key = "https://old.sgpc.net/hukumnama/jpeg%20hukamnama/hukamnama.mp3"#"Media/Punjabi Hukam Katha-Ang 616.mp3"
        
        #audio_url = create_presigned_url(audio_key)
        audio_url = audio_key
        
        logger.info("audio_url : "+ audio_url)
        
        directive = PlayDirective(
            play_behavior=PlayBehavior.REPLACE_ALL,
            audio_item=AudioItem(
                stream=Stream(
                    token=audio_key,
                    url=audio_url,
                    offset_in_milliseconds=0,
                    expected_previous_token=None),
                metadata=None))
        handler_input.response_builder.speak(speech_text).set_card(card).add_directive(directive).set_should_end_session(True)

        return handler_input.response_builder.response
        
    

class AudioStopIntentHandler(AbstractRequestHandler):
    # Handler for Stop – come here on pause or cancel too
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))
                
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("in AudioStopIntent and request")
        logger.info(handler_input.request_envelope.request)
        speech_text = "Goodbye"
        
        directive = StopDirective()

        handler_input.response_builder.speak(speech_text).add_directive(
            directive).set_should_end_session(True)
        return handler_input.response_builder.response

# ########## AUDIOPLAYER INTERFACE HANDLERS #########################
# from https://github.com/alexa/skill-sample-python-audio-player
# This section contains handlers related to Audioplayer interface

class PlaybackStartedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStarted Directive received.
    Confirming that the requested audio file began playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return  is_request_type("AudioPlayer.PlaybackStarted")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackStartedHandler")

        return handler_input.response_builder.response

class PlaybackFinishedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackFinished Directive received.
    Confirming that the requested audio file completed playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return  is_request_type("AudioPlayer.PlaybackFinished")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackFinishedHandler")
        return handler_input.response_builder.response

class PlaybackStoppedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStopped Directive received.
    Confirming that the requested audio file stopped playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackStopped")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackStoppedHandler and request is")
        logger.info(handler_input.request_envelope.request)

        return handler_input.response_builder.response

class PlaybackNearlyFinishedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackNearlyFinished Directive received.
    Replacing queue with the URL again. This should not happen on live streams.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackNearlyFinished")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackNearlyFinishedHandler")
        
        audio_key = "Media/Punjabi Hukam Katha-Ang 616.mp3"
        
        audio_url = create_presigned_url(audio_key)

        directive = PlayDirective(
            play_behavior=PlayBehavior.REPLACE_ENQUEUED,
            audio_item=AudioItem(
                stream=Stream(
                    token=audio_key,
                    url=audio_url,
                    offset_in_milliseconds=0,
                    expected_previous_token=None),
                metadata=None))     
        handler_input.response_builder.set_card(card).add_directive(directive).set_should_end_session(True)
        return handler_input.response_builder.response

class PlaybackFailedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackFailed Directive received.
    Logging the error and stoprestarting playing with no output speech and card.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackFailed")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        request = handler_input.request_envelope.request
        logger.info("Playback failed: {}".format(request.error))

        return handler_input.response_builder.response

class ExceptionEncounteredHandler(AbstractRequestHandler):
    """Handler to handle exceptions from responses sent by AudioPlayer
    request.
    """
    def can_handle(self, handler_input):
        # type; (HandlerInput) -> bool
        return is_request_type("System.ExceptionEncountered")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("\n**************** EXCEPTION *******************")
        logger.info(handler_input.request_envelope)
        return handler_input.response_builder.response

# ###################################################################

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("in SessionEnded")

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("exception")
        logger.info(exception)
        #logger.info(ask_utils.get_intent_name(handler_input))
        #The provided request is not an IntentRequest
        logger.info(ask_utils.get_request_type(handler_input))

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(AudioPlayIntentHandler())
sb.add_request_handler(AudioStopIntentHandler())
sb.add_request_handler(ShabadRandomIntentHandler())
# ########## AUDIOPLAYER INTERFACE HANDLERS #########################
sb.add_request_handler(PlaybackStartedHandler())
sb.add_request_handler(PlaybackFinishedHandler())
sb.add_request_handler(PlaybackStoppedHandler())
sb.add_request_handler(PlaybackNearlyFinishedHandler())
sb.add_request_handler(PlaybackFailedHandler())
sb.add_request_handler(ExceptionEncounteredHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
