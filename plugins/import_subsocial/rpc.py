# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

SUBSOCIAL_TYPES = \
    {'types': {
        'SpaceId': 'u64',
        'PostId': 'u64',
        'WhoAndWhen': {
            'type': 'struct',
            'type_mapping': [
                ('account', 'AccountId'),
                ('block', 'BlockNumber'),
                ('time', 'Moment'),
            ]
        },
        'Content': {
            'type': 'enum',
            'type_mapping': [
                ('None', 'Null'),
                ('Raw', 'Text'),
                ('IPFS', 'Text'),
                ('Hyper', 'Text'),
            ],
        },
        'Post': {
            'type': 'struct',
            'type_mapping': {
                'id': 'PostId',
                'created': 'WhoAndWhen',
                'updated': 'Option<WhoAndWhen>',
                'owner': 'AccountId',
                'extension': 'PostExtension',
                'space_id': 'Option<SpaceId>',
                'content': 'Content',
                'hidden': 'bool',
                'replies_count': 'u16',
                'hidden_replies_count': 'u16',
                'shares_count': 'u16',
                'upvotes_count': 'u16',
                'downvotes_count': 'u16',
                'score': 'i32'
            }.items(),
        },
        'PostExtension': {
            'type': 'enum',
            'type_mapping': [
                ('RegularPost', 'Null'),
                ('Comment', 'Comment'),
                ('SharedPost', 'PostId'),
            ],
        },
        'Space': {
            'type': 'struct',
            'type_mapping': {
                'id': 'SpaceId',
                'created': 'WhoAndWhen',
                'updated': 'Option<WhoAndWhen>',
                'owner': 'AccountId',
                'parent_id': 'Option<SpaceId>',
                'handle': 'Option<Text>',
                'content': 'Content',
                'hidden': 'bool',
                'posts_count': 'u32',
                'hidden_posts_count': 'u32',
                'followers_count': 'u32',
                'score': 'i32',
                'permissions': 'Option<SpacePermissions>'
            }.items()
        },
    }}
