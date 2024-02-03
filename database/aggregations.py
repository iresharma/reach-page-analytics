UNIQUE_AGGREGRATION = [
        {
            '$match': {
                'timestamp': {
                    '$gte': end,
                    '$lt': start
                }
            }
        }, {
            '$group': {
                '_id': '$ip',
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': None,
                'totalCount': {
                    '$sum': 1
                }
            }
        }
    ]