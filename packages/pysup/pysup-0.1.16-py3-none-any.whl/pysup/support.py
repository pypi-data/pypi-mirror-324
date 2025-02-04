#!/usr/bin/env python3
# coding: utf-8

from asyncio import run as asyncio_run
from httpx import AsyncClient
from enum import Enum
from decouple import config


class Ticket:
    class RequestMethod(Enum):
        GET = 1
        POST = 2
        DELETE = 3
        PATCH = 4
        PUT = 5

    def __init__(
        self,
        *,
        base_url: str | None = None,
        secret_token: str | None = None,
        user_id: int | None = None,
        filters: str | None = None,
    ):
        self.BASE_URL = base_url or config("SUPPORT_BASE_URL")
        self.HEADER = {
            "Authorization": secret_token or f"Bearer {config('SUPPORT_SECRET_TOKEN')}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.user_id = user_id

        if filters and not isinstance(filters, str):
            raise ValueError("The filters must be string type.")

        self.filters = f"{filters}" if filters else ""

    # Make the Request Methods
    async def get(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.get(url=url, headers=self.HEADER, params=data)
            return {**response.json(), "status_code": response.status_code}

    async def post(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.post(url=url, headers=self.HEADER, json=data)
            return {**response.json(), "status_code": response.status_code}

    async def put(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.put(url=url, headers=self.HEADER, json=data)
            return {**response.json(), "status_code": response.status_code}

    async def delete(self, url: str) -> dict:
        async with AsyncClient() as client:
            response = await client.delete(url=url, headers=self.HEADER)
            return {**response.json(), "status_code": response.status_code}

    async def request(self, url: str, method: int, data: dict | None = None) -> dict | None:
        url = url + self.filters

        match method:
            case Ticket.RequestMethod.GET.value:
                return await self.get(url, data)

            case Ticket.RequestMethod.POST.value:
                return await self.post(url, data)

            case Ticket.RequestMethod.PUT.value:
                return await self.put(url, data)

            case Ticket.RequestMethod.DELETE.value:
                return await self.delete(url)

    # Log
    async def log_list_async(self, log_id: int | str) -> dict | None:
        log_id = str(log_id) if isinstance(log_id, int) else log_id

        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/getLog/{log_id}",
        )

    def log_list_sync(self, log_id: int | str) -> dict | None:
        return asyncio_run(self.log_list_async(log_id=log_id))

    # Department
    async def department_list_async(self) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/department",
        )

    def department_list_sync(self) -> dict | None:
        return asyncio_run(self.department_list_async())

    async def department_create_async(self, *, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.POST.value,
            url=f"{self.BASE_URL}/department",
            data=data,
        )

    def department_create_sync(self, *, data: dict) -> dict | None:
        return asyncio_run(self.department_create_async(data=data))

    async def department_get_async(self, *, department_id: int) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/department/{department_id}",
        )

    def department_get_sync(self, *, department_id: int) -> dict | None:
        return asyncio_run(self.department_get_async(department_id=department_id))

    async def department_update_async(self, *, department_id: int, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.PUT.value,
            url=f"{self.BASE_URL}/department/{department_id}",
            data=data,
        )

    def department_update_sync(self, *, department_id: int, data: dict) -> dict | None:
        return asyncio_run(self.department_update_async(department_id=department_id, data=data))

    async def department_delete_async(self, *, department_id: int) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.DELETE.value,
            url=f"{self.BASE_URL}/department/{department_id}",
        )

    def department_delete_sync(self, *, department_id: int) -> dict | None:
        return asyncio_run(self.department_delete_async(department_id=department_id))

    # Ticket
    async def ticket_create_async(self, *, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.POST.value,
            url=f"{self.BASE_URL}/ticket",
            data=data,
        )

    def ticket_create_sync(self, *, data: dict) -> dict | None:
        return asyncio_run(self.ticket_create_async(data=data))

    async def ticket_get_async(self, ticket_id: int | str) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket/{ticket_id}",
        )

    def ticket_get_sync(self, ticket_id: int | str) -> dict | None:
        return asyncio_run(self.ticket_get_async(ticket_id=ticket_id))

    async def ticket_list_async(self) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket",
        )

    def ticket_list_sync(self) -> dict | None:
        return asyncio_run(self.ticket_list_async())

    async def all_ticket_list_async(self) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket",
        )

    def all_ticket_list_sync(self) -> dict | None:
        return asyncio_run(self.all_ticket_list_async())

    async def ticket_replies_async(self, ticket_id: int | str) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket/{ticket_id}/replies",
        )

    def ticket_replies_sync(self, ticket_id: int | str) -> dict | None:
        return asyncio_run(self.ticket_replies_async(ticket_id=ticket_id))

    async def ticket_update_async(self, *, ticket_id: int | str, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.PUT.value,
            url=f"{self.BASE_URL}/ticket/{ticket_id}",
            data=data,
        )

    def ticket_update_sync(self, *, ticket_id: int | str, data: dict) -> dict | None:
        return asyncio_run(self.ticket_update_async(ticket_id=ticket_id, data=data))

    async def ticket_delete_async(self, *, ticket_id: int | str) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.DELETE.value,
            url=f"{self.BASE_URL}/ticket/{ticket_id}",
        )

    def ticket_delete_sync(self, *, ticket_id: int | str) -> dict | None:
        return asyncio_run(self.ticket_delete_async(ticket_id=ticket_id))

    async def ticket_attach_async(self, file_id: int | str) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/file/{file_id}",
        )

    def ticket_attach_sync(self, file_id: int | str) -> dict | None:
        return asyncio_run(self.ticket_attach_async(file_id=file_id))

    # Replies
    async def replies_create_async(self, *, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.POST.value,
            url=f"{self.BASE_URL}/ticket-replies",
            data=data,
        )

    def replies_create_sync(self, *, data: dict) -> dict | None:
        return asyncio_run(self.replies_create_async(data=data))

    async def replies_update_async(self, *, reply_id: int, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.PUT.value,
            url=f"{self.BASE_URL}/ticket-replies/{reply_id}",
            data=data,
        )

    def replies_update_sync(self, *, reply_id: int, data: dict) -> dict | None:
        return asyncio_run(self.replies_update_async(reply_id=reply_id, data=data))

    async def replies_delete_async(self, *, reply_id: int) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.DELETE.value,
            url=f"{self.BASE_URL}/ticket-replies/{reply_id}",
        )

    def replies_delete_sync(self, *, reply_id: int) -> dict | None:
        return asyncio_run(self.replies_delete_async(reply_id=reply_id))

    async def replies_get_async(self, *, reply_id: int) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket-replies/{reply_id}",
        )

    def replies_get_sync(self, *, reply_id: int) -> dict | None:
        return asyncio_run(self.replies_get_async(reply_id=reply_id))
