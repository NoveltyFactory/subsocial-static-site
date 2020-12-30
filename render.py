# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import json
import asyncio
import aioipfs
import markdown

from substrateinterface import SubstrateInterface

import config


async def get_content(ipfshash):
    client = aioipfs.AsyncIPFS(port=5001)
    try:
        result = await client.dag.get(ipfshash)
        data = json.loads(result)
        return data
    finally:
        await client.close()


async def main():
    substrate = SubstrateInterface(
        url="wss://rpc.subsocial.network",
        ss58_format=42,
        type_registry_preset='polkadot',
        type_registry=config.SUBSOCIAL_TYPES,
    )

    result = substrate.query(
        module='Posts',
        storage_function='PostIdsBySpaceId',
        params=[1]
    )

    for i, r in enumerate(result.value):
        result = substrate.query(
            module='Posts',
            storage_function='PostById',
            params=[r]
        )
        hash = result.value['content']['IPFS']
        uuid = result.value['id']
        content = await get_content(hash)
        print(uuid, ':', content.get('title', ''))
        with open(f"output/{uuid}.html", "w", encoding="utf-8") as post:
            post.write(markdown.markdown(content['body']))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
