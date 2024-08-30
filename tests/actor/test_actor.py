# import asyncio
#
# import pytest
#
# from dspygen.rdddy.base_inhabitant import BaseInhabitant
# from dspygen.rdddy.base_query import BaseQuery
# from dspygen.rdddy.service_colony import ServiceColony
#
#
# @pytest.fixture()
# def service_colony(event_loop):
#     # Provide the event loop to the inhabitant system
#     return ServiceColony(event_loop)
#
#
# class DummyInhabitant(BaseInhabitant):
#     def __init__(self, service_colony, inhabitant_id=None):
#         super().__init__(service_colony, inhabitant_id)
#         self.processed_query = None
#
#     async def handle_query(self, query: BaseQuery):
#         self.processed_query = query
#
#
# @pytest.mark.asyncio()
# async def test_handler(service_colony):
#     inhabitant = await service_colony.inhabitant_of(DummyInhabitant)
#
#     query = BaseQuery(content="Query1")
#
#     await asyncio.sleep(0)
#
#     await service_colony.publish(query)
