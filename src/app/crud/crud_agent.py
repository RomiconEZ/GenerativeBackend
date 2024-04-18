from fastcrud import FastCRUD

from ..models.agent import Agent
from ..schemas.agent import AgentCreateInternal, AgentDelete, AgentUpdate, AgentUpdateInternal

CRUDAgent = FastCRUD[Agent, AgentCreateInternal, AgentUpdate, AgentUpdateInternal, AgentDelete]
crud_agents = CRUDAgent(Agent)
