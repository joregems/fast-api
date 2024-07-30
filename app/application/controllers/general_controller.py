from domain.useCases.interfaces.useCases import EntityUseCasesInterface
from domain.useCases.interactors.generic_interactors import CreateEntityUseCase
from domain.useCases.interactors.generic_interactors import GetEntityUseCase
from domain.useCases.interactors.generic_interactors import GetAllEntitiesUseCase
from domain.useCases.interactors.generic_interactors import UpdateEntityUseCase
from domain.useCases.interactors.generic_interactors import DeleteEntityUseCase
from uuid import UUID
from pydantic import BaseModel
from typing import TypeVar
from fastapi.encoders import jsonable_encoder
from domain.entities.user import UserPresent

EntityRepository = TypeVar('EntityRepository')
EntityPayload = TypeVar("EntityPayload", bound=BaseModel)
EntityPresent = TypeVar("EntityPresent", bound=BaseModel)

class GeneralController(EntityUseCasesInterface):


    async def create(
            self,
            entity:EntityPayload,
            response_model:EntityPresent,
            repository: EntityRepository
            )->EntityPresent:
        create_entity_use_case = CreateEntityUseCase(repository)
        db_entity = await create_entity_use_case.execute(entity)
        return response_model.model_validate(db_entity)


    async def get(
            self,
            id:UUID,
            response_model:EntityPresent,
            repository: EntityRepository)->EntityPresent:
        get_entity_use_case = GetEntityUseCase(repository)
        db_entity = await get_entity_use_case.execute(id=id)
        return response_model.model_validate(db_entity)


    async def get_all(
        self,
        response_model:EntityPresent,
        repository: EntityRepository)->list[EntityPresent]:
            get_all_users_use_case = GetAllEntitiesUseCase(repository)
            rows = await get_all_users_use_case.execute()
            users = [response_model.model_validate(r) for r in rows]
            return users


    async def update(
            self,
            id:UUID,
            entity:EntityPayload,
            repository: EntityRepository,
            response_model:EntityPresent
            )->EntityPresent:
        update_entity_use_case = UpdateEntityUseCase(repository)
        db_entity = await update_entity_use_case.execute(id=id, entity=entity)
        return response_model.model_validate(db_entity)


    async def delete(
            self,
            id:UUID,
            response_model:EntityPresent,
            repository: EntityRepository)->EntityPresent:
        delete_entity_use_case = DeleteEntityUseCase(repository)
        db_entity = await delete_entity_use_case.execute(id=id)
        return response_model.model_validate(db_entity)


    async def filter(
            self,
            query:dict,
            response_model:EntityPresent,
            repository: EntityRepository)->list[EntityPresent]:
        """
        example
        query={"id":{"operation":"__eq__", "value":id}
        
        """
        db_entity_list = await repository.filter(query)
        return [response_model.model_validate(ent) for ent in db_entity_list]
