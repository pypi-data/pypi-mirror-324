from agentuity.instrumentation import BaseInstrumentation
from agentuity.instrumentation import is_jsonable
from logging import getLogger
import agentuity
import json
from datetime import date, datetime
from hashlib import sha256
import uuid
import importlib.metadata

logger = getLogger(__name__)
crew_version = importlib.metadata.version("crewai")

version = "1" # change this to change the format of the events

banlist=[
	"i18n",
	"config",
	"callback",
	"output_json",
	"output_file",
	"output_pydantic",
	"converter_cls",
	"__id"
]

def tools_to_array(tools):
    result = []
    for tool in tools:
        res = {}
        if hasattr(tool, "name") and tool.name is not None:
            res["name"] = tool.name.rstrip()
        if hasattr(tool, "description") and tool.description is not None:
            res["description"] = tool.description.rstrip()
        if res:
            result.append(res)
    return result

def to_agent(value):
	# https://github.com/crewAIInc/crewAI/blob/2709a9205a042e2baabd7d2f97f40365337b8c30/src/crewai/cli/constants.py#L257
	llm = {"model":"openai/gpt-4o-mini"}
	if value.llm is not None:
		model = value.llm.model
		if not "/" in model:
			llm["model"] = "openai/" + model
		if value.llm.temperature is not None:
			llm["temperature"] = value.llm.temperature
		if value.llm.max_tokens is not None:
			llm["max_tokens"] = value.llm.max_tokens
		if value.llm.api_version is not None:
			llm["api_version"] = value.llm.api_version
		if value.llm.base_url is not None:
			llm["base_url"] = value.llm.base_url
	# the agent.id changes each run so we need to hash the role and model to get a stable id
	agentid = sha256(str(value.role.rstrip()+llm["model"]).encode('utf-8')).hexdigest()
	crew = {}
	agents = []
	tasks = []
	if value.crew is not None:
		agents = [agent.role.rstrip() for agent in value.crew.agents]
		tasks = [{"description":task.description.rstrip(),"agent":task.agent.role.rstrip()} for task in value.crew.tasks]
	crew["agents"] = agents
	crew["tasks"] = tasks
	return {"role":value.role.rstrip(),"id":agentid,"goal":value.goal.rstrip(),"backstory":value.backstory.rstrip(),"llm":llm,"crew":crew}


# https://github.com/crewAIInc/crewAI/blob/main/src/crewai/task.py
def task_to_dict(o: dict) -> dict:
	res = dict()
	for key, value in o.items():
		if key in banlist:
			continue
		if is_jsonable(value):
			res[key] = value
		else:
			if value == None:
				res[key] = None
				continue
			if isinstance(value, (datetime, date)):
				res[key] = value.isoformat()
				continue
			if isinstance(value, uuid.UUID):
				res[key] = str(value)
				continue
			if isinstance(value, set):
				res[key] = list(value)
				continue
			if key == "tools":
				res[key] = tools_to_array(value)
				continue
			if key == "agent":
				res[key] = to_agent(value)
				continue
			if key == "processed_by_agents":
				res[key] = [agent.rstrip() for agent in value]
				continue
			sval = str(value)
			if sval == "True":
				res[key] = True
			elif sval == "False":
				res[key] = False
			else:
				res[key] = sval
	return res

class CrewAIInstrumentation(BaseInstrumentation):
	def _instrument(self, **kwargs):
		logger.info("Instrumenting CrewAI")
		self._wrap("crewai.agent", "Agent.execute_task", self._beforeTask, self._afterTask)

	def _beforeTask(self, kwargs):
		task = kwargs.get("task")
		context = kwargs.get("context").rstrip()
		agentuity.event({"id":task.key,"version":version,"module":"crewai","crew_version":crew_version,"actor":"agent","action":"execute_task","stage":"before","task":task_to_dict(task.__dict__),"context":context})

	def _afterTask(self, kwargs, response):
		task = kwargs.get("task")
		context = kwargs.get("context").rstrip()
		agentuity.event({"id":task.key,"version":version,"module":"crewai","crew_version":crew_version,"actor":"agent","action":"execute_task","stage":"after","task":task_to_dict(task.__dict__),"context":context,"response":response.rstrip()})
