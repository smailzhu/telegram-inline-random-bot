__author__ = 'smailzhu'

import logging
import coloredlogs

import random
from telepot import glance
from telepot.aio.helper import AnswererMixin, InlineUserHandler

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


class InlineHandler(InlineUserHandler, AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = glance(msg, flavor='inline_query')

        def compute_answer():
            try:
                limit = int(query_string)
                if limit < 1:
                    raise Exception
                title = f'roll a D{limit} dice'
                msg_text = title + '\nresult is: ' + str(random.randint(1, limit))
            except Exception as e:
                title = "'@hexrandom_bot 6' to roll a D6 dice"
                msg_text = 'roll a D6 dice:\nresult is:' + str(random.randint(1, 6))

            articles = [{'type': 'article',
                         'id': 'smailzhu is cute', 'title': title, 'message_text': msg_text}]

            return articles, 0

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = glance(msg, flavor='chosen_inline_result')
        s = f"Chosen Inline Result: {result_id} {from_id} {query_string}"
        logger.info(s)

    def on_close(self, ex):
        pass
