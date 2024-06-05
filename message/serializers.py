from air_drf_relation.serializers import AirModelSerializer

from message.models import Message, Button


class MessageSerializer(AirModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'buttons', 'max_actions', 'created_at', 'updated_at')


class ButtonSerializer(AirModelSerializer):
    class Meta:
        model = Button
        fields = ('id', 'text', 'callback_data', 'created_at', 'updated_at')

