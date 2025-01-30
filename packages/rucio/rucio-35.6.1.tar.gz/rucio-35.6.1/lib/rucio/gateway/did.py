# Copyright European Organization for Nuclear Research (CERN) since 2012
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Iterable, Iterator, Mapping, Sequence
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Optional

import rucio.gateway.permission
from rucio.common.constants import RESERVED_KEYS
from rucio.common.exception import AccessDenied, InvalidObject, RucioException
from rucio.common.schema import validate_schema
from rucio.common.types import InternalAccount, InternalScope
from rucio.common.utils import gateway_update_return_dict
from rucio.core import did, naming_convention
from rucio.core import meta_conventions as meta_convention_core
from rucio.core.rse import get_rse_id
from rucio.db.sqla.constants import DIDType
from rucio.db.sqla.session import read_session, stream_session, transactional_session

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@stream_session
def list_dids(
    scope: str,
    filters: Mapping[Any, Any],
    did_type: str = 'collection',
    ignore_case: bool = False,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    long: bool = False,
    recursive: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List dids in a scope.

    :param scope: The scope name.
    :param filters: Filter arguments in form supported by the filter engine.
    :param did_type:  The type of the did: all(container, dataset, file), collection(dataset or container), dataset, container
    :param ignore_case: Ignore case distinctions.
    :param limit: The maximum number of DIDs returned.
    :param offset: Offset number.
    :param long: Long format option to display more information for each DID.
    :param recursive: Recursively list DIDs content.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    internal_scope = InternalScope(scope, vo=vo)

    # replace account and scope in filters with internal representation
    for or_group in filters:
        if 'account' in or_group:
            or_group['account'] = InternalAccount(or_group['account'], vo=vo)
        if 'scope' in or_group:
            or_group['account'] = InternalScope(or_group['scope'], vo=vo)

    result = did.list_dids(scope=internal_scope, filters=filters, did_type=did_type, ignore_case=ignore_case,
                           limit=limit, offset=offset, long=long, recursive=recursive, session=session)

    for d in result:
        yield gateway_update_return_dict(d, session=session)


@transactional_session
def add_did(
    scope: str,
    name: str,
    did_type: str,
    issuer: str,
    account: Optional[str] = None,
    statuses: Optional[dict[str, str]] = None,
    meta: Optional[dict[str, str]] = None,
    rules: Optional[Sequence[dict[str, Any]]] = None,
    lifetime: Optional[str] = None,
    dids: Optional[Sequence[dict[str, Any]]] = None,
    rse: Optional[str] = None,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Add data did.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param did_type: The data identifier type.
    :param issuer: The issuer account.
    :param account: The account owner. If None, then issuer is selected as owner.
    :param statuses: Dictionary with statuses, e.g.g {'monotonic':True}.
    :meta: Meta-data associated with the data identifier is represented using key/value pairs in a dictionary.
    :rules: Replication rules associated with the data did. A list of dictionaries, e.g., [{'copies': 2, 'rse_expression': 'TIERS1'}, ].
    :param lifetime: DID's lifetime (in seconds).
    :param dids: The content.
    :param rse: The RSE name when registering replicas.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    statuses = statuses or {}
    meta = meta or {}
    rules = rules or []
    dids = dids or []
    v_did = {'name': name, 'type': did_type.upper(), 'scope': scope}
    validate_schema(name='did', obj=v_did, vo=vo)
    validate_schema(name='dids', obj=dids, vo=vo)
    validate_schema(name='rse', obj=rse, vo=vo)
    kwargs = {'scope': scope, 'name': name, 'type': did_type, 'issuer': issuer, 'account': account, 'statuses': statuses, 'meta': meta, 'rules': rules, 'lifetime': lifetime}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='add_did', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not add data identifier to scope %s' % (issuer, scope))

    owner_account = None if account is None else InternalAccount(account, vo=vo)
    issuer_account = InternalAccount(issuer, vo=vo)
    internal_scope = InternalScope(scope, vo=vo)
    for d in dids:
        d['scope'] = InternalScope(d['scope'], vo=vo)
    for r in rules:
        r['account'] = InternalAccount(r['account'], vo=vo)

    rse_id = None
    if rse is not None:
        rse_id = get_rse_id(rse=rse, vo=vo, session=session)

    if did_type == 'DATASET':
        # naming_convention validation
        extra_meta = naming_convention.validate_name(scope=internal_scope, name=name, did_type='D', session=session)

        # merge extra_meta with meta
        for k in extra_meta or {}:
            if k not in meta:
                meta[k] = extra_meta[k]
            elif meta[k] != extra_meta[k]:
                print("Provided metadata %s doesn't match the naming convention: %s != %s" % (k, meta[k], extra_meta[k]))
                raise InvalidObject("Provided metadata %s doesn't match the naming convention: %s != %s" % (k, meta[k], extra_meta[k]))

        # Validate metadata
        meta_convention_core.validate_meta(meta=meta, did_type=DIDType[did_type.upper()], session=session)

    return did.add_did(scope=internal_scope, name=name, did_type=DIDType[did_type.upper()], account=owner_account or issuer_account,
                       statuses=statuses, meta=meta, rules=rules, lifetime=lifetime,
                       dids=dids, rse_id=rse_id, session=session)


@transactional_session
def add_dids(
    dids: Sequence[dict[str, Any]],
    issuer: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Bulk Add did.

    :param dids: A list of dids.
    :param issuer: The issuer account.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    for d in dids:
        if 'rse' in d:
            rse_id = None
            if d['rse'] is not None:
                rse_id = get_rse_id(rse=d['rse'], vo=vo, session=session)
            d['rse_id'] = rse_id

    kwargs = {'issuer': issuer, 'dids': dids}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='add_dids', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not bulk add data identifier' % (issuer))

    issuer_account = InternalAccount(issuer, vo=vo)
    for d in dids:
        d['scope'] = InternalScope(d['scope'], vo=vo)
        if 'account' in d.keys():
            d['account'] = InternalAccount(d['account'], vo=vo)
        if 'dids' in d.keys():
            for child in d['dids']:
                child['scope'] = InternalScope(child['scope'], vo=vo)
    return did.add_dids(dids, account=issuer_account, session=session)


@transactional_session
def attach_dids(
    scope: str,
    name: str,
    attachment: dict[str, Any],
    issuer: str,
    vo='def',
    *,
    session: "Session"
) -> None:
    """
    Append content to data did.

    :param attachment: The attachment.
    :param issuer: The issuer account.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    validate_schema(name='attachment', obj=attachment, vo=vo)

    rse_id = None
    if 'rse' in attachment:
        if attachment['rse'] is not None:
            rse_id = get_rse_id(rse=attachment['rse'], vo=vo, session=session)
        attachment['rse_id'] = rse_id

    kwargs = {'scope': scope, 'name': name, 'attachment': attachment}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='attach_dids', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not add data identifiers to %s:%s' % (issuer, scope, name))

    internal_scope = InternalScope(scope, vo=vo)
    issuer_account = InternalAccount(issuer, vo=vo)
    if 'account' in attachment.keys():
        attachment['account'] = InternalAccount(attachment['account'], vo=vo)
    for d in attachment['dids']:
        d['scope'] = InternalScope(d['scope'], vo=vo)
        if 'account' in d.keys():
            d['account'] = InternalAccount(d['account'], vo=vo)

    if rse_id is not None:
        dids = did.attach_dids(scope=internal_scope, name=name, dids=attachment['dids'],
                               account=attachment.get('account', issuer_account), rse_id=rse_id, session=session)
    else:
        dids = did.attach_dids(scope=internal_scope, name=name, dids=attachment['dids'],
                               account=attachment.get('account', issuer_account), session=session)

    return dids


@transactional_session
def attach_dids_to_dids(
    attachments: Sequence[dict[str, Any]],
    issuer: str,
    ignore_duplicate: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Append content to dids.

    :param attachments: The contents.
    :param issuer: The issuer account.
    :param ignore_duplicate: If True, ignore duplicate entries.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    validate_schema(name='attachments', obj=attachments, vo=vo)

    for a in attachments:
        if 'rse' in a:
            rse_id = None
            if a['rse'] is not None:
                rse_id = get_rse_id(rse=a['rse'], vo=vo, session=session)
            a['rse_id'] = rse_id

    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='attach_dids_to_dids', kwargs={'attachments': attachments}, session=session):
        raise AccessDenied('Account %s can not add data identifiers' % (issuer))

    issuer_account = InternalAccount(issuer, vo=vo)
    for attachment in attachments:
        attachment['scope'] = InternalScope(attachment['scope'], vo=vo)
        for d in attachment['dids']:
            d['scope'] = InternalScope(d['scope'], vo=vo)
            if 'account' in d.keys():
                d['account'] = InternalAccount(d['account'], vo=vo)

    return did.attach_dids_to_dids(attachments=attachments, account=issuer_account,
                                   ignore_duplicate=ignore_duplicate, session=session)


@transactional_session
def detach_dids(
    scope: str,
    name: str,
    dids: Sequence[dict[str, Any]],
    issuer: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Detach data identifier

    :param scope: The scope name.
    :param name: The data identifier name.
    :param dids: The content.
    :param issuer: The issuer account.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    kwargs = {'scope': scope, 'name': name, 'dids': dids, 'issuer': issuer}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='detach_dids', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not detach data identifiers from %s:%s' % (issuer, scope, name))

    internal_scope = InternalScope(scope, vo=vo)
    for d in dids:
        d['scope'] = InternalScope(d['scope'], vo=vo)

    return did.detach_dids(scope=internal_scope, name=name, dids=dids, session=session)


@stream_session
def list_new_dids(
    did_type: Optional[str] = None,
    thread: Optional[int] = None,
    total_threads: Optional[int] = None,
    chunk_size: int = 1000,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List recent identifiers.

    :param did_type : The DID type.
    :param thread: The assigned thread for this necromancer.
    :param total_threads: The total number of threads of all necromancers.
    :param chunk_size: Number of requests to return per yield.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    dids = did.list_new_dids(did_type=did_type and DIDType[did_type.upper()], thread=thread, total_threads=total_threads, chunk_size=chunk_size, session=session)
    for d in dids:
        if d['scope'].vo == vo:
            yield gateway_update_return_dict(d, session=session)


@transactional_session
def set_new_dids(
    dids: Sequence[dict[str, Any]],
    new_flag: bool = True,
    vo: str = 'def',
    *,
    session: "Session"
) -> bool:
    """
    Set/reset the flag new

    :param scope: The scope name.
    :param name: The data identifier name.
    :param new_flag: A boolean to flag new DIDs.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    for d in dids:
        d['scope'] = InternalScope(d['scope'], vo=vo)

    return did.set_new_dids(dids, new_flag, session=session)


@stream_session
def list_content(
    scope: str,
    name: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List data identifier contents.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    dids = did.list_content(scope=internal_scope, name=name, session=session)
    for d in dids:
        yield gateway_update_return_dict(d, session=session)


@stream_session
def list_content_history(
    scope: str,
    name: str,
    vo='def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List data identifier contents history.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    dids = did.list_content_history(scope=internal_scope, name=name, session=session)

    for d in dids:
        yield gateway_update_return_dict(d, session=session)


@stream_session
def bulk_list_files(
    dids: Iterable[dict[str, Any]],
    long: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List file contents of a list of data identifiers.

    :param dids:       A list of DIDs.
    :param long:       A boolean to choose if more metadata are returned or not.
    :param vo:         The VO to act on.
    :param session:    The database session in use.
    """

    for did_ in dids:
        did_['scope'] = InternalScope(did_['scope'], vo=vo)

    for file_ in did.bulk_list_files(dids=dids, long=long, session=session):
        yield gateway_update_return_dict(file_, session=session)


@stream_session
def list_files(
    scope: str,
    name: str,
    long: bool,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List data identifier file contents.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param long:       A boolean to choose if GUID is returned or not.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    dids = did.list_files(scope=internal_scope, name=name, long=long, session=session)

    for d in dids:
        yield gateway_update_return_dict(d, session=session)


@stream_session
def scope_list(
    scope: str,
    name: Optional[str] = None,
    recursive: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List data identifiers in a scope.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param recursive: boolean, True or False.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    dids = did.scope_list(internal_scope, name=name, recursive=recursive, session=session)

    for d in dids:
        ret_did = deepcopy(d)
        ret_did['scope'] = ret_did['scope'].external
        if ret_did['parent'] is not None:
            ret_did['parent']['scope'] = ret_did['parent']['scope'].external
        yield ret_did


@read_session
def get_did(scope: str, name: str, dynamic_depth: Optional[DIDType] = None, vo: str = 'def', *, session: "Session") -> "dict[str, Any]":
    """
    Retrieve a single data did.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param dynamic_depth: the DID type to use as source for estimation of this DIDs length/bytes.
    If set to None, or to a value which doesn't make sense (ex: requesting depth = CONTAINER for a did of type DATASET)
    will not compute the size dynamically.
    :param vo: The VO to act on.
    :return did: Dictionary containing {'name', 'scope', 'type'}, Exception otherwise
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    d = did.get_did(scope=internal_scope, name=name, dynamic_depth=dynamic_depth, session=session)
    return gateway_update_return_dict(d, session=session)


@transactional_session
def set_metadata(
    scope: str,
    name: str,
    key: str,
    value: Any,
    issuer: str,
    recursive: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Add metadata to data did.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param key: the key.
    :param value: the value.
    :param issuer: The issuer account.
    :param recursive: Option to propagate the metadata update to content.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    kwargs = {'scope': scope, 'name': name, 'key': key, 'value': value, 'issuer': issuer}

    if key in RESERVED_KEYS:
        raise AccessDenied('Account %s can not change this metadata value to data identifier %s:%s' % (issuer, scope, name))

    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='set_metadata', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not add metadata to data identifier %s:%s' % (issuer, scope, name))

    internal_scope = InternalScope(scope, vo=vo)
    return did.set_metadata(scope=internal_scope, name=name, key=key, value=value, recursive=recursive, session=session)


@transactional_session
def set_metadata_bulk(
    scope: str,
    name: str,
    meta: dict[str, Any],
    issuer: str,
    recursive: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Add metadata to data did.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param meta: the key-values.
    :param issuer: The issuer account.
    :param recursive: Option to propagate the metadata update to content.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    kwargs = {'scope': scope, 'name': name, 'meta': meta, 'issuer': issuer}

    for key in meta:
        if key in RESERVED_KEYS:
            raise AccessDenied('Account %s can not change the value of the metadata key %s to data identifier %s:%s' % (issuer, key, scope, name))

    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='set_metadata_bulk', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not add metadata to data identifier %s:%s' % (issuer, scope, name))

    internal_scope = InternalScope(scope, vo=vo)
    return did.set_metadata_bulk(scope=internal_scope, name=name, meta=meta, recursive=recursive, session=session)


@transactional_session
def set_dids_metadata_bulk(
    dids: Iterable[dict[str, Any]],
    issuer: str,
    recursive: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Add metadata to a list of data identifiers.

    :param issuer: The issuer account.
    :param dids: A list of dids including metadata.
    :param recursive: Option to propagate the metadata update to content.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    for entry in dids:
        kwargs = {'scope': entry['scope'], 'name': entry['name'], 'meta': entry['meta'], 'issuer': issuer}
        if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='set_metadata_bulk', kwargs=kwargs, session=session):
            raise AccessDenied('Account %s can not add metadata to data identifier %s:%s' % (issuer, entry['scope'], entry['name']))
        entry['scope'] = InternalScope(entry['scope'], vo=vo)
        meta = entry['meta']
        for key in meta:
            if key in RESERVED_KEYS:
                raise AccessDenied('Account %s can not change the value of the metadata key %s to data identifier %s:%s' % (issuer, key, entry['scope'], entry['name']))

    return did.set_dids_metadata_bulk(dids=dids, recursive=recursive, session=session)


@read_session
def get_metadata(
    scope: str,
    name: str,
    plugin: str = 'DID_COLUMN',
    vo: str = 'def',
    *,
    session: "Session"
) -> dict[str, Any]:
    """
    Get data identifier metadata

    :param scope: The scope name.
    :param name: The data identifier name.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    d = did.get_metadata(scope=internal_scope, name=name, plugin=plugin, session=session)
    return gateway_update_return_dict(d, session=session)


@stream_session
def get_metadata_bulk(
    dids: Iterable[dict[str, Any]],
    inherit: bool = False,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    Get metadata for a list of dids
    :param dids:               A list of dids.
    :param inherit:            A boolean. If set to true, the metadata of the parent are concatenated.
    :param vo:                 The VO to act on.
    :param session: The database session in use.
    """

    validate_schema(name='dids', obj=dids, vo=vo)
    for entry in dids:
        entry['scope'] = InternalScope(entry['scope'], vo=vo)
    meta = did.get_metadata_bulk(dids, inherit=inherit, session=session)
    for met in meta:
        yield gateway_update_return_dict(met, session=session)


@transactional_session
def delete_metadata(
    scope: str,
    name: str,
    key: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Delete a key from the metadata column

    :param scope: the scope of did
    :param name: the name of the did
    :param key: the key to be deleted
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)
    return did.delete_metadata(scope=internal_scope, name=name, key=key, session=session)


@transactional_session
def set_status(
    scope: str,
    name: str,
    issuer: str,
    vo: str = 'def',
    *,
    session: "Session",
    **kwargs
) -> None:
    """
    Set data identifier status

    :param scope: The scope name.
    :param name: The data identifier name.
    :param issuer: The issuer account.
    :param kwargs:  Keyword arguments of the form status_name=value.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='set_status', kwargs={'scope': scope, 'name': name, 'issuer': issuer}, session=session):
        raise AccessDenied('Account %s can not set status on data identifier %s:%s' % (issuer, scope, name))

    internal_scope = InternalScope(scope, vo=vo)

    return did.set_status(scope=internal_scope, name=name, session=session, **kwargs)


@stream_session
def get_dataset_by_guid(
    guid: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    Get the parent datasets for a given GUID.
    :param guid: The GUID.
    :param vo: The VO to act on.
    :param session: The database session in use.

    :returns: A did
    """
    dids = did.get_dataset_by_guid(guid=guid, session=session)

    for d in dids:
        if d['scope'].vo != vo:
            raise RucioException('GUID unavailable on VO {}'.format(vo))
        yield gateway_update_return_dict(d, session=session)


@stream_session
def list_parent_dids(
    scope: str,
    name: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List parent datasets and containers of a did.

    :param scope:   The scope.
    :param name:    The name.
    :param vo:      The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    dids = did.list_parent_dids(scope=internal_scope, name=name, session=session)

    for d in dids:
        yield gateway_update_return_dict(d, session=session)


@transactional_session
def create_did_sample(
    input_scope: str,
    input_name: str,
    output_scope: str,
    output_name: str,
    issuer: str,
    nbfiles: str,
    vo: str = 'def',
    *,
    session: "Session"
):
    """
    Create a sample from an input collection.

    :param input_scope: The scope of the input DID.
    :param input_name: The name of the input DID.
    :param output_scope: The scope of the output dataset.
    :param output_name: The name of the output dataset.
    :param account: The account.
    :param nbfiles: The number of files to register in the output dataset.
    :param issuer: The issuer account.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    kwargs = {'issuer': issuer, 'scope': output_scope}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='create_did_sample', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not bulk add data identifier' % (issuer))

    input_internal_scope = InternalScope(input_scope, vo=vo)
    output_internal_scope = InternalScope(output_scope, vo=vo)

    issuer_account = InternalAccount(issuer, vo=vo)

    return did.create_did_sample(input_scope=input_internal_scope, input_name=input_name, output_scope=output_internal_scope, output_name=output_name,
                                 account=issuer_account, nbfiles=nbfiles, session=session)


@transactional_session
def resurrect(
    dids: Iterable[dict[str, Any]],
    issuer: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> None:
    """
    Resurrect DIDs.

    :param dids: A list of dids.
    :param issuer: The issuer account.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """
    kwargs = {'issuer': issuer}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='resurrect', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not resurrect data identifiers' % (issuer))
    validate_schema(name='dids', obj=dids, vo=vo)

    for d in dids:
        d['scope'] = InternalScope(d['scope'], vo=vo)

    return did.resurrect(dids=dids, session=session)


@stream_session
def list_archive_content(
    scope: str,
    name: str,
    vo: str = 'def',
    *,
    session: "Session"
) -> Iterator[dict[str, Any]]:
    """
    List archive contents.

    :param scope: The archive scope name.
    :param name: The archive data identifier name.
    :param vo: The VO to act on.
    :param session: The database session in use.
    """

    internal_scope = InternalScope(scope, vo=vo)

    dids = did.list_archive_content(scope=internal_scope, name=name, session=session)
    for d in dids:
        yield gateway_update_return_dict(d, session=session)


@transactional_session
def add_did_to_followed(
    scope: str,
    name: str,
    account: str,
    *,
    session: "Session",
    vo: str = 'def'
) -> None:
    """
    Mark a did as followed by the given account

    :param scope: The scope name.
    :param name: The data identifier name.
    :param account: The account owner.
    :param session: The database session in use.
    """
    internal_scope = InternalScope(scope, vo=vo)
    internal_account = InternalAccount(account, vo=vo)
    return did.add_did_to_followed(scope=internal_scope, name=name, account=internal_account, session=session)


@transactional_session
def add_dids_to_followed(
    dids: Iterable[Mapping[str, Any]],
    account: str,
    *,
    session: "Session",
    vo: str = 'def'
) -> None:
    """
    Bulk mark datasets as followed

    :param dids: A list of dids.
    :param account: The account owner.
    :param session: The database session in use.
    """
    internal_account = InternalAccount(account, vo=vo)
    return did.add_dids_to_followed(dids=dids, account=internal_account, session=session)


@stream_session
def get_users_following_did(
    name: str,
    scope: str,
    *,
    session: "Session",
    vo: str = 'def'
) -> Iterator[dict[str, str]]:
    """
    Return list of users following a did

    :param scope: The scope name.
    :param name: The data identifier name.
    :param session: The database session in use.
    """
    internal_scope = InternalScope(scope, vo=vo)
    users = did.get_users_following_did(name=name, scope=internal_scope, session=session)
    for user in users:
        user['user'] = user['user'].external
        yield user


@transactional_session
def remove_did_from_followed(
    scope: str,
    name: str,
    account: str,
    issuer: str,
    *,
    session: "Session",
    vo: str = 'def'
) -> None:
    """
    Mark a did as not followed

    :param scope: The scope name.
    :param name: The data identifier name.
    :param account: The account owner.
    :param session: The database session in use.
    :param issuer: The issuer account
    """
    kwargs = {'scope': scope, 'issuer': issuer}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='remove_did_from_followed', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not remove data identifiers from followed table' % (issuer))

    internal_scope = InternalScope(scope, vo=vo)
    internal_account = InternalAccount(account, vo=vo)
    return did.remove_did_from_followed(scope=internal_scope, name=name, account=internal_account, session=session)


@transactional_session
def remove_dids_from_followed(
    dids: Iterable[Mapping[str, Any]],
    account: str,
    issuer: str,
    *,
    session: "Session",
    vo: str = 'def'
) -> None:
    """
    Bulk mark datasets as not followed

    :param dids: A list of dids.
    :param account: The account owner.
    :param session: The database session in use.
    """
    kwargs = {'dids': dids, 'issuer': issuer}
    if not rucio.gateway.permission.has_permission(issuer=issuer, vo=vo, action='remove_dids_from_followed', kwargs=kwargs, session=session):
        raise AccessDenied('Account %s can not bulk remove data identifiers from followed table' % (issuer))

    internal_account = InternalAccount(account, vo=vo)
    return did.remove_dids_from_followed(dids=dids, account=internal_account, session=session)
