from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    """
    Serializer for uploading a document.
    """

    file = serializers.FileField()

    def validate_file(self, value):
        """
        Allow only PDF files.
        """

        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF files are allowed."
            )

        return value


class ChatSerializer(serializers.Serializer):
    """
    Serializer for chat questions.
    """

    question = serializers.CharField(
        max_length=1000,
        allow_blank=False,
        trim_whitespace=True,
    )