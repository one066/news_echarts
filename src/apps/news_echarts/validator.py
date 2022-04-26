from marshmallow import Schema, fields, validate

# #######################################################################
#                        Validated
# #######################################################################


class NewsIdServiceValidated(Schema):
    news_id = fields.Int(required=True)


class LoginValidated(Schema):
    nick_name_or_email = fields.String(required=True)
    password = fields.String(required=True)


class EmailValidated(Schema):
    email = fields.Email(required=True)


class EmailLoginValidated(Schema):
    email = fields.Email(required=True)
    verification_code = fields.Int(required=True)


class ModifyInformationValidated(Schema):
    password = fields.String(validate=validate.Length(min=5))
    nick_name = fields.String(validate=validate.Length(min=3))
    phone_number = fields.String(validate=validate.Length(min=11, max=11))
    introduction = fields.String()
    photo_base64 = fields.String()


class AddMessageValidated(Schema):
    content = fields.Str(required=True)


class UpdateNewsValidated(Schema):
    news_id = fields.Int(required=True)
    positive = fields.String()
    abstract = fields.String()
    keywords = fields.String()


# #######################################################################
#                        Serialize
# #######################################################################


class UpdateNewestNewsServiceSerialize(Schema):
    total = fields.Int()
    news = fields.List(fields.Dict)


class GetNewsServiceSerialize(Schema):
    news = fields.List(fields.Dict)


class AnalysisResultServiceSerialize(Schema):

    class Meta:
        fields = ("analysis_result",)


class UserTokenSerialize(Schema):
    user_id = fields.String()
    token = fields.String()
    nick_name = fields.String()


class ClickServiceSerialize(Schema):
    title = fields.String()
    url = fields.String()


class RecommendedNewsSerialize(Schema):
    top_ten_news = fields.List(fields.Dict)


class ProfileSerialize(Schema):
    user_id = fields.String()
    email = fields.Email()
    nick_name = fields.String()
    phone_number = fields.String()
    introduction = fields.String()


class PhotoSerialize(Schema):
    photo_base64 = fields.String()


class HotSearchSerialize(Schema):

    class Meta:
        fields = ("hot_search",)


class TopWordsSerialize(Schema):

    class Meta:
        fields = ("words",)


class DataSerialize(Schema):

    class Meta:
        fields = ("data",)


class GetMessageSerialize(Schema):

    class Meta:
        fields = ("messages",)
