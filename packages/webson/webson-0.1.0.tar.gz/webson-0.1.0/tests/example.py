from webson import Webson
from intellibricks.llms import Synapse
import msgspec
from architecture import log

debug_logger = log.create_logger(__name__, log.DEBUG)


class Edital(msgspec.Struct):
    titulo: str
    link: str


class EditaisResult(msgspec.Struct):
    editais: list[Edital]


webson = Webson(llm=Synapse.of("google/genai/gemini-2.0-flash-exp"))

url = "https://prosas.com.br/editais"

casted = webson.cast(url, to=EditaisResult)

debug_logger.debug(casted)
