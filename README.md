# EVE Notifications - GCM Settings
This is a settings service that allows clients to register their token from the
[Google Cloud Messaging](https://developers.google.com/cloud-messaging/) service
with EVE Notifications. Tokens are stored as a list of tokens per character.
When requests come from internal services requesting the tokens for a given
character all tokens associated with that character are returned.

# External API

## External
Route: ``/external/``

### GET
* Auth: False

Returns the project ID that is required by applications when registering with
the GCM service.

```
{
  "project_id": "1045503414087"
}
```

## External Character Settings
Route: ``/external/characters/<character_id>/``

### PUT
* Auth: True

Allows clients to register themselves with the EVE Notifications service so that
when notifications are pushed we know what clients to send to.

```
{
    "gcm_token": "some_token_from_gcm_here"
}
```

## Internal
Route: ```/internal/```

### GET
* Auth: False
* Query Params:
  * character_ids: A list of character IDs that you're requesting GCM tokens for.

Returns a single list of all GCM tokens for the requested character IDs.

```
[
    "some_token_from_gcm_here_one",
    "some_token_from_gcm_here_two",
    "some_token_from_gcm_here_three"
]
```
