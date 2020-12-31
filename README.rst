subsocial-static-site
=====================

Render your `Subsocial <https://subsocial.network>`_ spaces as static sites so you can self-host them on your own domain.

This script is a plugin for the `Nikola static-site generator <https://getnikola.com>`_ that imports the posts from a Subsocial space.

.. image:: https://app.subsocial.network/ipfs/ipfs/QmeACtypY4PtJJSmKYQ598EBA2PxoLUVqkyzUAiCh2kbWt
    :alt: Screenshots of Subsocial rendered as Nikola static-site

Usage
-----

1. Start an IPFS daemon so the script can access the content.
2. Create and edit a new Nikola configuration with ``nikola init``.
3. Copy the files in ``#/plugins`` to your new Nikola site directory.
4. Run ``nikola import_subsocial --space=YOUR_SPACE_ID``.
5. Build your static site using ``nikola build`` and preview!

You should see log output from step 4 that looks as follows::

    [2020-12-31 11:11:11] INFO: import_subsocial: POST_ID: POST_TITLE

In case your post does not have a title, it won't be imported into Nikola::

    [2020-12-31 12:12:12] WARNING: import_subsocial: POST_ID: Ignoring post without title.

Support
-------

There's no support for this plugin — use at your own discretion!
