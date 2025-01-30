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

from typing import TYPE_CHECKING

import rucio.core.did
import rucio.core.scope
from rucio.common.constants import RseAttr
from rucio.core.account import has_account_attribute, list_account_attributes
from rucio.core.identity import exist_identity_account
from rucio.core.rse import list_rse_attributes
from rucio.core.rse_expression_parser import parse_expression
from rucio.core.rule import get_rule
from rucio.db.sqla.constants import BadPFNStatus, IdentityType

if TYPE_CHECKING:
    from typing import Optional

    from sqlalchemy.orm import Session

    from rucio.common.types import InternalAccount


def has_permission(issuer, action, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account has the specified permission to
    execute an action with parameters.

    :param issuer:  Account identifier which issues the command..
    :param action:  The action(API call) called by the account.
    :param kwargs:  List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    perm = {'add_account': perm_add_account,
            'del_account': perm_del_account,
            'update_account': perm_update_account,
            'add_rule': perm_add_rule,
            'add_subscription': perm_add_subscription,
            'add_scope': perm_add_scope,
            'add_rse': perm_add_rse,
            'update_rse': perm_update_rse,
            'add_protocol': perm_add_protocol,
            'del_protocol': perm_del_protocol,
            'update_protocol': perm_update_protocol,
            'add_qos_policy': perm_add_qos_policy,
            'delete_qos_policy': perm_delete_qos_policy,
            'declare_bad_file_replicas': perm_declare_bad_file_replicas,
            'declare_suspicious_file_replicas': perm_declare_suspicious_file_replicas,
            'add_replicas': perm_add_replicas,
            'delete_replicas': perm_delete_replicas,
            'skip_availability_check': perm_skip_availability_check,
            'update_replicas_states': perm_update_replicas_states,
            'add_rse_attribute': perm_add_rse_attribute,
            'del_rse_attribute': perm_del_rse_attribute,
            'del_rse': perm_del_rse,
            'del_rule': perm_del_rule,
            'update_rule': perm_update_rule,
            'approve_rule': perm_approve_rule,
            'update_subscription': perm_update_subscription,
            'reduce_rule': perm_reduce_rule,
            'move_rule': perm_move_rule,
            'get_auth_token_user_pass': perm_get_auth_token_user_pass,
            'get_auth_token_gss': perm_get_auth_token_gss,
            'get_auth_token_x509': perm_get_auth_token_x509,
            'get_auth_token_saml': perm_get_auth_token_saml,
            'add_account_identity': perm_add_account_identity,
            'add_did': perm_add_did,
            'add_dids': perm_add_dids,
            'attach_dids': perm_attach_dids,
            'detach_dids': perm_detach_dids,
            'attach_dids_to_dids': perm_attach_dids_to_dids,
            'create_did_sample': perm_create_did_sample,
            'set_metadata': perm_set_metadata,
            'set_metadata_bulk': perm_set_metadata_bulk,
            'set_status': perm_set_status,
            'queue_requests': perm_queue_requests,
            'set_rse_usage': perm_set_rse_usage,
            'set_rse_limits': perm_set_rse_limits,
            'get_request_by_did': perm_get_request_by_did,
            'get_request_metrics': perm_get_request_metrics,
            'cancel_request': perm_cancel_request,
            'get_next': perm_get_next,
            'set_local_account_limit': perm_set_local_account_limit,
            'set_global_account_limit': perm_set_global_account_limit,
            'delete_local_account_limit': perm_delete_local_account_limit,
            'delete_global_account_limit': perm_delete_global_account_limit,
            'config_sections': perm_config,
            'config_add_section': perm_config,
            'config_has_section': perm_config,
            'config_options': perm_config,
            'config_has_option': perm_config,
            'config_get': perm_config,
            'config_items': perm_config,
            'config_set': perm_config,
            'config_remove_section': perm_config,
            'config_remove_option': perm_config,
            'get_local_account_usage': perm_get_local_account_usage,
            'get_global_account_usage': perm_get_global_account_usage,
            'add_attribute': perm_add_account_attribute,
            'del_attribute': perm_del_account_attribute,
            'list_heartbeats': perm_list_heartbeats,
            'send_heartbeats': perm_send_heartbeats,
            'resurrect': perm_resurrect,
            'update_lifetime_exceptions': perm_update_lifetime_exceptions,
            'get_auth_token_ssh': perm_get_auth_token_ssh,
            'get_signed_url': perm_get_signed_url,
            'add_bad_pfns': perm_add_bad_pfns,
            'del_account_identity': perm_del_account_identity,
            'del_identity': perm_del_identity,
            'remove_did_from_followed': perm_remove_did_from_followed,
            'remove_dids_from_followed': perm_remove_dids_from_followed,
            'add_vo': perm_add_vo,
            'list_vos': perm_list_vos,
            'recover_vo_root_identity': perm_recover_vo_root_identity,
            'update_vo': perm_update_vo,
            'access_rule_vo': perm_access_rule_vo,
            'export': perm_export}

    return perm.get(action, perm_default)(issuer=issuer, kwargs=kwargs, session=session)


def _is_root(issuer):
    return issuer.external == 'root' or issuer.external == 'ddmadmin'


def perm_default(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Default permission.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)


def perm_add_rse(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_update_rse(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can update a RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_add_rule(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a replication rule.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if kwargs['account'] == issuer and not kwargs['locked']:
        return True
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True

    return False


def perm_add_subscription(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a subscription.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True

    return False


def perm_add_rse_attribute(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a RSE attribute.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    if kwargs['key'] in [RseAttr.RULE_DELETERS, RseAttr.AUTO_APPROVE_BYTES, RseAttr.AUTO_APPROVE_FILES, RseAttr.RULE_APPROVERS, RseAttr.DEFAULT_ACCOUNT_LIMIT_BYTES, RseAttr.DEFAULT_LIMIT_FILES, RseAttr.BLOCK_MANUAL_APPROVE]:
        # Check if user is a country admin
        admin_in_country = []
        for kv in list_account_attributes(account=issuer, session=session):
            if kv['key'].startswith('country-') and kv['value'] == 'admin':
                admin_in_country.append(kv['key'].partition('-')[2])
        if admin_in_country:
            if list_rse_attributes(rse_id=kwargs['rse_id'], session=session).get(RseAttr.COUNTRY) in admin_in_country:
                return True
    return False


def perm_del_rse_attribute(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete a RSE attribute.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    if kwargs['key'] in [RseAttr.RULE_DELETERS, RseAttr.AUTO_APPROVE_BYTES, RseAttr.AUTO_APPROVE_FILES, RseAttr.RULE_APPROVERS, RseAttr.DEFAULT_ACCOUNT_LIMIT_BYTES, RseAttr.DEFAULT_LIMIT_FILES, RseAttr.BLOCK_MANUAL_APPROVE]:
        # Check if user is a country admin
        admin_in_country = []
        for kv in list_account_attributes(account=issuer, session=session):
            if kv['key'].startswith('country-') and kv['value'] == 'admin':
                admin_in_country.append(kv['key'].partition('-')[2])
        if admin_in_country:
            if list_rse_attributes(rse_id=kwargs['rse_id'], session=session).get(RseAttr.COUNTRY) in admin_in_country:
                return True
    return False


def perm_del_rse(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete a RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_add_account(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)


def perm_del_account(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can del an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)


def perm_update_account(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can update an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_add_scope(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a scop to a account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_get_auth_token_user_pass(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if a user can request a token with user_pass for an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if exist_identity_account(identity=kwargs['username'], type_=IdentityType.USERPASS, account=kwargs['account'], session=session):
        return True
    return False


def perm_get_auth_token_gss(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if a user can request a token with user_pass for an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if exist_identity_account(identity=kwargs['gsscred'], type_=IdentityType.GSS, account=kwargs['account'], session=session):
        return True
    return False


def perm_get_auth_token_x509(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if a user can request a token with user_pass for an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if exist_identity_account(identity=kwargs['dn'], type_=IdentityType.X509, account=kwargs['account'], session=session):
        return True
    return False


def perm_get_auth_token_saml(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if a user can request a token with saml_nameid for an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if exist_identity_account(identity=kwargs['saml_nameid'], type_=IdentityType.SAML, account=kwargs['account'], session=session):
        return True
    return False


def perm_add_account_identity(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add an identity to an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """

    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_del_account_identity(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete an identity to an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """

    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_del_identity(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete an identity.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """

    return _is_root(issuer) or issuer.external in kwargs.get('accounts')


def perm_add_did(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add an data identifier to a scope.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    # Check the accounts of the issued rules
    if not _is_root(issuer) and not has_account_attribute(account=issuer, key='admin', session=session):
        for rule in kwargs.get('rules', []):
            if rule['account'] != issuer:
                return False

    return _is_root(issuer)\
        or has_account_attribute(account=issuer, key='admin', session=session)\
        or rucio.core.scope.is_scope_owner(scope=kwargs['scope'], account=issuer, session=session)\
        or kwargs['scope'].external == 'mock'


def perm_add_dids(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can bulk add data identifiers.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    # Check the accounts of the issued rules
    if not _is_root(issuer) and not has_account_attribute(account=issuer, key='admin', session=session):
        for did in kwargs['dids']:
            for rule in did.get('rules', []):
                if rule['account'] != issuer:
                    return False

    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_attach_dids(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can append an data identifier to the other data identifier.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)\
        or has_account_attribute(account=issuer, key='admin', session=session)\
        or rucio.core.scope.is_scope_owner(scope=kwargs['scope'], account=issuer, session=session)\
        or kwargs['scope'].external == 'mock'


def perm_attach_dids_to_dids(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can append an data identifier to the other data identifier.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    attachments = kwargs['attachments']
    scopes = [did['scope'] for did in attachments]
    scopes = list(set(scopes))
    for scope in scopes:
        if not rucio.core.scope.is_scope_owner(scope, issuer, session=session):
            return False
    return True


def perm_create_did_sample(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can create a sample of a data identifier collection.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)\
        or has_account_attribute(account=issuer, key='admin', session=session)\
        or rucio.core.scope.is_scope_owner(scope=kwargs['scope'], account=issuer, session=session)\
        or kwargs['scope'].external == 'mock'


def perm_del_rule(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an issuer can delete a replication rule.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    if _is_root(issuer):
        return True
    if get_rule(rule_id=kwargs['rule_id'], session=session)['account'] == issuer:
        return True

    # Check if user is a country admin
    admin_in_country = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.append(kv['key'].partition('-')[2])

    rule = get_rule(rule_id=kwargs['rule_id'], session=session)
    rses = parse_expression(rule['rse_expression'], filter_={'vo': issuer.vo}, session=session)
    if admin_in_country:
        for rse in rses:
            if list_rse_attributes(rse_id=rse['id'], session=session).get(RseAttr.COUNTRY) in admin_in_country:
                return True

    # DELETERS can approve the rule
    for rse in rses:
        rse_attr = list_rse_attributes(rse_id=rse['id'], session=session)
        if rse_attr.get(RseAttr.RULE_DELETERS):
            if issuer.external in rse_attr.get(RseAttr.RULE_DELETERS).split(','):
                return True

    return False


def perm_update_rule(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an issuer can update a replication rule.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    # Admin accounts can do everything
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True

    admin_reserved = {'account', 'state', 'priority', 'child_rule_id', 'meta', 'boost_rule'}
    if admin_reserved.intersection(kwargs['options'].keys()):
        return False  # Only priv accounts are allowed to change that

    # Country admins are allowed to change the rest.
    admin_in_country = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.append(kv['key'].partition('-')[2])

    rule = get_rule(rule_id=kwargs['rule_id'], session=session)
    rses = parse_expression(rule['rse_expression'], filter_={'vo': issuer.vo}, session=session)
    if admin_in_country:
        for rse in rses:
            if list_rse_attributes(rse_id=rse['id'], session=session).get(RseAttr.COUNTRY) in admin_in_country:
                return True

    # Only admin and country-admin are allowed to change locked state of rule
    if 'locked' in kwargs['options']:
        return False

    # Owner can change the rest of a rule
    if get_rule(kwargs['rule_id'], session=session)['account'] == issuer:
        return True

    return False


def perm_move_rule(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an issuer can move a replication rule.

    :param issuer:   Account identifier which issues the command.
    :param kwargs:   List of arguments for the action.
    :param session: The DB session to use
    :returns:        True if account is allowed to call the API call, otherwise False
    """
    # Admin accounts can do everything
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True

    # Country admins are allowed to change the but need to be admin for the original, as well as future rule
    admin_in_country = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.append(kv['key'].partition('-')[2])

    admin_source = False
    admin_destination = False

    if admin_in_country:
        rule = get_rule(rule_id=kwargs['rule_id'], session=session)
        rses = parse_expression(rule['rse_expression'], filter_={'vo': issuer.vo}, session=session)
        for rse in rses:
            if list_rse_attributes(rse_id=rse['id'], session=session).get(RseAttr.COUNTRY) in admin_in_country:
                admin_source = True
                break

        rses = parse_expression(kwargs['rse_expression'], filter_={'vo': issuer.vo}, session=session)
        for rse in rses:
            if list_rse_attributes(rse_id=rse['id'], session=session).get(RseAttr.COUNTRY) in admin_in_country:
                admin_destination = True
                break

        if admin_source and admin_destination:
            return True

    return False


def perm_approve_rule(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an issuer can approve a replication rule.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    # Admin accounts can do everything
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True

    rule = get_rule(rule_id=kwargs['rule_id'], session=session)
    rses = parse_expression(rule['rse_expression'], filter_={'vo': issuer.vo}, session=session)

    # APPROVERS can approve the rule
    for rse in rses:
        rse_attr = list_rse_attributes(rse_id=rse['id'], session=session)
        if rse_attr.get(RseAttr.RULE_APPROVERS):
            if issuer.external in rse_attr.get(RseAttr.RULE_APPROVERS).split(','):
                return True

    # LOCALGROUPDISK/LOCALGROUPTAPE admins can approve the rule
    admin_in_country = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.append(kv['key'].partition('-')[2])
    if admin_in_country:
        for rse in rses:
            rse_attr = list_rse_attributes(rse_id=rse['id'], session=session)
            if rse_attr.get(RseAttr.TYPE, '') in ('LOCALGROUPDISK', 'LOCALGROUPTAPE'):
                if rse_attr.get(RseAttr.COUNTRY, '') in admin_in_country:
                    return True

    # GROUPDISK admins can approve the rule
    admin_for_phys_group = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('group-') and kv['value'] == 'admin':
            admin_for_phys_group.append(kv['key'].partition('-')[2])
    if admin_for_phys_group:
        for rse in rses:
            rse_attr = list_rse_attributes(rse_id=rse['id'], session=session)
            if rse_attr.get(RseAttr.TYPE, '') == 'GROUPDISK':
                if rse_attr.get(RseAttr.PHYSGROUP, '') in admin_for_phys_group:
                    return True

    return False


def perm_reduce_rule(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an issuer can reduce a replication rule.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    return False


def perm_update_subscription(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can update a subscription.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True

    return False


def perm_detach_dids(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can detach an data identifier from the other data identifier.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return perm_attach_dids(issuer, kwargs, session=session)


def perm_set_metadata_bulk(issuer: "InternalAccount", kwargs: dict, *, session: "Optional[Session]" = None) -> bool:
    """
    Checks if an account can set a metadata on a data identifier.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return perm_set_metadata(issuer, kwargs, session=session)


def perm_set_metadata(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can set a metadata on a data identifier.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    cond = _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)
    if kwargs['scope'].external != 'archive':
        return cond or rucio.core.scope.is_scope_owner(scope=kwargs['scope'], account=issuer, session=session)
    meta = rucio.core.did.get_metadata(scope=kwargs['scope'], name=kwargs['name'], session=session)
    return cond or meta.get('account', False) == issuer


def perm_set_status(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can set status on an data identifier.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if kwargs.get('open', False):
        if not _is_root(issuer) and not has_account_attribute(account=issuer, key='admin', session=session):
            return False
    cond = (_is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session))
    if kwargs['scope'].external != 'archive':
        return cond or rucio.core.scope.is_scope_owner(scope=kwargs['scope'], account=issuer, session=session)
    meta = rucio.core.did.get_metadata(scope=kwargs['scope'], name=kwargs['name'], session=session)
    return cond or meta.get('account', False) == issuer


def perm_add_protocol(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a protocol to an RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_del_protocol(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete protocols from an RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_update_protocol(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can update protocols of an RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_add_qos_policy(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add QoS policies to an RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_delete_qos_policy(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete QoS policies from an RSE.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_declare_bad_file_replicas(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can declare bad file replicas.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    is_cloud_admin = bool([acc_attr for acc_attr in list_account_attributes(account=issuer, session=session) if (acc_attr['key'].startswith('cloud-')) and (acc_attr['value'] == 'admin')])
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session) or is_cloud_admin


def perm_declare_suspicious_file_replicas(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can declare suspicious file replicas.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return True


def perm_add_replicas(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add replicas.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    rse_id = str(kwargs.get('rse_id', ''))
    group = []

    for kv in list_account_attributes(account=issuer, session=session):
        if (kv['key'].startswith('group-') or kv['key'].startswith('country-')) and kv['value'] in ['admin', 'user']:
            group.append(kv['key'].partition('-')[2])
    rse_attr = list_rse_attributes(rse_id=rse_id, session=session)
    if group:
        if rse_attr.get(RseAttr.TYPE, '') == 'GROUPDISK':
            if rse_attr.get(RseAttr.PHYSGROUP, '') in group:
                return True
        if rse_attr.get(RseAttr.TYPE, '') == 'LOCALGROUPDISK':
            if rse_attr.get(RseAttr.COUNTRY, '') in group:
                return True

    return rse_attr.get(RseAttr.TYPE, '') in ['SCRATCHDISK', 'MOCK', 'TEST']\
        or _is_root(issuer)\
        or has_account_attribute(account=issuer, key='admin', session=session)


def perm_skip_availability_check(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can skip the availabity check to add/delete file replicas.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_delete_replicas(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete replicas.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return False


def perm_update_replicas_states(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete replicas.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    rse_id = str(kwargs.get('rse_id', ''))
    group = []

    for kv in list_account_attributes(account=issuer, session=session):
        if (kv['key'].startswith('group-') or kv['key'].startswith('country-')) and kv['value'] in ['admin', 'user']:
            group.append(kv['key'].partition('-')[2])
    rse_attr = list_rse_attributes(rse_id=rse_id, session=session)
    if group:
        if rse_attr.get(RseAttr.TYPE, '') == 'GROUPDISK':
            if rse_attr.get(RseAttr.PHYSGROUP, '') in group:
                return True
        if rse_attr.get(RseAttr.TYPE, '') == 'LOCALGROUPDISK':
            if rse_attr.get(RseAttr.COUNTRY, '') in group:
                return True

    return rse_attr.get(RseAttr.TYPE, '') in ['SCRATCHDISK', 'MOCK', 'TEST']\
        or _is_root(issuer)\
        or has_account_attribute(account=issuer, key='admin', session=session)


def perm_queue_requests(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can submit transfer or deletion requests on destination RSEs for data identifiers.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)


def perm_get_request_by_did(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can get a request by DID.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return True


def perm_get_request_metrics(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can get the request stats

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_cancel_request(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can cancel a request.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)


def perm_get_next(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can retrieve the next request matching the request type and state.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)


def perm_set_rse_usage(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can set RSE usage information.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer)


def perm_set_rse_limits(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can set RSE limits.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_set_local_account_limit(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can set an account limit.

    :param account: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    # Check if user is a country admin
    admin_in_country = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.append(kv['key'].partition('-')[2])
    rse_attr = list_rse_attributes(rse_id=kwargs['rse_id'], session=session)
    if admin_in_country and rse_attr.get(RseAttr.COUNTRY) in admin_in_country:
        return True
    quota_approvers = rse_attr.get(RseAttr.QUOTA_APPROVERS, None)
    if quota_approvers and issuer.external in quota_approvers.split(','):
        return True
    return False


def perm_set_global_account_limit(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can set a global account limit.

    :param account: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    # Check if user is a country admin
    admin_in_country = set()
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.add(kv['key'].partition('-')[2])
    resolved_rse_countries = {list_rse_attributes(rse_id=rse['rse_id'], session=session).get(RseAttr.COUNTRY)
                              for rse in parse_expression(kwargs['rse_expression'], filter_={'vo': issuer.vo}, session=session)}
    if resolved_rse_countries.issubset(admin_in_country):
        return True
    return False


def perm_delete_global_account_limit(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete a global account limit.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    # Check if user is a country admin
    admin_in_country = set()
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.add(kv['key'].partition('-')[2])
    resolved_rse_countries = {list_rse_attributes(rse_id=rse['rse_id'], session=session).get(RseAttr.COUNTRY)
                              for rse in parse_expression(kwargs['rse_expression'], filter_={'vo': issuer.vo}, session=session)}
    if resolved_rse_countries.issubset(admin_in_country):
        return True
    return False


def perm_delete_local_account_limit(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can delete an account limit.

    :param account: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    # Check if user is a country admin
    admin_in_country = []
    for kv in list_account_attributes(account=issuer, session=session):
        if kv['key'].startswith('country-') and kv['value'] == 'admin':
            admin_in_country.append(kv['key'].partition('-')[2])
    rse_attr = list_rse_attributes(rse_id=kwargs['rse_id'], session=session)
    if admin_in_country and rse_attr.get(RseAttr.COUNTRY) in admin_in_country:
        return True
    quota_approvers = rse_attr.get(RseAttr.QUOTA_APPROVERS, None)
    if quota_approvers and issuer.external in quota_approvers.split(','):
        return True
    return False


def perm_config(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can read/write the configuration.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_get_local_account_usage(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can get the account usage of an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return True


def perm_get_global_account_usage(issuer: str, kwargs: dict[str, str], *, session: "Optional[Session]" = None) -> bool:
    """
    Checks if an account can get the account usage of an account.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return True


def perm_add_account_attribute(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add attributes to accounts.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_del_account_attribute(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add attributes to accounts.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return perm_add_account_attribute(issuer, kwargs, session=session)


def perm_list_heartbeats(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can list heartbeats.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='handle_heartbeats', session=session)


def perm_send_heartbeats(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can send heartbeats.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session) or has_account_attribute(account=issuer, key='handle_heartbeats', session=session)


def perm_resurrect(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can resurrect DIDS.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_update_lifetime_exceptions(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can approve/reject Lifetime Model exceptions.

    :param issuer: Account identifier which issues the command.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session)


def perm_get_auth_token_ssh(issuer: "InternalAccount", kwargs: dict, *, session: "Optional[Session]" = None) -> bool:
    """
    Checks if an account can request an ssh token.

    :param issuer: Account identifier which issues the command.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return True


def perm_get_signed_url(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can request a signed URL.

    :param issuer: Account identifier which issues the command.
    :param session: The DB session to use
    :returns: True if account is allowed to call the API call, otherwise False
    """
    return _is_root(issuer) or has_account_attribute(account=issuer, key='sign-gcs', session=session)


def perm_add_bad_pfns(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can declare bad PFNs.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if kwargs['state'] in [BadPFNStatus.BAD.name, BadPFNStatus.TEMPORARY_UNAVAILABLE.name]:
        is_cloud_admin = bool([acc_attr for acc_attr in list_account_attributes(account=issuer, session=session) if (acc_attr['key'].startswith('cloud-')) and (acc_attr['value'] == 'admin')])
        return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session) or is_cloud_admin
    elif kwargs['state'] == BadPFNStatus.SUSPICIOUS.name:
        return True
    return _is_root(issuer)


def perm_remove_did_from_followed(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can remove did from followed table.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return _is_root(issuer)\
        or has_account_attribute(account=issuer, key='admin', session=session)\
        or kwargs['account'] == issuer\
        or kwargs['scope'].external == 'mock'


def perm_remove_dids_from_followed(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can bulk remove dids from followed table.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    if _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session):
        return True
    if not kwargs['account'] == issuer:
        return False
    return True


def perm_add_vo(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can add a VO.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return (issuer.internal == 'super_root')


def perm_list_vos(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can list a VO.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return (issuer.internal == 'super_root')


def perm_recover_vo_root_identity(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can recover identities for VOs.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return (issuer.internal == 'super_root')


def perm_update_vo(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can update a VO.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return (issuer.internal == 'super_root')


def perm_access_rule_vo(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if we're at the same VO as the rule_id's

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    return get_rule(kwargs['rule_id'], session=session)['scope'].vo == issuer.vo


def perm_export(issuer, kwargs, *, session: "Optional[Session]" = None):
    """
    Checks if an account can export the RSE info.

    :param issuer: Account identifier which issues the command.
    :param kwargs: List of arguments for the action.
    :param session: The DB session to use
    :returns: True if account is allowed, otherwise False
    """
    is_cloud_admin = bool([acc_attr for acc_attr in list_account_attributes(account=issuer, session=session) if (acc_attr['key'].startswith('cloud-')) and (acc_attr['value'] == 'admin')])
    return _is_root(issuer) or has_account_attribute(account=issuer, key='admin', session=session) or is_cloud_admin
