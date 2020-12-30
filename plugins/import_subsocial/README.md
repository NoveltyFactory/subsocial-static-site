This plugin imports the posts from a Subsocial space.  You need a local IPFS node running to be able to download the content.

To use it, first copy the `plugins/import_subsocial` folder into your Nikola site. 

Then run the following commands:
```
# ipfs daemon &

# nikola import_subsocial --space=YOUR_SPACE_ID
```
