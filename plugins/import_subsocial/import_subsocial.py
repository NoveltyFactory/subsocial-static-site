# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import os
import json
import time
import asyncio
from datetime import datetime

import aioipfs
import markdown
from urllib.parse import urlparse
from substrateinterface import SubstrateInterface

from nikola.plugin_categories import Command
from nikola import utils
from nikola.utils import req_missing
from nikola.plugins.basic_import import ImportMixin
from nikola.plugins.command.init import SAMPLE_CONF, prepare_config


import config


LOGGER = utils.get_logger('import_subsocial', utils.STDERR_HANDLER)


class CommandImportSubsocial(Command, ImportMixin):
    """Import a Subsocial space into a target folder."""

    name = "import_subsocial"
    needs_config = False
    doc_usage = "[options] --space=YOUR_SPACE_ID"
    doc_purpose = "import a Subsocial space"
    cmd_options = [
        {
            'name': 'output_folder',
            'long': 'output-folder',
            'short': 'o',
            'default': 'posts',
            'help': 'Location to write imported content.'
        },
        {
            'name': 'space',
            'long': 'space',
            'short': 's',
            'default': None,
            'help': 'Identifier of the space to be imported.'
        },
    ]

    def _execute(self, options, args):
        '''
            Import Subsocial Space
        '''
        if not options['space']:
            print(self.help())
            return
        self.output = options['output_folder']
        os.makedirs(self.output, exist_ok=True)

        substrate = SubstrateInterface(
            url="wss://rpc.subsocial.network",
            ss58_format=28,
            type_registry_preset='polkadot',
            type_registry=config.SUBSOCIAL_TYPES,
        )

        posts = substrate.query(
            module='Posts',
            storage_function='PostIdsBySpaceId',
            params=[int(options['space'])]
        )

        async def run(posts):
            self.ipfs_client = aioipfs.AsyncIPFS(port=5001)

            for i, r in enumerate(posts.value):
                result = substrate.query(
                    module='Posts',
                    storage_function='PostById',
                    params=[r]
                )

                await self.export_post(result.value)

            await self.ipfs_client.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(posts))
        loop.close()

    async def get_ipfs_dag_node(self, multihash):
        result = await self.ipfs_client.dag.get(multihash)
        data = json.loads(result)
        return data

    async def get_ipfs_file_content(self, multihash):
        result = await self.ipfs_client.cat(multihash)
        return result

    async def export_post(self, result):        
        # Variable `result` contains a dictionary.
        # {
        #   'id', 'created': {'account', 'block', 'time'}, 'updated': {},
        #   'owner', 'extension', 'space_id', 'content', 'hidden',
        #   'replies_count', 'hidden_replies_count', 'shares_count',
        #   'upvotes_count', 'downvotes_count', 'score'
        # }

        multihash = result['content']['IPFS']
        uuid = result['id']
        post_timestamp = int(result['created']['time']) / 1000
        post_date = datetime.fromtimestamp(post_timestamp)

        data = await self.get_ipfs_dag_node(multihash)
        # ['body', 'image', 'tags', 'title']

        if "title" not in data:
            LOGGER.warn(f"{uuid}: Ignoring post without title.")
            return
        LOGGER.info(f"{uuid}: {data['title']}")

        if 'image' in data:
            image = await self.get_ipfs_file_content(data['image'])
            with open(f"images/{uuid}.png", "wb") as f:
                f.write(image)
        else:
            image = None

        filename = f"{self.output}/{uuid}"
        self.write_content(
            f"{filename}.html",
            content=markdown.markdown(data['body'])
        )
        self.write_metadata(
            f"{filename}.meta",
            data["title"],
            uuid,
            post_date.strftime(r'%Y/%m/%d %H:%m:%S'),
            description="",
            tags=[t.lower() for t in data.get('tags', [])],
            nocomments=True,
            previewimage=f"/image/{uuid}.png" if image else None,
        )
