from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict


class Response(Response):
    def __init__(self, data={}, errors=[], status=200, success=True, headers={}, **kwargs):
        errors_list = []
        if status > 309:
            success = False
        if type(errors) is ReturnDict:
            for items in errors:
                if items == "non_field_errors":
                    data['message'] = errors[items][0]
                else:
                    errors_list.append({
                        'field':items,
                        'success':False,
                        'error':' '.join(errors[items]),
                    })
            if 'message' not in data and errors_list:
                data['message'] = f"{' '.join([items.capitalize() for items in errors_list[0]['field'].split('_')])}: {errors_list[0]['error']}"

            # errors_list = sum(errors.values(), [])
            # data['message'] = errors.get('non_field_errors', ['Invalid request!'])[0]
        # print(errors_list, data['message'])
        message = data.pop('message', None)
        data = dict(status=status, success=success, message=message, errors=errors_list, data=data)
        super(self.__class__, self).__init__(data, status=status, **kwargs)
