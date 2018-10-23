import datetime
import os
import copy

from boto3 import resource
from boto3.dynamodb.conditions import Key


# The boto3 dynamoDB resource
db = resource('dynamodb',
              region_name=os.environ.get("AWS_REGION_NAME"),
              aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
              aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))


#########
# USERS #
#########
def get_user(user_id):
    return _get_item('users', {'user_id': user_id})


def sync_or_create_user(openid_user):
    """
    Checks the user, returned by the authentication-service
    Requires a user-dict with at least: sub, email, updated_at
    """
    def _validate_user(openid_user):
        error = False
        msg = ''
        if not openid_user.get('sub'):
            error = True
            msg += ' sub'
        if not openid_user.get('email'):
            error = True
            msg += ' email'
        if not openid_user.get('updated_at'):
            error = True
            msg += ' updated_at'

        if error:
            return {'error': True, 'msg': 'Missing claims:' + msg}
        else:
            return {'msg': 'valid openid_user'}

    def _insert_user(openid_user):
        user = copy.deepcopy(openid_user)
        user['max_units'] = 10
        # user['active_units'] = []
        user['roles'] = ['user']
        user['user_id'] = openid_user.get('sub')

        # Generate additional, normalized key for db on insert or replace
        if openid_user.get('username'):
            federated_name = openid_user.get('username')
        elif openid_user.get('nickname'):
            federated_name = openid_user.get('nickname')
        elif openid_user.get('name'):
            federated_name = openid_user.get('name')
        else:
            federated_name = openid_user.get('email').split('@')[0]
        user['federated_name'] = federated_name

        if _put_item('users', user):
            # Tells client, that user is first-time user
            # '_action'-key does not persist
            user['_action'] = 'inserted'
            return user
        else:
            return {'error': True, 'msg': 'Unable to create user'}

    def _sync_user(openid_user, db_user):
        # NOTE: First update openid_user with existing local values, as they
        # will be overwritten on the put_item-request!
        user = copy.deepcopy(openid_user)
        user['federated_name'] = db_user.get('federated_name')
        user['max_units'] = db_user.get('max_units', 10)
        # user['active_units'] = db_user.get('active_units', [])
        user['roles'] = db_user.get('roles', ['user'])
        user['user_id'] = db_user.get('user_id')

        if _put_item('users', user, action='update'):
            user['_action'] = 'updated'
            return user
        else:
            return {'error': True, 'msg': 'Unable to sync user'}

    valid_input = _validate_user(openid_user)
    if valid_input.get('error'):
        return valid_input

    db_user = get_user(openid_user.get('sub'))
    # If no existing user
    if db_user.get('error'):
        if db_user.get('msg') == 'Item does not exist':
            return _insert_user(openid_user)
        else:
            return db_user
    elif db_user.get('updated_at') != openid_user.get('updated_at'):
        return _sync_user(openid_user, db_user)
    else:
        db_user['_action'] = 'checked'
        return db_user


def delete_user(user_id):
    # bookmarks_deleted =
    # searches_deleted =
    resp = _delete_item('users', {'user_id': user_id})
    if resp:
        return {'msg': 'Brugeren er nu slettet.',
                'id': user_id}
    else:
        return {'error': True,
                'msg': 'Brugeren fandtes ikke i databasen'}


def update_user_role(user_id, new_role):
    if new_role == 'employee':
        new_roles = ['user', 'employee']
    elif new_role == 'admin':
        new_roles = ['user', 'employee', 'admin']
    else:
        new_roles = ['user']

    key = {'user_id': user_id}
    updates = {
        'attribute': 'roles',
        'value': new_roles
    }
    resp = _update_item('users', key, updates)
    if resp:
        return resp
    else:
        return {'error': True, 'msg': 'Unable to update user_roles.'}


############
# SEARCHES #
############
def list_searches(user_id):
    kwargs = {}
    kwargs['table_name'] = 'searches'
    kwargs['pk'] = {'name': 'user_id', 'value': user_id}
    return _query_table(**kwargs)


def get_search(key):
    return _get_item('searches', key)


def add_search(item):
    resp = _put_item('searches', item)
    if resp:
        return {'msg': 'Søgningen blev gemt.'}
    else:
        return {'error': True,
                'msg': 'Ukendt serverfejl.'}


def update_search(user_id, created, description):
    key = {'user_id': user_id, 'created': created}
    update = {'attribute': 'description', 'value': description}
    resp = _update_item('searches', key, update)
    if resp:
        return resp
    else:
        return {'error': True,
                'msg': 'Unable to update search. Try again later.'}


def delete_search(item):
    # key = {'user_id': user_id, 'created': created}
    resp = _delete_item('searches', item)
    if resp:
        return {'msg': 'Søgningen blev slettet',
                'created': item.get('created')}
    else:
        return {'error': True,
                'msg': 'Søgningen blev ikke slettet'}


#############
# BOOKMARKS #
#############
def list_bookmarks(user_id, sort='sort_key', sort_desc=False, ids_only=False):
    # NOT USED
    kwargs = {}
    kwargs['table_name'] = 'bookmarks'
    kwargs['pk'] = {'name': 'user_id', 'value': user_id}
    if sort == 'created':
        kwargs['idx'] = 'user_id-created-index'
    if sort_desc:
        kwargs['rd'] = True
    resp = _query_table(**kwargs)
    # Return bookmarks
    if ids_only:
        return [_d.get('resource_id') for _d in resp]
    else:
        return resp


def put_bookmark(item):
    resp = _put_item('bookmarks', item)
    if resp:
        return {'msg': 'Materialet er nu bogmærket.',
                'id': item.get('resource_id')}
    else:
        return {'error': True,
                'msg': 'Ukendt serverfejl.'}


def delete_bookmark(item):
    # key = {'user_id': user_id, 'created': created}
    resp = _delete_item('bookmarks', item)
    if resp:
        return {'msg': 'Bogmærket er nu fjernet.',
                'id': item.get('resource_id')}
    else:
        return {'error': True,
                'msg': 'Ukendt serverfejl.'}


#########
# UNITS #
#########
def list_storage_units(user_id=None):
    kwargs = {}
    kwargs['table_name'] = 'storage_units'
    kwargs['pk'] = {'name': 'user_id', 'value': user_id}
    resp = _query_table(**kwargs)
    return resp


def get_storage_unit(unit_id, projection=None):
    partition_key = {'unit_id', unit_id}
    unit = _get_item('storage_units', partition_key)
    if unit:
        return unit
    else:
        return {'error': True, 'msg': 'Unable to query local db.'}


def insert_storage_unit(item):
    return False


def update_storage_unit(unit_id, status):
    return False


def delete_storage_unit(unit_id):
    return False


##########
# ORDERS #
##########
def get_order(user_id, resource_id):
    return _get_item('orders',
                     {'user_id': user_id},
                     {'resource_id': resource_id})


def list_orders(key, value, ids_only=False, limit=None):
    # List of orders only queries by partition_key, not also sort_key
    # as the sort_key of the orders-table is unique. Use _get_item for that
    kwargs = {}
    kwargs['table_name'] = 'orders'

    if key not in ['user_id', 'unit_id']:
        return {'error': True, 'msg': 'key must be unit_id or user_id'}

    kwargs['pk'] = {'name': key, 'value': value}
    if limit:
        kwargs['limit'] = limit

    if key == 'user_id':
        if ids_only:
            kwargs['proj'] = 'resource_id'
        return _query_table(**kwargs)
    else:
        kwargs['idx'] = 'unit_id-created-index'
        return _query_table(**kwargs)


def _insert_order(user_id, resource_id, unit_id):
    """
    """
    # Fetch entities
    unit = get_storage_unit(unit_id)
    if unit.get('error'):
        return unit

    user = get_user(user_id)
    if user.get('error'):
        return user

    existing_orders = list_orders(key='unit_id', value=unit_id)
    if isinstance(existing_orders, dict) and existing_orders.get('error'):
        return existing_orders

    # Test conditions
    # MOVE TO VIEW-HANDLER
    # if unit_id in user.get('active_units'):
    #     return {'msg': u'Du har allerede bestilt magasin-enheden'}

    # if len(user.get('active_units')) >= user.get('max_units'):
    #     return {'error': True, 'msg': u'Du kan ikke bestille flere materialer.'}

    # Baseline
    order = {
        'user_id': user_id,
        'resource_id': resource_id,
        'unit_id': unit_id
    }

    # If no existing orders on the unit
    if not existing_orders:
        # If unit is at readingroom, set status to available end expiration in 14 days
        if unit.get('status') == 'readingroom':
            order['status'] = 'available'
            order['expires'] = str(datetime.date.today() + datetime.timedelta(days=14))
            msg = 'Materialet er allerede tilgængelig på læsesalen.'
        # Else reserve the unit (like first in queue)
        else:
            order['status'] = 'waiting'
            msg = 'Materialet er bestilt. du får besked, når det er tilgængeligt på læsesalen.'
    # If existing orders on the unit, place in queue
    else:
        order['status'] = 'waiting'
        msg = str('Materialet er bestilt. Du er nummer ' + str(len(existing_orders)) + ' i køen.')

    # Insert order
    if _put_item('orders', order):
        # send_mail('order_created', user.get('email'))
        return {'msg': msg}
    else:
        return {'error': True, 'msg': 'Ukendt serverfejl. Bestillingen ikke gemt.'}


def delete_order(user_id, resource_id):
    """ Cancelled or finished or force-deleted by employee
    """
    deleted_order = _delete_item('orders',
                                 {
                                    'user_id': user_id,
                                    'resource_id': resource_id
                                 },
                                 return_item=True)
    if not deleted_order:
        return {'error': True, 'msg': 'Kunne ikke slette ordren.'}

    # Fetch unit-status. If at readingroom, update next in line 
    # and send availability-mail
    unit = get_storage_unit(deleted_order.get('unit_id'))
    if unit.get('status') == 'readingroom':
        # If next in line, update availability and expiration
        nxt = list_orders(key='unit_id', value=deleted_order.get('unit_id'), limit=1)
        if nxt:
            # Update order-keys and put back in db
            nxt[0]['status'] = 'available'
            nxt[0]['expires'] = str(datetime.date.today() + datetime.timedelta(days=14))
            if _put_item('orders', nxt[0], action='update'):
                # If order is updated, send availability-mail
                # send_mail('order_available', nxt[0]['email'])
                pass

    return {'msg': 'Bestillingen er nu slettet.', 'id': resource_id}


################
# BASE METHODS #
################
def _get_item(table, partition_key, sort_key=None, projection=None):
    """
    Return item read by primary key, and possibly sort_key.
    """
    if sort_key:
        partition_key.update(sort_key)
    kwargs = {'Key': partition_key}

    if projection:
        kwargs['ProjectionExpression'] = projection

    table = db.Table(table)
    response = table.get_item(**kwargs)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if response.get('Item'):
            return response.get('Item')
        else:
            return {'error': True, 'msg': 'Item does not exist'}
    else:
        return {'error': True, 'msg': 'Error in fetching item from ' + table + '-table'}


def _put_item(table_name, item, action='insert'):
    """
    Add one item (row) to table. item is a dictionary {col_name: value}.
    """
    now = datetime.datetime.utcnow().isoformat()

    if action == 'insert':
        item['created'] = now
    item['updated'] = now
    table = db.Table(table_name)

    response = table.put_item(Item=item)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def _update_item(table_name, partition_key, update_dict):
    """
    Update an item.
    PARAMS
    @table_name: name of the table
    @partition_key: dict containing the key name and val
    @update_dict: dict containing the key name and val of
    attributes to be updated
    eg. {"attribute": "processing_status", "value": "completed"}
    """
    table = db.Table(table_name)
    update_expr = 'SET updated=:now, {}=:val1'.format(update_dict['attribute'])

    response = table.update_item(
        Key=partition_key,
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ':now': datetime.datetime.utcnow().isoformat(),
            ':val1': update_dict['value']
        },
        ReturnValues='ALL_NEW'
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response.get('Attributes')
    else:
        return False


def _delete_item(table_name, key, return_item=False):
    """
    Delete an item (row) in table from its primary key. Consisting of
    partition-key and possibly a sort_key, all in key
    """
    table = db.Table(table_name)

    response = table.delete_item(
        Key=key,
        ReturnValues='ALL_OLD' if return_item else 'NONE'
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if return_item:
            return response.get('Attributes')
        else:
            return True
    else:
        return False


def _query_table(table_name, pk, sk=None, idx=None, rd=None, proj=None, limit=None):
    """
    Perform a query operation on the table.
    """
    kwargs = {}
    _pk = pk.get('name')
    _pkv = pk.get('value')

    if sk:
        _sk = sk.get('name')
        _skv = sk.get('value')
        kwargs['KeyConditionExpression'] = Key(_sk).eq(_skv) & Key(_pk).eq(_pkv)
    else:
        kwargs['KeyConditionExpression'] = Key(_pk).eq(_pkv)

    if proj:
        kwargs['ProjectionExpression'] = proj

    if idx:
        kwargs['IndexName'] = idx

    if limit:
        kwargs['Limit'] = limit

    # reverse_direction. Used when sorting descending
    if rd:
        kwargs['ScanIndexForward'] = False

    table = db.Table(table_name)
    response = table.query(**kwargs)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response.get('Items')
    else:
        return False


def _scan_table(table_name, filter_key=None, filter_value=None, limit=None):
    """
    Perform a scan operation on table. Can specify filter_key (col name) and its value to be filtered. This gets all pages of results.
    Returns list of items.
    http://boto3.readthedocs.io/en/latest/reference/customizations/dynamodb.html#dynamodb-conditions
    """
    table = db.Table(table_name)
    kwargs = {}

    if filter_key and filter_value:
        kwargs['FilterExpression'] = Key(filter_key).eq(filter_value)
    kwargs['Limit'] = limit or None
    # response = table.scan(FilterExpression=filtering_exp)
    response = table.scan(**kwargs)

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items
