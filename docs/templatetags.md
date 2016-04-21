`{% load pinax_documents_tags %}`

# Filters

## can_share

Returns True if `member` can share with `user`:

    {{ member|can_share:user }}

## readable_bytes

Display number of bytes using appropriate units.

    {{ 73741824|readable_bytes }}

yields "70MB".

