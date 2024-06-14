from pydantic import BaseModel, Field
from beanie import Document
from typing import List, Optional
from uuid import uuid4

class Lead(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    status: int = 0
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    
    class Settings:
        collection = "lead"

class LeadView(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

import motor.motor_asyncio
from beanie import init_beanie

async def init_lead():
    print("Initializing lead collection...")
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.test_db
    await init_beanie(database, document_models=[Lead])

async def create_lead():
    print("Creating the lead...")
    lead = Lead(first_name = "John", last_name = "Doe", email = "johndoe@example.com")
    await lead.insert()
    
    lead = Lead(first_name = "Mary", last_name = "Jane", email = "maryjane@example.com")
    await lead.insert()

async def read_leads():
    print("List some attributes of the lead...")
    leads = await Lead.find_all().project(LeadView).to_list()
    for lead in leads:
        print(lead)

async def read_one_lead_by_email(email: str):
    print("Find a lead with email: {}".format(email)) 
    lead = await Lead.find_one(Lead.email == email).project(LeadView)
    if lead:
        print(lead)

class Attributes(BaseModel):
    age: Optional[int] = None
    location: Optional[str] = None
    interests: Optional[List[str]] = None

class Persona(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    lead_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    attributes: Attributes
    
    class Settings:
        collection = "personas"
    
async def get_persona_by_lead_id(lead_id: str) -> Optional[Persona]:
    print("Find personas with lead id: {}".format(lead_id))
    return await Persona.find(Persona.lead_id == lead_id).to_list()

async def update_persona_details(id: str, update_fields: dict):
    print("Update {} of persona id {}".format(update_fields, id))
    await Persona.find_one(Persona.id == id).update({"$set": update_fields})

async def get_persona_by_attr(criteria: dict) -> Optional[Persona]:
    print("Find persona with the criteria: {}".format(criteria))
    personas = await Persona.find(criteria).to_list()
    return personas

async def init_persona():
    print("Initializing persona collection...")
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.test_db
    await init_beanie(database, document_models=[Persona])

async def insert_persona():
    new_persona = Persona(
        lead_id="unique_lead_id_123",
        name="John Doe",
        email="john.doe@example.com",
        attributes=Attributes(
            age=30,
            location="New York",
            interests=["tech", "music"]
        )
    )
    await new_persona.insert()

async def example_get_persona():
    lead_id = "unique_lead_id_123"
    personas = await get_persona_by_lead_id(lead_id)
    for persona in personas:
        print(persona)

async def example_update_persona():
    lead_id = "unique_lead_id_123"
    update_fields = {
        "attributes.age": 31,
        "attributes.location": "San Francisco"
    }
    await update_persona_details(lead_id, update_fields)

async def example_find_persona_by_attr():
    criteria = {"attributes.interests": "tech"}
    personas = await get_persona_by_attr(criteria)
    for persona in personas:
        print(persona)

import asyncio

async def main():
    
    await init_lead()
    
    # Lead processing
    # await create_lead()
    await read_leads()
    await read_one_lead_by_email("johndoe@example.com")
    
    await init_persona()
    
    # Persona processing
    # await insert_persona()
    await example_get_persona()
    await example_update_persona()
    await example_find_persona_by_attr()

asyncio.run(main())
