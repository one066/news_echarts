from flask import request

from extension.flask.api import APIBaseView, ok_response


class BaseView(APIBaseView):
    """
    自定义封装 view
    base view
    """
    validated_class = None
    serialize_class = None

    def method(self, *args, **kwargs):
        self.validated_data = self.get_validated_data(kwargs)
        self.action_result = self.action()
        return self.response()

    def get_validated_data(self, kwargs):
        """反序列化
        """
        if not self.validated_class:
            return {}

        # body data
        request_data = self.parse_json()
        # url data
        request_data.update(kwargs)
        validated_class = self.validated_class()
        validated_data = validated_class.load(request_data)
        return validated_data

    def action(self):
        raise NotImplementedError

    def response(self):
        """响应结果
        默认返回空 json 对象, 需要修改则在子类中覆盖这个方法
        """
        if self.serialize_class:
            data = self.serialize_class().dump(self.action_result)
            return ok_response(data)
        else:
            return ok_response({})


class GetView(BaseView):

    def get(self, *args, **kwargs):
        return super().method(args, kwargs)

    def get_validated_data(self, kwargs):
        """反序列化
        """
        if not self.validated_class:
            return {}

        request_data = {}
        # arg data
        for key, value in request.args.items():
            if isinstance(value, list) and len(value) == 1:
                request_data[key] = value[0]
            else:
                request_data[key] = value

        # url data
        request_data.update(kwargs)
        validated_class = self.validated_class()
        validated_data = validated_class.load(request_data)
        return validated_data

    def response(self):
        if not self.serialize_class:
            return {}
        data = self.serialize_class().dump(self.action_result)
        return data


class PostView(BaseView):

    def post(self, *args, **kwargs):
        return super().method(args, kwargs)


class PutView(BaseView):

    def put(self, *args, **kwargs):
        return super().method(args, kwargs)


class DeleteView(BaseView):

    def delete(self, *args, **kwargs):
        return super().method(args, kwargs)


class PatchView(BaseView):

    def patch(self, *args, **kwargs):
        return super().method(args, kwargs)
